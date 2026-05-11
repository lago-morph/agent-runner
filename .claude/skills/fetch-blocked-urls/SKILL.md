---
name: fetch-blocked-urls
description: Use when a web source is unreachable from the Claude Code sandbox — typical signals are WebFetch returning HTTP 403, "host not allowed", a tiny response (< 6 KB) whose body contains "Just a moment..." (Cloudflare challenge), or "Attention Required". The skill files a GitHub issue listing the URLs; the repository's `fetch-blocked-urls` action picks it up from a normal HTTP environment, fetches each page, commits the saved HTML and html2text markdown to a new `fetched/issue-N` branch, comments with merge instructions, and leaves the issue open for you to close once merged. Triggers on phrases like "fetch this URL", "the page is blocked", "Cloudflare is blocking us", "save these sources", "I need to read this page but I can't access it".
tags: [research, github, actions, blocked-sources]
allowed-tools: [Bash]
---

# Fetch blocked URLs

## When to use

Trigger this skill when **all** of the following are true:

- A web page is unreachable from this sandbox (`WebFetch` returns 403 / "host not allowed" / a Cloudflare challenge / a tiny suspicious response).
- You have already verified the issue is not a typo or a redirect (e.g., for GitHub repos you tried `raw.githubusercontent.com`; for blogs you tried both the canonical URL and any obvious mirror).
- You actually need the content to make progress — don't trigger for incidental references that aren't load-bearing.

If the source is paywalled (Every.to chain-of-thought past the visible portion; Lenny's Newsletter interview bodies), the fetcher cannot bypass that. It will commit whatever the action receives, which for paywalled content means the visible "subscribe to read" portion only. Note the limit and move on.

## What it does

The repository's `.github/workflows/fetch-blocked-urls.yml` workflow does the work. When the `fetch-urls` label is applied to an issue with a JSON URL list in its body:

1. Workflow triggers **only** on `issues: labeled` (plus `workflow_dispatch` for manual re-runs). It does NOT run on `opened`, `edited`, or `reopened` — applying the `fetch-urls` label is the sole affirmative trigger, and editing the issue body afterwards (e.g. to close it with a summary) does not re-fire the fetch.
2. **Label gate.** The workflow's first logged step checks that the just-applied label (`github.event.label.name`) is exactly `fetch-urls`. Applying any other label to an issue, including an unrelated label on an already-fetched issue, exits cleanly.
3. URLs are extracted from the issue body (`extract_urls.py`) by parsing **JSON only**:
   - A bare JSON value (array of URL strings or `{"urls": [...]}` object) at the very top of the body, OR
   - A ```` ```json ```` fenced code block anywhere in the body (preferred — renders nicely in the GitHub UI).
   - **Anything else in the body is ignored.** Free-form prose, session-URL footers, decoy links in markdown — all ignored. Only URL strings inside the JSON list are candidates for fetching.
   - URLs must start with `http://` or `https://`, be ≤ 2048 chars. Non-string entries are filtered. Duplicates dropped (first occurrence wins).
4. Cap: at most **50 URLs per issue**, 30-second per-URL timeout. Over the cap → the workflow comments and exits non-zero.
5. Each URL is fetched with `curl -L -A 'Mozilla/5.0 (compatible; agent-runner-fetch/1.0; …)' --max-time 30` (`fetch_urls.sh`).
6. For each URL, two files are written:
   - `research/fetched/issue-<N>/<sha1prefix>_<sanitized-host-and-tail>.html` — raw response body
   - `research/fetched/issue-<N>/<sha1prefix>_<sanitized-host-and-tail>.md` — best-effort html2text conversion (only written on HTTP 200)
7. The output is committed to a **new branch** `fetched/issue-<N>` (never to `main`, never to your working branch). If the branch already exists from a previous run, it is force-updated.
8. The action comments on the issue with merge instructions and a per-URL summary, then leaves the issue open until you close it.

## Authorization model

**The `fetch-urls` label is both the trigger and the security gate.** The workflow listens only for the `labeled` event, and the first step requires `github.event.label.name == 'fetch-urls'`. Applying that specific label is the affirmative authorization signal.

Why this works: in GitHub, only users with **Triage role or higher** can apply labels to issues. A drive-by user opening an issue cannot satisfy the gate even if they know the magic label name — they don't have the permission to apply it. Triage is granted explicitly by a repo admin. Equally, opening an issue (with or without the label) without the `labeled` event firing does nothing; a runner is not even spun up.

The earlier (pre-2026-05-10) version of this workflow gated on `author_association` instead. That gate silently failed because the **webhook payload and the REST API report different values** for the same user on the same event (the webhook said `CONTRIBUTOR`, the REST API said `MEMBER`). Don't reintroduce that check — the label-as-trigger is sufficient and not subject to that footgun.

Why no `opened`/`edited`/`reopened` triggers: an earlier design listened for all of those, gated on label presence. That worked but had three costs that motivated tightening to label-only:
- **Wasted runner minutes** on every unrelated issue opened or edited on the repo (the workflow ran, the gate exited, ~10 seconds of CI billed).
- **Surprise re-fetches.** Editing a fetched issue (e.g. to add a closing summary in the body) re-fired the workflow and force-pushed a new SHA to `fetched/issue-<N>`. The fetch happened on a *closed* issue, which is not what the author intended.
- **Muddied intent.** "The label IS the trigger" is a one-line invariant; "the label is a gate inside a workflow that runs on every issue event" is harder to reason about and easier to mis-tune.

The job is also bounded by:
- `permissions: contents: write, issues: write` — no secrets, no other repos
- 50-URL per-issue cap, 30s per-URL timeout
- **Never pushes to `main`** — always creates `fetched/issue-<N>`
- No `if: ${{ secrets.X != '' }}` checks (which would allow secret-conditioned behavior)

Residual risk: a compromised collaborator account with Triage role could apply the label to arbitrary issues. The action does not execute fetched content — it only stores it as files. Worst case: a junk branch gets created and is deleted.

## Usage from this session

The issue body **must** start with a JSON URL list. Two accepted shapes:

```json
["https://example.com/page", "https://another.example/article"]
```

or, with named field for future extensibility:

```json
{"urls": ["https://example.com/page"]}
```

A ```` ```json ```` fenced code block anywhere in the body is also accepted (and recommended — it renders nicely). Anything outside the JSON — context notes, session-URL footers, decoy links in prose — is **ignored**.

### Canonical `gh` CLI template

(Outer fence is four backticks so the inner ```` ```json ```` renders literally.)

````bash
gh issue create \
  --label fetch-urls \
  --title "[fetch-urls] <short description>" \
  --body "$(cat <<'EOF'
```json
{
  "urls": [
    "https://example.com/some-page",
    "https://another.example.com/article"
  ]
}
```

Context (optional, IGNORED by the workflow): why we need these / which
research thread this serves.
EOF
)"
````

### Canonical MCP path (preferred from this session)

```python
mcp__github__issue_write(
    method="create",
    owner="lago-morph",
    repo="agent-runner",
    title="[fetch-urls] <short description>",
    labels=["fetch-urls"],
    body='```json\n{"urls": ["https://example.com/page"]}\n```\n\nContext (ignored): ...',
)
```

Creating an issue with `labels=["fetch-urls"]` fires the `labeled` event GitHub-side, which triggers the workflow. If you create the issue without the label first, apply it separately to trigger the fetch.

### Notes

- The `fetch-urls` label is the trigger; the workflow does not run without it. The label is auto-created by `mcp__github__issue_write` on first use, or you can create it explicitly: `gh label create fetch-urls --description "Trigger fetch-blocked-urls.yml workflow"`.
- The issue **title** is convention only (`[fetch-urls] …`). The workflow does not read the title.
- The `gh` CLI must be authenticated to a user with Triage role or higher in this repo, so it can apply the label. Run `gh auth status` first if uncertain.
- If the JSON fails to parse or contains zero usable URLs, the workflow comments "No URLs found..." and exits cleanly. No branch is created.

After the action completes (typically 1–3 minutes), you'll see a comment on the issue with per-URL status and merge instructions. To pull the fetched content into your working branch:

```bash
git fetch origin fetched/issue-<N>
git merge --no-ff origin/fetched/issue-<N>
```

The action does not auto-close the issue — close it manually once you've merged so other agents know it's handled. **Editing the issue body after the fact does NOT re-fire the workflow.** Use one of the re-run paths below.

## Re-running against an existing issue

Editing the issue body does **not** re-fire the workflow (the `edited` trigger is intentionally disabled — see the *Authorization model* section for why). Two paths to re-run:

- **Remove and re-apply the `fetch-urls` label.** Each `labeled` event triggers a fresh run. The `fetched/issue-<N>` branch is force-updated (history reset) so the latest issue body is the source of truth.
- **`workflow_dispatch`.** Trigger manually from the Actions UI with `issue_number: <N>`. Bypasses the label gate; only users with `actions:write` (i.e., a repo collaborator) can dispatch.

```bash
gh workflow run fetch-blocked-urls.yml -f issue_number=<N>
```

If you edit the issue body to change which URLs are fetched, edit first, then re-apply the label — otherwise the re-run will use the *current* body, not the version that was current when the label was first applied. (Both paths use the gh CLI which reads the current body live; the workflow does not store snapshots.)

## Filename convention

Files fetched via this action live under `research/fetched/issue-<N>/` with sha1-prefixed sanitized names:

```
<sha1(url)[:10]>_<host-and-tail-sanitized>.html
<sha1(url)[:10]>_<host-and-tail-sanitized>.md
```

The sha1 prefix guarantees uniqueness even for pathological URLs (very long, query-heavy, or characters that collide after sanitization). The trailing host-and-path component is included verbatim (up to 80 chars) so file listings are still browsable.

Example: `https://www.jayminwest.com/agentic-engineering-book/6-harnesses` →
`4f2b8a91c3_www.jayminwest.com__agentic-engineering-book__6-harnesses.html`

The sha1-prefixed layout applies to every file the action writes. If any manually-curated fetches accumulate at other paths over time, keep them out of `research/fetched/issue-*/` so the two conventions don't collide.

## Result classification (per-URL summary)

Each fetched URL appears in the issue comment under "Per-URL summary" with a status:

- `(HTTP 200, N bytes)` — saved. Inspect for content quality (Cloudflare challenges can return 200 with a fake body; check the size and the first few KB).
- `FAILED (HTTP 4xx/5xx, …)` — saved (with whatever partial body came back) plus the first 200 chars of curl's stderr. Useful for debugging.
- `FAILED (HTTP 000, 0 bytes)` — connection error (DNS, TLS, timeout). Nothing useful saved.

When a Cloudflare challenge slips through as HTTP 200, the HTML body will be small (~5–10 KB) and contain "Just a moment..." / "challenge-platform". Inspect, then switch to a fallback.

## Fallbacks when the action also gets blocked

For sources whose Cloudflare challenge the action cannot solve (the runner is not a real browser, so JavaScript challenges fail):

1. **Wayback Machine.** `https://web.archive.org/web/2026*/<original-url>` — file a follow-up issue with the wayback URLs instead. Wayback snapshots are post-render, so they often work where the live URL doesn't.
2. **Google Cache** (when available): prefix the URL with `https://webcache.googleusercontent.com/search?q=cache:`
3. **Medium alternative front-ends.** For Medium articles, try `scribe.rip` or `freedium.cfd` mirrors with the same path.
4. **Manual save.** As a last resort, open the page in a real browser yourself, "Save as → Web page complete (single file)", and commit the HTML to `research/fetched/manual/` on a branch.

## Limitations

- **No login / no paywall bypass.** The action cannot authenticate. Captured content for paywalled URLs is the visible "subscribe to read" portion only.
- **JavaScript challenges.** Cloudflare's interactive challenges cannot be solved by curl. Use Wayback or manual save.
- **No JS-rendered DOM.** The fetcher receives the initial HTML response, not the rendered DOM. For SPAs that render content client-side, the saved HTML may be skeletal. Wayback's post-render snapshots are usually a fix.
- **Runner minute quota.** GitHub Actions minutes are not unlimited. Bundle related URLs into one issue rather than firing many small issues.
- **Each issue produces a new branch.** Don't be surprised by branch proliferation; `fetched/issue-*` branches are safe to delete after merge.

## Disabling

- **Skill:** delete `.claude/skills/fetch-blocked-urls/`.
- **Action:** delete `.github/workflows/fetch-blocked-urls.yml` (or rename to `.yml.disabled`).
- **Soft-disable:** remove the `fetch-urls` label from the repo. New issues then can't satisfy the gate.

## See also

- `.github/workflows/fetch-blocked-urls.yml` — the workflow definition (with inline security commentary)
- `.github/scripts/extract_urls.py` — URL extractor (bare + markdown-link + dedup)
- `.github/scripts/fetch_urls.sh` — per-URL curl + html2text + summary writer
- `.github/scripts/README.md` — short helper documentation with local-test recipes
- `.claude/skills/research-pipeline/SKILL.md` — the broader research methodology this fetcher supports; describes how fetched content gets read and cited

## Provenance

Adapted from [`lago-morph/software-factory`](https://github.com/lago-morph/software-factory) `@main`. Identical workflow logic; only the user-agent string and a few repo-specific references were rewritten for `agent-runner`.
