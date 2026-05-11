# Fanout run report — 20260511-r4

Run on 2026-05-11 (overnight, unattended; second of two rounds in the session). Goal: investigate the three actionable future-research clusters surfaced by Round 3 in `research/PLAN.md`. Skipped the OAuth-refresh recurring watch (next due ~2026-06-08).

## Summary

| Subtask | Branch | Status | Tests delta | PR |
|---------|--------|--------|-------------|-----|
| r4-sub-01 | `claude/parallelize-with-subagents-p4Opo--r4-sub-01` | merged | none | n/a (lead-merged) |
| r4-sub-02 | `claude/parallelize-with-subagents-p4Opo--r4-sub-02` | merged | none | n/a (lead-merged) |
| r4-sub-03 | `claude/parallelize-with-subagents-p4Opo--r4-sub-03` | merged | none | n/a (lead-merged) |

Three reports landed:

- `research/08-ae-book-context-tools.md` — r4-sub-01: AE book chapters 4 (Context), 5 (Tool Use), and the unread chapter 9 (Mental Models) + chapter 10 (Practitioner Toolkit) subchapters. Two fetches: index probe (issue #19), then 20-URL body fetch (issue #20). Headline: Raschka's *"apparent model quality is frequently context quality in disguise"* motivates a Layer-0 outer-harness audit step ahead of report 06's Core-Four diagnostic tree.
- `research/09-openhands-graphql-queries.md` — r4-sub-02: completed the deferred 🟡 row in report 05 by quoting the three resolver GraphQL strings verbatim. Corrected report 05's filename hypothesis (`queries.py`, not `graphql_queries.py`).
- `research/10-openhands-provider-pagination.md` — r4-sub-03: comparative pagination shape across GitHub / GitLab / Bitbucket Cloud / Azure DevOps / Forgejo. Recommended `_paginate` Protocol with GitHub-style default + per-provider overrides for Bitbucket Cloud and Azure DevOps.

## Merge log

- r4-sub-01 (`claude/parallelize-with-subagents-p4Opo--r4-sub-01`): merged with `--no-ff`, no conflicts at integration time. 2 files (+507 lines, including a `.fetch-work/urls.txt` union from two fetch merges that the subagent resolved internally).
- r4-sub-02 (`claude/parallelize-with-subagents-p4Opo--r4-sub-02`): merged with `--no-ff`, no conflicts. 1 file (+135 lines).
- r4-sub-03 (`claude/parallelize-with-subagents-p4Opo--r4-sub-03`): merged with `--no-ff`, no conflicts. 1 file (+376 lines).

All three sub-branches were dispatched in parallel in a single message with `isolation: "worktree"`. r4-sub-02 finished synchronously inside the dispatcher message (~2 min); r4-sub-01 and r4-sub-03 returned via background completion notifications (~17 min and ~6 min respectively).

## Deviations

- **r4-sub-01 cluster description was inaccurate (again).** PLAN.md said "chapter 5: Tools" but the actual slug is `5-tool-use` and the chapter title is "Tool Use." The probe-first lesson from Round 3 saved a body fetch — issue #19 caught the bad slug at index step. The Round-3 lesson generalizes: the dispatcher should never trust its own paraphrase of an external source's TOC headings; only verbatim slugs cited in a previously-fetched index page are safe.
- **r4-sub-02 corrected report 05's filename hypothesis.** The file is `queries.py`, not the speculated `graphql_queries.py`. Report 09 explicitly cross-references this so DESIGN.md / Stage-4 work doesn't waste time looking for the wrong filename.
- **r4-sub-03 found a 404 on `bitbucket_dc/service/repos.py`.** The actual upstream directory is `bitbucket_data_center/` (no `service/` subdirectory, no `get_paginated_repos` implementation). The Forgejo file was added as a supplementary read, bringing the comparison to 5 providers (GitHub baseline + 4 from this round).
- **r4-sub-01's two fetch issues (#19 and #20) both produced `.fetch-work/urls.txt` merge conflicts** when the subagent merged each fetched branch into its sub-branch. The subagent resolved by union-merge (kept all historical fetches in the manifest per skill convention). Worth surfacing as a process note for future fetch-heavy rounds.

## Final state

- Feature branch: `claude/parallelize-with-subagents-p4Opo` at the merge of r4-sub-03; this report's commit will follow.
- Total reports in `research/`: 10 (was 7 after Round 3, was 4 after Round 2).
- Sub-branches deleted from origin: **none** — sandbox proxy returns HTTP 403 on `git push --delete` (same limitation as Rounds 2 + 3). UI cleanup needed for `claude/parallelize-with-subagents-p4Opo--r4-sub-{01,02,03}` and `fetched/issue-{19,20}`.
- Sub-branches skipped: none.
- Fetch issues left open for UI cleanup: **#19** (chapter index probes), **#20** (subchapter body fetch). Both should be closed from the UI when convenient.

## In-flight items handed to PLAN.md

Per the `in-flight-workflow-tracking` skill, after this run wraps:

- `anthropics/claude-code-action#727` watch — recurring 4-week re-check (per Round-3 report 07's recommendation; next due ~2026-06-08). Already in PLAN.md.

## Lessons for the next round

1. **The dispatcher's paraphrase of an external TOC is unreliable evidence.** Round 3 had it (chapter 7 was "Patterns" not "architecture"); Round 4 had it again (chapter 5 was `5-tool-use` not `5-tools`). Rule: every PLAN.md cluster that names external chapters/sections must cite the verbatim TOC slug from a previously-fetched index page, with a URL.
2. **Fetch-issue manifests union-merge cleanly.** `.fetch-work/urls.txt` conflicts on multi-fetch branches are expected and the resolution is always "keep both lists." A future enhancement to the fetch-blocked-urls workflow could append rather than overwrite when the file already exists on the target branch.
3. **r4-sub-02 finished in ~2 minutes on a single small file fetch + 100-line report.** Trivially-bounded subtasks dispatched as full subagents are still net-positive over inline work because they free dispatcher context for parallel work.
