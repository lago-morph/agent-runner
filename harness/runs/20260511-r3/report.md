# Fanout run report — 20260511-r3

Run on 2026-05-11 (overnight, unattended). Goal: investigate the three future-research clusters from `research/PLAN.md`.

## Summary

| Subtask | Branch | Status | Tests delta | PR |
|---------|--------|--------|-------------|-----|
| sub-01 | `claude/parallelize-with-subagents-p4Opo--sub-01` | merged | none | n/a (lead-merged) |
| sub-02 | `claude/parallelize-with-subagents-p4Opo--sub-02` | merged | none | n/a (lead-merged) |
| sub-03 | `claude/parallelize-with-subagents-p4Opo--sub-03` | merged | none | n/a (lead-merged) |

Three reports landed:

- `research/05-openhands-github-mixins-jira.md` — sub-01: deep dive into OpenHands `repos.py` pagination, `resolver.py` GraphQL traversal, `provider.py` `get_authenticated_git_url`, and `jira_manager.py` orchestration. Two corrections to report 04's predictions: (a) Jira auth is Keycloak SSO + service-account basic auth, *not* in-band OAuth; (b) `JiraView` is an `ABC` with class-attribute hints, not a Pydantic model.
- `research/06-ae-book-remaining-chapters.md` — sub-02: AE book chapter 7 (Patterns) + chapter 8 subchapters 1/2/6. PLAN.md's cluster description had the wrong mental model — chapter 7 is "Patterns" not "architecture / context engineering". The subagent recovered by enumerating real chapter slugs after the first fetch returned only React-app 404s. Headline: Ralph Wiggum's `while :; do …` "state persists in commits" pattern is the structural twin of agent-runner's rate-limit-resume loop.
- `research/07-oauth-refresh-status-watch.md` — sub-03: brief operational watch. Trigger has NOT fired — `anthropics/claude-code-action/main/action.yml` still has only `claude_code_oauth_token`, issue #727 remains open with zero maintainer responses, no recent release mentions OAuth/refresh. Recommendation: keep `scripts/refresh_oauth.py`; re-check on a 4-week cadence.

## Merge log

- sub-01 (`claude/parallelize-with-subagents-p4Opo--sub-01`): merged with `--no-ff`, no conflicts. 1 file (+644 lines).
- sub-02 (`claude/parallelize-with-subagents-p4Opo--sub-02`): merged with `--no-ff`, no conflicts. 2 files (+485 lines, including a small `.fetch-work/urls.txt` update from the fetch-workflow runs). Brings in 4 prior commits including 2 fetch-workflow merges (issues #15 and #17).
- sub-03 (`claude/parallelize-with-subagents-p4Opo--sub-03`): merged with `--no-ff`, no conflicts. 1 file (+108 lines).

All three sub-branches were dispatched in parallel in a single message with `isolation: "worktree"` (per the Round-2 lesson learned + the patch a9f3a685 to `parallel-subagent-fanout/SKILL.md`). No cross-workdir contamination occurred this run; the worktrees behaved correctly. The dispatcher noticed and `.gitignore`-d the `.claude/worktrees/` directory that the worktree-isolation feature creates in the dispatcher's checkout (commit 8edcfaa).

## Deviations

- **sub-02 fetch issue #15 used invented URL slugs.** The PLAN.md cluster name ("chapter 7 architecture / context engineering") gave a false guide. The subagent issued issue #15 against `/7-architecture/...` paths that all 404'd to the React app's "Chapter Not Found" page. It then discovered the real chapter-7 slug is `/7-patterns` and opened issue #17 with corrected URLs, which succeeded. Issue #16 was an interim retry whose workflow apparently never re-fired (label re-application via `mcp__github__issue_write update` did not trigger the `issues: labeled` event). The cleaner workflow for next time: open a single issue per fetch, not retries.
- **sub-02 scope explicitly excluded multi-agent material** (orchestrator pattern, expert swarm, multi-agent collaboration, multi-agent landscape, production multi-agent systems, workflow coordination, operating agent swarms) per PLAN.md's scope guardrail. Listed in the §1 catalog but not body-read.
- **sub-03 used WebFetch instead of `mcp__github__*` for `anthropics/claude-code-action`.** The repo-scope policy on the GitHub MCP tools restricts them to `lago-morph/agent-runner`, so #727 + the releases page were fetched via WebFetch — equivalent data, different transport. Worth noting in the future-research watch entry so the next round doesn't waste a tool call.

## Final state

- Feature branch: `claude/parallelize-with-subagents-p4Opo` at `23a6de9` (pre-report-update); update commit will follow.
- Total reports in `research/`: 7 (was 4).
- Sub-branches deleted from origin: **none** — sandbox proxy returns HTTP 403 on `git push --delete` (same limitation as Round 2). UI cleanup needed for `claude/parallelize-with-subagents-p4Opo--sub-{01,02,03}` and `fetched/issue-{15,17}` (issue-16 was never created by the workflow because the second fetch never fired).
- Sub-branches skipped: none.
- Fetch issues left open for UI cleanup: **#15** (failed-slugs evidence), **#16** (interim retry that didn't fire), **#17** (succeeded). All three should be closed from the UI when convenient.

## In-flight items handed to PLAN.md

Per the `in-flight-workflow-tracking` skill, after this run wraps:

- `anthropics/claude-code-action#727` watch — recurring 4-week re-check (per report 07's recommendation). Promoted to PLAN.md as a future-research item with refreshed dates and a smaller scope.

## Lessons for the next round

1. **Verify the URL pattern before dispatching the fetch issue.** sub-02 burned ~3 minutes on a bad-slug fetch that could have been avoided by a single WebFetch probe of the book TOC page first. Add this to the parallel-subagent brief template for any subagent that opens a fetch issue: "If you don't already know the exact URL pattern, probe one URL by hand before opening the fetch issue."
2. **Cluster names in PLAN.md should encode actual section titles, not paraphrases.** "AE book remaining operational chapters — chapter 7 architecture / context engineering" was the dispatcher's mental model from Round 2 and was wrong. Rule: cite the source's own table-of-contents heading verbatim.
3. **Sub-03 model-tool-scope mismatch is worth a one-line CLAUDE.md note.** The GitHub MCP server is locked to `lago-morph/agent-runner`; cross-repo reads must go through WebFetch. (May already be in CLAUDE.md; check.)
