


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

# Foundations

Everything in agentic engineering flows from five interconnected pillars:

Pillar | Core Question  
---|---  
[Prompt](/2-prompt) | How to instruct the agent?  
[Model](/3-model) | What capabilities does the system provide?  
[Context](/4-context) | What information does the agent access?  
[Tool Use](/5-tool-use) | What actions can the agent take?  
[Harness](/6-harnesses) | What system orchestrates and constrains execution?  
  
This framing extends [agenticengineer.com](https://agenticengineer.com)'s "core four" with a fifth pillar: Harness. For a more granular hierarchy of intervention points, see the [Twelve Leverage Points](/agentic-engineering-book/1-twelve-leverage-points)—a framework that expands beyond the core five into architecture, workflows, and system-level concerns.

_[2026-04-12]_ : **Why Harness was added as a fifth pillar.** The original core four (Prompt, Model, Context, Tool Use) answered: what do you say, what brain do you use, what does it know, what can it do. A fifth question crystallized in early 2026: _what system orchestrates and constrains the agent's execution?_ Without a harness, there is no agent — only a model being prompted. Multiple authoritative practitioners converged on the formula `Agent = Model + Harness` within a 90-day window (Fowler, Raschka, Mollick, Hashimoto, Schmid), constituting a definitional crystallization event. Agent Psychometrics research (arXiv:2604.00594) formalized the independence: P(success) = σ(θ_LLM + θ_scaffold − β_difficulty), where harness quality and model quality contribute independently. Harness investment yields separable gains from model investment — meaning the fifth pillar carries foundational weight equal to the original four.

* * *

## The Pillars in Plain Language

Explaining agentic engineering in 60 seconds:

  * **Model** : The "brain" of the operation. Different models have varying levels of capability and intelligence.
  * **Context** : The "active memory"—what the agent has seen and can access during a session.
  * **Tools** : How agents take action. Reading and writing files, conducting web research, spawning subagents.
  * **Prompt** : The trigger that initiates model action. The interface between user (or system) and agent.
  * **Harness** : The execution environment that wraps the model—managing tool dispatch, context flow, safety enforcement, and loop control. Without a harness, a model produces text; with a harness, it completes tasks.



* * *

## How the Pillars Interact

The pillars are deeply interdependent:
    
    
    ┌──────────────────────────────────────────────────────┐
    │                      Harness                         │
    │                                                      │
    │   ┌─────────┐         ┌─────────┐                    │
    │   │ Prompt  │◄───────►│ Context │                    │
    │   └────┬────┘         └────┬────┘                    │
    │        │                   │                         │
    │        ▼                   ▼                         │
    │   ┌─────────┐         ┌─────────┐                    │
    │   │  Model  │◄───────►│ Tooling │                    │
    │   └─────────┘         └─────────┘                    │
    │                                                      │
    └──────────────────────────────────────────────────────┘
    

  * **The harness contains all four inner pillars** —it orchestrates prompt assembly, context management, model invocation, and tool dispatch as a unified execution environment
  * **Context fills as tools grow** —tool outputs consume context window space
  * **Context is treated differently by different models** —each model has its own strengths and quirks
  * **Certain models are better at tool calling** —capability varies significantly
  * **Prompting impacts how models react to their context and tools** —a prompt can intentionally disregard sections of context or available tools
  * **Harness quality is often the distinguishing factor** —apparent model quality differences frequently resolve to harness design differences (Raschka, 2026)



When one pillar changes, it ripples to the others:

  * **Downgrade the model** → massive performance impacts across the board
  * **Add more tools** → risk flooding the context window if not handled properly
  * **Alter context** → changes model behavior for that entire session, including tool usage
  * **Change the prompt** → can steer or override how the model interprets context and uses tools



* * *

## Is There a Hierarchy?

_[2025-12-10]_ : Until mid-2025, **model** sat at the top. The gap between state-of-the-art (SOTA) and other models was so large that model choice dominated outcomes.

_[2025-12-10]_ : The frontier narrowed through 2024. Claude 3.5 Sonnet (June 2024), Gemini 1.5 Pro, and GPT-4o compressed capability gaps. Differences between frontier models became less deterministic of outcomes. The other pillars now carry more weight:

  * **Tool use** is essential to any workflow that needs to take action. A model without tools produces analysis but cannot execute workflows.
  * **Context** alters the entire behavior of a model during a session.
  * **Prompting** determines the direction of the context window and model behavior.



_[2025-12-10]_ : Practical observation from production deployments: SOTA models provide superior outcomes across most tasks. The cost premium pays for itself through reduced iteration cycles and higher first-attempt success rates.

* * *

## How the Framework Has Evolved

_[2025-12-10]_ : Early LLMs (pre-2023) lacked tool use capabilities. GPT-3.5's function calling (June 2023) marked the transition to agentic systems. Claude 3 Opus demonstrated extended context windows (March 2024, 200k tokens). Each capability expansion required reevaluation of what agents could accomplish.

_[2025-12-10]_ : Current SOTA models (Claude 3.5 Sonnet, GPT-4o, Gemini 1.5 Pro) demonstrate capability across most coding tasks. Observable limitations center on context window constraints and tool availability rather than model intelligence.

* * *

## Common Mistakes

_[2025-12-10]_ : Observed patterns from new practitioners in agentic engineering:

  1. **Organization of information** —poor structure kills agent effectiveness. Unstructured context causes models to miss critical information.
  2. **Excessive trust in model outputs** —skipping verification leads to compounding errors in multi-step workflows.
  3. **Flooding context with unrelated tools** —unfocused agents waste tokens evaluating irrelevant options.
  4. **Using ad-hoc prompts with passive language** —vague instructions produce vague results.
  5. **Neglecting structure** in prompts, context, and tool responses—models perform better with consistent formatting.
  6. **Allowing too much freedom** —agents need constraints to succeed. Unbounded option spaces lead to analysis paralysis.
  7. **Insufficient instruction detail** —relying too heavily on agent discovery increases failure rates.
  8. **Failing to adhere to the[pit of success](/9-mental-models/1-pit-of-success) mindset**—making correct actions harder than incorrect ones.



_[2025-12-10]_ : Counter-intuitive finding: "more" does not equal better capability. More tools, more context, and more steering prompts degrade performance. **A focused agent is a productive agent.**

* * *

## Limits of the Framework

What this framework doesn't capture well:

  * **"Prompting" is too general.** It could mean sending ad-hoc "build me a website" prompts, or 2,500-line spec files that do cutting-edge engineering work. This distinction can be murky.



When the five-pillar lens has led astray:

  * The misconception that "more is better"—more tools, more context, more steering prompts. This floods agents and degrades performance.



* * *

## Connections

  * **To[Prompt](/2-prompt):** Prompts serve as the primary interface for instructing agents. Prompt design determines how effectively agents can parse instructions and structure their outputs. Poor prompt structure undermines gains from better models or tools.

  * **To[Model](/3-model):** Model selection defines the ceiling of agent capability. Different models excel at different tasks—tool calling, reasoning, code generation. Understanding model characteristics allows matching capability to task requirements.

  * **To[Context](/4-context):** Context management determines what information agents can access during execution. Context window constraints force tradeoffs between comprehensiveness and focus. Effective context strategies prevent information loss while avoiding token waste.

  * **To[Tool Use](/5-tool-use):** Tools translate agent intelligence into action. Well-designed tools provide clear interfaces and reliable outputs. Tool selection and restriction patterns shape what agents can accomplish and how efficiently they work.

  * **To[Harness](/6-harnesses):** The harness is the execution environment that wraps and coordinates the other four pillars. It handles tool dispatch, context management, safety enforcement, and loop control. `Agent = Model + Harness` — without the harness, the other pillars produce text rather than completed tasks.




[NextTwelve Leverage Points of Agentic Coding](/agentic-engineering-book/1-foundations/1-twelve-leverage-points)

[](/)

[](/agentic-engineering-book)

[](https://github.com/jayminwest)

[LinkedIn](https://www.linkedin.com/in/jaymin-west/)

[youtube](https://www.youtube.com/@jaymin-west)

[](https://consulting.jayminwest.com)

[](https://www.skool.com/prompt-to-prod-9369)

[](https://drive.google.com/file/d/1zRVZ8q2swx0erClyknx4X3c4rNrdV-IS/view)
