# Report 02 — OAuth refresh forks for claude-code-action

**Date:** 2026-05-11
**Author:** Subagent (run 20260511-r2, sub-01)
**Status:** ✅ complete

## Lead question

How do the leading community forks of `anthropics/claude-code-action` implement OAuth token refresh — specifically the refresh-token API call, where the new tokens are stored, how the workflow is scheduled, and what failure modes are handled — and which of those approaches should `agent-runner` adopt verbatim, adapt, or design differently?

## 1. Verdict in three sentences

The community has **one** load-bearing implementation: Guillaume Raille's three-repo stack — `grll/claude-code-login` (initial OAuth), `grll/claude-code-action` (the user-facing fork), and `grll/claude-code-base-action` (which contains the actual refresh code in `src/setup-oauth.ts`). The refresh model is **just-in-time** — every workflow invocation that uses OAuth checks the token's expiry, refreshes if it's within a 60-minute buffer, and writes the new triple back to GitHub Secrets via `gh secret set` using a Personal Access Token (`SECRETS_ADMIN_PAT`) with `secrets:write` scope. `agent-runner` should **adapt, not vendor**: borrow the API call shape (URL, payload, client_id, expiry-buffer logic) verbatim into its own `refresh-oauth.yml`, but invert the trigger from "every action invocation" to "scheduled cron + on-demand," because our cron-triggered runs may have no human-action invocation between expiries.

## 2. The refresh-token API call (verbatim from `setup-oauth.ts`)

The canonical reference is `grll/claude-code-base-action/src/setup-oauth.ts` (151 lines, fetched 2026-05-11 from `main`). The relevant function:

```typescript
const OAUTH_TOKEN_URL = 'https://console.anthropic.com/v1/oauth/token';
const CLIENT_ID = '9d1c250a-e61b-44d9-88ed-5944d1962f5e';

async function performRefresh(refreshToken: string): Promise<...> {
  const response = await fetch(OAUTH_TOKEN_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      grant_type: 'refresh_token',
      refresh_token: refreshToken,
      client_id: CLIENT_ID,
    }),
  });
  if (response.ok) {
    const data = await response.json();
    return {
      accessToken: data.access_token,
      refreshToken: data.refresh_token,
      expiresAt: (Math.floor(Date.now() / 1000) + data.expires_in) * 1000,
    };
  } else {
    const errorBody = await response.text();
    console.log(`❌ Token refresh failed: ${response.status} - ${errorBody}`);
    return null;
  }
}
```

(`grll/claude-code-base-action/src/setup-oauth.ts:30-61`)

Key facts to lock in:

- **Endpoint:** `POST https://console.anthropic.com/v1/oauth/token` (note: `console.anthropic.com`, *not* `api.anthropic.com`).
- **Content-Type:** `application/json` — payload is JSON, NOT form-urlencoded. Most generic OAuth 2.0 tutorials show `application/x-www-form-urlencoded`. This implementation uses JSON.
- **Required body fields (three):** `grant_type: "refresh_token"`, `refresh_token: <existing>`, `client_id: "9d1c250a-e61b-44d9-88ed-5944d1962f5e"`. No client_secret, no PKCE verifier, no scope, no redirect_uri — the refresh call is much simpler than the initial code-exchange call.
- **client_id is hardcoded.** It is the Claude desktop client's published OAuth client ID (visible in the URL emitted by the login step in `grll/claude-code-login`). This is *not* a secret. `agent-runner` should also hardcode it.
- **Response shape:** `{ access_token, refresh_token, expires_in, scope? }`. The `expires_in` field is **seconds** (per OAuth 2.0 RFC 6749). The implementation immediately converts to **milliseconds-since-epoch** via `(Math.floor(Date.now() / 1000) + data.expires_in) * 1000` and stores that.
- **The refresh response includes a NEW refresh_token.** This is critical: refresh tokens are rotated. The old refresh_token may or may not be invalidated server-side, but you must store the new one or your next refresh will eventually fail.

The initial OAuth code-exchange (separate call, only done once during login by `grll/claude-code-login/index.ts`) hits the same endpoint with `grant_type: 'authorization_code'` plus `code`, `redirect_uri`, `code_verifier`, and `state`. That's not the refresh path; cite for completeness only.

## 3. Where new tokens are stored

Two storage targets, both updated on every refresh:

### 3a. Local `~/.claude/.credentials.json` (within the runner)

The runner's home directory gets a credentials JSON written so that the spawned `claude-code` CLI can read it:

```typescript
const credentialsData = {
  claudeAiOauth: {
    accessToken: accessToken,
    refreshToken: refreshToken,
    expiresAt: expiresAt,
    scopes: ["user:inference", "user:profile"],
  },
};
await writeFile(credentialsPath, JSON.stringify(credentialsData, null, 2));
```

(`setup-oauth.ts:138-148`)

This mirrors the on-disk shape the Claude Code CLI uses on a developer laptop. **The `scopes` array is hardcoded to `["user:inference", "user:profile"]`** — the response's `scope` field is not threaded through. `agent-runner`'s `refresh-oauth.yml` doesn't strictly need to write this file (we only need to update the secret), but if `run.py` ever shells out to `claude` directly rather than via the action, the file must exist.

### 3b. GitHub Actions Secrets via `gh secret set`

```typescript
function updateGitHubSecrets(secretsAdminPat, accessToken, refreshToken, expiresAt) {
  const env = { ...process.env, GH_TOKEN: secretsAdminPat };
  execSync(`gh secret set CLAUDE_ACCESS_TOKEN --body "${accessToken}"`, { env, stdio: 'inherit' });
  execSync(`gh secret set CLAUDE_REFRESH_TOKEN --body "${refreshToken}"`, { env, stdio: 'inherit' });
  execSync(`gh secret set CLAUDE_EXPIRES_AT --body "${expiresAt}"`, { env, stdio: 'inherit' });
}
```

(`setup-oauth.ts:63-82`)

Three secrets, three names: `CLAUDE_ACCESS_TOKEN`, `CLAUDE_REFRESH_TOKEN`, `CLAUDE_EXPIRES_AT` (the last one is **milliseconds**, stored as a string).

The shell-injection surface here is real but limited: Anthropic controls the token strings, they're URL-safe by spec, and `gh secret set --body` quotes the value as a single argument before encrypting and uploading. Still, `agent-runner`'s adaptation should pipe via stdin (`echo "$VALUE" | gh secret set CLAUDE_ACCESS_TOKEN`) instead of `--body "$VALUE"` to eliminate the surface entirely.

### 3c. Authentication for the secret-update call

`gh secret set` requires a token with the `actions:write`/`secrets:write` GitHub permission on the repo. The default `${{ secrets.GITHUB_TOKEN }}` does **not** have this permission for repo secrets, by design — GitHub explicitly excludes secret-write from the default action token. Hence the need for `SECRETS_ADMIN_PAT`:

- **Type:** Fine-grained Personal Access Token (recommended over classic).
- **Scope:** Repository → Secrets: Write (read is implied).
- **Expiry:** README recommends 30-60 days with a calendar reminder for renewal. (Source: `grll/claude-code-login/README.md`, "Setting up SECRETS_ADMIN_PAT" section.)
- **Storage:** Itself a repo secret named `SECRETS_ADMIN_PAT`.

This creates a **bootstrap problem we should plan for** (not a blocker): the PAT itself expires and is *not* auto-refreshed. We need a recurring human task (set a calendar reminder; ideally a heartbeat run that warns when the PAT's `gh auth status` indicates impending expiry). Note that `agent-runner`'s DESIGN.md §7 already names this PAT as `AGENT_RUNNER_PAT`; the name differs but the role is identical.

## 4. How the refresh is scheduled — the surprising part

**The community fork does not schedule the refresh on a cron.** There is no `refresh-oauth.yml` with `on: schedule`. Instead, **every invocation of `grll/claude-code-action` performs the just-in-time check**:

1. `claude-code-action`'s `action.yml` calls `claude-code-base-action` as a composite step, passing the four OAuth inputs (`claude_access_token`, `claude_refresh_token`, `claude_expires_at`, `secrets_admin_pat`).
2. `claude-code-base-action`'s entrypoint calls `setupOAuthCredentials(...)` first thing.
3. That function checks `tokenExpired(expiresAtMs)`:
   ```typescript
   function tokenExpired(expiresAtMs: number): boolean {
     const bufferMs = 60 * 60 * 1000;  // 60-minute buffer
     return Date.now() >= (expiresAtMs - bufferMs);
   }
   ```
   (`setup-oauth.ts:23-28`)
4. If within the 60-minute window, refresh now, update secrets, write `~/.claude/.credentials.json`, then proceed with the actual Claude Code run.
5. If still valid, log `"✅ Token is still valid (expires in N minutes)"` and proceed.

**The implication for `agent-runner`:** the community model assumes the action is invoked *frequently enough* (humans typing `@claude` in PRs throughout the day) that the JIT check catches every expiry. Our usage is different — we run agents on cron (potentially nightly or weekly), so a token can expire between two scheduled runs with no human invocation in between. **We need a cron job that does the refresh check independently** of any agent run. Per DESIGN.md §7, we already plan `refresh-oauth.yml` on a 6-hour cron. That instinct was correct.

The community's example workflows are all reactive (issue_comment / pull_request_review_comment / pull_request_review / issues triggers — see `grll/claude-code-action/examples/claude.yml`). Not a single example uses `on: schedule`.

## 5. Token expiry mechanics

From the implementation we can reverse-engineer:

- **Access tokens:** issue #727 says they expire in "approximately 1 day." The `expires_in` field returned by the refresh endpoint is opaque, but a 24-hour value is consistent with the 60-minute refresh buffer (a 60-minute pre-expiry refresh on a 24-hour token gives 4% of the lifetime as headroom — sane for a typical web/CI cadence).
- **Refresh tokens:** lifetime not documented in any source we read. Empirically (per the existence of forks at all and the rotating-refresh pattern), they're long-lived but rotate on each refresh. If a refresh fails silently and the rotated refresh_token isn't persisted, the next refresh attempt will use the now-stale refresh_token and fail.
- **`CLAUDE_EXPIRES_AT` units:** **milliseconds** since Unix epoch, stored as a string. (Documented as "Token expiration timestamp (milliseconds)" in `grll/claude-code-login/action.yml` and confirmed by the `parseInt(credentials.expiresAt)` + `(... + expires_in) * 1000` math in `setup-oauth.ts`.)

## 6. Failure modes and how the community fork handles them

From `setup-oauth.ts` and the action.yml composition:

| Failure | Detection | Handling | Adequacy for `agent-runner` |
|---|---|---|---|
| Refresh API returns non-2xx | `if (response.ok)` else branch | Logs `❌ Token refresh failed: <status> - <body>` and returns `null` | **Insufficient.** No alerting; the run continues with the stale token, which will then fail with auth error during the actual Claude call. We need a Slack notification on refresh failure. |
| Network error reaching `console.anthropic.com` | try/catch around the fetch | Logs error, returns `null` | Same insufficiency. Add notification. |
| `SECRETS_ADMIN_PAT` not configured at all | `if (!credentials.secretsAdminPat)` | Prints a 9-line warning recommending setup, then **proceeds with the existing token** — does not fail the workflow | **Wrong for our use case.** If the PAT is missing for our scheduled refresh job, that's an operator configuration error and should fail loudly, not warn. |
| `gh secret set` fails (auth error, network, etc.) | try/catch around `execSync` | Logs error, **re-throws** (`throw error`) | Acceptable — fails the step. Combined with our notify-on-failure we'd see this. |
| Refresh succeeded, secret update failed mid-way | The three `gh secret set` calls run sequentially with no transactional rollback | Whichever ones succeeded stay updated; subsequent runs may see an inconsistent triple (new access_token, old refresh_token, old expires_at) | **Real risk.** The first two updates often succeed and the third fails on transient flake. Subsequent runs will then either detect the wrong expiry or use mismatched tokens. We should at minimum log enough to recover manually; consider updating in the order `expires_at` → `refresh_token` → `access_token` so a partial failure leaves the system "thinks token is older than it is" rather than the dangerous reverse. |
| The new refresh_token differs but the old is treated as still valid | The implementation always uses the response's `refresh_token` (not the request's) | Correct handling of refresh-token rotation | Adopt verbatim. |
| 60-minute buffer too tight for our weekly-run cadence | None | Hardcoded 60-minute buffer | **Probably fine** for cron-every-6h, but if we ever increase the cron interval to >24h we need a wider buffer. Make it configurable. |

What's *not* handled at all by the community fork:

- **No alerting.** A refresh failure produces console log output only. In a 6-hourly cron job, no human will read the logs. **We must add a Slack post on failure** (DESIGN.md §11 already calls this out for OAuth).
- **No heartbeat.** There's no positive-confirmation "auth healthy" signal, just absence-of-error. A misconfigured cron schedule (e.g. the workflow file rename and forgot to update) would produce silence indistinguishable from success. DESIGN.md §7 already specifies a daily "auth healthy" Slack heartbeat — keep that.
- **No retry.** A transient 503 from `console.anthropic.com` produces a single-shot failure. We should implement at least one retry with backoff in `refresh-oauth.yml`.

## 7. Mapping onto `agent-runner`'s `refresh-oauth.yml`

The verdict per piece:

| Concern | Community fork's choice | `agent-runner` should: | Why |
|---|---|---|---|
| Refresh endpoint URL | `https://console.anthropic.com/v1/oauth/token` | **Adopt verbatim** | This is the Anthropic OAuth surface; no alternative. |
| Request payload (JSON, three fields, hardcoded `client_id`) | As above | **Adopt verbatim** | Including the public client_id `9d1c250a-e61b-44d9-88ed-5944d1962f5e`. |
| Response handling (use NEW refresh_token, convert expires_in*1000 + now_ms) | As above | **Adopt verbatim** | Refresh-token rotation is real; the millisecond conversion matches the existing on-disk format. |
| 60-minute pre-expiry buffer | Hardcoded constant | **Adopt with a knob** | Default to 60 min, expose as a workflow input or env var so we can widen it if we move to a longer cron interval. |
| Secret names | `CLAUDE_ACCESS_TOKEN` / `CLAUDE_REFRESH_TOKEN` / `CLAUDE_EXPIRES_AT` | **Differ deliberately** | DESIGN.md §7 already locks `CLAUDE_CODE_OAUTH_TOKEN` and `CLAUDE_OAUTH_REFRESH_TOKEN`. Stay with our names; that's what `claude-code-action`'s official `claude_code_oauth_token` input is named. We should add `CLAUDE_OAUTH_EXPIRES_AT` (currently unnamed in DESIGN.md §7 — append it). |
| Storage backend (GitHub Secrets via `gh secret set`) | `gh secret set X --body "$VAL"` | **Adapt** — pipe via stdin instead of `--body` | Removes an argv-injection concern; `gh` accepts secret values from stdin natively. |
| PAT name and permissions | `SECRETS_ADMIN_PAT`, fine-grained, `secrets:write` | **Adopt scope, keep our name (`AGENT_RUNNER_PAT`)** | DESIGN.md §7 already names it. Permissions match. |
| Trigger model (just-in-time on every action invocation) | JIT only | **Differ — use cron + on-demand** | Our cron-runs cadence may exceed token lifetime. Run `refresh-oauth.yml` on `schedule` every 6h plus `workflow_dispatch` for manual recovery. |
| Failure handling | console log + warning + continue | **Differ — fail loudly + notify Slack** | A silent refresh failure breaks every subsequent run for 24h. Notify on failure; consider adding a daily heartbeat that posts "auth healthy" so silence is detectable. |
| Retry on transient API failure | None | **Add** — at least one retry with 30s backoff | A 503 in a 6h cron job means 6h of failed agent runs. |
| Update order of the three secrets | access → refresh → expires | **Reverse — update expires_at LAST** | If we crash mid-update, the system reads expires_at as still-old and refreshes again immediately, which is recoverable. The reverse (expires_at updated first, refresh_token never updated) leaves the system thinking the *old* refresh_token corresponds to the *new* expiry — undetectable until next refresh fails. |
| Write `~/.claude/.credentials.json` | Yes, in the runner | **Skip in `refresh-oauth.yml`** | Our refresh job's only job is to update secrets; it doesn't run Claude. The credentials.json is only needed by `runner.yml`'s actual agent step, where `claude-code-action` will write it itself. |

### Concrete `refresh-oauth.yml` skeleton

Pseudocode for what we should ship:

```yaml
name: Refresh Claude OAuth token

on:
  schedule:
    - cron: "0 */6 * * *"   # every 6h
  workflow_dispatch:         # manual recovery

permissions:
  contents: read             # don't need anything else; the PAT carries secrets:write

jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - name: Refresh and update secrets
        env:
          REFRESH_TOKEN:    ${{ secrets.CLAUDE_OAUTH_REFRESH_TOKEN }}
          EXPIRES_AT:       ${{ secrets.CLAUDE_OAUTH_EXPIRES_AT }}
          GH_TOKEN:         ${{ secrets.AGENT_RUNNER_PAT }}
          BUFFER_MIN:       "60"
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        run: python3 scripts/refresh_oauth.py
```

`scripts/refresh_oauth.py` does:

1. `expires_at_ms = int(os.environ["EXPIRES_AT"])`; if `time.time()*1000 < expires_at_ms - BUFFER_MIN*60*1000`, log "still valid, exiting 0".
2. `POST` to `https://console.anthropic.com/v1/oauth/token` with the three-field JSON body. Retry once on `5xx` or network error after 30s.
3. On success: pipe each new value into `gh secret set CLAUDE_OAUTH_EXPIRES_AT` LAST (after access then refresh). Each `gh` call gets a clean stdin via `subprocess.run(..., input=value, text=True)` — no shell quoting.
4. On failure: POST to Slack webhook with run URL + status + truncated error body, then `sys.exit(1)`.

Also add `scripts/auth_heartbeat.py` for the daily "auth healthy" Slack message DESIGN.md §7 already specifies.

## 8. The official Anthropic position (issue #727)

`anthropics/claude-code-action#727` ("Support refresh tokens for Claude Max subscribers in GitHub Actions") was opened December 8, 2025 by `eversluis`. Status as of fetch (2026-05-11): **open, no maintainer response visible**. Labels: `area:installation`, `enhancement`, `p2`, `provider:1p`. The issue accurately describes the problem (~1-day token expiry, no refresh path) and proposes three solutions: (1) accept a `claude_code_refresh_token` input, (2) issue longer-lived tokens for CI, (3) GitHub-App-mediated auth.

Confirmed against the current `anthropics/claude-code-action/main/action.yml`: the only OAuth input is `claude_code_oauth_token`, single value, **no built-in refresh.** The post-execution step revokes the GitHub App installation token only; it does not touch the Anthropic OAuth token.

So the official action *still* has no refresh logic as of 2026-05-11. The community fork is the only working option, and Anthropic shows no sign of merging this in soon. **Implication for `agent-runner`:** we cannot wait for the official action to ship this. Either vendor `grll/claude-code-base-action`'s `setup-oauth.ts` logic into our own script (the recommendation) or use `grll/claude-code-action@beta` directly — which has the marketplace summary's caveat that it's "potentially obsolete" once Anthropic ships native support.

(One inconsistency to flag: a marketplace summary mentioned "As of July 8, 2025, Anthropic integrated these capabilities natively" plus an uninstaller script. The current `anthropics/claude-code-action` action.yml does **not** show OAuth-refresh inputs, so either that note conflates a different feature, or refresh integration was reverted, or the summary was inaccurate. The dispositive evidence is the action.yml plus issue #727 still being open.)

## 9. Vendor vs. adapt vs. build — and the recommendation

Three options for `agent-runner`:

**(A) Vendor `grll/claude-code-action@beta` directly in `runner.yml`.** Pass the four OAuth inputs; let the JIT check do the work. **Cost:** zero implementation; we inherit a TypeScript+Bun action with a 60-minute buffer, no alerting, and the implicit assumption of frequent invocation. **Risk:** for cron-only repos, the JIT check still runs at every cron invocation, so this would actually work — but we lose visibility (no separate "refresh" run we can monitor; refresh failures bury inside agent-run logs).

**(B) Adapt the refresh logic into our own `refresh-oauth.yml` (the recommendation).** Reimplement `setup-oauth.ts` in ~80 lines of Python in `scripts/refresh_oauth.py`. Trigger on `schedule: */6h` plus `workflow_dispatch`. Add Slack notification, retry, ordered secret updates. **Cost:** one afternoon of work plus a test run. **Benefit:** independent visibility, alerting, and a clean audit story ("our refresh logic is N lines, here's the one curl call").

**(C) Build a brand-new approach (e.g. GitHub App, longer-lived tokens).** Out of scope; both depend on Anthropic-side changes we don't control.

**Recommendation: Option B.** The refresh logic is ~30 lines of substantive code (one HTTP call, three secret writes, the expiry check). Vendoring all of `grll/claude-code-base-action` to get those 30 lines pulls in Bun, the TypeScript toolchain, the prepare-prompt logic, and a published action contract we don't need. A small Python script we control end-to-end is the smaller blast radius.

We should still **use `grll/claude-code-action@beta` (or successor) inside `runner.yml`** for the actual agent invocation — that's the user-facing action with all the trigger-parsing and prompt-handling. The JIT refresh inside that action is a no-op when our scheduled `refresh-oauth.yml` has already done the work; it's a belt-and-suspenders backup.

## 10. Risks and unknowns to track

- **Refresh-token rotation lifetime.** Not documented. If Anthropic ever invalidates a refresh_token after a certain inactivity period, our 6h cron would prevent that, but if they cap *total* refresh-token lifetime independently, we'd silently break. **Mitigation:** the daily heartbeat detects this within 24h.
- **The hardcoded `client_id`.** Tied to the Claude Code desktop app's OAuth registration. If Anthropic rotates that ID (e.g., for security), every community fork breaks simultaneously. We accept this risk; it's industry-wide.
- **PAT expiry.** `AGENT_RUNNER_PAT` itself expires in 30-60 days per the README's recommendation. **Track this in PLAN.md as a recurring operational note** (already implied by DESIGN.md §7 but worth making explicit).
- **Secret-update race:** if `runner.yml` is mid-execution while `refresh-oauth.yml` rotates the secrets, the running job has a stale token in memory. This is fine — the stale token is still valid for ~60 min after rotation (we refresh 60 min ahead of expiry), so the run completes normally. New runs immediately pick up the fresh token. Document this property; do not "fix" it with locking.
- **`anthropics/claude-code-action` may add native refresh.** When it does, retire our custom code and the JIT logic in the fork both. Track via `gh issue view anthropics/claude-code-action#727` periodically.

## 11. Concrete updates this report implies

For follow-up commits (after this report lands and is merged via the dispatcher):

1. **DESIGN.md §7:** add `CLAUDE_OAUTH_EXPIRES_AT` to the secrets list (currently missing — only `CLAUDE_CODE_OAUTH_TOKEN` and `CLAUDE_OAUTH_REFRESH_TOKEN` are named). Add a sentence clarifying expiry is in milliseconds.
2. **DESIGN.md §7:** state the refresh endpoint and the `client_id`-is-public fact, citing this report.
3. **DESIGN.md §11:** append a "secrets-update-ordering" failure mode with the recovery rationale.
4. **DESIGN.md §10 (Stage 3):** reference `scripts/refresh_oauth.py` and `scripts/auth_heartbeat.py` as the deliverables; note that the JIT check inside `claude-code-action` is a backup, not the primary refresh path.
5. **A new short doc `RUNBOOK.md` (optional, can fold into DESIGN.md):** "If `refresh-oauth.yml` fails for >24h, do this: …" — basically, manually rerun `grll/claude-code-login` to get fresh credentials, set the three secrets, dispatch `refresh-oauth.yml` to confirm.

---

## Sources reviewed

| Source URL | Status | Notes |
|---|---|---|
| `https://raw.githubusercontent.com/grll/claude-code-base-action/main/src/setup-oauth.ts` | ✅ Full review | The 151-line file fetched verbatim via curl. Load-bearing for §2 (refresh API call), §3 (storage), §6 (failure modes). All quoted code blocks come from this file with line numbers. |
| `https://raw.githubusercontent.com/grll/claude-code-action/main/action.yml` | ✅ Full review | The composite-action wrapper. Confirmed it passes the four OAuth inputs (`claude_access_token`, `claude_refresh_token`, `claude_expires_at`, `secrets_admin_pat`) through to `claude-code-base-action`. Informed §4 (no schedule trigger) and §7 (mapping). |
| `https://raw.githubusercontent.com/grll/claude-code-login/main/action.yml` | ✅ Full review | The OAuth login action — performs the *initial* code exchange and writes the three secrets. Established that the same secret-naming convention applies to refresh. Informed §3a, §3b. |
| `https://raw.githubusercontent.com/grll/claude-code-login/main/README.md` | 🟡 Reconstructed (summary only via WebFetch) | The README summary covered the SECRETS_ADMIN_PAT prerequisites (fine-grained PAT, secrets:write, 30-60d expiry recommendation) and the three-secret naming. Full prose not quoted. Informed §3c. |
| `https://raw.githubusercontent.com/grll/claude-code-base-action/main/README.md` | 🟡 Reconstructed (summary only via WebFetch) | Confirmed the OAuth-via-PAT model and that no cron examples are documented. Informed §4 and §9. |
| `https://github.com/marketplace/actions/claude-code-action-with-oauth` | 🟡 Reconstructed (summary only via WebFetch) | The marketplace listing's "Token Refresh Mechanism" paragraph confirmed the JIT model. The "Anthropic introduced native GitHub Actions support" note flagged for §8 inconsistency review. Informed §8. |
| `https://github.com/anthropics/claude-code-action/issues/727` | 🟡 Reconstructed (summary only via WebFetch) | Confirmed: open, p2, no maintainer response. Original ask is for `claude_code_refresh_token` input. Informed §8 — "we cannot wait for the official action." |
| `https://raw.githubusercontent.com/anthropics/claude-code-action/main/action.yml` | 🟡 Reconstructed (summary only via WebFetch) | Confirmed: only `claude_code_oauth_token` input, no refresh. Disposes of the "Anthropic added native support" inconsistency in favor of "still not shipped as of 2026-05-11." Informed §8. |
| `https://raw.githubusercontent.com/grll/claude-code-action/main/examples/claude.yml` | ✅ Full review | The canonical example workflow. All four triggers are reactive (issue_comment, pull_request_review_comment, pull_request_review, issues); no `on: schedule`. Confirmed §4's "no community cron-refresh pattern." |
| `https://github.com/grll/claude-code-base-action/tree/main/src` | ✅ Full review (directory listing) | Six files: `index.ts`, `prepare-prompt.ts`, `run-claude.ts`, `setup-claude-code-settings.ts`, `setup-oauth.ts`, `validate-env.ts`. Pinpointed `setup-oauth.ts` as the file to read in full. |
| `https://github.com/grll/claude-code-action/tree/main/src` | ✅ Full review (directory listing) | Confirmed the user-facing fork delegates the entire OAuth flow to `claude-code-base-action`; no refresh logic lives in this repo. |
| `https://github.com/grll/claude-code-action/tree/main/examples` | ✅ Full review (directory listing) | Five example workflows; verified `claude.yml` is the canonical OAuth example. |
| `https://raw.githubusercontent.com/grll/claude-code-login/main/index.ts` | 🟡 Reconstructed (summary only via WebFetch) | Confirmed the file contains *only* initial-login functions (`generateLoginUrl`, `exchangeCode`, `saveCredentials`, `verifyState`, `cleanupState`); no refresh function. This is what told us refresh logic must live elsewhere — pointing to `setup-oauth.ts`. Informed §1 (clarifying which repo owns which piece). |
