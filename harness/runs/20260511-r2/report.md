# Fanout run report — 20260511-r2

Run on 2026-05-11. Goal: execute Round-2 research from `research/PLAN.md` (three clusters: OAuth refresh forks, AE book exec-layer chapters, OpenHands SDK git-provider abstraction).

## Summary

| Subtask | Branch | Status | Lines | Source SHA | Output |
|---------|--------|--------|-------|-----------|--------|
| sub-01 | `claude/research-merge-branches-wN3BO--sub-01` | merged | 279 | `9055649` | `research/02-oauth-refresh-forks.md` |
| sub-02 | `claude/research-merge-branches-wN3BO--sub-02` | merged | 453 | `a4fc725` | `research/03-ae-book-exec-layer.md` + `.fetch-work/urls.txt` |
| sub-03 | `claude/research-merge-branches-wN3BO--sub-03` | merged | 515 | `1334017` | `research/04-openhands-sdk-git-provider.md` |

## Merge log

- **sub-01**: cherry-picked `research/02-oauth-refresh-forks.md` from `origin/...--sub-01@9055649`. Clean.
- **sub-02**: cherry-picked `research/03-ae-book-exec-layer.md` + `.fetch-work/urls.txt` from `origin/...--sub-02@a4fc725`. Clean.
- **sub-03**: cherry-picked `research/04-openhands-sdk-git-provider.md` from `origin/...--sub-03@1334017`. The sub-03 branch had 4 contamination commits (issue-12 + issue-13 fetched-branch merges from sub-02 misrouting); cherry-pick of only the report file avoided pulling those onto the feature branch.

**Standard 3-way `git merge` was deliberately skipped** in favor of file-level cherry-pick because:
1. Sub-branches were contaminated by concurrent execution sharing one sandbox workdir.
2. Each subagent's deliverable was file-bounded (one new report file), so cherry-pick produces identical content with cleaner history.
3. The fetched raw HTML/markdown (`research/fetched/issue-{12,13}/`) was already cleaned up by sub-02 per the research-pipeline Phase 9 cleanup; replaying it via 3-way merge would have re-introduced and re-deleted the files in nested merge commits.

## Fetch workflow runs

- **Issue #12** (`[fetch-urls] AE book exec-layer chapters (round 2)`): opened by sub-02 first attempt; workflow ran but body-extraction surfaced the wrong URLs (the JSON code block was not formatted exactly as `extract_urls.py` expected). Branch `fetched/issue-12` was created with content but deemed unusable.
- **Issue #13** (`[fetch-urls] AE book exec-layer chapters (round 2)`, retry): opened by sub-02 with the JSON format copied verbatim from prior successful issue #5. Workflow succeeded; branch `fetched/issue-13` carried 6 paired `.html` + `.md` files. Sub-02 merged that branch in, read the markdown, and `git rm`'d all 12 raw files per Phase 9 cleanup.

Both issues remain OPEN; the research-pipeline convention is to leave them open for UI-side close. The `fetched/issue-12` and `fetched/issue-13` branches remain on origin (sandbox proxy blocks deletion); they can be deleted from the GitHub UI when convenient.

## Deviations

- **sub-03 reported 4 unrelated commits inherited from sub-02 contamination**, but its own report-add commit (`1334017`) was clean. Cherry-pick kept history clean.
- **sub-01 reported it briefly checked out sub-03 by mistake** at session start; it self-corrected, unstaged, switched to sub-01, and committed there. The misstep left untracked files in the shared workdir that sub-02 and sub-03 then encountered.
- **No subagent opened a PR** (per the brief: research fanout adapts the skill to skip per-sub-branch PRs; the dispatcher decides whether to PR the rolled-up branch at the end).

## Final state

- Feature branch: `claude/research-merge-branches-wN3BO` advanced from `5cc3dba` (state init) to four new commits adding the three reports + this run report + the INDEX/PLAN updates.
- Reports added: `research/02-oauth-refresh-forks.md` (279), `research/03-ae-book-exec-layer.md` (453), `research/04-openhands-sdk-git-provider.md` (515). Total ~1247 new lines of research.
- INDEX.md and PLAN.md updated to reflect the three new reports (entries + new "Future research" clusters spawned).
- Sub-branches retained on origin (`...--sub-01`, `...--sub-02`, `...--sub-03`) — sandbox-proxy blocks branch deletion; UI-side cleanup when convenient.

## Lessons learned for the next fanout

1. **Use `isolation: "worktree"` when dispatching parallel research subagents.** This run's contamination was avoidable. The `parallel-subagent-fanout` skill's brief template should call this out as a default for any fanout where subagents do branch-switching.
2. **For research fanouts where each sub produces a single deliverable file, plan cherry-picks ahead of merges.** Pre-assign report numbers per-subagent (here: 02/03/04) so file paths never collide; merge by `git checkout sub -- <path>` rather than 3-way.
3. **When using the fetch workflow, copy the body format from the most recent successful fetch issue.** Issue #12's body format was off, requiring a retry; issue #13 succeeded by mirroring issue #5's exact JSON-code-block layout.
4. **The `mcp__github__*` tools' repo-scope restriction is real.** Subagents researching external repos (grll/*, OpenHands/*, etc.) cannot use `mcp__github__get_file_contents`; they must reach for `raw.githubusercontent.com` + WebFetch, or the fetch workflow.
