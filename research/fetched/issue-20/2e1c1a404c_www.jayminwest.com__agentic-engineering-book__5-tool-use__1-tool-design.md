


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

# Tool Design

Well-designed tools make the difference between an agent that can accomplish tasks and one that constantly struggles with its own interface.

* * *

## Tool Examples as Design Pattern

_[2025-12-09]_ : JSON schemas define structural validity but can't teach usage—that's what examples are for.

**The Gap** : Schemas tell the model what parameters exist and their types, but not:

  * When to include optional parameters
  * Which parameter combinations make sense together
  * API conventions not expressible in JSON Schema



**The Pattern** : Provide 1-5 concrete tool call examples demonstrating correct usage at varying complexity levels.

**Example Structure** (for a support ticket API):

  1. **Minimal** : Title-only task—shows the floor
  2. **Partial** : Feature request with some reporter info—shows selective use
  3. **Full** : Critical bug with escalation, full metadata—shows the ceiling



This progression teaches when to use optional fields, not just that they exist.

**Results** : Internal testing showed accuracy improvement from 72% → 90% on complex parameter handling.

**Best Practices** :

  * Use realistic data, not placeholder values ("John Doe", not "{name}")
  * Focus examples on ambiguity areas not obvious from schema alone
  * Show the minimal case first—don't always demonstrate full complexity
  * Keep examples concise (1-5 per tool, not 20)



**See Also** :

  * [Prompt: Structuring](/agentic-engineering-book/2-prompt/2-structuring) — How tool examples relate to broader prompt design principles



**Source** : [Advanced Tool Use - Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)

* * *

## Rich User Questioning Patterns

_[2026-01-30]_ : Orchestration research from cc-mirror reveals sophisticated user clarification patterns that replace text-based menus with rich, decision-guiding question structures.

### Philosophy: Users Need to See Options

**Core insight:** "Users don't know what they want until they see the options"

Asking "What should I prioritize?" yields vague answers. Showing 4 options with descriptions, trade-offs, and recommendations enables informed decisions.

### The 4×4 Maximal Pattern

**Structure:**

  * 4 questions addressing different decision dimensions
  * 4 options per question with rich descriptions
  * Trade-offs and implications explicit
  * Recommended option guides optimal choice
  * Multi-select support when appropriate



**Example: Feature Implementation Scope Clarification**
    
    
    AskUserQuestion(
        questions=[
            {
                "text": "What's the primary goal?",
                "options": [
                    {
                        "label": "Performance optimization",
                        "description": "Focus on speed and efficiency. May increase code complexity and require more thorough testing.",
                        "recommended": True
                    },
                    {
                        "label": "Code simplicity",
                        "description": "Prioritize readability and maintainability over raw speed. Easier onboarding, longer execution time."
                    },
                    {
                        "label": "Feature completeness",
                        "description": "Cover all edge cases and scenarios. Comprehensive but longer timeline. Best for user-facing features."
                    },
                    {
                        "label": "Quick MVP",
                        "description": "Fast delivery with core features only. Technical debt acceptable. Good for validation before full build."
                    }
                ]
            },
            {
                "text": "How should we handle errors?",
                "options": [
                    {
                        "label": "Fail fast with clear messages",
                        "description": "Immediate error visibility. Easier debugging but more interruptions. Good for development."
                    },
                    {
                        "label": "Graceful degradation",
                        "description": "Continue operation with reduced functionality. Better UX but errors may go unnoticed."
                    },
                    {
                        "label": "Retry with exponential backoff",
                        "description": "Automatic recovery from transient failures. Adds complexity and potential latency."
                    },
                    {
                        "label": "Log and continue",
                        "description": "Silent failure recovery. Best for non-critical paths. Risk of hidden issues accumulating."
                    }
                ]
            },
            {
                "text": "What testing level?",
                "options": [
                    {
                        "label": "Unit tests only",
                        "description": "Fast feedback, isolated verification. Misses integration issues. Good for pure logic."
                    },
                    {
                        "label": "Integration tests",
                        "description": "Verify component interactions. Slower but catches real-world failures. Recommended for APIs."
                    },
                    {
                        "label": "Full E2E suite",
                        "description": "Complete user flow validation. Highest confidence but longest execution. Expensive to maintain."
                    },
                    {
                        "label": "Manual testing",
                        "description": "Skip automated tests initially. Fast development but manual verification burden. Technical debt."
                    }
                ]
            },
            {
                "text": "Deployment strategy?",
                "options": [
                    {
                        "label": "Feature flag rollout",
                        "description": "Deploy to all, enable gradually. Instant rollback. Requires flag infrastructure."
                    },
                    {
                        "label": "Canary deployment",
                        "description": "Small user percentage first. Catch issues early. Needs monitoring and rollback automation."
                    },
                    {
                        "label": "Blue-green deployment",
                        "description": "Full environment switch. Zero downtime. Doubles infrastructure cost temporarily."
                    },
                    {
                        "label": "Direct deployment",
                        "description": "Immediate production rollout. Fastest but highest risk. Acceptable for low-traffic features."
                    }
                ]
            }
        ]
    )

### Anti-Pattern: Text-Based Menus

**Avoid:**
    
    
    Please choose:
    1. Fast
    2. Cheap
    3. Good quality
    
    Which do you prefer?
    

**Problems:**

  * No context about trade-offs
  * Binary thinking (can't combine attributes)
  * Vague options without implications
  * No guidance toward optimal choice



### When to Use Maximal Questions

**Good fit:**

  * Request admits multiple valid interpretations
  * Choices meaningfully affect implementation approach
  * Actions carry risk or are difficult to reverse
  * User preferences influence trade-offs
  * Scope clarification prevents rework



**Poor fit:**

  * Decisions are obvious from context
  * Only one reasonable approach exists
  * User already provided detailed requirements
  * Questions would annoy rather than clarify



### Implementation Guidelines

**Option descriptions should include:**

  1. What this choice means concretely
  2. Primary trade-off or cost
  3. When this choice makes sense
  4. What happens if this choice is wrong



**The recommended flag signals:**

  * Optimal choice given typical constraints
  * Not forcing—user can override
  * Guides users unfamiliar with domain



**Multi-select enables:**

  * "Performance AND simplicity" combinations
  * "All of these except X" selections
  * Prioritization without forced ranking



**Sources:** [cc-mirror orchestration tools](https://raw.githubusercontent.com/numman-ali/cc-mirror/main/src/skills/orchestration/references/tools.md), [AskUserQuestion pattern documentation](https://raw.githubusercontent.com/numman-ali/cc-mirror/main/src/skills/orchestration/SKILL.md)

* * *

## Coding Agent Edit Formats

_[2026-04-11]_ : Edit format selection is a first-order tool design decision for coding agents — one with direct consequences for model error rates, output size, and edit application reliability. The choice is model-capability-driven, not aesthetic.

### Three Primary Format Archetypes

Format | Mechanism | Cognitive Load on Model | Production Evidence  
---|---|---|---  
**Whole-file rewrite** | Model returns complete updated file | Low — no line number tracking required | Reliable; expensive for large files  
**Unified diff (udiff)** | Standard diff format with `+`/`-` line prefixes | High — requires tracking original line numbers before writing new code | Used for legacy models with "lazy coding" tendency  
**Search-replace blocks** | Model specifies exact text to find and exact replacement text | Medium — no line numbers; exact string matching | Most models in production; Aider's primary format  
  
The cognitive load distinction is significant. Unified diff requires the model to know the line count of original content _before_ writing new code — a constraint that causes errors on complex edits. Search-replace blocks avoid this by using content identity rather than position. Whole-file rewrites sidestep both constraints at the cost of output token volume.

### Model-Capability-Driven Format Selection

Aider's production documentation provides the most concrete evidence available for model-specific format selection:

Model Family | Recommended Format | Reason  
---|---|---  
Most modern models (Claude, GPT-4o, Gemini 1.5+) | Search-replace (`diff`) | Reliable exact-match application; balanced output size  
Gemini models (older) | `diff-fenced` (path inside fence) | Standard fencing syntax failed consistently  
GPT-4 Turbo | `udiff` | Mitigated "lazy coding" — replacing implementation with placeholder comments  
Architect mode tasks | `editor-diff` / `editor-whole` | Streamlined for multi-file operations in a separate editor model  
  
**The practical implication:** format choice is not a configuration detail — it is a tool design decision that affects model reliability at the task level. When a model produces incorrect edits, audit the edit format before adjusting the prompt.

### Poka-Yoke Constraints for Coding Tools

Anthropic's SWE-bench implementation provides a concrete example of constraint-based tool design: converting relative to absolute filepaths as a required tool input. The result was measurable reduction in model path errors — the tool became harder to use incorrectly.

**The principle:** coding agent tools benefit from constraints that prevent common model errors:

  * Require absolute paths (eliminates relative-path resolution errors)
  * Require exact string matching in search-replace (prevents approximate matches that corrupt context)
  * Validate that referenced line numbers exist before executing edits (prevents off-by-one failures)



These are not validation afterthoughts — they are design decisions that change model behavior by making the wrong action structurally difficult.

**Sources:** [Aider Edit Formats](https://aider.chat/docs/more/edit-formats.html), [Building Effective Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents), [Components of a Coding Agent — Raschka](https://magazine.sebastianraschka.com/p/components-of-a-coding-agent) (2026-04-04)

* * *

## Coding Agent Tool Inventory

_[2026-04-11]_ : Coding agents use a recurring, minimal tool set. Raschka identifies the baseline as five named tools; Anthropic's SWE-bench work extends this with patch-application tools. Understanding the canonical inventory prevents over-engineering the tool layer.

### Standard Inventory

Tool | Role | Notes  
---|---|---  
`read_file` | Retrieve file content for context | Prefer whole-file for small files; line-range for large  
`write_file` / `apply_edit` | Persist changes to disk | Format depends on edit format choice (see above)  
`search` / `grep` | Find symbols, patterns, references across the repo | Critical for navigation without full-file reads  
`bash` / `shell` | Run commands, tests, linters, build tools | Primary execution feedback mechanism  
`list_files` / `ls` | Directory traversal and discovery | Supports repo orientation without reading every file  
  
Claude Code adds a sixth functional layer via hooks — pre/post action enforcement that operates outside the agent's direct tool calls. This is best understood as a meta-tool: it applies constraints and side effects that the agent cannot disable.

**Minimum viable set for most coding tasks:** `read_file`, `write_file`, `bash`, `search`. The other tools improve efficiency but are not required for correctness on small codebases.

**Sources:** [Components of a Coding Agent — Raschka](https://magazine.sebastianraschka.com/p/components-of-a-coding-agent) (2026-04-04), [Building Effective Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)

* * *

## Leading Questions

  * How do you write tool descriptions that work for both humans and LLMs?
  * When should you split one complex tool into multiple simple ones?
  * What parameters should be required vs. optional? How do you decide?
  * How do naming conventions affect tool selection accuracy?
  * What makes a tool description actionable vs. confusing?



* * *

## Connections

  * **To[Tool Selection](/agentic-engineering-book/5-tool-use/2-tool-selection):** Design choices directly impact selection accuracy
  * **To[Prompt](/agentic-engineering-book/2-prompt):** Tool descriptions are prompts themselves—see [Model-Invoked vs. User-Invoked Prompts](../2-prompt/_index.md#model-invoked-vs-user-invoked-prompts)
  * **To[Scaling Tools](/agentic-engineering-book/5-tool-use/4-scaling-tools):** Good design becomes critical when managing dozens of tools
  * **To[Orchestrator Pattern](/agentic-engineering-book/7-patterns/3-orchestrator-pattern):** AskUserQuestion maximal pattern demonstrates rich clarification as coordination tool. Orchestrators use structured questioning before delegation to absorb complexity and radiate simplicity.
  * **To[ReAct Pattern](/agentic-engineering-book/7-patterns/5-react-pattern):** Edit format choice directly affects observation quality in coding agent loops. Search-replace formats produce cleaner, verifiable observations than whole-file rewrites.



[PreviousTool Use](/agentic-engineering-book/5-tool-use)[NextTool Selection and Routing](/agentic-engineering-book/5-tool-use/2-tool-selection)

[](/)

[](/agentic-engineering-book)

[](https://github.com/jayminwest)

[LinkedIn](https://www.linkedin.com/in/jaymin-west/)

[youtube](https://www.youtube.com/@jaymin-west)

[](https://consulting.jayminwest.com)

[](https://www.skool.com/prompt-to-prod-9369)

[](https://drive.google.com/file/d/1zRVZ8q2swx0erClyknx4X3c4rNrdV-IS/view)
