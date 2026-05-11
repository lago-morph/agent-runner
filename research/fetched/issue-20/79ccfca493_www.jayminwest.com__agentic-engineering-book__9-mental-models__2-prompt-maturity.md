


[Agentic Engineering](/agentic-engineering-book)[](https://github.com/jayminwest/agentic-engineering-book "View on GitHub")

Chapter 1: Foundations

[Foundations](/agentic-engineering-book/1-foundations)[Twelve Leverage Points of Agentic Coding](/agentic-engineering-book/1-foundations/1-twelve-leverage-points)

Chapter 2: Prompt

[Prompt](/agentic-engineering-book/2-prompt)[Prompt Types](/agentic-engineering-book/2-prompt/1-prompt-types)[Prompt Structuring](/agentic-engineering-book/2-prompt/2-structuring)[Prompt Language](/agentic-engineering-book/2-prompt/3-language)

Chapter 3: Model

[Model](/agentic-engineering-book/3-model)[Model Selection](/agentic-engineering-book/3-model/1-model-selection)[Model Behavior](/agentic-engineering-book/3-model/2-model-behavior)[Model Limitations and Workarounds](/agentic-engineering-book/3-model/3-model-limitations)[Multi-Model Architectures](/agentic-engineering-book/3-model/4-multi-model-architectures)[Model Evaluation for Agents](/agentic-engineering-book/3-model/5-model-evaluation)

Chapter 4: Context

[Context](/agentic-engineering-book/4-context)[Context Fundamentals](/agentic-engineering-book/4-context/1-context-fundamentals)[Context Management Strategies](/agentic-engineering-book/4-context/2-context-strategies)[Advanced Context Patterns](/agentic-engineering-book/4-context/3-context-patterns)[Multi-Agent Context](/agentic-engineering-book/4-context/4-multi-agent-context)[Context Management Architectures](/agentic-engineering-book/4-context/5-context-management-architectures)[Context at Codebase Scale](/agentic-engineering-book/4-context/6-context-at-codebase-scale)

Chapter 5: Tool Use

[Tool Use](/agentic-engineering-book/5-tool-use)[Tool Design](/agentic-engineering-book/5-tool-use/1-tool-design)[Tool Selection and Routing](/agentic-engineering-book/5-tool-use/2-tool-selection)[Tool Restrictions and Security](/agentic-engineering-book/5-tool-use/3-tool-restrictions)[Scaling Tool Use](/agentic-engineering-book/5-tool-use/4-scaling-tools)[Skills and Meta-Tools](/agentic-engineering-book/5-tool-use/5-skills-and-meta-tools)

Chapter 6: Patterns

[Harnesses](/agentic-engineering-book/6-harnesses)[What Is a Harness?](/agentic-engineering-book/6-harnesses/1-what-is-a-harness)[The Harness Stack](/agentic-engineering-book/6-harnesses/2-harness-stack)[Harness Categories](/agentic-engineering-book/6-harnesses/3-harness-categories)[Harness as Control System](/agentic-engineering-book/6-harnesses/4-harness-as-control-system)[Harness Engineering](/agentic-engineering-book/6-harnesses/5-harness-engineering)[Security, Permissions, and Trust](/agentic-engineering-book/6-harnesses/6-security-permissions-trust)[Designing for Your Context](/agentic-engineering-book/6-harnesses/7-designing-for-your-context)

Chapter 7: Practices

[Patterns](/agentic-engineering-book/7-patterns)[Plan-Build-Review Pattern](/agentic-engineering-book/7-patterns/1-plan-build-review)[Self-Improving Expert Commands](/agentic-engineering-book/7-patterns/2-self-improving-experts)[Orchestrator Pattern](/agentic-engineering-book/7-patterns/3-orchestrator-pattern)[Autonomous Loops (Ralph Wiggum)](/agentic-engineering-book/7-patterns/4-autonomous-loops)[ReAct Pattern](/agentic-engineering-book/7-patterns/5-react-pattern)[Human-in-the-Loop Pattern](/agentic-engineering-book/7-patterns/6-human-in-the-loop)[Progressive Disclosure Pattern](/agentic-engineering-book/7-patterns/7-progressive-disclosure)[Expert Swarm Pattern](/agentic-engineering-book/7-patterns/8-expert-swarm-pattern)[Multi-Agent Collaboration Pattern](/agentic-engineering-book/7-patterns/9-multi-agent-collaboration)[The Multi-Agent Landscape](/agentic-engineering-book/7-patterns/10-multi-agent-landscape)[Production Multi-Agent Systems](/agentic-engineering-book/7-patterns/11-production-multi-agent-systems)

Chapter 8: Mental Models

[Practices](/agentic-engineering-book/8-practices)[Debugging Agents](/agentic-engineering-book/8-practices/1-debugging-agents)[Evaluation](/agentic-engineering-book/8-practices/2-evaluation)[Cost and Latency](/agentic-engineering-book/8-practices/3-cost-and-latency)[Production Concerns](/agentic-engineering-book/8-practices/4-production-concerns)[Workflow Coordination for Agents](/agentic-engineering-book/8-practices/5-workflow-coordination)[Knowledge Evolution](/agentic-engineering-book/8-practices/6-knowledge-evolution)[Operating Agent Swarms](/agentic-engineering-book/8-practices/7-operating-agent-swarms)

Chapter 9: Practitioner Toolkit

[Mental Models](/agentic-engineering-book/9-mental-models)[Pit of Success](/agentic-engineering-book/9-mental-models/1-pit-of-success)[Prompt Maturity Model](/agentic-engineering-book/9-mental-models/2-prompt-maturity-model)[Specs as Source Code](/agentic-engineering-book/9-mental-models/3-specs-as-source-code)[Context as Code](/agentic-engineering-book/9-mental-models/4-context-as-code)[Execution Topologies](/agentic-engineering-book/9-mental-models/5-execution-topologies)[Design as Bottleneck](/agentic-engineering-book/9-mental-models/6-design-as-bottleneck)[Software Factories](/agentic-engineering-book/9-mental-models/7-software-factories)

Chapter 10: Chapter 10

[Practitioner Toolkit](/agentic-engineering-book/10-practitioner-toolkit)[Claude Code](/agentic-engineering-book/10-practitioner-toolkit/1-claude-code)[Google ADK](/agentic-engineering-book/10-practitioner-toolkit/2-google-adk)[IDE Integrations](/agentic-engineering-book/10-practitioner-toolkit/3-ide-integrations)[Agent Frameworks](/agentic-engineering-book/10-practitioner-toolkit/4-agent-frameworks)[Multi-Agent Workspace Managers](/agentic-engineering-book/10-practitioner-toolkit/5-multi-agent-workspace-managers)[Enterprise Codebase Context Tools](/agentic-engineering-book/10-practitioner-toolkit/6-enterprise-context-tools)

Book Navigation

# Prompt Maturity Model

A framework for understanding and designing prompts at different levels of sophistication. Each level builds on the previous, adding new capabilities and complexity.

## The Seven Levels

### Level 1: Static

**What defines it** : Hardcoded instructions with no variation. The prompt is the same every time it runs.

**When to use it** : For simple, repeatable tasks that never need customization. Quick utilities where the overhead of parameters isn't worth it.

**Example** : A command that always formats code the same way, or always runs the same test suite.
    
    
    # format-code.md
    Run prettier on all TypeScript files in src/

**Trade-offs** :

  * Pros: Simplest to write and understand. No state to manage.
  * Cons: Inflexible. Requires creating new commands for variations.



* * *

### Level 2: Parameterized

**What defines it** : Uses `$ARGUMENTS` or other variables to accept input at runtime.

**When to use it** : When you need the same logic with different inputs. The behavior is consistent but the data varies.

**Example** : From the knowledge base examples, commands that take a file path or topic as input.
    
    
    # review-file.md
    Review the file at $ARGUMENTS for clarity and completeness.

**Trade-offs** :

  * Pros: Reusable across different inputs. Still straightforward logic.
  * Cons: Limited to simple substitution. No branching behavior.



* * *

### Level 3: Conditional

**What defines it** : Contains if/else logic or branching based on input characteristics.

**When to use it** : When the same command needs to behave differently depending on what it receives.

**Example** : A command that processes markdown differently than code files, or handles different file types.
    
    
    # analyze.md
    If $ARGUMENTS contains .ts or .js:
      - Check for type safety issues
    Else if $ARGUMENTS contains .md:
      - Check for broken links
    Else:
      - Provide general analysis

**Trade-offs** :

  * Pros: One command handles multiple scenarios. More intelligent.
  * Cons: Logic can become complex. Harder to predict behavior.



* * *

### Level 4: Contextual

**What defines it** : Reads external files or project state before acting. Uses context to inform decisions.

**When to use it** : When the prompt needs to understand the broader environment. Common with project-aware commands.

**Example** : The `/tools:prime` command that gathers project context, or commands that read CLAUDE.md before working.
    
    
    # contextualized-review.md
    1. Read CLAUDE.md to understand project conventions
    2. Read the file at $ARGUMENTS
    3. Review against project standards
    4. Suggest improvements that fit the codebase

**Trade-offs** :

  * Pros: Decisions informed by actual project state. More intelligent.
  * Cons: Slower due to file reads. Can fail if context is missing.



* * *

### Level 5: Higher Order

**What defines it** : Invokes other commands as subroutines. Orchestrates multiple operations.

**When to use it** : For workflows that combine several distinct steps, or meta-commands that coordinate other commands.

**Example** : This book's `/do` command orchestration (`.claude/commands/do.md`) demonstrates higher-order coordination by classifying user requirements and routing to appropriate expert domains. Workflow commands that call research, implement, and review commands in sequence also fit this level.
    
    
    # feature-workflow.md
    1. Call /research:gather-requirements $ARGUMENTS
    2. Call /plan:design-architecture
    3. Call /implement:build
    4. Call /review:validate

**Trade-offs** :

  * Pros: Compose complex behaviors from simpler parts. DRY.
  * Cons: Dependencies between commands. Harder to debug failures.



* * *

### Level 6: Self-Modifying

**What defines it** : Updates its own template based on outcomes or feedback.

**When to use it** : When a command should learn from its usage patterns and improve itself over time.

**Example** : The `*_improve.md` pattern seen in some agentic systems where commands track their failures and update their instructions.
    
    
    # adaptive-analyzer.md
    [CURRENT TEMPLATE]
    Analyze code for: ${FOCUS_AREAS}
     
    [IMPROVEMENT MECHANISM]
    After each run:
    - If analysis missed issues: add to FOCUS_AREAS
    - If too verbose: add to SUPPRESS_PATTERNS
    - Update this template

**Trade-offs** :

  * Pros: Commands get better with use. Adapt to project needs.
  * Cons: Non-deterministic. Can drift from original intent. Needs safeguards.



* * *

### Level 7: Meta-Cognitive

**What defines it** : Improves other commands, not just itself. Operates on the command system as a whole.

**When to use it** : For maintenance and evolution of the command ecosystem. Quality assurance for prompts.

**Example** : A bulk-update orchestrator that analyzes all commands and suggests improvements, or a command that identifies redundant commands and proposes consolidation.
    
    
    # command-optimizer.md
    1. Scan all .md commands in .claude/
    2. Identify patterns:
       - Duplicated logic
       - Commands that could be parameterized
       - Missing error handling
    3. Generate improvement proposals
    4. Execute approved updates

**Trade-offs** :

  * Pros: System-wide optimization. Maintains command quality.
  * Cons: Highest complexity. Requires understanding of entire system. Risk of breaking changes.



* * *

## Choosing the Right Level

**Start at the lowest level that solves the problem.**

  * **Level 1-2** : Most commands should live here. Simple is better.
  * **Level 3** : Use sparingly. Often a sign you need multiple commands instead.
  * **Level 4** : Standard for project-aware tools. Worth the context-gathering cost.
  * **Level 5** : Good for defined workflows. Keep orchestration logic simple.
  * **Level 6** : Experimental. Needs monitoring and rollback capability.
  * **Level 7** : Rare. Usually for tooling teams or advanced automation.



**Signals you need a higher level:**

  * Creating many similar commands → Move from 1 to 2
  * Copy-pasting logic between commands → Move to 5
  * Manually tweaking commands after each use → Consider 6
  * Spending more time maintaining commands than using them → Consider 7



**Signals you're at too high a level:**

  * Can't predict what the command will do
  * Debugging takes longer than the command saves
  * Other developers avoid using it
  * You're the only one who understands it



**The maturity sweet spot** : Most systems should have a pyramid distribution:

  * Many Level 1-2 commands (foundation)
  * Some Level 3-4 commands (core workflows)
  * Few Level 5 commands (orchestration)
  * Rare Level 6-7 commands (if any)



* * *

## Engineer Leverage Progression

_[2026-04-11]_ : The seven levels above describe prompt artifact sophistication. A complementary dimension describes practitioner workflow sophistication — how an individual engineer's _framing_ of AI use changes as leverage increases. This axis is orthogonal: an engineer can write a structurally sophisticated L4-L5 prompt while still operating in a low-leverage framing. Liu's central observation names the gap precisely: "One engineer treats AI like a better search engine. The other treats AI like an entire engineering team working in concert."

Three stages characterize the progression, observed independently by multiple practitioners:

### Stage 1 — Search-Engine Framing

**Framing:** AI as a better search interface or text transformer.

**Behavior:** Isolated, one-off queries. Context is provided per-query without codebase integration. Output is treated as reference material, not an executable artifact. Each query begins fresh with no compounding context.

**Prompt-level correlation:** Typically L1-L3. Parameterization adds flexibility, but the workflow remains point-to-point. A well-structured L4 prompt can appear in Stage 1 framing when the engineer pastes context manually without workflow integration.

**Named by:** Liu [1] — the "David" example: a meeting transcript pasted into a fresh session produces a plan disconnected from actual system architecture regardless of prompt quality.

**Key limitation:** No feedback loop. Each query begins fresh; there are no compounding returns.

### Stage 2 — Integrated Workflow Framing

**Framing:** AI as a pipeline stage whose output feeds subsequent stages.

**Behavior:** Complete context is provided — full meeting transcript plus codebase, not fragments. Output is designed for downstream consumption: PRD feeds tickets, tickets feed Plan.md, Plan.md feeds agentic execution. Humans design the workflow; AI executes stages within it.

**Prompt-level correlation:** Typically L4-L5. Contextual and higher-order prompts are structurally required by this framing — the workflow's pipeline structure forces L4+ because each stage must be informed by the previous stage's output.

**Named by:** Liu [1] — the "Elena" example: complete workflow from meeting to executable plan; Willison [7] — "lead on design, delegate on implementation."

**Key advancement:** Compounding context. Each stage's output enriches the next stage's input; returns accumulate across the pipeline.

### Stage 3 — System Designer Framing

**Framing:** AI as a component in a designed system with feedback loops, measurement, and self-improvement.

**Behavior:** Engineers define evaluation criteria before implementation. Error analysis precedes optimization. Measurement infrastructure — evals, tracing, human review — is designed first; automation of benchmarks follows manual understanding, not the reverse.

**Prompt-level correlation:** Typically L5-L7. Meta-cognitive prompts (Level 7) emerge from the demands of this framing: once an engineer treats the system as measurable, prompts that improve themselves become structurally necessary rather than optional.

**Named by:** Hamel [4][6] — manual error analysis is the highest-ROI starting point; "good writing is good thinking" — prompt engineering requires active intellectual engagement; Willison [7] — design decisions remain human before delegation to the system.

**Key advancement:** Feedback discipline. Improvement is systematic rather than intuitive; the measurement infrastructure determines what is worth optimizing.

* * *

Stage | Framing | Typical Prompt Level | Compounding Returns  
---|---|---|---  
Search-Engine | Query-response | L1-L3 | None — each query begins fresh  
Integrated Workflow | Pipeline stage | L4-L5 | Moderate — context accumulates across stages  
System Designer | Designed system with feedback | L5-L7 | High — measurement enables systematic improvement  
  
The stages correlate with but do not determine prompt level. An engineer can reach Stage 2 while using only L3-L4 prompts — the workflow framing will pull prompt sophistication upward as the engineer encounters the structural requirements of pipeline stages. Hamel's principle applies to the transition from Stage 2 to Stage 3: manual engagement precedes effective automation. Stage 3 cannot be reached by automating Stage 1 behaviors; the judgment about what to measure must be developed manually before measurement can compound.

Stage 2 integration maps directly to leverage points [#1 (ADWs) and #3 (Plans)](/agentic-engineering-book/1-foundations/1-twelve-leverage-points) in the Twelve Leverage Points hierarchy — the pipeline structure of Stage 2 is what makes Plans (#3) genuinely executable and ADWs (#1) designable rather than improvised. Stage 3 maps to #5 (Tests) and the measurement infrastructure that distinguishes production-grade from experimental systems. Stage 3 also corresponds to the individual prerequisite for operating at Shapiro Level 3-4 in the [Software Factories](/agentic-engineering-book/9-mental-models/7-software-factories) framework.

* * *

## Connections

  * **To[Prompt Structuring](/agentic-engineering-book/2-prompt/2-structuring):** Structural choices (output templates, failure sentinels, state machines) enable prompts to move up maturity levels—the techniques that make higher levels possible
  * **To[Self-Improving Experts](/agentic-engineering-book/7-patterns/2-self-improving-experts):** Self-modifying (Level 6) and meta-cognitive (Level 7) prompts parallel expert system evolution. The three-command expert pattern (Plan-Build-Improve) implements Level 6 maturity.
  * **To[Knowledge Evolution](/agentic-engineering-book/8-practices/6-knowledge-evolution):** Tracking prompt maturity progression mirrors knowledge base maturity—both evolve from simple to sophisticated through observation and refinement
  * **To[Twelve Leverage Points](/agentic-engineering-book/1-foundations/1-twelve-leverage-points):** The Engineer Leverage Progression stages map onto the leverage hierarchy: Stage 2 framing enables Plans (#3) and ADWs (#1); Stage 3 framing enables Tests (#5) and system-level measurement. The Anti-Patterns by Leverage Level section in that entry identifies the specific failure modes that Stage 1 framing produces when applied to high-leverage points.
  * **To[Evaluation](/agentic-engineering-book/8-practices/2-evaluation):** Prompt maturity and evaluation maturity co-evolve. Reaching Level 5+ prompt sophistication (higher-order, self-modifying) without corresponding evaluation infrastructure produces unmeasured complexity—changes to self-modifying prompts can degrade behavior in ways that only systematic evaluation detects. The Evaluation Maturity Curve in that section maps directly: Level 1–2 prompts (static, parameterized) pair with manual evaluation; Level 5+ prompts (higher-order, self-modifying) require at minimum scripted automated evaluation to remain maintainable.



[PreviousPit of Success](/agentic-engineering-book/9-mental-models/1-pit-of-success)[NextSpecs as Source Code](/agentic-engineering-book/9-mental-models/3-specs-as-source-code)

[](/)

[](/agentic-engineering-book)

[](https://github.com/jayminwest)

[LinkedIn](https://www.linkedin.com/in/jaymin-west/)

[youtube](https://www.youtube.com/@jaymin-west)

[](https://consulting.jayminwest.com)

[](https://www.skool.com/prompt-to-prod-9369)

[](https://drive.google.com/file/d/1zRVZ8q2swx0erClyknx4X3c4rNrdV-IS/view)
