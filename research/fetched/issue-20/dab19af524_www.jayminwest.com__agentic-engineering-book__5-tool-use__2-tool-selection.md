


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

# Tool Selection and Routing

The agent has twenty tools available. Selection accuracy directly impacts task completion. When selection fails, the issue is typically unclear tool descriptions or too many similar-looking options.

* * *

## Your Mental Model

**Tool selection is prompt-driven reasoning.** The model doesn't "route" based on keywords—it reads tool descriptions and parameters like instructions, then decides which matches the task at hand. Poor selection usually means unclear tool descriptions or too many similar-looking options.

* * *

## Selection Mechanisms

### Description-Based Selection

The agent reads tool names and descriptions, matching them to the task requirements. This means:

  * Tool names matter: `search_codebase` is clearer than `finder_v2`
  * Descriptions must distinguish similar tools: "Search git history" vs. "Search current files"
  * Parameter schemas signal intent: required `query` parameter suggests search-like behavior



### Context-Driven Filtering

Some patterns reduce the selection space:

  * **Role-based restrictions** : Scout agents only see read-only tools (see [Tool Restrictions](/agentic-engineering-book/5-tool-use/3-tool-restrictions))
  * **Dynamic discovery** : Rarely-used tools hidden until search reveals them (see [Scaling Tools](/agentic-engineering-book/5-tool-use/4-scaling-tools))
  * **Skill activation** : Temporary tool access when domain-specific mode activates (see [Skills](/agentic-engineering-book/5-tool-use/5-skills-and-meta-tools))



* * *

## Common Selection Failures

### Overlapping Functionality

**Problem** : Two tools do similar things with subtle differences. Agent picks randomly.

**Example** :

  * `read_file` \- Reads entire file
  * `read_file_section` \- Reads specific lines



If descriptions don't clarify when to use each, the agent struggles.

**Fix** : Make the distinction explicit in descriptions:

  * "Read entire file (use for files <500 lines)"
  * "Read specific section by line numbers (use for large files or targeted inspection)"



### Too Many Options

**Problem** : 50+ tools overwhelm the selection process. Agent either picks wrong tool or spends excessive tokens evaluating options.

**Fix** : Use dynamic discovery (see [Scaling Tools](/agentic-engineering-book/5-tool-use/4-scaling-tools)) or role-based filtering to reduce visible tool count.

### Vague Descriptions

**Problem** : Tool description doesn't explain when NOT to use the tool.

**Example** : "Searches the database" - for what? Structured queries? Full-text search? Recent records?

**Fix** : Add context and boundaries:

  * "Searches database via SQL queries. Use for structured lookups by ID, date range, or indexed fields. For full-text search, use `search_documents` instead."



* * *

## Improving Selection Accuracy

### Distinctive Naming

Use domain-specific prefixes when managing tool groups:

  * `git_commit`, `git_push`, `git_log` (clear grouping)
  * Not: `commit`, `push`, `log` (ambiguous without context)



### Comparison Tables in Context

When tools have overlapping use cases, provide selection guidance:
    
    
    | Tool | Use When | Don't Use When |
    |------|----------|----------------|
    | `search_files` | Finding files by name/path | Searching file contents |
    | `grep_contents` | Searching within files | Finding files by name |

This can go in the main system prompt or in tool descriptions themselves.

### Constrain When Appropriate

**Don't default to "give the agent everything."** If a build agent doesn't need database access, don't provide database tools. Fewer tools = better selection.

* * *

## Leading Questions

  * How do you measure tool selection accuracy in production?
  * When should you merge similar tools vs. keep them separate?
  * How does prompt caching affect tool selection overhead?
  * What's the relationship between tool count and inference latency?
  * Can you predict which tools an agent will struggle to select?



* * *

## Connections

  * **To[Tool Design](/agentic-engineering-book/5-tool-use/1-tool-design):** Design determines selectionability
  * **To[Tool Restrictions](/agentic-engineering-book/5-tool-use/3-tool-restrictions):** Restrictions are a selection optimization
  * **To[Scaling Tools](/agentic-engineering-book/5-tool-use/4-scaling-tools):** Large tool sets require selection strategies
  * **To[Prompt](/agentic-engineering-book/2-prompt):** Tool descriptions follow prompt design principles



[PreviousTool Design](/agentic-engineering-book/5-tool-use/1-tool-design)[NextTool Restrictions and Security](/agentic-engineering-book/5-tool-use/3-tool-restrictions)

[](/)

[](/agentic-engineering-book)

[](https://github.com/jayminwest)

[LinkedIn](https://www.linkedin.com/in/jaymin-west/)

[youtube](https://www.youtube.com/@jaymin-west)

[](https://consulting.jayminwest.com)

[](https://www.skool.com/prompt-to-prod-9369)

[](https://drive.google.com/file/d/1zRVZ8q2swx0erClyknx4X3c4rNrdV-IS/view)
