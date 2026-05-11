# Research Plan

Last updated: 2026-05-11

## In-flight

*(none)*

When in-flight items appear here, the per-item shape (identifier, opened, completion signal, action when complete, fallback, expected wall time, affects) is documented in `.claude/skills/in-flight-workflow-tracking/SKILL.md`. If any item lands here that has a "next session" handoff, promote the drain step to a `## MANDATORY FIRST ACTION` block above this section per that skill.

## Recently completed

- 2026-05-11: Round 1 prior-art research — report `01-prior-art-jayminwest-overstory-openhands.md`. Fetched via issues #5 and #6 (now closed); branches `fetched/issue-5` and `fetched/issue-6` remain on origin (branch deletion blocked by sandbox proxy; they can be deleted from the GitHub UI when convenient).

## Future research

Clusters worth investigating in a later round. Per the research-pipeline skill, each cluster names the sources, justifies why investigating it would extend the knowledge base, and estimates effort.

### Scope guardrail

`agent-runner`'s scope is the **execution layer** — running agents reliably in CI under a Claude Max subscription. Research on multi-agent orchestration, software-factory architecture, the Shapiro five-level framework, scenarios-as-holdout-sets, and Digital Twin patterns is being conducted in a separate repo and is **explicitly out of scope here**. Clusters below are limited to execution-layer concerns: harness mechanics, rate limits, cost/latency, OAuth, provider abstraction for issue/PR ops.

### Future research: AE book execution-layer chapters

**Sources:**
- https://www.jayminwest.com/agentic-engineering-book/6-harnesses/2-harness-stack
- https://www.jayminwest.com/agentic-engineering-book/6-harnesses/4-harness-as-control-system
- https://www.jayminwest.com/agentic-engineering-book/6-harnesses/5-harness-engineering
- https://www.jayminwest.com/agentic-engineering-book/6-harnesses/6-security-permissions-trust
- https://www.jayminwest.com/agentic-engineering-book/8-practices/3-cost-and-latency
- https://www.jayminwest.com/agentic-engineering-book/8-practices/4-production-concerns

**Justification:** Round 1 used only the chapter-6 *overview*. The "Key concepts" bullets carried the strategic framing, but the operational chapters (Cost and Latency, Production Concerns) likely contain directly applicable details on rate-limit handling, cost accounting, and incident response — all in `agent-runner`'s critical path. The four chapter-6 subchapters give us the canonical vocabulary for the harness as a control system, harness engineering, and the security boundary — the framing we'd cite in DESIGN.md and any future `LESSONS.md`.

**Effort:** ~6 source files via the fetch workflow (one labeled issue, ~3 min wall time). All on jayminwest.com so blocked from sandbox; workflow path required. Single subagent dispatch or a continuation of the lead session. ~1 hour total reading + report update.

### Future research: OpenHands `software-agent-sdk` git-provider abstraction

**Sources:**
- https://github.com/All-Hands-AI/OpenHands (locate the package boundary for `software-agent-sdk/`)
- The current OpenHands SDK docs at `https://docs.openhands.dev/sdk` (likely the entry point)
- Whatever path resolves to `GitService` / `ProviderHandler` once located (the earlier landscape scan placed it in `/openhands/integrations/`, which no longer exists)

**Justification:** Round 1 marked the GitService abstraction as 🟡 reconstructed — the abstraction *exists* and is *attested* in the earlier scan, but the current code path was not located. When `agent-runner` reaches Stage 4 (extract `ProviderClient` interface for GitLab+Jira backends), having the actual OpenHands interface signature would shorten our design loop substantially. Until then, this is parked.

**Effort:** ~2-4 source files once the right path is found. Likely a `gh api` call against `All-Hands-AI/software-agent-sdk` or wherever the SDK now lives, plus reading the relevant module. ~30 min wall time, one subagent dispatch.

### Future research: claude-code-action OAuth refresh community forks

**Sources:**
- https://github.com/grll/claude-code-login
- https://github.com/marketplace/actions/claude-code-action-with-oauth
- https://github.com/anthropics/claude-code-action/issues/727 (refresh-token feature request)

**Justification:** Not a Round-1 source per the original lead question, but emerged in DESIGN.md §7 as the single biggest operational risk. Before Stage 0 (proof of auth), we should read the actual refresh logic in these community forks — they've already solved this problem and we want to either vendor their approach or cite it directly in our `refresh-oauth.yml` workflow. Highest priority among the listed clusters.

**Effort:** ~3 files, one read pass. ~45 min. Should happen *before* Stage 0 implementation.

## Process notes

- Future-research clusters are ordered by relevance to the active roadmap, not by source affinity. The first three clusters above are all `agent-runner`-Stage-relevant; the last two are confirmatory or pre-positioning.
- Round 1's fetched content lives on `fetched/issue-5` and `fetched/issue-6` branches on origin (not merged into `main`, not into this PR). The report cites source URLs, not local snapshots, so the branches can be deleted whenever a maintainer with UI access wants to clean them up.
