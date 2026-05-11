# Report 08 — AE book chapters 4 (Context), 5 (Tool Use), and chapter 9-10 unread subchapters

**Date:** 2026-05-11
**Author:** Subagent dispatch (run_id: 20260511-r4, sub-01)
**Status:** ✅ complete

## Lead question

Which execution-layer ideas in AE book chapters 4 (Context), 5 (Tool Use), and the remaining 9-10 subchapters not covered by reports 01, 03, or 06 should reshape `agent-runner`'s DESIGN.md or roadmap, after explicitly excluding the multi-agent / orchestration material that PLAN.md's scope guardrail rules out?

## Orientation: what the cluster turned out to be

The PLAN.md cluster description hedged on chapter 5's title and on chapter 9-10 contents, so this round opened with index probes (issue #19 fetching the four chapter index pages) before dispatching the body fetch (issue #20 fetching 20 verified subchapter URLs). Two surprises landed early:

1. **Chapter 5's slug is `5-tool-use`, not `5-tools`.** The book's chapter 5 is titled "Tool Use" (the index sidebar even labels chapter 6 as "Patterns" and chapter 7 as "Practices" — that label drift is a sidebar-rendering artifact, not a structural change; the URL slugs `6-harnesses`, `7-patterns`, `8-practices` confirmed in report 03/06 still hold). A naive guess at `5-tools` would have produced the Round 3 bad-slug failure mode again. The probe step paid for itself.
2. **Chapter 9 is "Mental Models" and chapter 10 is "Practitioner Toolkit"** — confirmed via the chapter-9 and chapter-10 index pages. Report 01 had already discovered these names by reading single subchapters (9/7-software-factories and 10/5-multi-agent-workspace-managers respectively); this round enumerated the rest.

After scope filtering (multi-agent / orchestration material excluded per PLAN.md guardrail; non-Claude tooling deferred), the **in-scope reading list** was:

- Chapter 4 (Context): `1-context-fundamentals`, `2-context-strategies`, `3-context-patterns`, `5-context-management-architectures`, `6-context-at-codebase-scale` (`4-multi-agent-context` skipped)
- Chapter 5 (Tool Use): `1-tool-design`, `2-tool-selection`, `3-tool-restrictions`, `4-scaling-tools`, `5-skills-and-meta-tools` plus the chapter index
- Chapter 9 (Mental Models): `1-pit-of-success`, `2-prompt-maturity-model`, `3-specs-as-source-code`, `4-context-as-code`, `5-execution-topologies` (selectively — single-agent dimensions only), `6-design-as-bottleneck` (selectively — Models 1-3 only; Models 4-5 are factory-floor multi-agent)
- Chapter 10 (Practitioner Toolkit): `1-claude-code` (heavy — this chapter directly documents our inner harness), `3-ide-integrations` (lightly — context for "what alternatives are practitioners using"), `6-enterprise-context-tools` (selectively — Pattern-to-Tool mapping, ignoring multi-repo enterprise-only content)

`agent-runner`'s position in the resulting taxonomy is unchanged from reports 03 and 06: outer-harness on top of Claude Code (inner harness), CI substrate (GitHub Actions), Solo tier (1-5 concurrent agents per repo), single agent per CI run. Every section below is read through that lens.

---

## 1. Chapter 4 (Context): the seam `agent-runner` actually owns is "what fills the inner harness's context window"

Round 2's report 03 §1 noted that *Context management* (component 4 of Raschka's six-component harness stack) is the inner harness's responsibility — Claude Code's auto-compact handles it, `agent-runner` doesn't. Chapter 4 sharpens this: Claude Code owns the *mechanism* of compaction, but `agent-runner` owns the *composition* of what enters the context window in the first place. The two are different problems.

The chapter's load-bearing claims for our layer:

### 1.1 The capability-capacity model and the 40% threshold

From [`4-context/1-context-fundamentals`](https://www.jayminwest.com/agentic-engineering-book/4-context/1-context-fundamentals):

> *"Observable patterns suggest context utilization above 40% correlates with early signs of capability degradation, though the precise relationship between context usage and capability remains uncharacterized... Production deployments observing quality degradation typically find agents operating above 60% capacity."*

And from [`4-context/2-context-strategies`](https://www.jayminwest.com/agentic-engineering-book/4-context/2-context-strategies):

> *"GSD project (12K-star open source tool) treats context window as a non-renewable resource with explicit quality relationship: **Quality ∝ 1/(% context used)**. ... Their mitigation: each plan execution gets fresh 200K context window, sized to remain <50% utilized."*

For `agent-runner` this is sharper guidance than report 06 §3.2's "smart zone" framing (40-60% high-quality context window). The implications are:

- **`max_turns` budgeting at the AgentConfig level should target an *expected* peak utilization, not just an absolute turn cap.** A workflow that issues many file reads, large grep results, or wide bash output will hit the 60% threshold faster than one that doesn't. We can't measure utilization directly from outside Claude Code — the threshold is enforced by the wrapper observing stream-json events for `tokens_used` accumulation.
- **The Claude Code 2.1.9+ "real-time context utilization percentage" feature** (the chapter cites the `[45K/200K tokens] 22%` display) is exposed as a stream-json event that our wrapper can consume directly. **Implication for DESIGN.md §4 (Run JSON):** add a `peak_context_pct: float` field per attempt, populated from the highest `context_pct` observed during the run. Combined with the §9 evaluation metric of P95/P99 token consumption (report 06 §9), this gives us the quality-risk dimension report 03 §6.2 was missing.

### 1.2 "Context as payload, not log" — direct guidance for trigger-prompt assembly

From [`4-context/3-context-patterns`](https://www.jayminwest.com/agentic-engineering-book/4-context/3-context-patterns):

> *"The default mental model (accumulation): User message → append. Tool result → append. Agent response → append. Context fills until you hit limits.*
> *Context loading mental model: For this specific call: Load: base config (always); Load: project context (if relevant); Load: tool definitions (only what this agent needs); Load: query (the specific task); Load: retrieved facts (verified, not raw); Nothing else."*

This is a direct framing for the trigger prompt `agent-runner` constructs. Today's draft trigger framing (from DESIGN.md §5 and report 03 §4) treats the prompt as `<system> + CLAUDE.md + <trigger payload>`, where trigger payload is the issue body, PR diff URL, and trigger metadata wrapped in `<trigger>...</trigger>`. The chapter's "payload" framing argues this is the right shape — but adds a discipline: **only what this run needs, not "everything that might be relevant."**

The flip side: the chapter calls out **accumulation working better for "long-running sessions where recomputing context is expensive."** `agent-runner`'s sessions are CI-ephemeral (seconds-to-minutes), so we are explicitly in the "load not accumulate" regime. We will never benefit from a session-history-replay model.

**Implication for DESIGN.md §5 (run.py / prompt assembly):** the trigger payload should include only the directly task-relevant content (issue body, the *specific* PR diff or specific file under review — not a dump of "all recent commits"). When a workflow needs accumulated state from a prior attempt of the same trigger, that should be encoded explicitly as the "outcome summary" field already proposed in report 06 §3.1 (`attempt_summaries: list[str]`), not as a free-form log replay.

### 1.3 ACE (Agentic Context Engineering): a contradicting voice we explicitly do NOT adopt

From the same `3-context-patterns` chapter, the Stanford/SambaNova ACE framework argues *"contexts should grow — comprehensive evolving playbooks outperform compressed prompts in complex domains"* — opposite to the "load not accumulate" guidance just adopted. The chapter resolves the contradiction:

> *"Frequent Intentional Compaction: Compress proactively at 40-60% — Use For: General-purpose coding, bounded tasks.*
> *ACE (Growing Contexts): Expand deliberately with learned patterns — Use For: Knowledge-intensive domains, tool-heavy tasks."*

`agent-runner`'s workflows are bounded coding tasks under CI, not knowledge-intensive long-horizon work. ACE is the right pattern for a different layer (an agent that lives in a single repo and accumulates project-specific knowledge across hundreds of runs), but that lives in our LESSONS.md (per report 06 §10 / chapter 8/6 Knowledge Evolution), not in the per-run prompt context. **This round confirms LESSONS.md should adopt the ACE structured-bullet format (`[ID] helpful=N harmful=M :: assertion`) introduced in §3 below — but the per-run context stays minimal.**

### 1.4 Active context management architectures — read for context, not adopted

[`4-context/5-context-management-architectures`](https://www.jayminwest.com/agentic-engineering-book/4-context/5-context-management-architectures) surveys three points on the design spectrum: passive accumulation (the default — what Claude Code does), LCM (Lossless Context Management — Voltropy/Volt; PostgreSQL-backed immutable store with summary DAG and `lcm_grep`/`lcm_expand` tools), and Sapling (continuous curation; in-memory five-stage pipeline targeting 50-60% steady utilization).

For `agent-runner`:

- **Both LCM and Sapling are inner-harness replacements, not outer-harness additions.** They replace Claude Code's compaction layer wholesale. We don't get to mix-and-match — if a future Claude Code version adopts Sapling-like inter-turn curation natively, we benefit; if not, this is not a knob we own.
- **The chapter's framing-level claim is the takeaway for us:** *"the engine should manage context, not the model. ... The model focuses on reasoning; the engine handles memory management."* This reinforces the report 03 §1 component-4 conclusion: don't try to manage context at the outer layer — that battle is fought by the inner harness, and we'd just be adding a third compaction layer that fights the other two. The right move at our layer is to keep the *input* to that layer minimal (§1.2 above).

The one operational borrow worth noting: Sapling's **commitment-tracking** behavior (extracting "I will edit foo.ts" from assistant messages, flagging unfulfilled commitments in the next turn) is structurally similar to the `attempt_summaries` field already proposed in report 06 §3.1. If/when our wrapper grows a stream-json post-processor for resume semantics, the "what did the agent commit to that it didn't finish" extraction is a useful signal for the next-attempt prompt.

### 1.5 Context at codebase scale — direct guidance for AgentConfig in large user repos

[`4-context/6-context-at-codebase-scale`](https://www.jayminwest.com/agentic-engineering-book/4-context/6-context-at-codebase-scale) is a pattern catalog for brownfield codebases. The chapter's framing is direct:

> *"Brownfield context management is archaeological fieldwork, not search. ... The relevant context for an agent is rarely the code itself. It is the constraint behind the code — the PCI requirement that forced that data flow, the performance incident that caused that denormalization, the deprecated library that couldn't be removed."*

The seven patterns (Semantic Indexing, Hierarchical Convention Files, ADRs, Dependency-Graph Queries, Progressive Codebase Disclosure, Tribal Knowledge Codification, Graduated Adoption) are mostly user-repo-side concerns — the user adopting `agent-runner` does this work in their own repo. But two implications land at our layer:

- **AgentConfig should have a documented escape hatch for brownfield-context tools.** When a user has built a Serena MCP server, an Augment Context Engine, or a custom Qdrant+tree-sitter `codebase_search` MCP for their repo, our AgentConfig schema should make it trivial to wire that MCP in for a given workflow. Today that's implicit in `allowed_tools` — should be documented in DESIGN.md §11 with an example.
- **Hierarchical Convention Files (Pattern 2) are auto-discovered by Claude Code itself.** The chapter notes Claude Code natively loads `services/payments/CLAUDE.md` when operating in that subtree — `agent-runner` does not need to do anything for this to work. **Implication for DESIGN.md §5:** explicitly note that we do not project-flatten the user's `CLAUDE.md` into a single prompt; we let Claude Code's hierarchical-loading discover module-level files. This avoids breaking the inner harness's design.
- **The five-stage Graduated Adoption framework (Encoding → Documenting → Consolidating → Specializing → Enforcing)** maps onto how `agent-runner` itself should be deployed inside any individual user repo. Stage 1 (Encoding) is the user authoring their first AgentConfig and slash-command-equivalent workflow; Stage 5 (Enforcing) is hooks running tests before each merge. This is good narrative for the eventual user-facing onboarding doc, not for DESIGN.md proper.

---

## 2. Chapter 5 (Tool Use): the AgentConfig.allowed_tools whitelist is doing more work than DESIGN.md §2 currently shows

The chapter's load-bearing principle for our layer comes from [`5-tool-use/3-tool-restrictions`](https://www.jayminwest.com/agentic-engineering-book/5-tool-use/3-tool-restrictions):

> *"In multi-agent systems, tool restrictions aren't just about capability — they're security boundaries. Treat tool access like production IAM: deny-all by default, allowlist only what each subagent needs."*

This is the same conclusion report 03 §1 reached from the chapter-6 harness-stack tool-access-component framing, and the same conclusion report 06 §7 reached from the chapter-7/7 progressive-disclosure framing. **Chapter 5/3 makes it explicit operational doctrine.** The implications for our AgentConfig schema:

### 2.1 The role-tool table is directly importable

The chapter gives a **canonical role-to-tool mapping** that maps cleanly onto AgentConfig presets:

| Role | Tools | Rationale |
|---|---|---|
| Reviewer/Analyzer | Read, Grep, Glob | Read-only; can't accidentally modify files |
| Test Runner | Bash, Read, Grep | Execute tests and read results; no file editing |
| Builder/Implementer | Read, Edit, Write, Grep, Glob | Full modification access for implementation |
| Orchestrator | Task, Read, Glob | Routes work, has minimal direct access |
| Scout/Explorer | Read, Grep, Glob, WebFetch | Discovery only, no modification |

For `agent-runner` v1 (single-agent-per-run, no orchestrator role) the relevant rows are Reviewer (for the PR-comment-on-issue trigger), Test Runner (for the verify-on-CI trigger), and Builder (for the actual implement-this-feature trigger). **Implication for DESIGN.md §2 (AgentConfig schema):** ship these three as named presets (`role: "reviewer" | "test-runner" | "builder"`) that select default `allowed_tools` lists; user can override but doesn't have to specify by hand.

### 2.2 MCP tool naming convention — verbatim borrow

From the same chapter:

> *"Naming Convention: `mcp__<server>__<tool>` — Double underscores separate the three components ... Examples: `mcp__playwright__browser_navigate`, `mcp__supabase__execute_sql`, `mcp__kotadb__search_code`."*

This is exactly the convention `mcp__github__issue_write`-style that we already use in our skills. No change needed; just document in DESIGN.md §11 that this is canonical and stable.

### 2.3 Wildcard patterns and the line-continuation footgun

[`5-tool-use/3-tool-restrictions`](https://www.jayminwest.com/agentic-engineering-book/5-tool-use/3-tool-restrictions) documents Claude Code 2.1.0's wildcard support and 2.1.6-2.1.7's security fixes:

- Wildcards like `Bash(npm *)` work but expand the permission surface; prefer specific patterns.
- **Line-continuation injection was a real vulnerability:** `Bash(git add)` allowed could be bypassed by `git add \\\n && rm -rf /`. Fixed in Claude Code 2.1.7 (validates across line continuations).
- **Glob expansion can escape intended scope** for destructive operations.

For `agent-runner` workflows, the operational discipline is:

- **Pin the inner Claude Code version explicitly per workflow** (or at least floor it at ≥2.1.7) — older versions have the line-continuation footgun. Already de-facto true if we're tracking latest, but worth a defensive minimum-version assertion in the workflow setup step.
- **Avoid `Bash(*)` in any AgentConfig.** Equivalent to `--dangerously-skip-permissions` for shell. Always specify either an exact-match list or a narrow wildcard like `Bash(pytest *)`.

**Implication for DESIGN.md §11 (security):** add a workflow setup step that asserts `claude --version >= 2.1.7`; document that AgentConfig `allowed_tools` MUST NOT contain `Bash(*)` and SHOULD prefer exact matches over wildcards.

### 2.4 Sandbox vs. permissions — independent layers

A sharp distinction from [`10-practitioner-toolkit/1-claude-code`](https://www.jayminwest.com/agentic-engineering-book/10-practitioner-toolkit/1-claude-code) (cross-cited from chapter 5):

> *"Using `--dangerously-skip-permissions` does NOT disable sandboxing. You can run Claude Code unattended with the flag, and sandbox restrictions still apply at the OS level."*

For our CI workflows this is operationally important. We routinely run with `--dangerously-skip-permissions` (CI is non-interactive — there's no human to approve prompts). The chapter confirms this is safe **provided sandbox mode is on** (bubblewrap on Linux; the GitHub Actions runner is itself a containerized environment so the sandbox-as-OS-isolation property holds for free). **Implication for DESIGN.md §11:** document the defense-in-depth claim explicitly — `--dangerously-skip-permissions` + GitHub Actions runner isolation + workflow `permissions:` block scoping = three independent layers, none of which is removed by the flag.

### 2.5 Tool design and selection — the Coding Agent Edit Formats finding

[`5-tool-use/1-tool-design`](https://www.jayminwest.com/agentic-engineering-book/5-tool-use/1-tool-design) §"Coding Agent Edit Formats" gives Aider's production-tested format-by-model table:

| Model Family | Recommended Format | Reason |
|---|---|---|
| Most modern models (Claude, GPT-4o, Gemini 1.5+) | Search-replace (`diff`) | Reliable exact-match application; balanced output size |
| GPT-4 Turbo | `udiff` | Mitigated "lazy coding" |
| Gemini (older) | `diff-fenced` | Standard fencing failed consistently |

This is mostly irrelevant to `agent-runner` because Claude Code owns the edit-format choice for its own Edit/Write tool calls. The borrow is at the *principle* level: **format choice is a tool design decision that affects model reliability** — when our workflows produce wrong edits, audit the inner-harness edit format before adjusting prompts. We don't expose this knob.

The same chapter also names the **"Coding Agent Tool Inventory"** baseline (Raschka, 2026-04):

> *"Minimum viable set for most coding tasks: `read_file`, `write_file`, `bash`, `search`."*

This is the same set as the Builder preset in §2.1 above, modulo `search`/`grep` naming. **Adopted as the v1 default for AgentConfig.role: "builder".**

### 2.6 Skills as meta-tools — clarifies our own skills' status

[`5-tool-use/5-skills-and-meta-tools`](https://www.jayminwest.com/agentic-engineering-book/5-tool-use/5-skills-and-meta-tools) frames Skills as a **third category beyond tools and prompts**:

> *"Tools: What the agent can do (read files, make API calls). Prompts: How the agent thinks (general reasoning patterns). Skills: Domain-specific thinking modes (temporary reasoning specialization)."*

The cost framing matters: *"Traditional Tools: ~100 tokens per invocation. Skills: ~1,500+ tokens per invocation."*

For `agent-runner`'s own skill ecosystem (`.claude/skills/`), the implication is that skills carry a real per-invocation token cost that should be weighed against bake-into-prompt for high-frequency operations. The skills we already have (`fetch-blocked-urls`, `research-pipeline`, `parallel-subagent-fanout`, etc.) are correctly scoped — they're sometimes-invoked specialized procedures, not always-loaded boilerplate.

**Implication for our skills convention (not DESIGN.md):** when a skill description starts feeling like it should be in CLAUDE.md instead, that's a sign the activation is too frequent and the token cost is no longer winning over baking it in.

The chapter's **"Context Contracts for Agent Capability Declaration"** sub-section describes a JSON-schema-frontmatter pattern with declared `inputs` (required spec_file, expertise, memory) and `outputs` (`allowed_modifications` globs, `forbidden_patterns`). The three validation gates (pre-spawn validation, scope enforcement via hooks, registry generation) are an interesting future direction for AgentConfig — declarative `outputs.allowed_modifications` would let our workflow's CI step grep PRs for files-touched-outside-the-declared-scope without parsing the agent transcript. **Roadmap candidate, not v1.**

---

## 3. Chapter 9 mental models — three single-agent-applicable models worth importing

Chapter 9 has seven subchapters; report 01 already covered §7 (Software Factories — Shapiro framework, multi-agent scope). Of the remaining six, three are directly applicable to `agent-runner`'s single-agent CI execution layer; three are partially applicable.

### 3.1 §9/1 Pit of Success — the framing for prompt assembly

[`9-mental-models/1-pit-of-success`](https://www.jayminwest.com/agentic-engineering-book/9-mental-models/1-pit-of-success) reframes prompt engineering as probability-distribution shaping:

> *"Shape the input tokens so the most probable output tokens are the correct ones. ... The context window isn't just 'information for the model' — it's the gravitational field that pulls outputs toward certain regions of possibility space."*

The operational guidance this distills to:

> *"Position information by importance: System-level identity and constraints → beginning (establishes frame). Task-specific context and data → middle (bulk of working memory). Specific instruction and format → end (highest attention, immediate priming)."*

This is the same conclusion report 06 §8's Common-Failure-Mode "Context Overflow" reached (*"Move critical instructions to end of prompt — recency bias"*) and the same conclusion the existing DESIGN.md §5 trigger-payload-at-end ordering already encodes. This chapter is the framing-level version of why; report 06 §8 is the operational form. No new implication beyond what report 06 already proposed.

The "eliminate competing attractors" sub-rule does add one new discipline:

> *"Don't provide examples of things you don't want (they become attractors). Don't hedge instructions ('maybe do X or possibly Y'). Don't include irrelevant context that could prime wrong directions."*

For `agent-runner`'s prompt-assembly conventions: the trigger payload should not include "here are examples of things to avoid" inline — those become attractors. Anti-pattern guidance belongs in CLAUDE.md or LESSONS.md, where it's part of the always-loaded prefix and gets cached, not in the dynamic per-run trigger.

### 3.2 §9/2 Prompt Maturity Model — calibrates where our slash-command equivalents should live

[`9-mental-models/2-prompt-maturity-model`](https://www.jayminwest.com/agentic-engineering-book/9-mental-models/2-prompt-maturity-model) defines seven prompt levels (Static / Parameterized / Conditional / Contextual / Higher-Order / Self-Modifying / Meta-Cognitive) and counsels:

> *"Start at the lowest level that solves the problem. ... Most systems should have a pyramid distribution: Many Level 1-2 commands (foundation), Some Level 3-4 commands (core workflows), Few Level 5 commands (orchestration), Rare Level 6-7 commands (if any)."*

For `agent-runner`, the equivalent of "commands" is **AgentConfig workflows**. Mapping our existing/planned workflows onto the maturity scale:

| Workflow | Maturity Level | Why |
|---|---|---|
| `verify-pr-on-trigger` (run tests on agent's PR commit; report 06 §5) | Level 1-2 (Static / Parameterized) | Same logic per trigger; only the PR ref varies |
| `respond-to-issue-comment` (parse comment, dispatch agent with comment-as-trigger) | Level 3 (Conditional) | Branches on comment content / role / file mention |
| `pr-review-with-agentconfig` (load AgentConfig, materialize trigger payload, invoke claude -p) | Level 4 (Contextual) | Reads CLAUDE.md, AgentConfig, repo state before acting |
| Stage-2 multi-step workflows | Level 5 (Higher-Order) | Out of scope for v1 per report 06 §2 (Quick Flow / Standard only) |
| `LESSONS.md` self-update | Level 6 (Self-Modifying) | Out of scope — human-curated only per report 06 §10 |
| Cross-AgentConfig optimization | Level 7 (Meta-Cognitive) | Out of scope — would only matter at >10 AgentConfigs |

**Implication for DESIGN.md §10 (roadmap):** v1 ships only Level 1-4 workflows; Level 5+ is deferred. The chapter's pyramid principle is the discipline — don't reach for higher maturity until the lower levels are saturated.

The chapter's **Engineer Leverage Progression** (Search-Engine framing → Integrated Workflow framing → System Designer framing) is a useful frame for how `agent-runner` itself should evolve: v1 is solidly Stage 2 (Integrated Workflow — trigger feeds into agent feeds into PR), and the LESSONS.md + evaluation metrics from report 06 §9 are the seam by which we eventually move into Stage 3 (System Designer with feedback loops). Not a v1 implication; a roadmap framing.

### 3.3 §9/3 Specs as Source Code — directly governs how we write workflow definitions

[`9-mental-models/3-specs-as-source-code`](https://www.jayminwest.com/agentic-engineering-book/9-mental-models/3-specs-as-source-code) (Sean Grove's mental model):

> *"Throwing away prompts after generating code is like checking in compiled binaries while discarding source. ... Specs are the truth. Generated code is secondary (can be regenerated). Specs are machine-readable and executable (by agents)."*

For `agent-runner`'s artifact taxonomy:

- **AgentConfig YAML files ARE source code.** Already version-controlled per repo convention.
- **Workflow YAML files ARE source code.** Already version-controlled.
- **The trigger framing template (the `<trigger>...</trigger>` wrapper from report 03 §4) IS source code.** Should live in a `prompts/` or `templates/` directory in the user's repo, version-controlled, not embedded in the workflow YAML as a heredoc.
- **DESIGN.md and LESSONS.md ARE source code** for `agent-runner`'s own behavior. Already conventional.

The chapter's **GSD project example** (cited from `2026-02-06`) is the direct analogue: *"PLAN.md files are not transformed into prompts, they ARE the prompts. The executor reads them verbatim. ... GSD uses semantic XML within markdown (`<action>`, `<verify>`, `<done>`) for Claude comprehension."* This is structurally identical to what `agent-runner` is converging on with the `<trigger>...</trigger>` wrapper — and the `<verify>` tag suggestion maps directly onto the `verify:` command field proposed in report 06 §5/§12. **Worth adopting the structured-XML-within-markdown convention for AgentConfig's prompt-template fields.**

**Implication for DESIGN.md §2 (AgentConfig schema):** add a `prompt_template_path: str` field pointing at a versioned prompt file in the user's repo (not inlined in the AgentConfig YAML). The template file uses the structured-XML-within-markdown pattern and is the single source of truth for the per-run prompt — code review of that file IS the review of the workflow's behavior.

### 3.4 §9/4 Context as Code — directly governs LESSONS.md format

[`9-mental-models/4-context-as-code`](https://www.jayminwest.com/agentic-engineering-book/9-mental-models/4-context-as-code) extends specs-as-source to all knowledge artifacts:

> *"Knowledge artifacts are source code. Version control them, test them, refactor them, and document them with the same rigor you apply to Python or JavaScript."*

The chapter's **ACE playbook format** is the structural template:

> *"`[str-00001] helpful=5 harmful=0 :: Use structured output for complex tasks` ... Each line is: Uniquely identified ([prefix-ID]) — enables precise references; Performance tested (helpful=X harmful=Y) — like unit tests for knowledge; Category-organized (str-, cal-, mis-, con-, too-) — modular design; Self-describing."*

Report 06 §10 already proposed LESSONS.md should adopt the chapter-8/6 PRESERVE/APPEND/DATE/REMOVE curation contract with `*[YYYY-MM-DD]*:` timestamps. **This chapter sharpens that:** the *line-level structure* should also adopt the `[prefix-ID] helpful=N harmful=M :: assertion` format. Concretely:

```
[res-00001] helpful=3 harmful=0 *[2026-05-11]*:: State persists in commits, not context windows.
[ver-00002] helpful=2 harmful=0 *[2026-05-11]*:: Prefer binary, localized feedback signals over interpretive ones.
[ctx-00003] helpful=1 harmful=0 *[2026-05-11]*:: Context utilization >40% correlates with capability degradation; design for <50% peak.
```

The category prefixes for `agent-runner` map onto our domains: `res-` (resume semantics), `ver-` (verification), `ctx-` (context management), `tri-` (trigger framing), `oau-` (OAuth/auth), `gat-` (gates / human-in-the-loop), `obs-` (observability), `mcp-` (MCP / tool integration), `sec-` (security).

The helpful/harmful counters become operationally meaningful when LESSONS.md drives prompt-assembly choices: when we eventually decide "include this lesson in the trigger context for runs of type X," we can track whether runs that included it succeeded more often than runs that didn't. v1 may carry zero counters; the format reserves the column.

**Implication for repo conventions (not DESIGN.md proper):** when LESSONS.md is created, its line format adopts `[<prefix-NNNNN>] helpful=N harmful=M *[YYYY-MM-DD]*:: <assertion>`. Categories named above. Counters maintained manually by the human curator until evaluation infrastructure (report 06 §9) lands and can update them automatically.

### 3.5 §9/5 Execution Topologies — single-agent slice only

[`9-mental-models/5-execution-topologies`](https://www.jayminwest.com/agentic-engineering-book/9-mental-models/5-execution-topologies) names five topologies (Parallel / Sequential / Synthesis / Nested / Persistent). For `agent-runner` v1's single-agent-per-run model, **only Sequential and Persistent apply**:

- **Sequential** is what every CI run already is — phases (checkout → AgentConfig load → claude -p invocation → verify → PR-comment) execute in strict order. The chapter's measurement indicators (phase count, phase success rate, rework rate) are operational metrics worth tracking — they overlap with report 06 §9's starter metrics but add the "phase success rate" dimension that we don't yet capture.
- **Persistent** is what `agent-runner` enables across multiple CI runs: state persists in artifacts (the user's repo, the `agent-runner`-managed branches, the Run JSON in `state/`). The chapter's measurement indicators (session count contributing to expertise, expertise growth rate, pattern reuse rate) map onto LESSONS.md curation cadence.

Parallel, Synthesis, and Nested are multi-agent topologies — **out of scope** per PLAN.md guardrail.

The chapter's **Four Improvement Vectors** (Wider / Deeper / Thicker / Less Friction) are useful as a framing for "how does `agent-runner` improve over time":

| Vector | What "improvement" means at our layer | Today | Direction |
|---|---|---|---|
| Wider (more parallel branches) | Concurrent CI runs across triggers | 1 per trigger | Out of scope (per-trigger serial) |
| Deeper (longer autonomous chains) | More turns within a run before max_turns | bounded by AgentConfig | Cap stays bounded; trust is the gate |
| Thicker (more tool invocations) | Tools the agent can productively use per workflow | small whitelist | Grows as MCP servers are added |
| Less Friction (fewer human checkpoints) | Promotion from PR-review-required to auto-merge | All workflows PR-required | Per report 06 §6 establish-precedent gate |

The **Trust Gradient** table from this chapter (Low / Medium / High trust → Width / Depth / Thickness / Friction settings) is a useful framing for the `is_autonomous` field already proposed in report 06 §6 — *"Trust increases through demonstrated reliability: Low friction runs accumulate without failure; Quality metrics remain stable as autonomy increases; Edge cases handled gracefully without escalation."* No new implication; reinforces the report-06 proposal.

### 3.6 §9/6 Design as Bottleneck — Models 1-3 apply, Models 4-5 don't

[`9-mental-models/6-design-as-bottleneck`](https://www.jayminwest.com/agentic-engineering-book/9-mental-models/6-design-as-bottleneck) presents five mental models. The first three apply to `agent-runner`'s single-agent layer:

**Model 1 (Design as Bottleneck):** *"When implementation is automated, design becomes the constraint."* For `agent-runner` specifically, this argues **the AgentConfig + prompt template is the high-leverage artifact**, not the wrapper code. Investing engineering hours in better trigger framing, better AgentConfig presets, and better verify commands has higher ROI than investing the same hours in wrapper-internals refactoring. (The corollary: when a workflow is producing bad runs, audit the AgentConfig and prompt before audit the wrapper.)

**Model 2 (Agents as Pistons):** *"If there is work on your hook, you must run it. ... The hook IS the assignment. Execution is immediate. Completion is the only signal."* This is structurally identical to how `agent-runner` already operates: the GitHub trigger event IS the assignment, the wrapper invokes `claude -p` immediately (no negotiation), and the run produces a single completion artifact (Run JSON + PR/comment). The chapter validates the design choice we already made; no new implication, but it's worth noting in DESIGN.md §10 as a design-rationale reference.

**Model 3 (Persistent Identity, Ephemeral Execution):** *"Agents are like employees — permanent identity, but each workday is fresh."* For `agent-runner`'s topology:

- **Persistent identity** lives in the AgentConfig file (name, role, tool whitelist, model preference, verify command, prompt template path) plus the LESSONS.md accumulated track record.
- **Ephemeral execution** is each `claude -p` invocation — fresh context, fresh tools, dies with the job.
- **Seancing** (the chapter's term for "querying past session records for decisions and rationale") maps onto the wrapper reading `git log` and prior-attempt Run JSONs at the start of a resumed run (already proposed in report 06 §3.1). The `attempt_summaries: list[str]` field IS the seancing artifact.

The chapter's **CV-style identity schema** is over-engineered for our single-agent model, but the underlying structure is right. **Implication for DESIGN.md §2:** AgentConfig should grow optional `track_record` fields (e.g., `runs_completed: int`, `notable_outcomes: list[str]`) that the wrapper updates after each successful run, providing the seam for the report 06 §6 "establish precedent" gate (autonomy promotion requires N successful supervised runs).

**Models 4 (Work as Ledger) and 5 (Factory Floor vs. Workshop) are explicitly multi-agent / production-scale — out of scope per PLAN.md guardrail.** The Bead system, the Batch-Closure Heresy, and the 3-vs-30-agent phase-change framing all assume parallel agent populations at orchestrator scale. We're solo-tier (1-5 concurrent per repo), single-agent-per-run; the workshop model holds for v1 and v2.

That said, the **ledger-vs-logging distinction** (*"Logs are diagnostic artifacts — searched when something breaks. The ledger is an operational artifact — queried continuously for routing, attribution, and improvement"*) is worth noting for the Run JSON design: our Run JSONs are halfway between log and ledger — they're append-only, attributed (each attempt has a wrapper invocation timestamp + claude version + token count), and queryable by aggregation tools. We should document them as the **ledger for `agent-runner`'s own operations**, and resist the temptation to retroactively edit them. Report 03 §1 already encodes this for the transcript split (Run JSON = working memory; transcript = full ledger); chapter 9/6 Model 4 sharpens it: **never batch-close a Run JSON entry retroactively**, even when the wrapper crashed mid-attempt and you're tempted to clean it up.

---

## 4. Chapter 10/1 (Claude Code) — direct documentation of our inner harness

[`10-practitioner-toolkit/1-claude-code`](https://www.jayminwest.com/agentic-engineering-book/10-practitioner-toolkit/1-claude-code) is the longest single chapter in the book (2045 lines). Most of it is multi-agent / Claude Code Teams material that PLAN.md scope rules out. The single-agent execution-layer-relevant sections:

### 4.1 Subagent system — read for what we explicitly DON'T use

The chapter notes Claude Code's subagent system (Task tool, `.claude/agents/*.md` filesystem definitions, `tools:` frontmatter). This is the inner harness's mechanism for one Claude Code session to spawn N specialized sub-sessions. **For `agent-runner` v1, we explicitly don't use it** — every CI run is a single flat `claude -p` invocation, no subagent spawning. The read is defensive: if a workflow's prompt or AgentConfig accidentally encourages subagent spawning, that's a quality-of-output risk (multi-agent compound-reliability arithmetic per report 03 §6.3). **Implication:** AgentConfig presets should not inherit `Task` in `allowed_tools` by default — enforces single-agent execution.

### 4.2 Tool restriction as forcing function for delegation

The chapter cites:

> *"The default Claude Code HEAD agent inherits all tools. ... If the orchestrator literally cannot read files, write code, or execute bash, it has no choice but to spawn subagents."*

For `agent-runner`'s inverse case (we want NO delegation, only direct execution), the symmetric move is: **leave Read/Edit/Write/Bash on the whitelist, leave Task OFF.** The agent has no choice but to do the work directly within its single session. **Implication for DESIGN.md §2:** AgentConfig schema should default-exclude Task from `allowed_tools` for v1; users opting into subagent-spawning workflows must explicitly add it.

### 4.3 Hook context injection — additionalContext for soft boundaries

Claude Code 2.1.9 added the ability for PreToolUse hooks to inject `additionalContext` rather than only allow/block:

> *"Hooks can now return context that influences the model's decision-making without hard-blocking ... The hook becomes an advisor, not a gatekeeper."*

For `agent-runner`'s wrapper-side hooks, this is a useful capability to layer on top of the existing `--allowed-tools` whitelist. Concrete use case: **OAuth-rate-limit-headroom warning.** Today our wrapper detects rate-limit-rejection events and triggers resume; with `additionalContext` injection, a PreToolUse hook on rate-limit-expensive operations could pre-warn the model *"you have ~2 minutes of rate-limit budget remaining; finish your current task and return rather than starting new explorations"* — softer than blocking, but lets the agent self-throttle. **Roadmap candidate, Stage 2.**

### 4.4 Memory management (2.1.32) — `.claude/rules/` and session-memory

The chapter documents the seven-tier memory hierarchy:

| Tier | Location | Scope | Automatic |
|---|---|---|---|
| 1 | `/Library/.../CLAUDE.md` | Org-wide | ✗ |
| 2 | `./CLAUDE.md` | Project | ✗ |
| 3 | `./.claude/rules/*.md` | Project/Path-scoped | ✗ |
| 4 | `~/.claude/CLAUDE.md` | User global | ✗ |
| 5 | `./CLAUDE.local.md` | Project local | ✗ |
| 6 | `~/.claude/projects/.../summary.md` | Session | ✓ |
| 7 | `@path/to/file` | Import | ✗ |

For `agent-runner`'s CI-ephemeral runs, **Tier 6 (session memory) does not survive** — each CI job has a fresh `~/.claude/projects/`. This is the right behavior for our model (per §3.6's Persistent Identity / Ephemeral Execution) and we shouldn't try to persist it across runs.

What we CAN exploit: **Tier 3 (`.claude/rules/*.md` with `paths:` frontmatter)** is project/path-scoped and lives in version control. The chapter cites:

```yaml
---
paths:
  - "**/*_test.py"
  - "tests/**/*.py"
---

# Test File Conventions
- Use pytest fixtures for shared setup
- Prefix test functions with test_
- Mock external dependencies
```

These rules load only when the agent operates on matching files. **Implication for DESIGN.md §11:** document `.claude/rules/` as the recommended pattern for path-scoped guidance in user repos; it composes cleanly with our hierarchical `CLAUDE.md` discovery. AgentConfig does not need a separate field to reference these — Claude Code discovers them automatically.

### 4.5 Sandbox-mode-vs-permissions independence (cross-cite from §2.4)

Already covered in §2.4 above. The chapter is the canonical source for the claim that `--dangerously-skip-permissions` does not disable sandboxing. **Implication for DESIGN.md §11:** cite this chapter as the source for the defense-in-depth claim.

### 4.6 The "Harness Quality as the Distinguishing Factor" framing

The chapter opens with Raschka's principle (cited 2026-04-11):

> *"Apparent model quality is frequently context quality in disguise. When a coding agent underperforms, the first audit target is the harness, not the model."*

This is the single most-load-bearing operational claim from chapter 10/1 for `agent-runner`. Our position in the harness stack means **when an agent-runner workflow underperforms, the audit sequence is: (1) inner harness configuration — Claude Code version, allowed_tools, model selection; (2) outer harness — AgentConfig content, trigger framing, verify command; (3) only then the model.** This reinforces report 06 §8's Diagnostic Decision Tree but adds a layer-ordering: outer-harness audit before inner-harness audit before model audit. **Implication for LESSONS.md:** the on-call triage guide (per report 06 §8) should add a "layer 0" check at the top: "Did the AgentConfig load correctly? Did the trigger payload assemble correctly? Did Claude Code launch with the right `--allowed-tools`?" before descending into the Core Four (Prompt / Model / Context / Tools).

---

## 5. Chapter 10/3 and 10/6 — IDE integrations and enterprise context tools (lightly)

[`10-practitioner-toolkit/3-ide-integrations`](https://www.jayminwest.com/agentic-engineering-book/10-practitioner-toolkit/3-ide-integrations) surveys Cursor, Windsurf, GitHub Copilot, Continue.dev, JetBrains AI, and Aider. **Mostly out of scope for `agent-runner` execution layer** — these are interactive developer tools, not CI execution layers. The chapter's two cross-cutting points worth noting:

- **The integration spectrum (extension-based / fork-based / native AI editor) does not include the CI-substrate option `agent-runner` occupies.** Our category — "outer harness in CI for an inner-harness coding agent" — is not in the chapter's taxonomy. This is consistent with PLAN.md's positioning of `agent-runner` as occupying a different layer than these tools.
- **Aider as a CLI alternative inner harness.** The chapter cites Aider as a CLI-based AI coding assistant. If a user wanted to run `agent-runner` with Aider as the inner harness instead of Claude Code, the AgentConfig schema would need an `inner_harness: "claude-code" | "aider"` field. **Roadmap candidate; deferred until a user asks.**

[`10-practitioner-toolkit/6-enterprise-context-tools`](https://www.jayminwest.com/agentic-engineering-book/10-practitioner-toolkit/6-enterprise-context-tools) is a tool survey for the chapter-4/6 brownfield-context patterns. The relevant content for our layer is the **Pattern-to-Tool Map** structure: it tells us which user-side context tools compose well via MCP and which don't. The actionable cross-cuts:

- **Native MCP-composable tools** (Serena MCP for LSP-backed dependency-graph queries; Augment Code's Context Engine MCP for managed semantic indexing; Sourcegraph MCP server for org-scale code search; Continue.dev's custom RAG MCP server; Qdrant+tree-sitter DIY) all wire into `agent-runner` workflows the same way: declare the MCP server in the AgentConfig, add the corresponding `mcp__<server>__*` entries to `allowed_tools`. **No new schema needed**; this is an existing capability.
- **Non-composable tools** (Tabnine Enterprise — self-contained IDE assistant, no MCP; Cursor — separate IDE environment; Cognition Devin / DeepWiki — SaaS documentation generators) cannot be wired into `agent-runner` workflows directly. The actionable note: when a user asks "can I use Tabnine through agent-runner?", the answer is no — Tabnine and Devin are documentation-generation tools whose output should be committed to the repo (as CLAUDE.md / `.claude/rules/` files / ADRs) before `agent-runner` invokes Claude Code on it. **Implication for the eventual user-facing onboarding doc:** document this pattern explicitly.

---

## 6. Out-of-scope content noted but skipped

Per PLAN.md's Scope guardrail, the following multi-agent / orchestration material was **deliberately not body-read** in this report (or read only at the framing-level for cross-references):

| Chapter | Why skipped |
|---|---|
| §4/4 Multi-Agent Context | Multi-agent context isolation, orchestrator context cleanliness, persistent state vs ephemeral context — out of scope for our single-agent-per-run model. The chapter index page noted that the chapter exists; not body-read. |
| §9/5 Execution Topologies — Parallel, Synthesis, Nested portions | Multi-agent topologies. Sequential and Persistent (single-agent applicable) were body-read; the multi-agent sections were skimmed for the framing-level Trust Gradient table and the Wider/Deeper/Thicker/Less-Friction improvement-vectors framework, but the per-topology operational guidance was not body-read. |
| §9/6 Design as Bottleneck — Models 4 (Work as Ledger) and 5 (Factory Floor vs Workshop) | Model 4's Bead system and Model 5's 3-vs-30-agent phase-change are explicitly multi-agent / production-scale orchestration. The ledger-vs-logging distinction was body-read as a framing-level reinforcement of report 03 §1's Run-JSON-vs-transcript split, but the multi-agent specifics were skipped. |
| §10/1 Claude Code — TeammateTool / Agent Teams sections | Native multi-agent coordination layer. The 5 coordination patterns (Lead-Teammate, Swarm, Pipeline, Council, Plan Approval) are all multi-agent — out of scope. The "Use subagents vs use agent teams" decision framework was read at the catalog level. |
| §10/1 Claude Code — Feature Gate Reverse Engineering / claude-sneakpeek | Not multi-agent, but explicitly research-only / unstable / observational. Not actionable for production agent-runner workflows; noted but not adopted. |
| §10/1 Claude Code — Claude Cowork / Claude Dispatch | Different product (knowledge-worker tasks, not coding); not relevant to our coding-agent CI layer. |
| §10/2 Google ADK | Different framework. Out of scope per PLAN.md's "non-Claude framework" implicit exclusion (`agent-runner` is Claude-Max-OAuth-specific). |
| §10/4 Agent Frameworks (LangGraph / CrewAI / AutoGen / Claude Agent SDK comparison) | Framework comparison — out of scope; Claude Agent SDK is the inner harness we already use, the others are alternatives to compare to. |
| §10/5 Multi-Agent Workspace Managers | Already body-read in report 01 (Overstory section); rest is multi-agent — out of scope. |

The exclusion list is consistent with the PLAN.md scope guardrail: `agent-runner`'s scope is the **execution layer for single-agent CI workflows under Claude Max**. Multi-agent orchestration, alternative-framework integration, and software-factory architecture all live in the sister-research repo.

---

## 7. Implications for DESIGN.md

This round adds the following to the cumulative design-doc edits proposed by reports 03 and 06:

1. **DESIGN.md §2 (AgentConfig schema):** ship named role presets (`role: "reviewer" | "test-runner" | "builder"`) that select default `allowed_tools` lists (per §2.1); document that `Task` is excluded from `allowed_tools` by default to enforce single-agent execution (per §4.2); add optional `prompt_template_path: str` pointing at a versioned prompt file using structured-XML-within-markdown convention (per §3.3); add optional `track_record` fields (`runs_completed`, `notable_outcomes`) updated by the wrapper after successful runs (per §3.6); add optional `mcp_servers: list[str]` for declaring user-side context tools (Serena, Augment, Sourcegraph, Continue.dev RAG) per §5.

2. **DESIGN.md §4 (Run JSON):** add `peak_context_pct: float` per attempt, populated from stream-json `context_pct` events (per §1.1); ensure existing `attempt_summaries: list[str]` (per report 06 §3.1) is treated as the seancing artifact (per §3.6 Model 3); document Run JSONs as the **operational ledger** for `agent-runner` — never batch-close retroactively (per §3.6 Model 4 cross-applicability).

3. **DESIGN.md §5 (run.py / prompt assembly):** the trigger payload is a **payload, not a log** — include only directly task-relevant content; never dump prior-attempt transcripts (per §1.2); never include "things to avoid" examples inline — those become attractors (per §3.1); rely on Claude Code's native hierarchical CLAUDE.md discovery; do not project-flatten user-repo CLAUDE.md files into a single prompt (per §1.5).

4. **DESIGN.md §10 (roadmap):** v1 ships only Level 1-4 prompt-maturity workflows (Static / Parameterized / Conditional / Contextual); Levels 5-7 deferred (per §3.2). Stage-2 candidate: PreToolUse-hook `additionalContext` injection for soft rate-limit-headroom warnings (per §4.3). Stage-3 candidate: AgentConfig `inner_harness: "claude-code" | "aider"` field if a user requests Aider support (per §5).

5. **DESIGN.md §11 (security / verification):** assert minimum Claude Code version ≥2.1.7 in the workflow setup step (per §2.3 line-continuation footgun); MUST NOT permit `Bash(*)` in any AgentConfig; SHOULD prefer exact-match patterns over wildcards (per §2.3); document the defense-in-depth claim explicitly: `--dangerously-skip-permissions` + GitHub Actions runner isolation + workflow `permissions:` block scoping = three independent layers, none removed by the flag (per §2.4); cite chapter 10/1 as canonical source.

6. **DESIGN.md §11 (observability):** add the **layer-ordered audit sequence** to the on-call triage guide (per §4.6): Layer 0 (outer-harness configuration: AgentConfig load, trigger payload assembly, claude launch args) → Layer 1 (inner-harness state: Claude Code version, allowed_tools, model) → Layer 2 (Core Four from report 06 §8: Prompt, Model, Context, Tools). This precedes the report-06-§8 Diagnostic Decision Tree, not replaces it.

7. **Repo conventions (not DESIGN.md proper):** when LESSONS.md is created, line format adopts `[<prefix-NNNNN>] helpful=N harmful=M *[YYYY-MM-DD]*:: <assertion>` (per §3.4); category prefixes `res-` / `ver-` / `ctx-` / `tri-` / `oau-` / `gat-` / `obs-` / `mcp-` / `sec-` (per §3.4); helpful/harmful counters maintained manually in v1, automated by evaluation infrastructure when it lands (per report 06 §9 cross-reference). Version-control AgentConfig YAML, workflow YAML, and prompt-template files as **specs that ARE source code** (per §3.3); the GSD-style `<action>` / `<verify>` / `<done>` semantic-XML-within-markdown convention is the canonical prompt-template shape.

### Cross-cutting "adopt verbatim" maxims from this round

Three single-line statements stand out as worth importing into LESSONS.md alongside the maxims from reports 03 and 06:

> *"Shape the input tokens so the most probable output tokens are the correct ones."* (§9/1 Pit of Success)
> *"Knowledge artifacts are source code. Version control them, test them, refactor them."* (§9/4 Context as Code)
> *"Apparent model quality is frequently context quality in disguise. When a coding agent underperforms, the first audit target is the harness, not the model."* (§10/1 Claude Code, citing Raschka 2026-04-11)

### Cross-cutting "differ" — what this round confirms is *not* for us

- **Active context-management architectures (LCM, Sapling) at the outer layer.** Both replace the inner harness's compaction; we don't get to mix-and-match. Wait for Claude Code to adopt or release the upstream version.
- **ACE (Agentic Context Engineering) at the per-run prompt level.** ACE is the right pattern for LESSONS.md curation but not for per-run trigger payloads — we're in the bounded-coding-task regime, not the knowledge-intensive long-horizon regime.
- **Claude Code Agent Teams / TeammateTool / multi-agent coordination.** Single-agent-per-run is our v1 model; agent-teams is multi-agent orchestration that PLAN.md guardrail rules out.
- **Claude Code session memory (Tier 6).** Doesn't survive CI-ephemeral runs; persistent state lives in the user's repo (Tiers 2-3, 5, 7) and our Run JSONs.
- **Cursor / Windsurf / Tabnine / Devin as inner harnesses.** All are interactive-developer tools or self-contained SaaS — none are CI-execution-layer-compatible the way Claude Code (CLI) is.

---

## Sources reviewed

| Source URL | Status | Notes |
|---|---|---|
| https://www.jayminwest.com/agentic-engineering-book/4-context | ✅ Full review | Fetched via issue #19 (chapter index probe). Chapter overview + when-to-read-what + connections informed the §1 orientation and the in-scope reading list. |
| https://www.jayminwest.com/agentic-engineering-book/4-context/1-context-fundamentals | ✅ Full review | Fetched via issue #20. Capability capacity model (40% / 60% thresholds), context-vs-memory distinction, one-agent-one-task principle, Pit-of-Success principle, capability-degradation monitoring approaches. Informed §1.1, §3.1, and §7 implication 2 (peak_context_pct). |
| https://www.jayminwest.com/agentic-engineering-book/4-context/2-context-strategies | ✅ Full review | Fetched via issue #20. GSD project's `Quality ∝ 1/(% context used)` formula, Frequent Intentional Compaction (40-60%), context-utilization percentage display thresholds (0-30 / 30-60 / 60-80 / 80-95 / 95+), Federated Knowledge Architecture. Informed §1.1, §1.3, and §7 implication 2. |
| https://www.jayminwest.com/agentic-engineering-book/4-context/3-context-patterns | ✅ Full review | Fetched via issue #20. Progressive Disclosure pattern (3-tier), Context Loading vs Context Accumulation framing, ACE (Agentic Context Engineering) framework with Generator/Reflector/Curator architecture and `[ID] helpful=X harmful=Y` playbook format. Informed §1.2, §1.3, §3.4 (LESSONS.md format), and §7 implication 3. |
| https://www.jayminwest.com/agentic-engineering-book/4-context/5-context-management-architectures | ✅ Full review | Fetched via issue #20. LCM (immutable store + summary DAG + lcm_grep/lcm_expand + llm_map / agentic_map), Sapling (operation model + 5-stage pipeline + commitment tracking + 50-60% steady-state target), passive-accumulation baseline. Informed §1.4 (read-for-context, not adopted) and the "differ" cross-cutting list. |
| https://www.jayminwest.com/agentic-engineering-book/4-context/6-context-at-codebase-scale | ✅ Full review | Fetched via issue #20. Width-vs-depth distinction, two failure types (coverage / relevance), 7 patterns (Semantic Indexing / Hierarchical Convention Files / ADRs / Dependency-Graph Queries / Progressive Codebase Disclosure / Tribal Knowledge Codification / Graduated Adoption with Encoding→Documenting→Consolidating→Specializing→Enforcing 5 stages), 4-archetype decision matrix. Informed §1.5 and §7 implication 1 (mcp_servers field). |
| https://www.jayminwest.com/agentic-engineering-book/5-tool-use | ✅ Full review | Fetched via issue #20. Chapter overview (Tool Use, NOT "tools"), Hands/Senses/Skills mental model. Confirmed correct chapter slug `5-tool-use`; informed orientation. |
| https://www.jayminwest.com/agentic-engineering-book/5-tool-use/1-tool-design | ✅ Full review | Fetched via issue #20. Tool Examples as Design Pattern (72%→90% accuracy claim), Rich User Questioning Patterns (4×4 maximal pattern), **Coding Agent Edit Formats** (whole-file/udiff/search-replace × model-family table from Aider production), Poka-Yoke Constraints (absolute paths, exact-match), Coding Agent Tool Inventory (read_file / write_file / search / bash baseline). Informed §2.5 (edit format, baseline tool inventory). |
| https://www.jayminwest.com/agentic-engineering-book/5-tool-use/2-tool-selection | ✅ Full review | Fetched via issue #20. Description-based selection mechanics, common selection failures (overlapping functionality, too many options, vague descriptions), distinctive naming, comparison-tables-in-context, "don't default to giving the agent everything" — fewer tools = better selection. Informed §2.1 and the deny-by-default discipline. |
| https://www.jayminwest.com/agentic-engineering-book/5-tool-use/3-tool-restrictions | ✅ Full review | Fetched via issue #20. **Tool Restrictions as Security Boundaries** (deny-all + allowlist; production IAM thinking), the canonical Reviewer/Test-Runner/Builder/Orchestrator/Scout role-tool table, MCP tool naming convention (`mcp__<server>__<tool>`), Wildcard Permission Patterns (`Bash(npm *)`), Permission Bypass Vulnerabilities (line continuation injection fixed in 2.1.7, glob expansion escapes), best practices for secure permissions. Informed §2.1, §2.2, §2.3, and §7 implications 1 + 5. |
| https://www.jayminwest.com/agentic-engineering-book/5-tool-use/4-scaling-tools | ✅ Full review | Fetched via issue #20. Dynamic Tool Discovery (`defer_loading: true`, 85% token reduction, 49%→74% / 79.5%→88.1% selection-accuracy improvement claims), Programmatic Tool Orchestration (`allowed_callers: ["code_execution_20250825"]`, 37% token reduction), MCP Deployment Architecture (stdio / Streamable HTTP / Sidecar), MCP Auto-Selection Mode (Claude Code 2.1.7+ `auto:N` thresholds). Informed background context for our existing MCP usage; no direct DESIGN.md implication beyond noting `defer_loading` as available if our skill set grows large. |
| https://www.jayminwest.com/agentic-engineering-book/5-tool-use/5-skills-and-meta-tools | ✅ Full review | Fetched via issue #20. Skills as Meta-Tools (third category beyond tools and prompts), token cost (~100 tokens/tool vs ~1500 tokens/skill), Context Contracts for Agent Capability Declaration (declarative input/output JSON schemas, three validation gates: pre-spawn / scope enforcement / registry generation). Informed §2.6 and the roadmap-candidate context-contracts note. |
| https://www.jayminwest.com/agentic-engineering-book/9-mental-models | ✅ Full review | Fetched via issue #19. Chapter overview confirming the 7-subchapter taxonomy and chapter title (Mental Models). Informed orientation. |
| https://www.jayminwest.com/agentic-engineering-book/9-mental-models/1-pit-of-success | ✅ Full review | Fetched via issue #20. Rico-Mariani-attributed Pit-of-Success framing, transformer-attention-based context-window framing, "shape input tokens so most probable outputs are correct," position-information-by-importance (system→middle→instruction-at-end), eliminate-competing-attractors discipline. Informed §3.1 and the cross-cutting "adopt verbatim" maxim. |
| https://www.jayminwest.com/agentic-engineering-book/9-mental-models/2-prompt-maturity-model | ✅ Full review | Fetched via issue #20. Seven prompt-maturity levels (Static / Parameterized / Conditional / Contextual / Higher-Order / Self-Modifying / Meta-Cognitive), pyramid-distribution recommendation, **Engineer Leverage Progression** three stages (Search-Engine / Integrated Workflow / System Designer) cross-cited with leverage points #1 (ADWs) / #3 (Plans) / #5 (Tests). Informed §3.2 and §7 implication 4 (v1 ships Level 1-4 only). |
| https://www.jayminwest.com/agentic-engineering-book/9-mental-models/3-specs-as-source-code | ✅ Full review | Fetched via issue #20. Sean Grove's "specs are the truth" framing, traditional-vs-agentic project structure diagrams, GSD project's PLAN.md-as-prompts evidence (semantic XML within markdown: `<action>` `<verify>` `<done>`), BMAD-METHOD's living-artifacts inversion. Informed §3.3 and §7 implication 1 (prompt_template_path). |
| https://www.jayminwest.com/agentic-engineering-book/9-mental-models/4-context-as-code | ✅ Full review | Fetched via issue #20. **ACE playbook line format** (`[prefix-ID] helpful=X harmful=Y :: assertion`), git-as-version-control-for-knowledge, helpful/harmful counters as unit tests, modular organization (str-/cal-/mis-/con-/too- prefixes), Refactoring (semantic deduplication), Documents-to-Code continuum, Agent-as-Code BMAD-METHOD example. Informed §3.4 and §7 implication 7 (LESSONS.md format). |
| https://www.jayminwest.com/agentic-engineering-book/9-mental-models/5-execution-topologies | ✅ Full review (selectively) | Fetched via issue #20. Five topologies (Parallel / Sequential / Synthesis / Nested / Persistent) — only Sequential and Persistent body-read in detail; Parallel/Synthesis/Nested skimmed. Four Improvement Vectors (Wider/Deeper/Thicker/Less-Friction), Trust Gradient table (Low/Medium/High trust × Width/Depth/Thickness/Friction), topology combinations, anti-patterns by topology. Informed §3.5. |
| https://www.jayminwest.com/agentic-engineering-book/9-mental-models/6-design-as-bottleneck | ✅ Full review (selectively) | Fetched via issue #20. Five mental models — Models 1 (Design as Bottleneck — Theory of Constraints + Mollick "Shape of the Thing" cross-citation), 2 (Agents as Pistons — GUPP propulsion principle, hook-IS-the-assignment), 3 (Persistent Identity Ephemeral Execution — three-layer identity/history/session, seancing, Gas Town polecats CV) body-read; Models 4 (Work as Ledger — Gas Town Bead system, Batch-Closure Heresy, ledger-vs-logging table) read at framing level for the no-retroactive-edit principle; Model 5 (Factory Floor vs Workshop — phase-change at 10+ agents) skimmed at catalog level only. Informed §3.6 and §7 implication 2 (Run JSON as ledger). |
| https://www.jayminwest.com/agentic-engineering-book/10-practitioner-toolkit | ✅ Full review | Fetched via issue #19. Chapter overview confirming chapter title and 6-tool catalog. Informed orientation. |
| https://www.jayminwest.com/agentic-engineering-book/10-practitioner-toolkit/1-claude-code | ✅ Full review (heavy) | Fetched via issue #20. **Harness Quality as the Distinguishing Factor** (Raschka 2026-04-11 cross-citation), subagent system + nesting constraint workarounds, **Tool Restriction as Forcing Function for Delegation** (the inverse pattern that argues for excluding `Task` from `allowed_tools` in our case), Hook Context Injection (`additionalContext` for soft boundaries, Claude Code 2.1.9), Memory Management (seven-tier hierarchy with session memory tier 6 and `.claude/rules/` tier 3 with path scoping), Sandbox-Mode-vs-Permissions independence (`--dangerously-skip-permissions` does NOT disable sandboxing). Skipped: TeammateTool / Agent Teams sections (multi-agent), Feature Gate Reverse Engineering / claude-sneakpeek (research-only), Claude Cowork / Claude Dispatch (different product). Informed §4.1, §4.2, §4.3, §4.4, §4.5, §4.6, and §7 implications 1, 2, 5, 6. |
| https://www.jayminwest.com/agentic-engineering-book/10-practitioner-toolkit/3-ide-integrations | ✅ Full review (lightly) | Fetched via issue #20. Integration Spectrum (extension-based / fork-based / native AI editor), 6-tool comparison table (Cursor / Windsurf / GitHub Copilot / Continue.dev / JetBrains AI / Aider with model options + multi-file edit + agent mode + self-hosted + cost). Informed §5 (Aider as alternative inner harness, deferred roadmap candidate). |
| https://www.jayminwest.com/agentic-engineering-book/10-practitioner-toolkit/6-enterprise-context-tools | ✅ Full review (selectively) | Fetched via issue #20. Pattern-to-Tool Map for the 7 chapter-4/6 patterns (Aider Repo Map / Augment Code / Sourcegraph Amp / Continue.dev / Qdrant+tree-sitter for Semantic Indexing; CLAUDE.md native for Hierarchical Convention Files; ADR markdown native for Decision Records; Serena MCP / Augment Code for Dependency-Graph Queries; RepoMapper MCP for Progressive Codebase Disclosure; Cognition Devin/DeepWiki for Tribal Knowledge Codification; Tabnine Enterprise for compliance-bound Enforcing). Informed §5 (MCP-composable vs non-composable distinction). |
| https://www.jayminwest.com/agentic-engineering-book/4-context/4-multi-agent-context | ⏭️ Out of scope | Multi-agent context isolation, orchestrator context cleanliness, persistent state vs ephemeral context. Per PLAN.md scope guardrail. Listed in chapter-4 index but not fetched. |
| https://www.jayminwest.com/agentic-engineering-book/9-mental-models/7-software-factories | ⏭️ Already read | Read in report 01 (Round 1). Not re-fetched. |
| https://www.jayminwest.com/agentic-engineering-book/10-practitioner-toolkit/2-google-adk | ⏭️ Out of scope | Different framework (Google ADK). Per PLAN.md non-Claude framework exclusion. Not fetched. |
| https://www.jayminwest.com/agentic-engineering-book/10-practitioner-toolkit/4-agent-frameworks | ⏭️ Out of scope | Framework comparison (LangGraph / CrewAI / AutoGen / Claude Agent SDK). Out of scope for execution-layer focus. Not fetched. |
| https://www.jayminwest.com/agentic-engineering-book/10-practitioner-toolkit/5-multi-agent-workspace-managers | ⏭️ Already read | Read in report 01 (Overstory section). Per PLAN.md scope guardrail (multi-agent). Not re-fetched. |
| https://www.jayminwest.com/agentic-engineering-book/5-tools | ❌ Invalid URL | Probed at index-fetch time (issue #19). Returned content but the chapter at that slug does not exist — chapter 5's actual slug is `5-tool-use` (confirmed via the chapter-5 index page rendering inside other chapters' sidebars). Bad-slug attempt; no content lost (immediately retried with correct slug in issue #20). |
