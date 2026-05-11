# Report 07 — OAuth refresh shipping status watch

**Date:** 2026-05-11
**Author:** Subagent (run 20260511-r3, sub-03)
**Status:** ✅ complete (operational watch)

## Lead question

Has Anthropic shipped native OAuth-refresh support in `anthropics/claude-code-action` — specifically, has `action.yml` gained a `claude_code_refresh_token` (or analogous) input — that would let `agent-runner` retire its custom `scripts/refresh_oauth.py` plus the JIT logic in the community fork? This report is the recurring operational watch defined by Report 02 §11.

## Trigger criteria from report 02

Report 02 §10–§11 defines the trigger to retire our custom refresh code as follows (verbatim, with light extraction):

From §10 (Risks and unknowns to track):

> **`anthropics/claude-code-action` may add native refresh.** When it does, retire our custom code and the JIT logic in the fork both. Track via `gh issue view anthropics/claude-code-action#727` periodically.

The dispositive evidence from Report 02 §8 was:

> Confirmed against the current `anthropics/claude-code-action/main/action.yml`: the only OAuth input is `claude_code_oauth_token`, single value, **no built-in refresh.** The post-execution step revokes the GitHub App installation token only; it does not touch the Anthropic OAuth token.

So the **trigger condition** that this watch tests for is:

1. `anthropics/claude-code-action`'s `main/action.yml` adds an input named `claude_code_refresh_token` (or a refresh-shaped equivalent: `oauth_refresh_token`, `refresh_token`, etc.), **and/or**
2. Issue #727 is closed by a maintainer with a release pointer, **and/or**
3. A release of `anthropics/claude-code-action` ships notes mentioning OAuth refresh / token rotation.

Any one of those firing means we should begin the retirement audit; all three firing makes it a deletion sprint.

## Status as of 2026-05-11

### `action.yml` on main

Fetched `https://raw.githubusercontent.com/anthropics/claude-code-action/main/action.yml`. The authentication-related inputs are exactly:

- `anthropic_api_key` — "Anthropic API key (required for direct API, not needed for Bedrock/Vertex/Foundry)"
- `claude_code_oauth_token` — "Claude Code OAuth token (alternative to anthropic_api_key)"
- `github_token` — "GitHub token with repo and pull request permissions (optional if using GitHub App)"

**No `claude_code_refresh_token`. No `oauth_refresh_token`. No `refresh_token`. No refresh-shaped input of any kind.** The shape is unchanged from Report 02's snapshot: a single opaque `claude_code_oauth_token` with no companion refresh field and no expiry hint.

### Issue #727

`https://github.com/anthropics/claude-code-action/issues/727` — fetched 2026-05-11.

- **State:** open
- **Labels:** `area:installation`, `enhancement`, `p2`, `provider:1p` (unchanged from Report 02's snapshot — same four labels)
- **Original ask (unchanged):** accept a `claude_code_refresh_token` input, OR issue longer-lived tokens for CI, OR have the GitHub App handle auth
- **Maintainer response:** none visible. No Anthropic employee has commented since the issue was opened on December 8, 2025 (~5 months of silence).

The issue is in exactly the same state Report 02 documented: open, p2, no maintainer engagement.

### Releases

`https://github.com/anthropics/claude-code-action/releases`, last 10 tags:

| Tag | Date | OAuth-relevant? |
|---|---|---|
| v1.0.119 | May 9 | no notes |
| v1.0.118 | May 9 | no notes |
| v1.0.117 | May 8 | no notes |
| v1.0.116 | May 7 | "Updated HackerOne links in SECURITY.md" — not OAuth |
| v1.0.115 | May 6 | no notes |
| v1.0.114 | May 6 | no notes |
| v1.0.113 | May 6 | no notes |
| v1.0.112 | May 4 | "Fixed trigger_phrase to match case-insensitive" — not OAuth |
| v1.0.111 | May 1 | no notes |
| v1 (umbrella v1.0) | Aug 26 | major release; no OAuth/refresh mention |

**None of the recent releases mention OAuth, refresh tokens, or authentication changes.** Notably, `CHANGELOG.md` does not exist at the repo root (HTTP 404), so the per-tag release notes (most of which are blank) are the only release-channel signal available.

## Verdict

**Trigger fired: NO.**

None of the three trigger conditions are met:

1. `action.yml` has not gained a refresh-token input.
2. Issue #727 is still open with zero maintainer responses.
3. No release in the last 10 tags mentions OAuth/refresh.

The state of native-refresh support in `anthropics/claude-code-action` is **unchanged from Report 02's snapshot** (which was already 2026-05-11; this report was written the same day to establish a baseline). Future watches at this report's cadence (see §Recommendation) should compare against this baseline.

**Rough timing prediction.** With a `p2` label, no maintainer responses in ~5 months, and no Anthropic-internal signal in the public action repo, native refresh is unlikely to ship in the next 1–2 quarters. Realistic earliest: late Q3 2026; more likely Q4 2026 or later. If Anthropic instead routes Max-subscriber CI through the GitHub App path (option 3 in #727), that could ship faster but would land as a different feature surface and require a separate audit of `runner.yml`.

## Recommendation

**Keep watching. Do not retire `scripts/refresh_oauth.py` or the surrounding cron/JIT machinery.** Specifically:

1. **Re-run this watch on a 4-week cadence.** Re-fetch the same three sources (action.yml, #727, releases) and diff against §"Status as of 2026-05-11" above. If any of the three changes, escalate to a full retirement-audit report.
2. **Consider adding a thumbs-up reaction or a brief comment to #727** from an `agent-runner` maintainer to keep the issue visible. (Optional; do not have a subagent do this — it's a human relations call.)
3. **Do not pre-emptively wire refresh-token plumbing on the action-side.** If the input lands, it will land with a documented name and contract; speculative pre-wiring against a guessed input name will just create churn.
4. **When the trigger does fire:** retirement work is roughly (a) replace `grll/claude-code-action@beta` with `anthropics/claude-code-action@<version>` in `runner.yml`, (b) wire `CLAUDE_OAUTH_REFRESH_TOKEN` into the new input, (c) delete `.github/workflows/refresh-oauth.yml`, (d) delete `scripts/refresh_oauth.py` and `scripts/auth_heartbeat.py` (or repurpose the heartbeat for a different signal), (e) delete the `AGENT_RUNNER_PAT` secret if nothing else needs it, (f) update DESIGN.md §7 and §11. None of that is needed today.

The custom refresh code in `agent-runner` is therefore expected to remain load-bearing for at least the next quarter, probably longer.

---

## Sources reviewed

| Source URL | Status | Notes |
|---|---|---|
| `https://raw.githubusercontent.com/anthropics/claude-code-action/main/action.yml` | ✅ Fetched 2026-05-11 | Authentication inputs are `anthropic_api_key`, `claude_code_oauth_token`, `github_token`. No refresh-shaped input. Unchanged from Report 02. |
| `https://github.com/anthropics/claude-code-action/issues/727` | ✅ Fetched 2026-05-11 (via WebFetch; the GitHub MCP tool is restricted to `lago-morph/agent-runner` in this session) | Open, labels `area:installation`/`enhancement`/`p2`/`provider:1p`, no maintainer responses. Opened 2025-12-08 by `eversluis`. State unchanged from Report 02 snapshot. |
| `https://github.com/anthropics/claude-code-action/releases` | ✅ Fetched 2026-05-11 (via WebFetch) | Last 10 tags v1.0.111–v1.0.119 plus the v1 umbrella. No OAuth/refresh/auth-related notes in any of them. |
| `https://raw.githubusercontent.com/anthropics/claude-code-action/main/CHANGELOG.md` | ❌ HTTP 404 | The repo does not maintain a top-level CHANGELOG.md; release notes only. |
| `research/02-oauth-refresh-forks.md` (this repo) | ✅ Re-read for trigger criteria | §10 defines the trigger; §8 establishes the prior baseline. |
