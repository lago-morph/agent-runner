# Research Plan

Last updated: 2026-05-11 (post Round 2)

## In-flight

*(none)*

When in-flight items appear here, the per-item shape (identifier, opened, completion signal, action when complete, fallback, expected wall time, affects) is documented in `.claude/skills/in-flight-workflow-tracking/SKILL.md`. If any item lands here that has a "next session" handoff, promote the drain step to a `## MANDATORY FIRST ACTION` block above this section per that skill.

## Recently completed

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

### Future research: OpenHands GitHub mixin patterns + Jira manager

**Sources:**
- `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/github/service/repos.py` (~11.6 KB — pagination + GraphQL shape)
- `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/github/service/resolver.py` (GitHub-Resolver auto-link issue→PR logic)
- `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/provider.py` lines 495-651 (`get_authenticated_git_url`, Azure DevOps + Bitbucket DC URL-construction subtleties)
- `https://raw.githubusercontent.com/OpenHands/OpenHands/main/enterprise/integrations/jira/jira_manager.py` (14 KB — JiraView shape, OAuth handshake, `start_job` semantic)

**Justification:** Round 2's report 04 located the abstraction and read the top-level Protocol + orchestrator end-to-end, but did NOT body-read the GitHub mixin implementations or the Jira manager. Body-reading these would matter (a) when `agent-runner` extracts its own `providers/github/` package and wants borrowed-not-reinvented pagination + GraphQL patterns, and (b) when Stage 5 adds Jira backing for `IssueTracker`. The Run/Issue association logic in `resolver.py` is also possibly inspirational for `agent-runner`'s own Run-PR-Issue association (DESIGN.md §4). Park until Stage 4 (provider extraction) or Stage 5 (Jira) is on deck.

**Effort:** ~4 source files, all reachable via raw.githubusercontent.com (no fetch workflow needed). ~45 min reading + ~15 min report. Single subagent dispatch.

### Future research: AE book remaining operational chapters

**Sources:** the AE book's remaining unread chapter-7 + chapter-8 subchapters (chapter 6/1, 6/3, 6/7, 7/3, 7/4, 7/11, 8/1, 8/2, 8/5+ — exact list TBD from the book TOC fetched in Round 1).

**Justification:** Round 2 read the four chapter-6 subchapters most directly relevant (stack, control system, engineering, security) plus chapter 8/3 + 8/4. Chapter 7 (architecture / context engineering) and the remaining 8/x subchapters were not read. Lower priority than the explicit roadmap clusters, but worth a sweep before any major DESIGN.md revision.

**Effort:** ~6-10 source files via fetch workflow (jayminwest.com blocked). One labeled issue, ~3 min wall time. ~1.5 hours total. Single subagent dispatch.

### Future research: Anthropic native OAuth-refresh shipping status

**Sources:**
- `https://github.com/anthropics/claude-code-action/issues/727` (poll periodically)
- `https://raw.githubusercontent.com/anthropics/claude-code-action/main/action.yml` (look for new `claude_code_refresh_token` input)
- Anthropic changelog / Claude Code release notes (URL TBD when first checked)

**Justification:** Report 02 §11 calls out that when Anthropic ships native refresh in `claude-code-action`, we should retire our custom `refresh_oauth.py` and JIT logic. This is an *operational watch*, not a research task — but the trigger to audit is the moment `action.yml` gains a `claude_code_refresh_token` input. Worth a 5-min check every ~30 days.

**Effort:** Trivial. ~5 min per check. Could be a `loop` skill task or a manual reminder.

## Process notes

- Future-research clusters are ordered by relevance to the active roadmap, not by source affinity.
- Reports' fetched raw content (when not deleted via Phase 9 cleanup) lives on `fetched/issue-N` branches on origin (not merged into `main`). Reports cite source URLs, not local snapshots, so the branches can be deleted whenever a maintainer with UI access wants to clean them up.
- Round 2 used the `parallel-subagent-fanout` skill. Lesson learned: **dispatch parallel subagents with `isolation: "worktree"`** — without it, concurrent subagents stomp on each other's branches in the shared sandbox workdir. Round 2 recovered by cherry-picking just the report files into the feature branch in plan order; future fanout dispatchers should add this to their default brief.
