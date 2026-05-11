# Research Plan

Last updated: 2026-05-11 (post Round 3)

## In-flight

*(none — Round 3 wrapped synchronously; all subagents merged before the dispatcher signed off)*

When in-flight items appear here, the per-item shape (identifier, opened, completion signal, action when complete, fallback, expected wall time, affects) is documented in `.claude/skills/in-flight-workflow-tracking/SKILL.md`. If any item lands here that has a "next session" handoff, promote the drain step to a `## MANDATORY FIRST ACTION` block above this section per that skill.

## Recently completed

- **2026-05-11 — Round 3** (parallel fanout, 3 subagents, all `isolation: "worktree"`): three reports landed —
  - `05-openhands-github-mixins-jira.md` (sub-01) — body-read of OpenHands `repos.py` / `resolver.py` / `provider.py:495-651` / `jira_manager.py`. Headline borrow: `get_authenticated_git_url` verbatim.
  - `06-ae-book-remaining-chapters.md` (sub-02) — AE book chapter-7 Patterns + chapter-8 1/2/6; fetched via issue #17 (issue #15 was a wrong-slug attempt that 404'd; issue #16 was an interim retry that didn't re-fire). Headline: Ralph Wiggum's commits-as-state pattern is the structural twin of agent-runner's resume loop.
  - `07-oauth-refresh-status-watch.md` (sub-03) — operational watch. Anthropic native OAuth-refresh has NOT shipped; keep `scripts/refresh_oauth.py`; next watch ~2026-06-08.

  Run state: `harness/runs/20260511-r3/`. Fetch issues **#15** (failed slugs), **#16** (retry that didn't fire), **#17** (succeeded) and sub-branches `claude/parallelize-with-subagents-p4Opo--sub-{01,02,03}` and `fetched/issue-{15,17}` remain on origin (sandbox proxy blocks deletion); UI cleanup when convenient.

- **2026-05-11 — Round 2** (parallel fanout, 3 subagents): three reports landed —
  - `02-oauth-refresh-forks.md` (sub-01) — community OAuth-refresh prior art for `refresh-oauth.yml`.
  - `03-ae-book-exec-layer.md` (sub-02) — AE book exec-layer chapters; fetched via issue #13.
  - `04-openhands-sdk-git-provider.md` (sub-03) — relocated OpenHands `GitService` Protocol (`OpenHands/OpenHands` org rename + path move to `openhands/app_server/integrations/`).

  Run state: `harness/runs/20260511-r2/`. Fetch issues #12 (workflow exec failure — body extraction lost the JSON) and #13 (succeeded) opened by sub-02; both should be closed from the GitHub UI. Branches `fetched/issue-12`, `fetched/issue-13`, `claude/research-merge-branches-wN3BO--sub-{01,02,03}` remain on origin (sandbox proxy blocks deletion); UI cleanup when convenient.

- **2026-05-11 — Round 1** prior-art research — report `01-prior-art-jayminwest-overstory-openhands.md`. Fetched via issues #5 and #6 (now closed); branches `fetched/issue-5` and `fetched/issue-6` remain on origin (branch deletion blocked by sandbox proxy; can be deleted from the GitHub UI when convenient).

## Future research

Clusters worth investigating in a later round. Per the research-pipeline skill, each cluster names the sources, justifies why investigating it would extend the knowledge base, and estimates effort.

### Scope guardrail

`agent-runner`'s scope is the **execution layer** — running agents reliably in CI under a Claude Max subscription. Research on multi-agent orchestration, software-factory architecture, the Shapiro five-level framework, scenarios-as-holdout-sets, and Digital Twin patterns is being conducted in a separate repo and is **explicitly out of scope here**. Clusters below are limited to execution-layer concerns: harness mechanics, rate limits, cost/latency, OAuth, provider abstraction for issue/PR ops.

### Future research: GraphQL queries used by OpenHands resolver.py

**Sources:**
- `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/github/service/graphql_queries.py` (or wherever the three string constants `get_thread_from_comment_graphql_query`, `get_review_threads_graphql_query`, `get_thread_comments_graphql_query` live — Round 3 report 05 §3 noted they are imported from a sibling module not directly fetched)

**Justification:** Report 05's §3 documents the *algorithm* of `get_review_thread_comments` end-to-end but does not include the verbatim GraphQL query strings. If `agent-runner` ports the review-thread-from-any-comment-id lookup (needed for nested-PR-review-thread `@agent-runner` triggers — DESIGN.md §9 trigger-comment path), the queries themselves are load-bearing and must be quoted verbatim, not paraphrased. ~5-min recovery; only worth doing when the port is actually scheduled.

**Effort:** 1 source file via raw.githubusercontent.com. ~5 min wall time. Trivial — could be folded into the start of Stage-4 work rather than its own subagent dispatch.

### Future research: Anthropic native OAuth-refresh shipping status (recurring)

**Sources:**
- `https://github.com/anthropics/claude-code-action/issues/727` (use WebFetch — GitHub MCP scope is `lago-morph/agent-runner` only)
- `https://raw.githubusercontent.com/anthropics/claude-code-action/main/action.yml`
- `https://github.com/anthropics/claude-code-action/releases` (last 10)

**Justification:** Report 07 (Round 3) ran the first formal check; trigger has not fired. Report 02 §11 says the trigger to retire `scripts/refresh_oauth.py` is a `claude_code_refresh_token` (or analogous) input appearing in `action.yml`. Recurring 4-week cadence keeps drift small; next check **~2026-06-08**.

**Effort:** ~5-10 min per check. A `loop` skill task or manual reminder.

### Future research: AE book chapters 4 (Context) + 5 (Tools) + 9-10 unread subchapters

**Sources:**
- `https://www.jayminwest.com/agentic-engineering-book/4-context/...` (TOC TBD via fetch)
- `https://www.jayminwest.com/agentic-engineering-book/5-tools/...` (TOC TBD)
- Remaining 9/x and 10/x subchapters not yet covered by reports 01, 03, or 06 (Round 1 covered 9/7 + 10/5; the rest is unread).

**Justification:** Round 3 (sub-02) discovered the book's actual chapter taxonomy is **1: Foundations · 2: Models · 3: Prompting · 4: Context · 5: Tools · 6: Harnesses · 7: Patterns · 8: Practices · 9: ? · 10: ?**. Reports 03 + 06 cover most of chapters 6, 7, 8 (the operational core). Chapter 4 ("Context") and Chapter 5 ("Tools") were not covered and are likely directly relevant to (a) DESIGN.md context-management decisions for the resume loop and (b) MCP / tool-restriction design for the harness. Chapters 9-10 may or may not be on-scope; the fetched TOC will tell us.

**Effort:** ~10-15 source files via fetch workflow (jayminwest.com blocked). One labeled issue, ~5 min wall time. ~2 hours total. Single subagent dispatch. **Probe TOC first** (lesson learned from Round 3 — see process notes below).

### Future research: OpenHands GraphQL pagination beyond GitHub mixin

**Sources:**
- `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/gitlab/service/repos.py`
- `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/bitbucket/service/repos.py`
- `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/azure_devops/service/repos.py`

**Justification:** Report 05 §2 documents GitHub's `Link: rel="next"` pagination loop. Each provider has a different pagination convention (GitLab uses `X-Next-Page` / `X-Total-Pages`; Bitbucket uses `next` URL in JSON body; Azure DevOps uses `continuationToken` in response headers). A small comparative read would let DESIGN.md's `ProviderClient` Protocol declare a `_paginate(url, max) -> list[dict]` method whose default implementation handles GitHub-style and which each provider mixin overrides as needed. Currently the borrow is GitHub-only.

**Effort:** ~3 source files via raw.githubusercontent.com. ~30 min wall time. Single subagent dispatch. Schedule when Stage 4 actually needs a second provider.

## Process notes

- Future-research clusters are ordered by relevance to the active roadmap, not by source affinity.
- Reports' fetched raw content (when not deleted via Phase 9 cleanup) lives on `fetched/issue-N` branches on origin (not merged into `main`). Reports cite source URLs, not local snapshots, so the branches can be deleted whenever a maintainer with UI access wants to clean them up.
- Round 2 used the `parallel-subagent-fanout` skill. Lesson learned: **dispatch parallel subagents with `isolation: "worktree"`** — without it, concurrent subagents stomp on each other's branches in the shared sandbox workdir. Round 2 recovered by cherry-picking just the report files into the feature branch in plan order; future fanout dispatchers should add this to their default brief.
- **Round 3 lesson — verify URL pattern before dispatching the fetch issue.** sub-02 burned ~3 minutes on a bad-slug fetch (issue #15) that returned all React-app 404s because the dispatcher's PLAN.md cluster description encoded the wrong chapter title ("architecture / context engineering" vs. the real "Patterns"). Before opening any `[fetch-urls]` issue, probe at least one URL of the intended pattern via WebFetch first.
- **Round 3 lesson — cluster names should encode actual TOC headings verbatim, not paraphrases.** Cite the source's own table-of-contents wording when describing future-research clusters.
- **Round 3 lesson — GitHub MCP scope is repo-locked.** The `mcp__github__*` tools are restricted to `lago-morph/agent-runner` in this session. Cross-repo work (e.g., reading `anthropics/claude-code-action` issues) must go through WebFetch. Worth a one-line CLAUDE.md / AGENTS.md note if not already there.
