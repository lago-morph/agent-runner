# AGENTS.md suggestions — 2026-05-11-01

These are proposed additions to the project's agents file (typically `AGENTS.md` at the repo root). The repo currently has no `AGENTS.md`; this document doubles as a seed.

Each section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for doing it, grounded in something that happened (or nearly happened).

Decide each on its own merits. Skip ones that don't apply to your operating posture; copy-paste the ones that do.

---

## Suggestion 1: PR-only writes to `main`

### Proposed addition

> **PR-only writes to `main`.** Never attempt `git push origin main` from a Claude Code on the Web sandbox. The proxy will 403 the push, and the apparent failure mode (a network error rather than a permission error) wastes diagnostic time. Always use the feature-branch + PR + merge pattern. The branch name pattern is `claude/<short-task-slug>`.
>
> *Grounded in: PR #9, where a direct push to `main` was 403'd before the PR workflow was reached.*

### Why this earns its place in your agents file

A fresh agent without this rule will spend its first attempt trying the most natural action — `git push origin main` — and will read the 403 as a transport problem rather than a policy enforcement. That's at minimum one wasted tool call plus a chain-of-thought paragraph diagnosing "is the proxy down?" The cost to add the rule is zero — the rule fits in two sentences and removes ambiguity at first encounter. The PR workflow is also already encoded in the `always-commit-skill-to-repo` skill, so stating it in `AGENTS.md` is a redundant safeguard, not a new requirement.

---

## Suggestion 2: Skill mirroring for in-session updates

### Proposed addition

> **Skill installs go to two locations when the skill must run in this session.** Commit to `.claude/skills/<name>/` for persistence (this is the source of truth). Also `cp` to `~/.claude/skills/<name>/` so the running harness picks up the change without a session restart. The `~/.claude/` copy is ephemeral and must not be committed. The skill registry will list the skill twice — that is harmless duplication, not a bug.
>
> *Grounded in: PR #10, where the upstream `self-retrospective` update was mirrored to both locations and the harness re-scanned showing the new description.*

### Why this earns its place in your agents file

The "skill not picking up your edits" failure mode is silent — the agent sees the old behaviour in the skill list and assumes the install didn't happen, when in fact only the repo copy updated and the running session still has the original. Without the mirror, the only fix is a session restart, which loses all in-flight context. The cost of mirroring is one extra `cp` per file. The cost of *not* mirroring is up to a full session's worth of work if the new skill behaviour was needed mid-session. Asymmetric cost.

---

## Suggestion 3: `subscribe_pr_activity` default-on

### Proposed addition

> **Subscribe to PR activity immediately after creating a PR.** Call `mcp__github__subscribe_pr_activity` as the next tool after `mcp__github__create_pull_request`. Do not ask the user first. The only exception is if the user has explicitly opted out *for this specific PR*. The cost of an unwanted subscription is one webhook delivery; the cost of missing CI failures or review comments on a PR you authored is at minimum a follow-up round-trip and potentially a stale merge.
>
> *Grounded in: PR #9, which codified this policy in the `always-commit-skill-to-repo` skill.*

### Why this earns its place in your agents file

The default-on policy is already in the skill, but skill text is read on activation, not on every PR creation. An agents-file rule is read once at session start and primes the agent. Defence-in-depth on a load-bearing default is cheap: two sentences. The alternative is the previous policy of "offer to subscribe when the user wants ongoing automation", which produced silent failure modes where the agent created a PR and walked away while CI was still running.

---

## Suggestion 4: Plumbing-PR autopilot is acceptable; source-code PRs are not

### Proposed addition

> **Plumbing-PR autopilot (subscribe → status-read → self-merge) is permitted for PRs that touch only skill files, config, docs, or generated artifacts. It is NOT permitted for PRs touching source code, schema migrations, CI workflows, dependency upgrades crossing a major version, or anything in `/auth/`, `/security/`, or `*.lock` files.** When in doubt, stop at the open PR and hand back to the user.
>
> *Grounded in: PRs #9 and #10, both of which executed the autopilot cleanly on skill-file changes only.*

### Why this earns its place in your agents file

Without this rule the agent has to re-derive "is this safe to self-merge?" per PR. With it, the rule is grep-able: does the diff touch any path in the negative list? If yes, stop. If no, autopilot. That converts a judgement call into a deterministic check. The cost is one paragraph; the cost of getting it wrong (an autonomous merge of a code change to `main` without review) is asymmetric and not always reversible — even `git revert` leaves the bad merge in history.

---

## Suggestion 5: Prefer `git clone` for fetching content outside the MCP allow-list

### Proposed addition

> **For reading files from a GitHub repository other than the working repo, prefer `git clone --depth 1` over `WebFetch` or `mcp__github__get_file_contents`.** The GitHub MCP server is allow-listed to the working repo only and will refuse other repos. WebFetch is per-URL and incurs HTML-parsing overhead per file. One shallow clone gives the full tree in one command with deterministic content. Clean up `/tmp/<clone-dir>` when done.
>
> *Grounded in: PR #10, where `git clone --depth 1 https://github.com/lago-morph/software-factory.git /tmp/software-factory` retrieved the upstream skill tree in one step.*

### Why this earns its place in your agents file

The first instinct for "read these GitHub files" is WebFetch with a raw-content URL, which works but requires URL guessing (path under `raw.githubusercontent.com`, branch name, etc.) and one call per file. A new agent will often miss the cheaper option. Stating it in `AGENTS.md` saves the discovery cost and produces materially cheaper sync operations.

---

## Suggestion 6: Verify UTC date with a tool call before any date-stamped filename

### Proposed addition

> **Never trust the model's notion of "today's date" for filename stamping.** Even when the system context provides a `currentDate`, verify with `date -u +%Y-%m-%d` (or `python3 -c "import datetime; print(datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d'))"`) before writing any file whose name embeds the date. Filename drift breaks day-sequence numbering and is silent — there is no error, only a hole in the sequence.
>
> *Grounded in: the `self-retrospective` skill itself, which explicitly mandates this and is the reason the retrospective package landed at `retrospective/2026-05-11-01.md` with verifiable provenance.*

### Why this earns its place in your agents file

The cost is one tool call. The cost of a wrong date in a filename is permanent — the file ends up under the wrong day's prefix, the day's sequence number is off, and subsequent retrospectives can't reliably find their predecessors. This is the kind of rule that earns its place precisely because it is boring to state and expensive to violate.

---

## Suggestion 7: Decide once, then act; don't litigate in chain-of-thought

### Proposed addition

> **When choosing between two acceptable actions (e.g., "self-merge or hand back", "ask the user or proceed"), decide once based on the session's precedent and act. Do not flip-flop in chain-of-thought. The Opus 4.7 reasoning stream is fully visible to the user; visible indecision is wasted stream output and undermines confidence.**
>
> *Grounded in: PR #10's open-merge-or-not deliberation, where the same decision was re-litigated three times in chain-of-thought before the call was made. The eventual decision was correct; the path to it was noisy.*

### Why this earns its place in your agents file

This is a meta-rule rather than a technical one, but it has a measurable cost: each deliberation cycle is 30–80 tokens of visible chain-of-thought that adds nothing to the eventual action. Across a long session, that compounds. The corrective is one sentence: lock in the decision criterion (precedent + risk class) and commit. Reviewers can disagree with the criterion; that is fine and editable. They cannot productively engage with five iterations of "but on the other hand…".

---

## Suggestion 8: Clean up `/tmp` workspaces after consumption

### Proposed addition

> **After consuming a `/tmp/<workdir>` (e.g., a shallow clone of an upstream repo), `rm -rf` it before ending the task.** The sandbox `/tmp` is ephemeral and will be lost on session end, so this is not a persistence concern — it is hygiene. A leftover `/tmp/<repo>` from a prior task is one more thing the next agent has to interpret ("is this stale or in-flight?") and is the kind of low-signal artifact that quietly bloats sandbox state.
>
> *Grounded in: PR #10 cleanup step, which removed `/tmp/software-factory` after the sync committed.*

### Why this earns its place in your agents file

Cheap to state, cheap to comply with, removes a small but real cognitive cost from any subsequent agent that pokes around `/tmp`. The alternative is the gradual accumulation of stale clones that look like work-in-progress but aren't.