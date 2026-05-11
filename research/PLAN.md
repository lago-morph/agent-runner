# Research Plan

Last updated: 2026-05-11 (post Round 5)

## In-flight

*(none — Round 4 wrapped synchronously; all subagents merged before the dispatcher signed off)*

When in-flight items appear here, the per-item shape (identifier, opened, completion signal, action when complete, fallback, expected wall time, affects) is documented in `.claude/skills/in-flight-workflow-tracking/SKILL.md`. If any item lands here that has a "next session" handoff, promote the drain step to a `## MANDATORY FIRST ACTION` block above this section per that skill.

## Recently completed

- **2026-05-11 — Round 5** (single-subagent dispatch, `isolation: "worktree"`): one report landed —
  - `11-ae-book-foundations-models-prompting.md` (r5-sub-01) — AE book chapters 1 (Foundations), 2 (Prompt — singular slug `2-prompt`), 3 (Model — singular slug `3-model`). Three fetches: probe with brief's wrong slugs (#21, silent-404), corrected probe (#22), body fetch (#23). ~70% recap of reports 03/06/08 + three net-new contributions (Rabanser arXiv:2602.16666, Twelve Leverage Points + Anti-Patterns catalog, compound-error `p^n` math) + 11 itemized DESIGN.md edit suggestions.

  Run state: `harness/runs/20260511-r5/`. Fetch issues **#21** + **#22** + **#23** and sub-branch `claude/parallelize-with-subagents-p4Opo--r5-sub-01` and branches `fetched/issue-{21,22,23}` remain on origin (sandbox proxy blocks deletion); UI cleanup when convenient. Issue #21's silent-404 evidence is intentionally kept open as the verbatim record of the slug-paraphrase failure mode.

- **2026-05-11 — Round 4** (parallel fanout, 3 subagents, all `isolation: "worktree"`): three reports landed —
  - `08-ae-book-context-tools.md` (r4-sub-01) — AE book ch 4 Context + ch 5 Tool Use + ch 9 Mental Models + ch 10 Practitioner Toolkit. Two fetches: index probe (#19) then body fetch (#20). Headline: Raschka's "context quality in disguise" inverts debugging order, motivates Layer-0 outer-harness audit before report 06's Core-Four diagnostic tree.
  - `09-openhands-graphql-queries.md` (r4-sub-02) — completed report 05's deferred 🟡 row by quoting the three resolver GraphQL strings verbatim from `openhands/app_server/integrations/github/queries.py` (corrected report 05's `graphql_queries.py` hypothesis).
  - `10-openhands-provider-pagination.md` (r4-sub-03) — comparative pagination shapes across 5 providers; recommended `_paginate` Protocol = GitHub-style default + overrides for Bitbucket Cloud and Azure DevOps.

  Run state: `harness/runs/20260511-r4/`. Fetch issues **#19** (index probes) and **#20** (subchapter bodies) and sub-branches `claude/parallelize-with-subagents-p4Opo--r4-sub-{01,02,03}` and `fetched/issue-{19,20}` remain on origin (sandbox proxy blocks deletion); UI cleanup when convenient.

- **2026-05-11 — Round 3** (parallel fanout, 3 subagents, all `isolation: "worktree"`): three reports landed —
  - `05-openhands-github-mixins-jira.md` (sub-01) — body-read of OpenHands `repos.py` / `resolver.py` / `provider.py:495-651` / `jira_manager.py`. Headline borrow: `get_authenticated_git_url` verbatim.
  - `06-ae-book-remaining-chapters.md` (sub-02) — AE book chapter-7 Patterns + chapter-8 1/2/6; fetched via issue #17 (issue #15 was a wrong-slug attempt that 404'd; issue #16 was an interim retry that didn't re-fire). Headline: Ralph Wiggum's commits-as-state pattern is the structural twin of agent-runner's resume loop.
  - `07-oauth-refresh-status-watch.md` (sub-03) — operational watch. Anthropic native OAuth-refresh has NOT shipped; keep `scripts/refresh_oauth.py`; next watch ~2026-06-08.

  Run state: `harness/runs/20260511-r3/`. Fetch issues **#15** (failed slugs), **#16** (retry that didn't fire), **#17** (succeeded) and sub-branches `claude/parallelize-with-subagents-p4Opo--sub-{01,02,03}` and `fetched/issue-{15,17}` remain on origin (sandbox proxy blocks deletion); UI cleanup when convenient.

- **2026-05-11 — Round 2** (parallel fanout, 3 subagents): three reports landed —
  - `02-oauth-refresh-forks.md` (sub-01) — community OAuth-refresh prior art for `refresh-oauth.yml`.
  - `03-ae-book-exec-layer.md` (sub-02) — AE book exec-layer chapters; fetched via issue #13.
  - `04-openhands-sdk-git-provider.md` (sub-03) — relocated OpenHands `GitService` Protocol (`OpenHands/OpenHands` org rename + path move to `openhands/app_server/integrations/`).

  Run state: `harness/runs/20260511-r2/`. Fetch issues #12 + #13; branches `fetched/issue-12`, `fetched/issue-13`, `claude/research-merge-branches-wN3BO--sub-{01,02,03}` remain on origin (UI cleanup when convenient).

- **2026-05-11 — Round 1** prior-art research — report `01-prior-art-jayminwest-overstory-openhands.md`. Fetched via issues #5 and #6 (now closed); branches `fetched/issue-5` and `fetched/issue-6` remain on origin.

## Future research

Clusters worth investigating in a later round. Per the research-pipeline skill, each cluster names the sources, justifies why investigating it would extend the knowledge base, and estimates effort.

### Scope guardrail

`agent-runner`'s scope is the **execution layer** — running agents reliably in CI under a Claude Max subscription. Research on multi-agent orchestration, software-factory architecture, the Shapiro five-level framework, scenarios-as-holdout-sets, and Digital Twin patterns is being conducted in a separate repo and is **explicitly out of scope here**. Clusters below are limited to execution-layer concerns: harness mechanics, rate limits, cost/latency, OAuth, provider abstraction for issue/PR ops.

### Future research: Anthropic native OAuth-refresh shipping status (recurring)

**Sources:**
- `https://github.com/anthropics/claude-code-action/issues/727` (use WebFetch — GitHub MCP scope is `lago-morph/agent-runner` only)
- `https://raw.githubusercontent.com/anthropics/claude-code-action/main/action.yml`
- `https://github.com/anthropics/claude-code-action/releases` (last 10)

**Justification:** Report 07 (Round 3) ran the first formal check; trigger has not fired. Report 02 §11 says the trigger to retire `scripts/refresh_oauth.py` is a `claude_code_refresh_token` (or analogous) input appearing in `action.yml`. Recurring 4-week cadence keeps drift small; **next check ~2026-06-08**.

**Effort:** ~5-10 min per check. A `loop` skill task or manual reminder.

### Future research: OpenHands `comments` resource handlers (review-thread reply posting)

**Sources:**
- `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/github/service/comments.py` (or wherever the GitHub comment-creation code lives)
- Same path under `gitlab/` and `bitbucket/` for cross-provider comparison.

**Justification:** Report 05 §3 documented `get_review_thread_comments` (the *read* side). When `agent-runner` Stage 5 lands and needs to *reply* to a triggering comment in the same review thread, the GitHub REST endpoint shape and the OpenHands wrapper are the canonical reference. Not yet on the critical path; schedule when Stage 5 is on deck.

**Effort:** ~3 source files via raw.githubusercontent.com. ~30 min wall time. Single subagent dispatch.

### Future research: Bitbucket Data Center single-file stub deep-read

**Sources:**
- `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/bitbucket_data_center/bitbucket_dc_service.py`

**Justification:** Report 10 (Round 4) noted the Bitbucket DC service is a single-file stub with no pagination logic. Worth a 15-minute body-read to confirm what it *does* implement (auth flow? branch list? commit fetch?) so report 05's §6 "Borrow / Skip" recommendation generalizes correctly. Lowest priority of the open clusters; only do if Stage 4 is actually adding Bitbucket DC support.

**Effort:** 1 source file. ~15 min. Could be folded into Stage-4 prep work rather than its own subagent dispatch.

## Process notes

- Future-research clusters are ordered by relevance to the active roadmap, not by source affinity.
- Reports' fetched raw content (when not deleted via Phase 9 cleanup) lives on `fetched/issue-N` branches on origin (not merged into `main`). Reports cite source URLs, not local snapshots, so the branches can be deleted whenever a maintainer with UI access wants to clean them up.
- **Round 2 lesson — `isolation: "worktree"` is required for parallel fanout.** Encoded into `parallel-subagent-fanout/SKILL.md` (commit a9fa9e8). Rounds 3 and 4 both used worktree isolation and confirmed: zero cross-workdir contamination, zero merge cleanup post-fanout.
- **Round 3 + Round 4 lesson — the dispatcher's paraphrase of an external TOC is unreliable evidence.** Round 3 had it (chapter 7 was "Patterns" not "architecture"); Round 4 had it again (chapter 5 was `5-tool-use` not `5-tools`). Rule: every PLAN.md cluster that names external chapters/sections must cite the verbatim TOC slug from a previously-fetched index page, with a URL. Add the verbatim slugs above when this PLAN.md is next revised.
- **Round 3 lesson — verify URL pattern before dispatching the fetch issue.** Round 4 r4-sub-01 generalized this into a two-fetch pattern (probe-then-body) when the slugs are unknown. ~3 extra minutes wall time, prevents whole-fetch waste.
- **Round 4 lesson — `.fetch-work/urls.txt` merge conflicts are normal on multi-fetch sub-branches.** Resolution is always "keep both lists" (union merge). A future enhancement to `.github/workflows/fetch-blocked-urls.yml` could append rather than overwrite when the file already exists on the target branch.
- **Round 3 lesson — GitHub MCP scope is repo-locked.** The `mcp__github__*` tools are restricted to `lago-morph/agent-runner` in this session. Cross-repo work (e.g., reading `anthropics/claude-code-action` issues, searching `OpenHands/OpenHands` code) must go through WebFetch. Worth a one-line CLAUDE.md / AGENTS.md note if not already there.
- **Round 4 lesson — small subtasks are still worth dispatching as subagents.** r4-sub-02 finished in ~2 min on a single small file fetch + 100-line report. The dispatcher gained parallel context window for the larger r4-sub-01 + r4-sub-03 jobs. Don't gate fanout on subtask size.
- **Round 5 lesson — slug-paraphrase failure is a confirmed three-time pattern.** Three rounds in a row (3, 4, 5), the dispatcher's paraphrase of an external chapter title produced wrong URL slugs that needed correction at probe step. Round 5's case was especially bad — the brief swapped chapters 2 and 3 entirely. The Round 3 + Round 4 rule still stands: cite verbatim slugs from a previously-fetched index page. **For the AE book specifically**, the verified verbatim chapter slugs (post-Round-5) are: `1-foundations`, `2-prompt`, `3-model`, `4-context`, `5-tool-use`, `6-harnesses`, `7-patterns`, `8-practices`, `9-mental-models`, `10-practitioner-toolkit`. Use these directly in any future AE-book PLAN.md cluster.
- **Round 5 lesson — SPA silent-404s return 200-OK with the navigation skeleton only.** A `jayminwest.com` page that returns ~6 KB of HTML with body content of just the nav-tree is a silent 404 in disguise. The fetch workflow can't tell from the HTTP status. Detection: post-fetch inspection — if the html2text `.md` body is < 8 KB AND contains only the chapter-list navigation skeleton with no chapter title H1, the slug is wrong. A future enhancement to `.github/scripts/fetch_urls.sh` could surface this in the per-URL summary by checking byte counts + grep'ing for nav-only patterns. Until then, drain-step manual inspection is required.
