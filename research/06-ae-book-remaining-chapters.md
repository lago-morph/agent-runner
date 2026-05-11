# Report 06 — AE book remaining operational chapters (chapter 7 patterns + remaining chapter 8 practices)

**Date:** 2026-05-11
**Author:** Subagent dispatch (run_id: 20260511-r3, sub-02)
**Status:** ✅ complete

## Lead question

Which execution-layer ideas in the AE book chapters not covered by report 03 — chapter 7 (Patterns) and chapter 8 subchapters 1, 2, and 6 — should reshape `agent-runner`'s DESIGN.md or roadmap, after explicitly excluding the multi-agent / orchestration material that PLAN.md's scope guardrail rules out?

## Orientation: what the cluster turned out to be

The PLAN.md cluster name ("AE book remaining operational chapters — chapter 7 architecture / context engineering and remaining 8/x") was based on inaccurate assumptions about the book's structure. The actual book has:

- **Chapter 7 = Patterns** (`/agentic-engineering-book/7-patterns/...`), not "architecture" or "context engineering" — the latter is part of chapter 4.
- **Chapter 8 = Practices**, with seven subchapters: `1-debugging-agents`, `2-evaluation`, `3-cost-and-latency` (in report 03), `4-production-concerns` (in report 03), `5-workflow-coordination` (multi-agent — out of scope), `6-knowledge-evolution`, `7-operating-agent-swarms` (multi-agent — out of scope).

The first fetch attempt (issue #15) used invented slugs (`/7-architecture/1-context-engineering`, `/8-practices/1-workflow-patterns`, etc.) that 404'd to the React app's "Chapter Not Found" component. The corrected fetch (issue #17) targeted the real URL pattern enumerated above and succeeded for all 10 in-scope URLs at HTTP 200.

After scope filtering (multi-agent material excluded per PLAN.md guardrail), the **in-scope reading list** was:

- Chapter 7 (Patterns): the index, plus `1-plan-build-review`, `2-self-improving-experts`, `4-autonomous-loops` (Ralph Wiggum), `5-react-pattern`, `6-human-in-the-loop`, `7-progressive-disclosure`.
- Chapter 8 (Practices): `1-debugging-agents`, `2-evaluation`, `6-knowledge-evolution`.

`agent-runner`'s position in the resulting taxonomy is unchanged from report 03: outer-harness on top of Claude Code (inner harness), CI substrate (GitHub Actions), Solo tier (1-5 concurrent agents per repo), single agent per CI run. The patterns chapter is read through that lens — every "this multi-agent variant scales it up" footnote is noted but not adopted.

---

## 1. Patterns chapter — overview, decision tree, and where `agent-runner` lands

The chapter ([`7-patterns`](https://www.jayminwest.com/agentic-engineering-book/7-patterns)) opens with a pattern catalog and a decision tree (verbatim, abbreviated):

> *Start: What kind of task?*
> *├─► Architectural/Creative Decision → Plan-Build-Review (or Orchestrator if multi-expert)*
> *├─► Mechanical/Repetitive Task → Autonomous Loops if completion criteria are machine-verifiable*
> *├─► Interactive/Exploratory Task → ReAct if each action informs the next*
> *├─► High-Stakes/Uncertain Decision → Human-in-the-Loop*
> *└─► Large Knowledge Base Task → Progressive Disclosure if context can't fit in one prompt*

The chapter's strongest framing-level claim is that **patterns are options with tradeoffs, not prescriptions** — and the safest default is *"if you're unsure, start with Plan-Build-Review."*

For `agent-runner` the relevant rows of the catalog map cleanly to actual workflows we'll ship or have already drafted:

| Pattern | `agent-runner` analogue | Verdict |
|---|---|---|
| Plan-Build-Review | The PR-review workflow (agent proposes a plan in a comment, builds, opens a PR for human review) | **Adopt** as the default workflow shape for v1 |
| Autonomous Loops (Ralph Wiggum) | The rate-limit-resume loop in the run-state machine; structurally also the right shape for any "fix all linter errors" / "migrate API call sites" workflow | **Adopt** the *resume semantics* (fresh context per attempt + git history as memory); **do not adopt** the indefinite-loop philosophy at v1 — bounded retries only |
| ReAct | What Claude Code already does internally per turn | **Inner-harness concern** — `agent-runner` doesn't reimplement; we just need to ensure our tool whitelist preserves the test/lint/compile signal channel |
| Human-in-the-Loop | The PR review itself; the augmentation-mode workflows from report 03 §6.1 | **Adopt** the gate-placement discipline; specifically the `risk → gate-tier` table (§6 below) |
| Progressive Disclosure | How `agent-runner` exposes MCP/Skills/tools to the agent (relevant to AgentConfig minimalism — see report 03 §5) | **Adopt** the Tier-1/Tier-2/Tier-3 framing as a constraint on AgentConfig |
| Self-Improving Experts | The closest analogue is `agent-runner`'s eventual `LESSONS.md` runbook (report 03 §8 item 8) | **Adapt** at the prompt/CLAUDE.md level, not at the AgentConfig level — see §3 below |
| Orchestrator / Expert Swarm / Multi-Agent Collaboration / Multi-Agent Landscape / Production Multi-Agent | Out of scope per PLAN.md guardrail | **Skipped** — see §10 |

The chapter's anti-pattern list also contains one item that earns a mention here even though it's a context-management lesson: **Emergency Context Rewriting** (*"Full context rewrites when hitting token limits, using the LLM to 'summarize' or 'compress' existing context to free up space"*). The chapter's recommendation is unambiguous: *"Better Alternatives: Incremental deltas; Frequent intentional compaction; Fresh agent boots — the 'one agent, one task' approach—start fresh rather than trying to compress unbounded context."* The "fresh agent boot" recommendation is the same operational seam as Ralph Wiggum's resume semantics (§3) and report 03 §6.6's *"start fresh + summary of prior attempt's outcome"* rule — three separate chapters converging on the same architectural choice.

---

## 2. Plan-Build-Review (§7/1) — the default workflow shape

The chapter ([`7-patterns/1-plan-build-review`](https://www.jayminwest.com/agentic-engineering-book/7-patterns/1-plan-build-review)) names a four-phase loop (Research-Plan-Build-Improve) where the Improve phase closes back into Research/Plan/Build by updating their *Expertise* sections. For `agent-runner` the load-bearing claims are:

- **Bad research compounds exponentially.** The chapter's table:

| Research Quality | Plan Accuracy | Lines of Wrong Code | Cost to Fix |
|---|---|---|---|
| Excellent | 95% | ~50 | Hours |
| Good | 80% | ~500 | Days |
| Poor | 50% | ~5,000 | Weeks |
| Terrible | 10% | Complete rewrite | Months |

> *"A 10-minute research mistake can create a 10-week refactoring disaster. The leverage is asymmetric—investing in research quality pays exponential dividends."*

For `agent-runner` this is the case for **the trigger payload framing** to include explicit research expectations when the agent's task is non-trivial. The trigger framing change report 03 §4 already proposed (the `<trigger>...</trigger>` wrapper for prompt-injection defense) is the same hook that should also carry a "for research-required tasks, produce a research summary before any code changes" instruction. One change, two benefits.

- **Scale-adaptive execution.** The chapter's BMAD-METHOD framing names four workflow depths: Quick Flow (3 steps, bug fixes), Standard (4 steps, features), Full Planning (6+ steps, new subsystems), Enterprise (8+ steps, compliance). The `agent-runner` analogue: **AgentConfig should declare the workflow depth a given trigger expects**, and the prompt assembly should adapt accordingly. v1 ships only Quick Flow and Standard; Full Planning and Enterprise are out of scope until a customer asks. **Implication for DESIGN.md §2 (AgentConfig schema):** add an optional `workflow_depth: Literal["quick", "standard", "full"]` field defaulting to `"standard"`, used to select prompt overlays.

- **Research as artifact, not just understanding.** The chapter's prescription that *"the output of research isn't just understanding—it's concise summary documents that capture findings"* maps onto report 03's Run JSON / transcript split: when an agent does research as part of its work, that summary should be committed to a file in the PR, not left only in the transcript. **Implication:** for tasks classified as `task_type: "research"` (per report 03 §3 Schmid trajectory-capture point), the agent's first commit in the PR branch should be the research summary `.md` — making it reviewable as the spec the build phase implements.

The chapter is otherwise written for laptop / IDE deployment (slash commands in `.claude/commands/experts/...`). At our layer the equivalent of a slash command is *which AgentConfig the trigger selects*. The Research/Plan/Build/Improve four-command structure does not map onto our single-CI-run model and is **not adopted** as a multi-step workflow — but its individual disciplines (research summary, scale-adaptive depth, the Quality Gate validation pattern from §8/1) do.

---

## 3. Autonomous Loops / Ralph Wiggum (§7/4) — the structural twin of our resume loop

This is the most directly applicable chapter in the entire fetched set. The pattern reduces to:

> *`while :; do cat PROMPT.md | claude-code ; done`*

Each iteration: loads task spec, spawns fresh Claude Code session, executes, commits, exits, repeats. Three operational claims are load-bearing for `agent-runner`:

### 3.1 *"Git history is memory"* — fresh context, persisted state

> *"State persists in commits, not context windows. Each iteration reads `git log` to understand prior attempts—what succeeded, what failed, what patterns emerged. Fresh context prevents cascading errors from poisoned conversation history."*

This is the same conclusion report 03 §6.6 reached from the multi-agent-lessons section ("It is better to start with fresh context on a fresh problem"), but with operational mechanism. For `agent-runner`'s rate-limit-resume loop:

- **Resume is not "continue from saved transcript."** Resume is "fresh `claude -p` invocation, with the prior attempt's *outcome summary* (not its transcript) injected into the prompt, and the working tree at whatever commit the prior attempt left it."
- **The prior attempt's commits ARE the durable memory.** The next attempt reads `git log` to see what was tried. This means the wrapper (`run.py`) should *not* squash or amend the prior attempt's commits before resuming — leave them intact even if they're incomplete, because that is the only signal the resumed agent has.
- **The Run JSON should record an "outcome summary" field, not just exit codes.** Per report 03 §1 the Run JSON is working memory; this chapter sharpens that — when an attempt ends (rate-limit, max-turns, timeout), the wrapper should write a 1-3 sentence machine-generated summary of *what the agent did and where it stopped* into the Run JSON, and the next attempt's prompt should include that summary as part of the trigger context.

**Implication for DESIGN.md §4 (Run JSON):** add `attempt_summaries: list[str]` — one entry per attempt, each a short prose summary of what that attempt accomplished, written by the wrapper from the stream-json final-message event before the next attempt fires.

### 3.2 *"The smart zone"* — context-window quality is non-uniform

> *"Empirical testing shows only 40-60% of context window exhibits high-quality reasoning. Early tokens and late tokens show degraded performance. Tight task scoping keeps work within this smart zone. When tasks expand beyond it, iteration quality degrades."*

Two consequences for `agent-runner`:

- **Bounded `max_turns` is not just a cost gate; it's a quality gate.** Per report 03 §2 the `max_turns` cap is a computational guide. The Ralph chapter's smart-zone insight provides the *why* — letting an agent run past its smart-zone window doesn't just cost more tokens, it produces lower-quality output. Our cap default should be tuned to keep most runs within the smart zone, not to the absolute API limit.
- **Single big workflows should be split into chained smaller agent runs.** For a task that genuinely needs more turns than the smart zone holds, prefer "agent A produces a research summary in run N; agent B implements in run N+1" — using git as the handoff channel — over "one agent, more turns."

### 3.3 *"Failures are data"* — commit on partial success

> *"Failed iterations create commits with error messages that guide subsequent attempts. The pattern embraces failure as exploration rather than blocking progress."*

For `agent-runner` this argues against a "transactional" model where an attempt's commits are reverted on failure. If attempt 1 of a multi-step task gets through 3 of 5 steps and then hits a rate limit, **those 3 steps' commits should stay**, and attempt 2 starts from that state. The wrapper should never `git reset --hard` on a rate-limit failure.

### 3.4 What we explicitly do NOT take from this chapter

- **Indefinite loops** (`while :;`). v1 of `agent-runner` has bounded retries (`max_attempts` from AgentConfig) — typically 2-3, not 30. The Ralph philosophy of *"naive persistence through repeated attempts compounds into eventual success"* is the right *frame* for resume but the wrong *bound* for a CI workflow that must terminate in a finite job-time budget.
- **The Anthropic Claude Code Ralph plugin** (the chapter mentions it ships with stop hooks, plan regeneration, progress reporting, safety checks). If/when that plugin stabilizes we may end up using it as the inner-loop engine; for now the explicit `claude -p` + wrapper is what we have.

### 3.5 What this chapter says about model selection that report 03 did not

The chapter's model-selection table:

| Model | Iterations to Completion | Cost per Iteration | Total Cost |
|---|---|---|---|
| Sonnet | 20 iterations | ~$0.40 | ~$8 |
| Opus 4.5 | 5 iterations | ~$1.20 | ~$6 |

Under *subscription* auth (Claude Max, our model) cost-per-iteration is zero dollars — but the *rate-limit budget* is the constraint. Translated: Opus 4.5 burns the rate-limit envelope ~1.5× faster per iteration but converges in 4× fewer iterations, so net rate-limit consumption is ~37% of Sonnet's. **For tasks where iteration count is the rate-limit-window risk, Opus is the right model under our auth model**, even though under API auth the dollar math is closer.

**Implication for DESIGN.md §2 (AgentConfig schema):** add a `model: str` field (already implicit in CLAUDE.md selection); document that Opus is preferred for tasks expected to need >5 iterations under subscription auth, since its rate-limit-budget efficiency dominates Sonnet's at iteration counts where Sonnet would otherwise multiply rate-limit consumption.

---

## 4. Self-Improving Experts (§7/2) — what to take, what to leave

The chapter ([`7-patterns/2-self-improving-experts`](https://www.jayminwest.com/agentic-engineering-book/7-patterns/2-self-improving-experts)) describes a three-command (Plan / Build / Improve) pattern where the Improve command analyzes git history and updates the *Expertise* sections of the Plan and Build commands. The chapter is explicit about which sections evolve:

> *"Expertise sections: Mutable domain knowledge that evolves with experience. Workflow sections: Stable process descriptions that define how the expert operates. Only Expertise sections get updated, ensuring the process remains consistent while knowledge accumulates."*

And the four conservative update rules: **PRESERVE**, **APPEND**, **DATE** (`*[YYYY-MM-DD]*:` prefix), **REMOVE** only with clear evidence.

### Why this isn't load-bearing for `agent-runner` v1

`agent-runner` does not own a per-task "expertise" file the way the chapter assumes — that is a *prompt-engineering* artifact owned by the developer using Claude Code, not by `agent-runner`. We orchestrate the harness; we don't curate the agent's domain expertise.

### Where it does land

The chapter's **Expertise / Workflow split** is a useful framing for `agent-runner`'s **own** documentation:

- `DESIGN.md` is the Workflow section (stable, slow-changing, governs how `agent-runner` operates).
- `LESSONS.md` (proposed in report 03 §8 item 8) is the Expertise section (mutable, accretes timestamped entries from observed failures, governed by PRESERVE/APPEND/DATE/REMOVE — see also §6/knowledge-evolution below).
- `AgentConfig` files in user repos sit in the Workflow tier (their `allowed_tools`, `max_turns`, `max_attempts` fields are stable per repo).
- The user's `CLAUDE.md` is *their* Expertise tier, not ours.

**Implication for repo conventions (not DESIGN.md proper):** when we create `LESSONS.md`, it should adopt the AE chapter's `*[YYYY-MM-DD]*:` timestamping convention and the four PRESERVE/APPEND/DATE/REMOVE rules verbatim. This costs nothing and inherits a battle-tested format — see also §7 (Knowledge Evolution) which is the same convention applied at chapter-8 scope.

The chapter's anti-patterns (Updating Workflow Sections; Removing Patterns Without Evidence; Not Dating New Expertise Entries; Letting Expertise Sections Grow Unbounded; Improving Without Production Evidence; Mixing Multiple Domains in One Expert) are all directly applicable to how we should curate `LESSONS.md`. The most actionable: *"Letting Expertise Sections Grow Unbounded"* — when `LESSONS.md` exceeds some budget (the chapter doesn't name one; we should pick ~2K tokens as a hard cap) we either consolidate or split.

---

## 5. ReAct (§7/5) — Claude Code already implements it; what we owe is signal quality

The ReAct chapter ([`7-patterns/5-react-pattern`](https://www.jayminwest.com/agentic-engineering-book/7-patterns/5-react-pattern)) is mostly an inner-harness concern — Claude Code already does Thought-Action-Observation loops via extended thinking + tool calls. The execution-layer-relevant content is the **Coding Agent Specialization** section's claim about observation signal quality:

> *"The observation step is the highest-leverage design surface in a coding agent's ReAct loop. Generic tool outputs (file content, search results) are weak feedback signals; coding-specific outputs (test results, lint errors, compiler diagnostics) are strong ones. The difference determines whether the loop converges or drifts."*

The chapter's signal taxonomy:

| Signal Type | Source | Feedback Quality |
|---|---|---|
| Test results | pytest, jest, cargo test | Binary + localized |
| Lint output | ruff, eslint, clippy | Binary + localized |
| Compiler errors | tsc, gcc, rustc | Binary + localized |
| Build output | Build system | Binary + systemic |
| Generic tool output | File reads, search results | Non-binary, interpretive |

> *"Prefer binary, localized feedback signals over interpretive ones. When the observation is 'tests pass' or 'lint: 0 errors,' the model has an unambiguous success criterion."*

For `agent-runner` this is direct guidance for **what to put in the AgentConfig `allowed_tools` whitelist**. Two implications:

- **`Bash` (or its equivalent) must be on the whitelist if the inner ReAct loop is to converge on coding tasks** — because that's the channel through which `pytest` / `ruff` / `tsc` produce the binary signals the agent steers on. Without it the agent has to reason from interpretive signals (file content, grep results) and the chapter is explicit that this drifts.
- **Verification-Driven Development.** The chapter's exact framing:

> *"Provide failing tests the agent must pass. Provide linter configuration the agent must satisfy. Provide integration test suites for self-evaluation. The agent's ReAct loop terminates when observations confirm success against objective criteria, not when the model judges its own work complete."*

This connects directly to report 03 §6.1's augmentation/automation distinction. The "did CI pass on the agent's commit" check that report 03 §2 proposed adding to the Run JSON's `status` semantics is, in this chapter's vocabulary, the verification-driven termination signal. **For automation-mode workflows (report 03 §6.1), CI-pass-on-the-commit is not optional — it's the binary signal that closes the loop.**

The chapter also cites *"METR controlled study finding (2026): Experienced developers using AI coding tools were 19% slower, despite subjective assessments of ~20% improvement."* This is the same finding report 03 §3 cites from the SWE-bench reference, repeated here as an argument for verification-driven loops. It strengthens the case for never marking a run truly successful on `claude -p` exit code alone.

**Implication for DESIGN.md §11 (verification gate):** every `agent-runner` workflow should declare a verification command (`verify: pytest` or `verify: ruff check && pytest`) in its AgentConfig, and the Run JSON's `status` should not advance to `succeeded` until that command has returned 0 against the agent's commit. This is the operational form of report 03 §2's "verification-driven completion check."

---

## 6. Human-in-the-Loop (§7/6) — gate placement formalism

The chapter ([`7-patterns/6-human-in-the-loop`](https://www.jayminwest.com/agentic-engineering-book/7-patterns/6-human-in-the-loop)) gives the discipline behind the augmentation-mode workflows that `agent-runner` will ship in v1. The **risk-based gate criteria** table:

| Risk Factor | Low (Auto-proceed) | Medium (Notify) | High (Require Approval) |
|---|---|---|---|
| Reversibility | Git commit | Config change | Database migration |
| Blast radius | Single file edit | Module changes | Production deployment |
| Cost | API call < $0.10 | Batch operation < $10 | Operation > $100 |
| Sensitivity | Internal code | Customer data access | Credentials, payments |
| Precedent | Routine operation | First-time pattern | Novel approach |

The chapter is also unambiguous about what is **always** gated:

> *"Always gate: Production deployments, Database schema changes, External API calls with side effects (sending emails, creating accounts), Credential or permission changes, Cost-incurring operations above threshold, Deleting data (especially without backups)."*

For `agent-runner`, mapping this to GitHub-context blast radii:

| GitHub action | Risk tier (per chapter) | `agent-runner` gating mechanism |
|---|---|---|
| Open a PR (default branch untouched) | Low — auto-proceed | None; agent's PR is the human-review surface |
| Push to a feature branch | Low | None |
| Comment on issue/PR | Low | None |
| Merge a PR (via `gh pr merge`) | High — require approval | Workflow `permissions:` block omits `contents: write` for PR merge in v1 |
| Push to `main` directly | High — require approval | Workflow `permissions:` omits direct push; branch protection enforces |
| `gh release create` / publish | High — require approval | Out of scope for v1 |
| Delete a branch / release / issue | High — require approval | Out of scope; `--allowed-tools` whitelist must omit |

This is a sharper version of report 03 §6.2's severity-1 violations list. The gate mechanism remains the same (workflow `permissions:` block as the structural enforcement) but the **gating taxonomy is now explicitly tied to reversibility/blast/cost/sensitivity/precedent dimensions**, which gives reviewers a checkable framework when they're proposing new workflows.

The chapter's **Gate Decision Tree** is also worth promoting verbatim into the runbook:

> *"Is this action reversible within 5 minutes? — Yes: Is it modifying production systems? — Yes: GATE; No: Auto-proceed. — No: GATE.*
> *Does this action affect external parties? — Yes: GATE.*
> *Is this the first time performing this type of operation? — Yes: GATE (establish precedent)."*

The "establish precedent" gate is the one easiest to forget. For `agent-runner`, it argues that **any new AgentConfig (or significant change to an existing one) should trigger a human-review gate on its first run** before being eligible for unattended/automation-mode execution. We don't need new infrastructure for this — a per-AgentConfig `is_autonomous: bool` field defaulting to `false` (i.e., always-PR-review) suffices, with explicit opt-in to autonomous runs once an AgentConfig has accumulated track record.

The chapter's anti-patterns are the canonical augmentation-mode failure modes:

- **Gate Fatigue** — *"Too many approval requests desensitize humans to risk... Reserve gates for genuinely high-risk operations."* Translated for us: avoid per-commit human approval; gate at the PR boundary (the natural batching unit) rather than at every action.
- **Vague Approval Requests** — *"Approval requests must include action, context, risk assessment, and explicit options."* Translated: the agent's PR description (which is what the human sees at the gate) should include the equivalent of the chapter's effective approval request template — what was changed, why, what the rollback is, what could go wrong. This is a prompting concern (`CLAUDE.md` template) more than an `agent-runner` concern.
- **Synchronous Gates in Async Workflows** — *"Match gate synchronicity to workflow."* For us this is automatic: GitHub PRs ARE async approval with state persistence. We don't risk this anti-pattern in v1; we *would* risk it if we ever added a "wait inline for human approval" step in a workflow.
- **Missing Rollback Plans** — *"Every high-risk gate must include rollback plan."* For us: any AgentConfig that authorizes a high-risk action class must declare its rollback procedure (e.g., a `rollback: revert <commit>` field in AgentConfig).
- **Gates Without Audit Trail** — *"Log every approval request and response."* For us this is free — GitHub PR review records are the audit trail.

**Implication for DESIGN.md §10 (roadmap) and §11 (workflows):** add an `is_autonomous: bool = False` field to AgentConfig, and require that promotion from non-autonomous to autonomous follow the chapter's "establish precedent" / "calibration" discipline (some N successful supervised runs on the same AgentConfig before opting into autonomy).

---

## 7. Progressive Disclosure (§7/7) — the AgentConfig minimalism mandate, sharpened

The chapter ([`7-patterns/7-progressive-disclosure`](https://www.jayminwest.com/agentic-engineering-book/7-patterns/7-progressive-disclosure)) frames a three-tier loading model:

> *"Tier 1: Metadata Index (~1-5% of context budget). Tier 2: Activated Content (~10-30% of budget). Tier 3: On-Demand Resources (fetched as needed)."*

The chapter's most direct critique of overloading harnesses is the **GitHub MCP integration** example:

> *"Anthropic's GitHub MCP integration illustrates the eager loading trap: 'tens of thousands of tokens' consumed just to make repositories and issues accessible. This pre-loads capability descriptions that may never be used, leaving less space for actual task work."*

This is also exactly the example report 03 §5 cited from chapter 8/3's token-cost-by-feature-type table. The two chapters reinforce each other: **MCP servers are expensive in context tokens, and most of what they offer goes unused in any given run.**

The token-economics table:

| Approach | 10 Skills | 100 Skills | 1000 Skills |
|---|---|---|---|
| Eager Loading | 50k tokens | 500k tokens | 5M tokens (impossible) |
| Progressive Disclosure | ~6k tokens | ~7k tokens | ~8k tokens |

> *"Progressive disclosure scales logarithmically; eager loading scales linearly."*

For `agent-runner`, two operational implications already implicit in report 03 are now explicit constraints:

- **`AgentConfig.allowed_tools` should default to the smallest set that completes the task class.** The chapter's anti-pattern *"Over-Eager Activation: Activating multiple knowledge items 'just in case' defeats the purpose"* applies directly to the temptation to add tools "in case the agent needs them." Default-deny; add only the named subset the workflow's task class requires.
- **Prefer plain `gh` CLI over the GitHub MCP for one-shot operations.** Report 03 §5 already reached this conclusion from the chapter 8/3 cost angle; this chapter sharpens it with the *"effectively unlimited expertise within fixed context budgets"* framing — the GitHub MCP, by always loading everything, is the wrong tier-3 tool for our workflow shape. (If/when we need MCP for stateful integrations like persistent session, we revisit; v1's GitHub interactions are stateless one-shots.)

The chapter also names **Excessive Metadata** as an anti-pattern (*"Keep metadata to 50-200 characters. Full details belong in Tier 2."*). For `agent-runner`'s own AgentConfig file shape this argues for terse field descriptions and pointers to docs, not embedded long-form prose.

**Implication for DESIGN.md §2 (AgentConfig schema):** add a normative comment stating that `allowed_tools` defaults to deny-all, that MCP servers are opt-in per AgentConfig (not global), and that AgentConfig field documentation is tier-1 metadata (terse), with full operational guidance kept in DESIGN.md §11.

---

## 8. Debugging Agents (§8/1) — the runbook this report's report-03 sibling promised

The chapter ([`8-practices/1-debugging-agents`](https://www.jayminwest.com/agentic-engineering-book/8-practices/1-debugging-agents)) is the most directly importable runbook in the entire fetched set. Its **Core Four** taxonomy:

| Component | Symptoms | First Check |
|---|---|---|
| Prompt | Wrong interpretation, missed instructions | Does the prompt clearly specify what NOT to do? |
| Model | Capability limits, reasoning errors | Can a more capable model do this task? |
| Context | Hallucination, outdated info, missed details | What context was actually available? |
| Tools | Wrong tool choice, tool errors, bad outputs | Did tools return what was expected? |

> *"The diagnostic sequence: Check tools first (easiest to verify), then context (what did the agent know?), then prompt (ambiguity?), then model (capability?) last."*

This is a tighter formulation than the five-class taxonomy in report 03 §3 (model / context / prompt / harness / tool). Two ways to reconcile:

- The Core Four collapses "harness" into "tools" and "context" — at the chapter's framing, harness failures show up as tool failures (wrong tool / tool errors) or context failures (missing or stale state). For `agent-runner`'s LESSONS.md taxonomy, **adopt the Core Four for the *triage*, but keep the five-class taxonomy in the Run JSON `failure_classification` field** so we don't lose the harness/tool distinction on incident records.

The chapter's **Diagnostic Decision Tree** (Step 1 characterize → Step 2A-F by failure type) is a 60-second checklist worth importing verbatim into the LESSONS.md runbook. Each branch (wrong output / stuck-looping / stopped-early / wrong-tool / hallucination / crash) gets a 4-bullet check sequence.

### What this chapter adds that report 03 didn't have

- **Common Failure Modes catalog** with diagnosis + root causes + fixes per mode. Particularly:
  - **Context Overflow** — *"Move critical instructions to end of prompt (recency bias)."* This is direct guidance for our prompt assembly: the trigger payload (which is dynamic, frequently the load-bearing instruction for that run) should sit at the end of the prompt, not the beginning.
  - **Tool Errors** — *"Tool returning error messages agent can't interpret"* — directly applicable to our wrapper: when we wrap shell commands or surface CI output to the agent, the wrapper should pre-parse common error shapes (rate-limit envelope, OAuth-expired) into structured, agent-readable messages rather than raw stderr.
  - **Premature Termination** — *"Vague or easily-satisfied completion criteria... Implicit rather than explicit requirements."* Reinforces §5 (verification-driven completion); the binary verify command is the antidote.
  - **Quality Gate Failures** — *"No validation between workflow phases. Completion criteria too vague or easily satisfied. Pressure to ship fast bypasses quality checks."* The chapter recommends *adversarial review gates* between phases. For `agent-runner` v1 (single-phase per run) this is the verify command running after the agent's last commit and before the run is marked succeeded.

- **Anti-pattern: Debugging in Production** — *"Reproduce the failure locally or in a dev environment. Use production logs to understand the failure mode, but fix and test in isolation."* For `agent-runner` this argues for a `--dry-run` / local-replay capability in run.py: given a failed run's stream-json transcript, replay it locally without touching GitHub. This is a Stage-2-or-later feature but worth recording in the roadmap.

- **Anti-pattern: The Infinite Retry Loop** — *"Limit retries (2-3 max). On persistent failure, escalate to human or halt with detailed error... If retries are frequently triggered, that's a signal to fix the root cause, not increase the retry limit."* Reinforces the bound on `max_attempts` and adds: when a workflow's runs are frequently hitting the retry limit, that's a signal to investigate the root cause, not raise the cap. Possibly a metric to track per AgentConfig: retry-rate-per-7-days.

- **Hook testing patterns** — the chapter has a long section on testing Claude Code hooks (PreToolUse / PostToolUse). For `agent-runner` we don't currently use Claude Code's hook system (our equivalent is the run.py wrapper plus the workflow steps), so most of this is not directly applicable. The relevant cross-cutting takeaway: **manual hook testing outside of Claude Code is mandatory**. For `agent-runner`'s analogue — the run.py wrapper — this means the rate-limit detector, the OAuth refresh, and the stream-json consumer should each have unit tests that exercise them with synthetic inputs without spawning Claude Code.

### Case studies worth noting

The chapter's case studies are useful failure-mode exemplars to seed LESSONS.md with:

- **Case 1: The Disappearing Instructions** — context overflow at 24K tokens; constraint at line 5 of system prompt got out-prioritized by recency. Fix: constraints near *end* of prompt, repeated at intervals. Direct application to our prompt assembly.
- **Case 5: The Intermittent Success** — same prompt + context, 60% success at temperature 0.7 due to multiple plausible reasoning paths. Fix: temperature 0.1 + explicit step-by-step structure. Probably not load-bearing for us (Claude Code defaults its own temperature; we don't expose it) but a reminder that *"identical inputs, varying outputs"* is a normal failure shape we should expect.

**Implication for DESIGN.md / LESSONS.md:** import the Diagnostic Decision Tree verbatim into LESSONS.md as the on-call triage guide; import the Common Failure Modes catalog as the deeper reference; pre-populate LESSONS.md with the chapter's six case studies (with attribution) so we have non-empty content from day one.

---

## 9. Evaluation (§8/2) — what we should measure, and the bare minimum for v1

The chapter ([`8-practices/2-evaluation`](https://www.jayminwest.com/agentic-engineering-book/8-practices/2-evaluation)) frames evaluation as the difference between engineering and tinkering. Its four **starter metrics**:

| Metric | What It Measures |
|---|---|
| Task completion rate | % of runs that produce usable output |
| Failure mode distribution | What breaks and how often |
| Cost per success | Token usage / successful completions |
| Latency distribution | P50, P95, P99 response time |

For `agent-runner` these map onto Run JSON fields we already have or should add:

| Metric | Source |
|---|---|
| Task completion rate | Aggregate over Run JSONs by `status == "succeeded"` (with verify-passing definition from §5 above) |
| Failure mode distribution | Aggregate over Run JSONs by `failure_classification` |
| Cost per success | Total `tokens_used` / count of `succeeded` runs (rate-limit-budget metric, not dollars — per report 03 §5 inversion) |
| Latency distribution | Job duration percentiles from Actions API or from Run JSON `started_at`/`ended_at` |

**Implication for DESIGN.md §4 (Run JSON):** ensure these four fields are present (most already are — `tokens_used`, `started_at`, `ended_at`, `status`). The one we're missing is a `success_verified: bool` derived from §5's verify command.

The chapter's **three-tier evaluation strategy** (Smoke / Core / Full) maps onto release gates:

| Tier | Cases | Runtime | When to Run |
|---|---|---|---|
| Smoke | 3-10 | <1 min | Every prompt change |
| Core | 20-50 | 3-10 min | Before committing |
| Full | All cases | 30+ min | Nightly, pre-deploy |

For `agent-runner` v1 this is aspirational — we don't have an eval set. The actionable v1 ask is **the Smoke tier only**: 3-10 hand-crafted test cases (e.g., "trigger a run that intentionally hits max_turns and verify the wrapper records the right Run JSON status," "trigger a run with an invalid AgentConfig and verify graceful failure") run on every PR to `agent-runner` itself. These are unit/integration tests for the wrapper, not for any specific user agent.

The chapter's **Reliability Dimensions Beyond Task Completion** section is the formal version of report 03 §6.2's four-dimension reliability gate (consistency / robustness / predictability / safety). The chapter cites the same Rabanser et al. paper. The single point report 03 didn't make explicit:

> *"Average performance (mean completion rate, median latency) hides critical failures. Slice eval sets by category, track worst-case performance at p95 and p99, and measure maximum cost per run — not average."*

**Implication for DESIGN.md §11 (observability):** when we eventually surface metrics dashboards, P95/P99 of `tokens_used`-per-run must be a first-class metric, not P50 alone — because a single run that consumes 10× the typical token budget signals the rate-limit-budget risk in a way that means doesn't.

The chapter's **anti-patterns** are also worth importing into LESSONS.md as guardrails:

- **Evaluation Theater** — *"An elaborate eval suite with comprehensive metrics... Nobody acts on the findings."* Translated: don't build observability we won't act on. For v1 the right discipline is "ship the four starter metrics, build dashboards only if/when we use them in operational decisions."
- **Metric Fixation** — *"Optimize a single metric while ignoring everything else."* Direct application: don't tune the wrapper to minimize `tokens_used` if that drops `task_completion_rate`. Always measure together.
- **Golden Path Testing** — *"Eval cases cover the happy path... Agent performs well on eval but fails in production on ambiguous inputs."* For our v1 unit-test set: at least 30% of cases should test failure paths (rate-limit hit, OAuth expired, malformed AgentConfig) rather than happy paths.
- **Eval Hoarding** — *"Eval sets grow without pruning."* Standing rule: when adding a new test case, identify whether an existing case should retire.

The chapter's **Annotation Workflow Design** section (single-arbiter principle, binary labeling, do not outsource error analysis, criteria drift is expected) and the **Error Analysis Practice** section (four-step methodology: sample → open coding → axial coding → iterate to saturation) are operational disciplines that apply to the human side of running `agent-runner` on real workflows. Not a v1 feature, but the Husain four-step process should govern how we triage real-world failures from our first dogfood run onward.

---

## 10. Knowledge Evolution (§8/6) — governance for LESSONS.md (and this research/ folder)

The chapter ([`8-practices/6-knowledge-evolution`](https://www.jayminwest.com/agentic-engineering-book/8-practices/6-knowledge-evolution)) frames the discipline that report 03 §8 already proposed (LESSONS.md) and that §4 above echoes. The chapter's **Grow-and-Refine Principle**:

> *"A knowledge base that only grows becomes unwieldy. One that constantly condenses loses nuance. Sustainable evolution requires both phases."*

And its **PRESERVE / APPEND / DATE / REMOVE** framework:

- PRESERVE: existing patterns stay by default
- APPEND: new insights get their own dated annotations (`*[YYYY-MM-DD]*: ...`)
- DATE: every new content gets a timestamp
- REMOVE: only with high-confidence evidence (multiple contradicting implementations, fundamental tech shift, provable harm, strict superseded)

For `agent-runner`'s `LESSONS.md` (when we create it) and for the existing `research/` folder, this gives us:

- **Adoption verbatim** of the four operations as the curation contract.
- **Adoption verbatim** of the *"Letting Expertise Sections Grow Unbounded"* anti-pattern as a soft cap (proposed in §4 above as ~2K tokens for LESSONS.md).
- **The Status Progression model** (Seedling → Growing → Mature → Evergreen) is potentially overkill for our scale but is a useful frame for the research/ INDEX.md status column we already maintain (✅ complete / 🟡 partial / 📝 draft / ⏳ blocked-on-fetch / 🗑️ deprecated). The existing convention serves the same purpose; no change.

The chapter's **Delta-Based Updates vs Full Rewrites** section warns directly against the LLM-rewrite anti-pattern that the §1 (Patterns chapter) anti-pattern *"Emergency Context Rewriting"* also names. The measured impact:

> *"75.1% fewer rollouts with delta-based updates vs full rewrites; 82.3% latency reduction (fewer tokens to process); preservation of edge case handling and anti-patterns."*

For our research/ folder this argues against ever asking an agent to "compress" or "rewrite" an existing report — the right operation is always APPEND a new report or APPEND a dated note inside the existing one.

The chapter's **Learning Separation in Multi-Agent Systems** subsection (read-only during execution, writes only post-hoc by a dedicated improve-agent) is multi-agent material — out of scope. But the *single-writer principle* that motivates it is worth noting for our context: when multiple `agent-runner` runs (in different repos / different jobs) might be reading the same shared `LESSONS.md`-equivalent in the future, only one process at a time should write. For v1 this is trivially satisfied (each user repo has its own `LESSONS.md`).

**Implication for repo conventions (not DESIGN.md proper):** when LESSONS.md is created, its header should declare it as the project's "Expertise tier" per §7/2 (Self-Improving Experts) terminology, and its curation contract should state: PRESERVE/APPEND/DATE/REMOVE per §8/6. The research/ folder INDEX.md and PLAN.md already follow this discipline implicitly; no change needed there.

---

## 11. Out-of-scope content noted but skipped

Per PLAN.md's Scope guardrail, the following multi-agent / orchestration material was **deliberately not body-read** in this report:

| Chapter | Why skipped |
|---|---|
| §7/3 Orchestrator Pattern | Multi-agent coordination (planner + N specialists) — out of scope for `agent-runner` v1 (single agent per run) per Round 1 STEELMAN.md and report 03 §6.3 compound-reliability arithmetic |
| §7/8 Expert Swarm Pattern | Multi-agent consistency-governance — out of scope; see §6/3 above for cross-references |
| §7/9 Multi-Agent Collaboration Pattern | Multi-agent coordination — out of scope |
| §7/10 The Multi-Agent Landscape | Architectural-decision-making across multi-agent ecosystem — out of scope |
| §7/11 Production Multi-Agent Systems | Running 10+ agents in production — out of scope |
| §8/5 Workflow Coordination for Agents | Structured metadata for multi-agent coordination — out of scope; subtitle "for Agents" (plural) confirms multi-agent framing |
| §8/7 Operating Agent Swarms | Multi-agent production-scale operations — out of scope |

The §7 chapter's overview (§1 of this report) does cite each of these as cross-references in its decision tree and pattern catalog; the framing-level content (when to escalate from single-agent to multi-agent) was read at the catalog level only, not at the per-chapter detail level. The scope decision is unchanged: **`agent-runner` is a single-agent-per-run execution layer**, and the multi-agent territory belongs to the sister "software factory" research effort (per Round 1 §4 and report 03's confirmation).

The PLAN.md cluster description that mentioned "chapter 7 architecture / context engineering" was based on inaccurate assumptions about the book's structure. The actual chapter-7 (Patterns) content is what this report covers; "context engineering" / "context windows" / "tool design" / "skills" / "MCP" / "memory" / "state" / "retrieval" / "observability" / "feedback loops" — the names that appeared in the original (404'd) issue-15 fetch list — are real *concepts* but they correspond to chapter 4 (Context), chapter 5 (Tool Use), and other earlier chapters that report 03 already drew on indirectly. They are also potential clusters for a future round if the existing reports' coverage of these concepts ever feels insufficient — but they are not the cluster this report was tasked with.

---

## 12. Implications for DESIGN.md

This round adds the following to the cumulative design-doc edits proposed by report 03:

1. **DESIGN.md §2 (AgentConfig schema):** add `workflow_depth: Literal["quick", "standard", "full"]` (default `"standard"`) per §2 (Plan-Build-Review scale-adaptive); add `is_autonomous: bool = False` per §6 (Human-in-the-Loop establish-precedent gate); document that `allowed_tools` defaults to deny-all per §7 (Progressive Disclosure); document that `model: str` selection should prefer Opus for high-iteration-count tasks under subscription auth per §3.5 (Ralph Wiggum cost table).
2. **DESIGN.md §4 (Run JSON):** add `attempt_summaries: list[str]` per §3.1 (resume-with-summary); add `success_verified: bool` per §5 (verification-driven termination); ensure `tokens_used`, `started_at`, `ended_at` are present per §9 (starter metrics).
3. **DESIGN.md §5 (run.py / prompt assembly):** place trigger payload at the *end* of the prompt (recency bias) per §8 Common Failure Mode "Context Overflow"; pre-parse known error shapes (rate-limit, OAuth-expired) into agent-readable messages per §8 Common Failure Mode "Tool Errors"; never `git reset --hard` on rate-limit failure (preserve partial-success commits) per §3.3 (Ralph "failures are data").
4. **DESIGN.md §10 (roadmap):** classify automation-mode workflows under §6's gate-decision-tree dimensions (reversibility / blast / cost / sensitivity / precedent), not just augmentation/automation binary; add `--dry-run`/local-replay capability to run.py as a Stage-2 item per §8 anti-pattern "Debugging in Production."
5. **DESIGN.md §11 (verification gate / observability):** every workflow's AgentConfig declares a `verify:` command per §5 (Verification-Driven Development); the Run JSON's `status` does not advance to `succeeded` until verify returns 0 against the agent's commit; observability metrics include P95/P99 of `tokens_used`-per-run, not just P50, per §9 reliability-dimensions.
6. **DESIGN.md §11 (security / gates):** the Human-in-the-Loop gate-decision-tree (reversibility → external-effect → first-time-pattern) governs whether a new workflow ships in autonomous mode per §6; promotion from non-autonomous to autonomous requires N supervised runs as track record.
7. **A new `LESSONS.md`** (or appendix to DESIGN.md): adopt the §8 (Debugging Agents) Diagnostic Decision Tree as the on-call triage guide; adopt the §8 Common Failure Modes catalog as the deeper reference; pre-seed with the §8 case studies; curate per §10 (Knowledge Evolution) PRESERVE/APPEND/DATE/REMOVE with `*[YYYY-MM-DD]*:` timestamps and a soft ~2K-token cap.
8. **Repo conventions (not DESIGN.md proper):** never ask an agent to "compress" or "rewrite" an existing report or LESSONS.md — APPEND only, per §10 delta-based-updates anti-pattern.

### Cross-cutting "adopt verbatim" maxims from this round

Two single-line statements stand out as worth importing into LESSONS.md alongside report 03's three:

> *"State persists in commits, not context windows."* (§7/4 Ralph Wiggum)
> *"Prefer binary, localized feedback signals over interpretive ones."* (§7/5 ReAct, coding-agent specialization)

### Cross-cutting "differ" — what this round confirms is *not* for us

- **Indefinite while-true loops.** Ralph's *naive persistence* philosophy is the wrong bound for CI; we adopt the resume semantics (fresh context + git history) but cap iterations.
- **Multi-step expert command sets** (Plan-Build-Improve as four separate slash commands). At our layer the equivalent of a "command" is a workflow trigger; we don't expose multi-step expert chains in v1.
- **The `Improve` command pattern** as a discrete agent that updates Plan/Build expertise. Our equivalent is human-curated `LESSONS.md` updates; we do not auto-evolve our own runbook in v1.
- **Multi-agent learning separation** (§8/6's read-only-during-execution rule). Trivially satisfied by single-agent-per-run; revisit only if/when multi-process write contention becomes a thing.

---

## Sources reviewed

| Source URL | Status | Notes |
|---|---|---|
| https://www.jayminwest.com/agentic-engineering-book/7-patterns | ✅ Full review | Fetched via issue #17. Chapter index: pattern catalog table, decision tree, selection matrix, multi-pattern composition examples, anti-pattern "Emergency Context Rewriting" (with ACE paper citation and four better-alternatives list). Informed §1 (overview/decision tree) and §11 (cross-cutting "fresh agent boots" → resume semantics convergence point). |
| https://www.jayminwest.com/agentic-engineering-book/7-patterns/1-plan-build-review | ✅ Full review | Fetched via issue #17. Bad-research-compounds-exponentially table (95%/80%/50%/10% accuracy → 50/500/5000/rewrite LOC), Research-as-artifact framing, Scale-Adaptive Execution (BMAD-METHOD: Quick/Standard/Full/Enterprise), four-dimension override criteria, integration with self-improving experts, BMAD 34.5k-stars production evidence. Informed §2 in full and §12 implication 1 (AgentConfig.workflow_depth). |
| https://www.jayminwest.com/agentic-engineering-book/7-patterns/2-self-improving-experts | ✅ Full review | Fetched via issue #17. Three-command (Plan/Build/Improve) learning triangle, Expertise vs. Workflow split, PRESERVE/APPEND/DATE/REMOVE conservative-update rules, timestamp convention `*[YYYY-MM-DD]*:`, Hermes Agent (47K-stars Feb 2026) as recent open-source instantiation, six anti-patterns table. Informed §4 in full (mostly negative result for v1; positive for LESSONS.md curation). |
| https://www.jayminwest.com/agentic-engineering-book/7-patterns/4-autonomous-loops | ✅ Full review | Fetched via issue #17. Ralph Wiggum core implementation (`while :; do cat PROMPT.md \| claude-code; done`), git-history-as-memory, smart-zone insight (40-60% of context window high quality), failures-are-data, machine-verifiable success criteria, backpressure controls, model selection table (Sonnet 20×$0.40 vs Opus 5×$1.20), Huntley attribution and Anthropic-plugin-vs-original-philosophy split, METR 19% slower finding. Informed §3 in full and §12 implications 1, 2, 3. |
| https://www.jayminwest.com/agentic-engineering-book/7-patterns/5-react-pattern | ✅ Full review | Fetched via issue #17. Thought-Action-Observation core loop, structured-output variant, trade-offs vs Direct Generation/CoT/PBR/Ralph, four anti-patterns (Thought-Free Actions, Observation Overload, Infinite Loops, Reasoning Without Evidence), production considerations (context management, latency budgeting, cost tracking), **Coding Agent Specialization section with signal-quality taxonomy table** (test/lint/compile = binary localized; file-content/grep = interpretive), Verification-Driven Development framing with SWE-bench production gap (80% Verified vs 23% Pro) and METR 19% finding, temperature-effects on multi-step reliability. Informed §5 in full and §12 implication 5 (verify command). |
| https://www.jayminwest.com/agentic-engineering-book/7-patterns/6-human-in-the-loop | ✅ Full review | Fetched via issue #17. Risk-based gate criteria table (5 dimensions × 3 tiers), gate decision tree, common gate triggers, pre-action / post-action / checkpoint / escalation gates, sync vs async approval, hybrid timeout-with-escalation, effective-approval-request template, Claude Code TeammateTool / lifecycle-hooks / HUMAN_IN_LOOP-variable implementations, five anti-patterns (Gate Fatigue, Vague Approval Requests, Synchronous-in-Async, Missing Rollback, Gates Without Audit Trail), good-fit vs poor-fit lists. Informed §6 in full and §12 implication 6 (gate-decision-tree governance). |
| https://www.jayminwest.com/agentic-engineering-book/7-patterns/7-progressive-disclosure | ✅ Full review | Fetched via issue #17. Three-tier model (metadata index / activated content / on-demand resources), Claude Skills production example, **token-economics table (10/100/1000 skills × eager-vs-progressive)**, four implementation patterns (tool descriptions as metadata, structured indices, hierarchical disclosure, lazy loading with prefetch), trade-off analysis vs eager loading, **Anthropic GitHub MCP "tens of thousands of tokens" trap**, three anti-patterns (Excessive Metadata, Missing Index Updates, Over-Eager Activation). Informed §7 in full and §12 implication 1 (AgentConfig minimalism / MCP opt-in). |
| https://www.jayminwest.com/agentic-engineering-book/8-practices/1-debugging-agents | ✅ Full review | Fetched via issue #17. Agent-vs-traditional debugging table, **Core Four framework (Prompt/Model/Context/Tools) with diagnostic sequence (tools→context→prompt→model)**, six-branch Diagnostic Decision Tree (wrong-output/stuck-looping/stopped-early/wrong-tool/hallucination/crash), eight Common Failure Modes (Context Overflow, Tool Errors, Hallucination, Instruction Drift, Tool Selection Confusion, Premature Termination, Quality Gate Failures, State Confusion in Multi-Agent), debugging tools (structured logging / minimal reproduction / A/B testing / context inspection / trace replay / model comparison), eight anti-patterns (Debugging Without Logs, Changing Multiple Things, Not Reproducing, Assuming Model, Debugging in Production, Ignoring Partial Successes, Infinite Retry Loop), hook testing patterns, five Case Studies (Disappearing Instructions / Tool Selection Oscillation / Phantom Hallucination / Multi-Agent State Drift / Intermittent Success), debugging checklist. Informed §8 in full and §12 implications 3, 7. |
| https://www.jayminwest.com/agentic-engineering-book/8-practices/2-evaluation | ✅ Full review | Fetched via issue #17. Why-evaluation-is-harder-for-agents framing (3 consequences), Vibes-to-Rigor spectrum with three-question calibration, **four starter metrics table (completion rate / failure mode distribution / cost per success / latency distribution)**, rubric-based scoring / comparative / constraint satisfaction, **four reliability dimensions (Consistency / Robustness / Predictability / Safety) with Rabanser et al. arXiv:2602.16666 citation**, three-tier eval strategy (Smoke / Core / Full × case count and runtime), error analysis four-step methodology (Husain), eval-driven development (eval-first loop, hold-out sets), evaluation maturity curve (Manual/Scripted/Automated/Production-integrated), four anti-patterns (Evaluation Theater, Metric Fixation, Golden Path Testing, Eval Hoarding). Informed §9 in full and §12 implications 2, 4, 5 (P95/P99 metrics). |
| https://www.jayminwest.com/agentic-engineering-book/8-practices/6-knowledge-evolution | ✅ Full review | Fetched via issue #17. Knowledge-bases-are-gardens framing, Grow-and-Refine principle, **PRESERVE/APPEND/DATE/REMOVE framework with operational rules and timestamp convention**, Learning Separation in Multi-Agent (single-writer principle — noted, mostly out-of-scope), utility-tracking pattern for evidence-based removal, Delta-Based Updates vs Full Rewrites with measured impact (75.1% fewer rollouts, 82.3% latency reduction), Emergency Context Rewriting anti-pattern (cross-references §7 patterns chapter), when-full-rewrites-are-justified, status progression model (Seedling → Growing → Mature → Evergreen), update-checklist. Informed §10 in full and §12 implication 7 (LESSONS.md curation contract). |
| https://www.jayminwest.com/agentic-engineering-book/7-patterns/3-orchestrator-pattern | ⏭️ Out of scope | Multi-agent orchestration (planner + N specialists). Per PLAN.md scope guardrail. Cited at the catalog level in §1; not body-read. |
| https://www.jayminwest.com/agentic-engineering-book/7-patterns/8-expert-swarm-pattern | ⏭️ Out of scope | Multi-agent consistency-governance. Per PLAN.md scope guardrail. Cited at the catalog level in §1; not body-read. |
| https://www.jayminwest.com/agentic-engineering-book/7-patterns/9-multi-agent-collaboration | ⏭️ Out of scope | Multi-agent coordination. Per PLAN.md scope guardrail. Cited at the catalog level in §1; not body-read. |
| https://www.jayminwest.com/agentic-engineering-book/7-patterns/10-multi-agent-landscape | ⏭️ Out of scope | Multi-agent architectural decision-making. Per PLAN.md scope guardrail. Cited at the catalog level in §1; not body-read. |
| https://www.jayminwest.com/agentic-engineering-book/7-patterns/11-production-multi-agent-systems | ⏭️ Out of scope | 10+ agents in production. Per PLAN.md scope guardrail. Cited at the catalog level in §1; not body-read. |
| https://www.jayminwest.com/agentic-engineering-book/8-practices/5-workflow-coordination | ⏭️ Out of scope | Structured metadata for multi-agent coordination. Per PLAN.md scope guardrail. Listed in chapter-8 index (§1) but not fetched. |
| https://www.jayminwest.com/agentic-engineering-book/8-practices/7-operating-agent-swarms | ⏭️ Out of scope | Multi-agent production-scale operations. Per PLAN.md scope guardrail. Listed in chapter-8 index (§1) but not fetched. |
| https://www.jayminwest.com/agentic-engineering-book/7-architecture (and 12 subchapter URLs) | ❌ Invalid URL | Fetched via issue #15 with invented slugs (PLAN.md cluster name was inaccurate). All URLs returned the React app's "Chapter Not Found" page (HTTP 200 but no content). The actual chapter at this position is `/7-patterns` (§1 above); "context engineering" / "tool design" / "skills" / "MCP" / "memory" / "state" / "retrieval" / "observability" / "feedback loops" are real concepts but live in chapters 4 and 5, not in a chapter-7 architecture sub-chapter. |
| https://www.jayminwest.com/agentic-engineering-book/8-practices/{1-workflow-patterns,2-prompt-patterns,5-testing-and-verification,6-debugging-and-incident-response,7-evaluation-and-iteration,8-team-practices} | ❌ Invalid URL | Fetched via issue #15 with invented slugs. All URLs returned "Chapter Not Found". The real chapter-8 subchapter list (per the index page rendered in issue #15's `8-practices` fetch) is `1-debugging-agents`, `2-evaluation`, `3-cost-and-latency`, `4-production-concerns`, `5-workflow-coordination`, `6-knowledge-evolution`, `7-operating-agent-swarms` — corrected via issue #17. |
