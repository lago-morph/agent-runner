# Report 11 — AE book chapters 1 (Foundations), 2 (Prompt), and 3 (Model)

**Date:** 2026-05-11
**Author:** Subagent dispatch (run_id: 20260511-r5, sub-01)
**Status:** ✅ complete

## Lead question

Which execution-layer ideas in AE book chapters 1 (Foundations), 2 (Models), and 3 (Prompting) — the still-unread foundational portion of the book — should reshape `agent-runner`'s DESIGN.md or roadmap, given that reports 01/03/06/08 have already mined chapters 4-10 for the operationally-novel material?

## Orientation: what the cluster turned out to be

Two surprises landed in the index probe (issue #22) and changed the shape of this round:

1. **The chapter titles in the PLAN.md cluster (and in this subtask's brief) were inverted.** The book's actual structure is:
   - Chapter 1 — **Foundations** (slug `1-foundations`) — exactly as stated.
   - Chapter 2 — **Prompt** (singular, slug `2-prompt`) — *not* "Models" as the brief claimed. The brief's "chapter 2 (Models)" was wrong; the real chapter on Models is chapter 3.
   - Chapter 3 — **Model** (singular, slug `3-model`) — *not* "Prompting" as the brief claimed.

   The slugs `2-models` and `3-prompting` in the brief returned HTTP 200 from the SPA but with only the navigation skeleton (no chapter body) — silent 404s in disguise. This is the third instance in five rounds of paraphrased/guessed external slugs being wrong (Round 3 had `7-architecture`-vs-`7-patterns`; Round 4 had `5-tools`-vs-`5-tool-use`). The probe step paid for itself again.

2. **Chapter 1 has only ONE subchapter in the book index sidebar:** `1-foundations/1-twelve-leverage-points`. So the in-scope reading is actually compact: 1 subchapter for Foundations, 3 for Prompt (`1-prompt-types`, `2-structuring`, `3-language`), and 4 (of 5) for Model (`1-model-selection`, `2-model-behavior`, `3-model-limitations`, `5-model-evaluation`; `4-multi-model-architectures` is multi-model orchestration, ⏭️ out of scope per PLAN.md guardrail). Plus the three chapter index pages themselves — and chapter 1's index page actually contains substantial framework content (the 5-pillar model and its 2026-04-12 "why Harness was added" rationale), unlike chapters 2 and 3's indexes which are short overview blurbs.

The expected outcome from the PLAN.md note ("Chapter 1 is probably the highest-recap, lowest-novelty target") turned out to be **half wrong**: the 5-pillar framing and `Agent = Model + Harness` definition are indeed recap of report 01, but the **Twelve Leverage Points hierarchy** and the dated-2026-04-11 **Anti-Patterns by Leverage Level catalog** — both from the chapter 1 body and the single Foundations subchapter — are net-new material with direct DESIGN.md and LESSONS.md applicability. The Prompt and Model chapters are higher-recap than Foundations once normalized against reports 03/06/08, but each contributes a small number of operationally-actionable items.

`agent-runner`'s position is unchanged from reports 03/06/08: outer-harness on top of Claude Code (inner harness), CI substrate, Solo tier, single agent per CI run, subscription auth (Claude Max OAuth).

---

## 1. Chapter 1 (Foundations) — recap of the pillar frame, but TWO net-new pieces

### 1.1 Recap: the 5-pillar `Agent = Model + Harness` frame (already in reports 01, 03)

Chapter 1's index page ([`1-foundations`](https://www.jayminwest.com/agentic-engineering-book/1-foundations)) restates and formalizes the 5-pillar decomposition (Prompt, Model, Context, Tool Use, Harness) and the `Agent = Model + Harness` definition. Both are extensively used in prior reports — see report 01 §2 ("the harness frame maps directly onto `agent-runner`") and report 03 §1 (Raschka's six-component decomposition of Harness, which is one level finer-grained than this five-pillar decomposition).

What is *new* in the chapter 1 index, but not load-bearing for `agent-runner`:

- A dated-2026-04-12 paragraph naming the **"definitional crystallization event"** for `Agent = Model + Harness` — five practitioners (Fowler, Raschka, Mollick, Hashimoto, Schmid) converging on the formula within a 90-day window.
- Citation of **Agent Psychometrics research (arXiv:2604.00594)** that operationalizes the formula as `P(success) = σ(θ_LLM + θ_scaffold − β_difficulty)` — additively independent contributions of model and scaffold quality.

Both are useful citation-handles but do not change any `agent-runner` decision; this is the report-01 thesis with footnotes.

### 1.2 Net-new: the Twelve Leverage Points hierarchy

The Foundations subchapter ([`1-foundations/1-twelve-leverage-points`](https://www.jayminwest.com/agentic-engineering-book/1-foundations/1-twelve-leverage-points)) adapts Donella Meadows's "Places to Intervene in a System" to agentic engineering. Lower numbers = higher leverage. The hierarchy (verbatim):

| # | Leverage Point | Core Question |
|---|---|---|
| 12 | Context | What does the agent actually know? |
| 11 | Model | What tradeoffs exist: cost, speed, intelligence? |
| 10 | Prompt | Are instructions concrete and followable? |
| 9 | Tools | What actions can agents take, and in what form? |
| 8 | Standard Out | Can agents and operators see what's happening? |
| 7 | Types | Is typing consistent and enforced? |
| 6 | Documentation | Can agents navigate and trust the documentation? |
| 5 | Tests | Are tests helping agents or just theatre? |
| 4 | Architecture | Is the codebase agentically intuitive? |
| 3 | Plans | Can agents complete tasks without further input? |
| 2 | Templates | Do agents know what good output looks like? |
| 1 | ADWs (AI Developer Workflows) | How does work flow between agents? |

Rows #1 and #2 (ADWs and Templates) are multi-agent / orchestration territory and ⏭️ out of scope for `agent-runner` per the PLAN.md guardrail. But **#3 through #12 are all directly applicable to a single-agent CI execution layer**, and the hierarchy gives `agent-runner` a *prioritization frame* the prior reports did not have.

Specifically: the levels above #9 (Tools) — i.e. #8 Standard Out, #7 Types, #6 Documentation, #5 Tests, #4 Architecture, #3 Plans — are properties of the *target repo* under which an `agent-runner` agent runs, not properties of `agent-runner` itself. `agent-runner`'s direct surface is Context (#12), Model (#11), Prompt (#10), and Tools (#9): the four pillars also called out in the chapter as "Low Leverage (Local Fixes)." The chapter is explicit that:

> *"Lower numbers indicate higher leverage points that affect the entire system. Changes at the top (#1-#4) cascade throughout the system; changes at the bottom (#9-#12) produce local fixes."*

**Implication for `agent-runner`'s scope discipline:** the harness owns four of the lowest-leverage knobs in the framework. This is consistent with — and validating of — report 01's "Solo tier" recommendation and the explicit decision to defer multi-agent orchestration. It also reinforces that the path to *higher-leverage* improvements for end users is not features in `agent-runner` itself; it's better target-repo Architecture (#4), better Plans (#3), and better Templates (#2) — which `agent-runner` should *enable* (by running well) but not *enforce*.

**What this could change in DESIGN.md:** add a one-paragraph "scope philosophy" footnote naming the 4 leverage points `agent-runner` directly addresses (#9-#12), and explicitly disclaiming the higher-leverage points (#1-#8) as "user's-codebase concerns we don't touch." This sharpens the existing Solo-tier framing and gives users a vocabulary for "what should I do *outside* agent-runner to get more value?"

### 1.3 Net-new: the Anti-Patterns by Leverage Level catalog

The same subchapter has a dated-2026-04-11 section catalogging seven named anti-patterns sourced from four practitioners (Liu, Hamel, Willison) and mapped to specific leverage levels:

| Anti-Pattern | Corrupts | Failure Type | Source |
|---|---|---|---|
| **Isolated Prompting** | #12 Context | Missing context, not missing prompt skill | Liu [1] |
| **Tool Proliferation** | #9 Tools | Parallel instances without integration plan | Liu [1] |
| **Testing Theatre** | #5 Tests | Generic evals optimized on wrong target | Hamel [4] |
| **Metric Over-Aggregation** | #5 Tests | Insufficient failure-mode discrimination | Hamel [5] |
| **Design Delegation** | #3-#4 Plans/Architecture | AI as architect, not implementer | Willison [7] |
| **Post-Hoc Learning** | #1 ADWs | Point-tool knowledge without workflow design | Liu [1] |
| **Automated Optimization Before Understanding** | #1-#2 ADWs/Templates | Judgment outsourced before developed | Hamel [6] |

The two with direct `agent-runner` applicability:

- **Isolated Prompting** (corrupts #12 Context). *"An engineer provides fragment context — meeting notes, a code snippet, a requirements section — without supplying architectural context or codebase integration. The model produces a syntactically coherent output that is semantically disconnected from the actual system."* This is precisely the failure mode that `agent-runner`'s trigger-prompt assembly must guard against. Today the trigger payload includes the issue body and PR diff URL; the chapter argues that "the issue body alone" is *Isolated Prompting* unless paired with codebase/architecture context (which Claude Code's CLAUDE.md-loading provides automatically — the inner harness handles it). The lesson is to verify the `CLAUDE.md` of the target repo is loaded BEFORE the trigger fires, not just assume it. This is testable: a smoke-test run that asserts the workspace context layer is present.

- **Tool Proliferation** (corrupts #9 Tools). *"15 coding agents in 15 separate terminal windows creating illusion of work rather than integrated output."* `agent-runner` is at the opposite end (single agent per CI run, by design), so this anti-pattern *validates* the v1 contract from report 01 §3. Worth citing in DESIGN.md as one more independent voice against parallel-agent fanout.

The other five anti-patterns either operate above `agent-runner`'s leverage layer (Design Delegation, Post-Hoc Learning, Automated Optimization Before Understanding all corrupt #1-#4 — user's-codebase concerns) or relate to evaluation infrastructure that `agent-runner` doesn't ship (Testing Theatre, Metric Over-Aggregation corrupt #5 — these are advisory for users, not constraints on `agent-runner`).

**LESSONS.md candidates** (per the format report 08 §6 sharpened):

- `[ANTI-iso-00001] helpful=0 harmful=0 *[2026-05-11]*:: Isolated Prompting — issue body alone without CLAUDE.md / codebase context produces semantically disconnected output. Verify workspace-context layer is loaded before the trigger fires; this is the inner harness's job but the outer harness is responsible for not bypassing it (e.g., by running outside the repo checkout).`
- `[ANTI-prolif-00001] helpful=0 harmful=0 *[2026-05-11]*:: Tool Proliferation — N agents in N windows is not equivalent to a designed multi-agent workflow. agent-runner's single-agent-per-run contract is the correct shape; do not relax this without an explicit ADW design (per chapter 1 leverage point #1).`

---

## 2. Chapter 2 (Prompt) — operational patterns, mostly recap of 7-level model from chapter 9

### 2.1 The Prompt chapter index ([`2-prompt`](https://www.jayminwest.com/agentic-engineering-book/2-prompt))

The index page covers four areas, almost all of which are either restatements of well-known prompt-engineering practice or cross-references to deeper subchapters:

- **The prompt is not just text** — system instructions + user messages + injected context + structural cues. This is reading-level orientation; no `agent-runner` decision rides on it.
- **Static / Parameterized / Conditional / Contextual / Composed taxonomy** — five-level summary of the seven-level prompt-maturity model that report 08 §5 already covered (under the chapter 9/2 name "Prompt Maturity Model"). See vocabulary correction in §4 below.
- **The prompt-model contract** — every prompt makes implicit assumptions about model capabilities. Useful framing but operationally a restatement of "test prompts on the model you'll deploy on."
- **Three principles**: Clarity Over Cleverness, Structure Reduces Variance, Constraints Enable Creativity, Examples Beat Explanations. Standard fare, no `agent-runner` action item.

**One net-new framing from the chapter index** that *is* `agent-runner`-relevant: the **One-Shot vs. Conversational Agents** distinction:

> *"One-shot agents should receive everything they need upfront. The initial prompt is the entire interface—if it's insufficient, the task fails. This favors: comprehensive instructions over brevity; explicit constraints and stopping conditions; self-contained context (no assumptions about follow-up).
> Conversational agents operate differently. They can clarify, iterate, and adapt. ... Mixing these paradigms causes problems. A one-shot prompt that asks clarifying questions wastes the user's time. A conversational prompt that tries to do everything at once overwhelms the interaction."*

`agent-runner` is **categorically a one-shot agent harness**: the CI run starts with a trigger payload, runs to completion or rate-limit, and either ships output or aborts. There is no conversational loop available — the agent cannot ask the user a clarifying question mid-run. This means the trigger-prompt construction has stronger constraints than the chapter spells out for general one-shot agents:

- **Stopping conditions must be in the prompt.** The chapter's example list ("when X, when Y") is directly applicable. Today `agent-runner`'s prompt assembly leaves stopping conditions to Claude Code's defaults (max_turns from AgentConfig, internal heuristics). A more disciplined prompt template would name explicit stopping conditions.
- **Uncertainty handling cannot be "ASK the user" branches.** The chapter's example pattern ("ASK the user when ambiguous; PROCEED when reversible") is unavailable to a CI-substrate one-shot. The harness-level alternative is "PROCEED with documented assumption + flag in the PR description for human review." This is a useful mental model for the Run JSON's failure-classification field (per report 03 §6.4) — a third bucket beyond `success` / `failure`: `proceeded-with-assumption`.

**Implication for DESIGN.md:** §5 (trigger payload assembly) should explicitly note "agent-runner is a one-shot harness; the trigger prompt must include explicit stopping conditions and proceed-with-documented-assumption defaults; clarifying-question patterns are unavailable." This is not a code change — it's a documentation tightening.

### 2.2 [`2-prompt/1-prompt-types`](https://www.jayminwest.com/agentic-engineering-book/2-prompt/1-prompt-types) — the 7-level maturity model (recap)

This subchapter lays out the same 7-level prompt maturity model that report 08 §5 already extracted from chapter 9/2 "Prompt Maturity Model." The two are the same framework:

| Level | Name | Key Characteristic |
|---|---|---|
| 1 | Static | Fixed instructions, no variation |
| 2 | Parameterized | Accepts input to customize behavior |
| 3 | Conditional | Branches based on input or state |
| 4 | Contextual | Incorporates external information |
| 5 | Composed | Invokes other prompts/commands |
| 6 | Self-Modifying | Updates itself based on execution |
| 7 | Meta-Cognitive | Improves other prompts in the system |

This is not actually new material relative to report 08 — it's the *same* framework presented twice (here in chapter 2 framed as prompt complexity; in chapter 9 framed as engineer maturity). What chapter 2/1 adds that chapter 9/2 didn't:

- **Concrete example prompts at each level** (e.g., the Level 4 "Architecture Review" example that reads `docs/ARCHITECTURE.md`, `src/config/schema.ts`, `.env.example` before proceeding).
- **The Level 6 "Conservative Update Rules"** (PRESERVE / APPEND / DATE / REMOVE) for self-modifying prompts. This is operationally useful — it's the discipline `agent-runner` would need if it ever shipped a self-improving prompt template (which it doesn't today and probably never should at the harness level; see §5).
- **The Level 7 "Bulk-Update Coordination"** pattern (multi-agent orchestration of Level 6 improvements in parallel via lightweight models). ⏭️ Multi-agent — out of scope.

**`agent-runner`'s prompt level is L4 (Contextual)** — the trigger prompt loads CLAUDE.md, the AgentConfig, and the trigger payload, and proceeds. It has no L5 composition (does not invoke other prompts), no L6 self-modification, no L7 meta-cognition. This is intentional and correct; the chapter validates that "Start Low, Evolve Up" is the recommended discipline. The DESIGN.md should explicitly tag the prompt level as L4 so future contributors know not to bolt on L5+ behaviors without an architectural decision.

### 2.3 [`2-prompt/2-structuring`](https://www.jayminwest.com/agentic-engineering-book/2-prompt/2-structuring) — the canonical 7-section structure and the forbidden-meta-commentary list

This subchapter contains genuinely new operational material:

**The Canonical 7-Section Structure** (frontmatter + Title + Purpose + Variables + Instructions + Workflow + Report). This is the structural template Anthropic-style Claude Code agents/commands use. `agent-runner`'s prompt assembly does not currently use this structure (it's unstructured markdown today), but adopting it for the trigger-prompt template would make the contract more machine-parseable and easier for users to override.

**The Forbidden Meta-Commentary List** (verbatim from the chapter):

> *"The most consistent failure mode is agents prefacing output with explanation. Explicitly forbid patterns like 'Based on the changes...', 'I have created...', 'Here is the...', 'Let me...' — these break downstream parsing."*

Full forbidden-prefix list:
- `"Based on the changes..."`
- `"I have created..."`
- `"Here is the..."`
- `"This commit..."`
- `"I can see that..."`
- `"Looking at..."`
- `"Let me..."`
- `"I will..."`
- `"The changes..."`

This is **directly actionable for `agent-runner`'s trigger-prompt template** — the template should include a "do not prefix output with the following phrases" block. The downstream-parsing concern is real for `agent-runner`: when the run summary is appended to the PR description or the issue comment, these prefixes are noise that degrade the user experience. Today the prompt does not forbid them.

**Output Styles as Behavioral Toggles** (dated 2025-12-09). The pattern is "one agent, multiple output formats via a style parameter" — relevant for `agent-runner` if a future use case wants both a human-readable PR description and a machine-parseable `run.json` artifact from the same run. Not on the v1 critical path; worth a roadmap note as a "post-Stage-4 generalization" once `AgentConfig` has matured.

### 2.4 [`2-prompt/3-language`](https://www.jayminwest.com/agentic-engineering-book/2-prompt/3-language) — research-grounded linguistic patterns

This subchapter is the most evidence-dense in chapter 2, citing four research papers and several practitioner blogs. The findings most relevant to `agent-runner`:

- **Declarative > Imperative for reasoning tasks (~23% lift on SatLM benchmark, arxiv:2305.09656).** The pattern: declarative phrasing ("the implementation meets these criteria...") encourages state-based thinking; imperative phrasing ("implement these criteria...") works better for sequential procedural steps. The chapter's recommended split ("declarative for goals, imperative for workflow") is directly applicable to `agent-runner`'s trigger-prompt template — the goal-statement section should be declarative ("the PR satisfies the issue's success criteria"), the workflow section imperative ("read the issue, examine the diff, implement the change, run tests").

- **The Pink Elephant problem: negative constraints backfire at scale.** *"InstructGPT research revealed that negative constraints backfire at scale. When prompts say 'never do X,' models become more likely to do X as conversation length increases."* `agent-runner`'s trigger-prompt today has at least one explicit negative constraint in the AgentConfig `forbidden_tools` list (which gets rendered into the prompt). The chapter argues this should be reframed as "use only the following tools: [allowed list]" rather than "never use [forbidden list]." This is a small prompt-template change with measurable downside if done wrong. Worth flagging as a candidate A/B in the eval suite (per report 03 §6.2) before adopting.

- **The DETAIL framework (arxiv:2512.02246) — Specificity is task-type dependent.** Mathematical tasks gain +0.47 accuracy from specificity; decision-making tasks gain only +0.02; creative writing actually *loses* 0.12. For `agent-runner`'s coding-agent use case, specificity is in the +0.31 range — meaningful but not dominant. The take-away: specificity is worth pursuing, but with diminishing returns; once the prompt has API signatures, error-handling requirements, and test-coverage requirements, more detail is unlikely to help.

- **~21 words optimal prompt length (Google research, no specific citation in the chapter).** Likely doesn't apply to `agent-runner` — our prompts are L4 Contextual with substantial workspace and trigger payload, far longer than 21 words. The finding is a guidance for the *instruction* portion of the prompt, not the context portion. Worth keeping in mind for the AgentConfig `prompt_template` field.

- **Bare imperatives > hedged requests.** *"Could you maybe try to validate the input if possible?"* parses worse than `"Validate input before processing."` Standard practice; no `agent-runner` action.

**Implication for DESIGN.md / LESSONS.md:** the trigger-prompt template should:
1. Use declarative phrasing for goals, imperative for workflow steps.
2. Reframe `forbidden_tools` rendering as positive `allowed_tools` listing (Pink Elephant mitigation).
3. Not over-specify (DETAIL framework — diminishing returns for code generation past the key constraints).
4. Use bare imperatives, not hedged phrasing.

These are template-level changes; they don't touch the harness logic. Suggest a §5.1 sub-section in DESIGN.md titled "Prompt-language guidelines" that codifies these rules.

---

## 3. Chapter 3 (Model) — mostly recap of frontier-default + capability-capacity, plus three net-new pieces

### 3.1 [`3-model`](https://www.jayminwest.com/agentic-engineering-book/3-model) and [`3-model/1-model-selection`](https://www.jayminwest.com/agentic-engineering-book/3-model/1-model-selection) — recap with two new framings

The headline message of chapter 3 — **"Default to frontier; downgrade only with evidence"** — is consistent with report 01 §2 and report 03 §6.1. For `agent-runner`'s subscription-auth model under Claude Max, "frontier" is whichever Anthropic model the subscription tier provides (Opus 4.6 as of April 2026 per the chapter); the user has no model-selection knob in the runtime sense. The chapter's framework therefore mostly *validates* `agent-runner`'s "use whatever the inner harness chose" stance.

Two net-new framings worth noting:

1. **"Access tier is distinct from capability tier."** *"As of April 2026, the highest-capability model (Claude Mythos Preview) is not accessible via the standard API — it is restricted to enrolled programs."* For `agent-runner`, this confirms that the subscription-auth model (Claude Max via OAuth) operates at the standard-API frontier ceiling and not above it. No code change; useful for explaining to users why `agent-runner` doesn't expose a model knob.

2. **"Within the frontier tier, harness ecosystem matters more than model capability differences."** This is a sharper restatement of report 01's "the harness is the primary control surface" — it now has a research-citable backing (Agent Psychometrics arXiv:2604.00594, again). For `agent-runner`, this is a thumb on the scale for "invest in `agent-runner`'s outer-harness reliability rather than fretting about model selection."

The **autoresearch / overnight-trained-SLM pathway** (Karpathy 2026-03-06; Lütke/Shopify 2026-03-10) is genuinely interesting frontier-engineering material but completely out of scope for `agent-runner`. ⏭️ Note for the wider AE-book reading record but no `agent-runner` implication.

### 3.2 [`3-model/2-model-behavior`](https://www.jayminwest.com/agentic-engineering-book/3-model/2-model-behavior) — temperature compounding (operationally important)

The single most actionable item from this subchapter:

> *"Temperature compounds in multi-step workflows. A single task at temperature 1.0 might succeed 95% of the time. Ten sequential tasks at the same temperature? Reliability degrades to approximately 60%. The math: 0.95^10 ≈ 0.60."*

| Temperature | Single-Step Success | 10-Step Success |
|---|---|---|
| 0.0 (near-deterministic) | ~99% | ~90% |
| 0.5 (moderate creativity) | ~97% | ~74% |
| 1.0 (high creativity) | ~95% | ~60% |

The chapter's recommendation: **default to temperature 0** for multi-step workflows (which is exactly what `agent-runner`'s runs are — the whole CI run is a many-turn workflow), and isolate higher-temperature steps to non-reliability-critical paths.

`agent-runner` does not currently expose a temperature knob to users — it inherits whatever Claude Code's default is. Per Anthropic's documentation, Claude Code defaults to temperature 0.0 for code-generation contexts. **This means `agent-runner` is already in the right place by inheritance**, but the implication is to *not* expose a temperature override in `AgentConfig` (or if exposed, default it to 0 and strongly warn against raising it).

**Recommendation for DESIGN.md:** add a one-line note that the harness assumes temperature 0 (inherited from Claude Code defaults) and does not currently expose a temperature override; if such an override is added in the future, the default must remain 0 with a clear warning about compound-error degradation.

Also notable: the **agentic task behavioral profile of Claude** ("systematic caution... tends to request clarification before proceeding when task parameters are ambiguous, rather than assuming and proceeding") is the inverse of the one-shot agent constraint from §2.1 above. The chapter actually frames this as a *reliability advantage* for production agentic systems ("fewer silent failures, more recoverable mid-task pauses"). For `agent-runner`, this means Claude's tendency to pause and ask becomes *visible as an incomplete-but-recoverable run* — which the trigger-prompt's `proceed-with-documented-assumption` directive (§2.1) needs to balance against. There is a real tradeoff here: forcing Claude to always proceed reduces silent-failure protection. The right answer is probably "let Claude pause/ask, and surface the question in the PR description, but do not block the run."

### 3.3 [`3-model/3-model-limitations`](https://www.jayminwest.com/agentic-engineering-book/3-model/3-model-limitations) — version pinning (concrete recommendation)

The subchapter covers six limitation classes (math, hallucination, context window, instruction drift, tool use, version stability). Most of these are recap of report 08 §1 (capability-capacity model, 40-60% threshold) or report 06 §3 (instruction drift, periodic reinforcement).

The genuinely new operational item is **explicit version pinning**:

> *"Pin to specific model versions in production. Test new versions in staging before promotion... Production: `MODEL_VERSION = "claude-opus-4.5-20251101"` — Pinned version. Not: `claude-opus-latest`."*

And the **Spotify regression criterion** (dated 2025-12-10):

> *"Spotify's production agent infrastructure runs continuous regression testing against new model releases. Deployment decision: if new version scores >5% better on capability benchmarks but breaks <2% of existing workflows, upgrade proceeds with targeted prompt adjustments. If breakage exceeds 5%, upgrade deferred until prompts can be updated."*

For `agent-runner` under subscription auth, **the user does not control model version** — Claude Code (and through it, Claude Max) chooses the model. This means version-pinning is actually NOT directly applicable as a user knob. But the *pattern* is applicable indirectly:

- **`agent-runner` should record the model version actually used** (the inner harness exposes this via stream-json events) in the Run JSON's `attempt` record. Today the Run JSON schema (per report 03 §4 and report 08 §1.1) tracks `peak_context_pct` and other metrics; it should also track `model_id` and `model_version` so that a regression in run quality after a Claude Code upgrade can be correlated with the version change.

- **The Spotify-style regression criterion is the kind of evaluation framework `agent-runner`'s eval suite (report 03 §6.2 / report 06 §9) should adopt the *vocabulary* of**, even if `agent-runner` doesn't ship the eval suite itself. A future eval-harness add-on could compute "X% better, Y% breakage" against a corpus of recorded runs — but that is post-Stage-4 work.

**Recommendation for DESIGN.md:** add `model_id` and `model_version` to the Run JSON `attempt` record schema. This is a schema-level change with no logic implications; the inner harness already emits the information via stream-json.

### 3.4 [`3-model/5-model-evaluation`](https://www.jayminwest.com/agentic-engineering-book/3-model/5-model-evaluation) — capability-reliability gap (load-bearing concept)

This subchapter contains the single most important new concept from chapter 3: the **capability-reliability gap** (Rabanser et al., arXiv:2602.16666, Princeton, 2026):

> *"On GAIA (general assistant tasks): accuracy improved steadily; reliability showed barely any improvement, even among the latest models. On τ-bench (customer service simulation): reliability improved at one-seventh the rate of accuracy."*

> *"Selecting a newer, higher-accuracy model does not reliably produce a more consistent or robust agent. Capability and reliability require independent measurement and independent improvement strategies."*

The chapter operationalizes "reliability" as four dimensions: **consistency, robustness, predictability, safety**. Of these:

- **Consistency** (same outcome on repeated identical runs) "remained low across all models." This is the dimension `agent-runner`'s rate-limit-resume loop most depends on — when a run resumes after a 5-hour rate-limit window, the second-half behavior should be consistent with the trajectory the first-half was on. Low consistency means the resume-loop's outcome-summary injection (per report 06 §7) is doing more load-bearing work than the first read might suggest.
- **Discrimination** (whether confidence successfully separates successes from failures) "mostly worsened" on GAIA. This is bad news for any plan that relies on the agent's self-reported success/failure to drive automation decisions.

The **compound error problem** restated as `p^n`:

| Per-Step Accuracy | 10 Steps | 20 Steps | 50 Steps | 100 Steps |
|---|---|---|---|---|
| 99% | 90.4% | 81.8% | 60.5% | 36.6% |
| 98% | 81.7% | 66.8% | 36.4% | 13.3% |
| 95% | 59.9% | 35.8% | 7.7% | 0.6% |
| 90% | 34.9% | 12.2% | 0.5% | 0.003% |

**Architectural implication for `agent-runner`** (the chapter is explicit on three of these):

1. **"Optimize per-step reliability above all else."** Small per-step improvements compound. This validates `agent-runner`'s focus on the rate-limit-resume loop as a per-step reliability mechanism (it removes "session-died-from-rate-limit" as a failure class).
2. **"Minimize workflow length."** Shorter workflows have exponentially higher success rates. This argues for `AgentConfig.max_turns` defaulting *low* rather than high — chapter 6 §3 (report 06) had this implication; chapter 3/5 sharpens it with the math.
3. **"Implement recovery mechanisms."** Retries, validation gates, error correction. `agent-runner`'s rate-limit-resume is one such mechanism; the chapter argues for more (output validation gates, especially).

**Recommendation for DESIGN.md:** add a "compound error / capability-reliability gap" rationale paragraph to §6 (or wherever the rate-limit-resume design lives) citing Rabanser et al. as the academic backing for "we engineer for per-step reliability and recovery, not for raw capability." This is currently implicit in the design; the chapter gives it a citable name.

The **DeepMind cognitive framework** (Burnell et al., 2026 — 10 cognitive faculties: Perception, Generation, Attention, Learning, Memory, Reasoning, Metacognition, Executive Functions, Problem Solving, Social Cognition) is interesting taxonomy but not directly actionable for `agent-runner` — it's a *research framework* for measuring models, not a *design framework* for building harnesses. Note for the record; no DESIGN.md implication.

---

## 4. Vocabulary corrections

Several places where prior reports used a term loosely that this round's reading defines precisely:

| Where in prior report | Loose usage | Precise term from book |
|---|---|---|
| Report 01 §2, multiple | "Core Four" pillars | **Core Five** — the book added Harness as a fifth pillar ([dated 2026-04-12 in chapter 1 index](https://www.jayminwest.com/agentic-engineering-book/1-foundations)). The "Core Four" name persists at agenticengineer.com but the book deliberately extended it. |
| PLAN.md cluster description; this subtask's brief | "AE book chapters 1, 2, 3" framed as Foundations / Models / Prompting | Actual chapter titles are **Foundations** (slug `1-foundations`), **Prompt** (singular, slug `2-prompt`), **Model** (singular, slug `3-model`). Chapters 2 and 3 were swapped in the brief; both are singular nouns in the book. |
| Report 08 §6 | References the "Prompt Maturity Model" only via chapter 9/2 | The same 7-level model appears in **chapter 2/1** (`Prompt Types`) and **chapter 9/2** (`Prompt Maturity Model`) — they are framings of the same framework (chapter 2/1 frames as prompt complexity; chapter 9/2 frames as engineer maturity). Cite both for completeness. |
| Reports 03, 06 (when discussing temperature) | Did not specify temperature setting | Chapter 3/2 establishes that **temperature 0 is the production default** for multi-step workflows because of compound error. `agent-runner`'s inheritance of Claude Code's temp-0 default is now explicitly endorsed by the book, not just convention. |
| Reports 03, 06 (compound-error framing) | "rate limits cascade" / "errors accumulate" | The precise term is **compound error problem** (chapter 3/5). Use that language in DESIGN.md and LESSONS.md going forward. |
| Reports 03, 06, 08 (when discussing reliability vs capability) | Used the two terms interchangeably | Chapter 3/5 establishes them as **independent dimensions** with empirical evidence (Rabanser et al., arXiv:2602.16666). "Capability" = mean task success rate; "reliability" = the four dimensions of consistency, robustness, predictability, safety. They improve at different rates. |

---

## 5. Implications for DESIGN.md (concrete suggested edits)

The diff against DESIGN.md as it stands (per reports 03/06/08) is small but directional:

1. **§Scope philosophy (new footnote or sidebar)** — name the four leverage points `agent-runner` directly addresses (#9 Tools, #10 Prompt, #11 Model, #12 Context per the Twelve Leverage Points hierarchy) and explicitly disclaim the higher-leverage points (#1-#8) as "user's-codebase concerns we don't touch." Cite [`1-foundations/1-twelve-leverage-points`](https://www.jayminwest.com/agentic-engineering-book/1-foundations/1-twelve-leverage-points). [§1.2 above]

2. **§5 (trigger payload assembly)** — note that `agent-runner` is a one-shot harness; the trigger prompt must include explicit stopping conditions and proceed-with-documented-assumption defaults; clarifying-question patterns are unavailable. Reference the chapter 2 index "One-Shot vs. Conversational" framing. [§2.1 above]

3. **§5 — new subsection §5.1 "Prompt-language guidelines"** — codify the four chapter-2/3 rules: (a) declarative phrasing for goals, imperative for workflow steps; (b) Pink Elephant — render `allowed_tools` positively, not `forbidden_tools` negatively; (c) DETAIL framework — specificity is high-value but has diminishing returns past a few constraints; (d) bare imperatives, no hedging. [§2.4 above]

4. **§5 — note** that `agent-runner`'s prompt level is **L4 (Contextual)** per the 7-level model and tag this so contributors know not to bolt on L5+ behaviors without an architectural decision. [§2.2 above]

5. **§5 — new "do not prefix output with the following phrases" block** in the trigger prompt template (the chapter's verbatim 9-phrase forbidden list). [§2.3 above]

6. **§4 (Run JSON schema)** — add `model_id` and `model_version` to the `attempt` record so post-hoc regression analysis after an inner-harness upgrade is possible. [§3.3 above]

7. **§4 (Run JSON schema)** — add a third bucket beyond `success` / `failure`: **`proceeded-with-assumption`** for runs where Claude proceeded but flagged uncertainty (per the chapter 3/2 "systematic caution" profile). [§3.2 above]

8. **§6 (rate-limit-resume rationale)** — add a "compound error / capability-reliability gap" paragraph citing Rabanser et al. (arXiv:2602.16666) as the academic backing for "we engineer for per-step reliability and recovery, not for raw capability." [§3.4 above]

9. **§ (somewhere on configuration knobs)** — note that `agent-runner` does not expose a temperature override; if such an override is added in the future, the default must remain 0 with a clear warning about compound-error degradation. [§3.2 above]

10. **§ (configuration discussion)** — note `AgentConfig.max_turns` should default *low* rather than high, with the compound-error math as the rationale. (Reinforces an implicit decision from report 06 §3.) [§3.4 above]

None of these are code changes (modulo the Run JSON schema additions in #6 and #7); all are documentation tightenings that codify decisions already made or implicit and give them citable rationale.

---

## 6. Net-new contributions (against reports 03/06/08)

The chapters are roughly **70% recap, 30% net-new** when normalized against the four prior AE-book reports. Genuinely new contributions, in order of decision-impact:

1. **Capability-reliability gap (Rabanser et al., arXiv:2602.16666)** — the academic backing for "engineer the harness for reliability dimensions, not capability." [§3.4]
2. **Twelve Leverage Points hierarchy** — gives `agent-runner` a prioritization frame for where it sits in the broader practitioner stack. Identifies the four leverage levels `agent-runner` directly owns (#9-#12). [§1.2]
3. **Anti-Patterns by Leverage Level catalog (dated 2026-04-11)** — two patterns directly applicable: Isolated Prompting (validates the workspace-context-load discipline), Tool Proliferation (validates the single-agent-per-run contract). LESSONS.md candidates listed in §1.3.
4. **Forbidden meta-commentary list** — concrete 9-phrase list to add to the trigger-prompt template. [§2.3]
5. **Compound error math (`p^n`)** — sharper version of the rate-limit / multi-step argument; sharpens `max_turns` default policy. [§3.4]
6. **Temperature compounding** with explicit numbers — endorses `agent-runner`'s inheritance of Claude Code's temp-0 default and argues against ever exposing a knob. [§3.2]
7. **One-shot vs. Conversational distinction** — names the categorical constraint `agent-runner` operates under and the design implications (no clarifying-questions, must include stopping conditions). [§2.1]
8. **Spotify-style regression criterion** ("upgrade if >5% better and <2% breakage; defer if >5% breakage") — vocabulary for a future eval-harness add-on. [§3.3]
9. **Pink Elephant problem** — argues for reframing `forbidden_tools` rendering as `allowed_tools` listing in the trigger-prompt template. [§2.4]
10. **Declarative-vs-imperative split** with SatLM 23% lift — concrete prompt-language rule for the trigger template. [§2.4]
11. **Claude-specific "systematic caution" behavioral profile** — informs the third Run JSON state `proceeded-with-assumption`. [§3.2]

Items not in this list (e.g., the autoresearch / SLM-training pathway, the DeepMind cognitive framework, the Level 7 bulk-update coordination pattern, the Capability-Gated Access Tiers around Claude Mythos Preview) are interesting but do not drive any `agent-runner` decision.

---

## 7. Out-of-scope content noted but skipped

Per the PLAN.md scope guardrail (multi-agent / orchestration / software-factory material is in a sister repo), the following subchapter was deliberately not body-fetched:

- **`3-model/4-multi-model-architectures`** — orchestrator patterns, cascades, routing strategies, planning-vs-execution separation across multiple models. ⏭️ Multi-model orchestration is multi-agent territory.

The following passages within fetched subchapters were noted but skipped:

- **Chapter 2/1 §"Level 7 Meta-Cognitive — Bulk-Update Coordination"** (parallel delegation of Level 6 improvements via lightweight models). ⏭️
- **Chapter 3/1 §"When to Train Your Own" (autoresearch / overnight SLM training)** (Karpathy 2026-03-06; Lütke/Shopify 2026-03-10). Out of scope for an execution-layer harness; this is for teams owning model training infrastructure.
- **Chapter 3/2 §"Multi-Model Orchestration Patterns"**. ⏭️
- **Chapter 3/5 §"DeepMind Cognitive Framework"** — interesting research taxonomy, but operates at the level of measuring models, not designing harnesses; not actionable for `agent-runner`.

The chapter index pages for chapter 2 and chapter 3 are short overview blurbs (10-22 KB) compared to chapter 1's body-content-rich index (16 KB with substantial framework material). For chapters 2 and 3, the operative content is in the subchapters; the index pages are mostly cross-references.

---

## Sources reviewed

| Source URL | Status | Notes |
|---|---|---|
| https://www.jayminwest.com/agentic-engineering-book/1-foundations | ✅ | Index page with 5-pillar framework body content + dated 2026-04-12 "why Harness" rationale + Agent Psychometrics arXiv:2604.00594 citation. Informed §1.1. |
| https://www.jayminwest.com/agentic-engineering-book/2-models | ❌ silent 404 | URL probe (issue #22) returned HTTP 200 but only the SPA navigation skeleton — the real chapter 2 slug is `2-prompt`. Recorded as evidence of the slug-paraphrase trap (Round 3 + Round 4 + this round's third instance). |
| https://www.jayminwest.com/agentic-engineering-book/3-prompting | ❌ silent 404 | Same as `2-models` above — real chapter 3 slug is `3-model`. SPA returns nav-only skeleton. |
| https://www.jayminwest.com/agentic-engineering-book/1-foundations/1-twelve-leverage-points | ✅ | Twelve Leverage Points hierarchy + dated 2026-04-11 Anti-Patterns by Leverage Level catalog (7 named patterns from Liu/Hamel/Willison). Informed §1.2 + §1.3. The single load-bearing source for the report. |
| https://www.jayminwest.com/agentic-engineering-book/2-prompt | ✅ | Chapter index with One-Shot vs. Conversational distinction, prompt-model contract, four prompt-engineering principles. Informed §2.1. |
| https://www.jayminwest.com/agentic-engineering-book/2-prompt/1-prompt-types | ✅ | 7-level prompt maturity model (recap of chapter 9/2 from report 08); Conservative Update Rules (PRESERVE/APPEND/DATE/REMOVE); Bulk-Update Coordination (⏭️). Informed §2.2. |
| https://www.jayminwest.com/agentic-engineering-book/2-prompt/2-structuring | ✅ | Canonical 7-section structure; verbatim Forbidden Meta-Commentary 9-phrase list; Output Styles as Behavioral Toggles. Informed §2.3. |
| https://www.jayminwest.com/agentic-engineering-book/2-prompt/3-language | ✅ | Declarative vs Imperative + SatLM (arxiv:2305.09656) 23% lift; Pink Elephant problem (InstructGPT); DETAIL framework (arxiv:2512.02246); ~21-word optimal length; bare imperatives. Informed §2.4. |
| https://www.jayminwest.com/agentic-engineering-book/3-model | ✅ | Chapter index with frontier-default rule + access-tier-vs-capability-tier framing + cross-provider selection. Informed §3.1. |
| https://www.jayminwest.com/agentic-engineering-book/3-model/1-model-selection | ✅ | "Default to frontier; downgrade only with evidence" + Mythos Preview gap evidence + autoresearch/SLM pathway (⏭️). Informed §3.1. |
| https://www.jayminwest.com/agentic-engineering-book/3-model/2-model-behavior | ✅ | Temperature compounding (0.95^10 ≈ 0.60 table); Claude "systematic caution" agentic behavioral profile; AgentArch arXiv:2509.10769 architecture sensitivity. Informed §3.2. |
| https://www.jayminwest.com/agentic-engineering-book/3-model/3-model-limitations | ✅ | Six limitation classes (math, hallucination, context window 40-60% threshold, instruction drift, tool use, version stability); explicit version pinning pattern; Spotify regression criterion (>5% better / <2% breakage). Informed §3.3. |
| https://www.jayminwest.com/agentic-engineering-book/3-model/5-model-evaluation | ✅ | Compound error problem table (p^n); capability-reliability gap (Rabanser et al., arXiv:2602.16666 — Princeton 2026); DeepMind cognitive framework (10 faculties — noted but not actionable). Informed §3.4. |
| https://www.jayminwest.com/agentic-engineering-book/3-model/4-multi-model-architectures | ⏭️ | Skipped per scope guardrail (multi-model = multi-agent territory). |

**Sources status summary:** 11 ✅ / 0 🟡 / 2 ❌ (silent 404 from slug-guess) / 1 ⏭️ (out-of-scope)
