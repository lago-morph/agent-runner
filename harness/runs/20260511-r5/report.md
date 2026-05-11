# Fanout run report — 20260511-r5

Run on 2026-05-11 (overnight, unattended; third of three rounds in this session). Goal: wrap-up round for the only remaining unconditionally-actionable PLAN.md cluster — AE book chapters 1, 2, 3. Single-subagent dispatch (not really "fanout" but follows the same merge + report discipline).

## Summary

| Subtask | Branch | Status | Tests delta | PR |
|---------|--------|--------|-------------|-----|
| r5-sub-01 | `claude/parallelize-with-subagents-p4Opo--r5-sub-01` | merged | none | n/a (lead-merged) |

One report landed:

- `research/11-ae-book-foundations-models-prompting.md` — r5-sub-01: AE book chapters 1 (Foundations), 2 (Prompt — singular), 3 (Model — singular). Two surprises: the dispatcher's brief inverted the chapter-2 / chapter-3 titles and slugs (chapter 2 is "Prompt" not "Models"; chapter 3 is "Model" not "Prompting"), and chapter 1 turned out to contain net-new framework material (Twelve Leverage Points + dated Anti-Patterns catalog) rather than being pure recap as the dispatcher predicted. Headline: ~70% recap, 3 net-new contributions, 11 itemized DESIGN.md edit suggestions in the report's §5.

## Merge log

- r5-sub-01 (`claude/parallelize-with-subagents-p4Opo--r5-sub-01`): merged with `--no-ff`, no conflicts. 8 files (+875 lines, including the report + 6 fetched .html/.md files from issue-21 deliberately retained as evidence of the SPA silent-404 failure mode + a `.fetch-work/urls.txt` union update).

The subagent dispatched 3 fetch issues over its run (issue #21 was the first probe with the brief's wrong slugs `2-models`/`3-prompting` and silent-404'd; issue #22 was the corrected probe; issue #23 was the body fetch with 10 URLs all ✅).

## Deviations

- **Brief encoded the wrong chapter-2 / chapter-3 titles.** The PLAN.md cluster description said "Chapter 2 (Models) and Chapter 3 (Prompting)" — both wrong. The actual chapters are 2 = "Prompt" and 3 = "Model". The subagent caught this at the index-probe step (per the Round 3 + Round 4 lesson) and recovered by issuing a corrected probe (issue #22). This is the **third instance in three rounds** of paraphrased external slugs being wrong. The pattern is now well-established and the lesson is escalated to PLAN.md process notes (see below).
- **SPA silent-404 detected.** A 200-OK response from `jayminwest.com` with body of ~6 KB containing only the navigation skeleton is a silent 404. The fetch workflow itself can't tell — only post-fetch inspection of the `.md` body length + content can. Worth a process-note in PLAN.md so future fetch-heavy rounds can detect this in their drain step.
- **Chapter 1 was richer than expected.** PLAN.md predicted "highest-recap, lowest-novelty target." Actual: the chapter index page contains substantial framework content (5-pillar model with dated 2026-04-12 "why Harness was added" rationale + Agent Psychometrics arXiv:2604.00594 citation), and the single Foundations subchapter (`1-foundations/1-twelve-leverage-points`) is the load-bearing source for two of report 11's three net-new contributions. Expectation calibration miss; report 11 explicitly notes the prediction was half wrong.

## Final state

- Feature branch: `claude/parallelize-with-subagents-p4Opo` at the merge of r5-sub-01; this report's commit will follow.
- Total reports in `research/`: 11 (was 10 after Round 4, was 7 after Round 3, was 4 after Round 2).
- Sub-branches deleted from origin: **none** — sandbox proxy returns HTTP 403 on `git push --delete`. UI cleanup needed for `claude/parallelize-with-subagents-p4Opo--r5-sub-01` and `fetched/issue-{21,22,23}`.
- Sub-branches skipped: none.
- Fetch issues left open for UI cleanup: **#21** (silent-404 evidence — keep open as the verbatim record of the slug-paraphrase failure mode), **#22** (corrected probe), **#23** (body fetch).
- Fetched-content retained as evidence: 6 files under `research/fetched/issue-21/` (3 HTML + 3 .md for the silent-404 SPA responses to `1-foundations`, `2-models` (wrong), `3-prompting` (wrong)). These are deliberately NOT cleaned up per Phase-9 rule (failed-fetch evidence).

## Session-level summary (Rounds 3 + 4 + 5)

This overnight session ran three back-to-back fanout rounds:

- **Round 3** (3 subagents) — exhausted the original PLAN.md "Future research" clusters. Produced reports 05, 06, 07.
- **Round 4** (3 subagents) — exhausted the new clusters surfaced by Round 3. Produced reports 08, 09, 10.
- **Round 5** (1 subagent) — wrap-up of the last unconditionally-actionable cluster. Produced report 11.

Total: **7 new reports** (05-11), bringing the research corpus from 4 to 11 reports. Total lines added: ~3,300 across reports + ~500 across run reports + state. Five fetched-issue cycles (#15, #17, #19, #20, #21+22+23). Zero merge conflicts at the integration layer (the `.fetch-work/urls.txt` conflicts on multi-fetch sub-branches were resolved internally by subagents). Zero subagent failures.

The remaining PLAN.md clusters are all contingent — date-contingent (OAuth watch, due 2026-06-08) or stage-contingent (comments handlers / Bitbucket DC stub, both pending Stage 4/5 scheduling). PLAN.md reflects this; the next session can proceed cleanly with no MANDATORY-first-action drain.

## Lessons for the next round

1. **The slug-paraphrase failure is now a third-time pattern.** Round 3 had `7-architecture` vs `7-patterns`; Round 4 had `5-tools` vs `5-tool-use`; Round 5 had `2-models`/`3-prompting` vs `2-prompt`/`3-model`. PLAN.md's process notes already say "every PLAN.md cluster that names external chapters/sections must cite the verbatim TOC slug from a previously-fetched index page" — Round 5 confirms this rule is load-bearing.
2. **SPA silent-404 detection should be a fetch-workflow output.** The `fetch_urls.sh` script in `.github/scripts/` records HTTP code + bytes; a future enhancement could flag responses where bytes < 8 KB AND body contains only the navigation skeleton, marking them as "200-but-empty" in the per-URL summary. Until then, manual post-fetch inspection at drain time is required.
3. **Single-subagent "fanout" is fine when only one cluster remains.** Round 5 used the same state.json + report.md + INDEX/PLAN-update discipline as Rounds 3 and 4 with a single subtask, and the discipline still paid for itself in trace clarity. Don't skip the report just because there's one subtask.
