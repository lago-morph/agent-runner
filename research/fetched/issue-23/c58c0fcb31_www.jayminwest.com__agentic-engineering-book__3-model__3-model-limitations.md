


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

# Model Limitations and Workarounds

Models have predictable failure modes. Recognition enables workarounds. Engineering around limitations is more productive than waiting for model improvements.

* * *

## Core Questions

### Mathematical Operations

  * Why do models fail at precise arithmetic?
  * When should calculation be delegated to tools?
  * How do you structure math-heavy workflows?



### Information Accuracy

  * What causes hallucination in agentic contexts?
  * How do verification tools reduce false information?
  * When should responses require citations?



### Context Management

  * How do context window limits affect reliability?
  * Why do early instructions fade in long conversations?
  * What's the optimal context utilization threshold?



### Instruction Adherence

  * Why do models drift from instructions over time?
  * How does reinforcement prevent degradation?
  * When should system prompts be repeated?



### Tool Interaction

  * What causes tool selection errors?
  * How do schemas reduce malformed parameters?
  * When should tool outputs be validated?



### Version Stability

  * Why do model upgrades break working implementations?
  * How does version pinning reduce risk?
  * What evaluation patterns catch behavioral changes?



* * *

## Math and Calculation Failures

Models struggle with precise arithmetic. Transformers are not optimized for exact computation—they excel at pattern recognition, not numeric precision.

**Observable behavior** : Multi-digit arithmetic, floating-point operations, and sequential calculations produce incorrect results with high confidence. The model may get 47 × 83 wrong while appearing certain of its answer.

### Workaround: Calculator Tools

Delegate numeric operations to external tools. Structure workflows so models set up problems and tools execute calculations.
    
    
    # Anti-pattern: Model does arithmetic
    """Calculate the total cost: 47 items at $83.27 each"""
    # Model output: "$3,923.69" (incorrect - should be $3,913.69)
     
    # Pattern: Tool-delegated calculation
    def calculate_total(items: int, price_per_item: float) -> float:
        """Precise calculation via tool."""
        return items * price_per_item
     
    # Model interprets request, calls tool with parameters
    # Tool returns: 3913.69
    # Model formats: "Total cost: $3,913.69"

**When to use** : Any workflow requiring exact numeric results—financial calculations, scientific computations, statistical analysis. Models can interpret requirements and format output; tools handle precision.

**Limitation scope** : Basic arithmetic, complex calculations, floating-point precision. Models can approximate, estimate, and reason about numbers—they cannot compute them reliably.

* * *

## Hallucination and Verification

Models confidently produce false information when they lack knowledge or misinterpret context. This is not a bug—it's fundamental to how language models work. They predict plausible text, not verified facts.

**Observable behavior** : When asked about obscure facts, recent events, or specific details outside training data, models generate plausible-sounding but incorrect responses. The confidence level gives no signal about accuracy.

### Workaround: Retrieval-Augmented Generation

Ground responses in retrieved sources. Require citations for factual claims. Structure prompts to separate retrieved information from generated analysis.
    
    
    # Pattern: RAG with citation requirements
     
    ## Instructions
    When answering factual questions:
    1. Search available knowledge sources
    2. Quote relevant passages verbatim
    3. Cite sources for all factual claims
    4. Distinguish between retrieved facts and inferences
     
    ## Output Format
    **Answer**: [response based on sources]
     
    **Sources**:
    - [Source 1]: "exact quote"
    - [Source 2]: "exact quote"
     
    **Inferences**: [reasoning based on sources]

**Implementation pattern** : Models call retrieval tools first, receive source documents, then synthesize responses with explicit source attribution. Downstream validation can check citations against sources.

**When to use** : Factual question-answering, documentation synthesis, research tasks, any scenario where accuracy matters more than creativity.

### Grounding Strategies

Approach | Use Case | Reliability Gain  
---|---|---  
**Citation required** | Factual claims | High—forces source grounding  
**Multi-source verification** | Critical facts | Very high—cross-reference detection  
**Structured retrieval** | Domain-specific knowledge | Medium—depends on source quality  
**Output validation** | Parseable results | High—catch formatting errors  
  
_[2025-12-10]_ : HumanLayer's ACE research (2025) demonstrated that retrieval-augmented approaches reduce hallucination rates by 60-80% in knowledge-intensive tasks. The key is not just retrieving context, but structuring prompts to make citation mandatory rather than optional.

* * *

## Context Window Limits

Models advertise 200K-1M token context windows. This doesn't mean all tokens are usable or that filling the window produces good results.

**Observable behavior** : Context utilization above 60% correlates with capability degradation. Output quality decreases, instruction adherence weakens, and error rates increase. Models exhibit recency bias—tokens near the end of context receive more weight than earlier tokens.

### The Capability-Capacity Tradeoff

_[2025-12-10]_ : Research across 50+ agent implementations shows consistent pattern: context fill inversely correlates with capability. A 60% full context window means 40% remaining capability, not 60% used resources.
    
    
    Context Utilization vs. Capability
    0%   ████████████████████  100% capable
    20%  ████████████████░░░░   80% capable
    40%  ████████████░░░░░░░░   60% capable
    60%  ████████░░░░░░░░░░░░   40% capable
    80%  ████░░░░░░░░░░░░░░░░   20% capable
    100% ░░░░░░░░░░░░░░░░░░░░    0% capable
    

As context fills, every token competes for attention. Signal-to-noise ratio degrades.

### Workaround: Strategic Context Placement

Place critical instructions at both the beginning and end of context. Repeat essential constraints periodically throughout long conversations.

**Pattern: Instruction anchoring**
    
    
    # System prompt (start of context)
    CRITICAL CONSTRAINT: All output must be valid JSON.
    Never include explanatory text outside the JSON structure.
     
    [... middle of context with tool outputs, file reads, etc. ...]
     
    # Reinforcement (before generation)
    REMINDER: Output must be valid JSON only.
    Format: {"status": "...", "result": "..."}

Repetition is not redundancy—it's strategic placement within the attention mechanism.

### Frequent Intentional Compaction

_[2025-12-10]_ : The standard pattern is to compact at 90%+ utilization as emergency response. Effective pattern: compact deliberately at 40-60% utilization, before quality degrades.

**Pattern: Proactive context management**
    
    
    Traditional (reactive):
    0% → 20% → 40% → 60% → 80% → 95% → COMPACT (emergency)
                                         └─> quality already degraded
    
    Effective (proactive):
    0% → 20% → 40% → COMPACT → 20% → 40% → COMPACT
                     └─> maintain quality throughout
    

Boot fresh instances when context grows unwieldy. Attempting to salvage degraded context through compression rarely succeeds.

**See Also** :

  * [Context Management Strategies](/agentic-engineering-book/4-context/2-context-strategies) — Detailed compaction patterns
  * [Context Fundamentals](/agentic-engineering-book/4-context/1-context-fundamentals) — Capability-capacity model



* * *

## Instruction Drift

Models forget or deviate from instructions over long interactions. This is not disobedience—it's attention dilution. As context fills with intermediate outputs, early instructions receive less weight in prediction.

**Observable behavior** : Agent starts strong, following instructions precisely. After 15-20 turns, output format changes, constraints are ignored, or the model introduces patterns explicitly forbidden in the original prompt.

### Workaround: Periodic Reinforcement

Restate critical instructions at regular intervals. Use system prompt anchoring for constraints that must never change.

**Pattern: Checkpoint verification**
    
    
    ## Workflow
    1. Parse input and validate
    2. **CHECKPOINT**: Verify output format requirements
    3. Execute task
    4. **CHECKPOINT**: Validate against constraints
    5. Format output (JSON only, no explanatory text)
    6. **CHECKPOINT**: Final validation before return

Each checkpoint reminds the model of essential constraints. The act of checking forces the instruction back into active attention.

### System Prompt Anchoring

Place immutable constraints in system prompts rather than user messages. Most implementations give system prompts higher attention weight.
    
    
    # System (high-attention position)
    ABSOLUTE CONSTRAINT: Output must be valid JSON.
    NEVER include text outside JSON structure.
    NEVER add explanatory preambles.
     
    # User message (task-specific)
    Analyze the file and return results.
    [specific task details...]

System prompts persist across the conversation. User messages accumulate and dilute attention.

* * *

## Tool Use Errors

Models select wrong tools or provide malformed parameters. Function calling is learned behavior, not guaranteed protocol.

**Observable behavior** : Given 20 available tools, model selects a search tool when a file read is needed. Or calls the correct tool but swaps parameter order. Or provides string where integer is required.

### Workaround: Constrained Schemas and Examples

Define strict JSON schemas for tool parameters. Provide concrete examples demonstrating correct usage patterns.

**Pattern: Tool definition with examples**
    
    
    {
      "name": "search_codebase",
      "description": "Search for patterns in project files",
      "parameters": {
        "type": "object",
        "properties": {
          "pattern": {"type": "string", "description": "Regex pattern to search"},
          "file_type": {"type": "string", "enum": ["py", "js", "ts", "md"]},
          "case_sensitive": {"type": "boolean", "default": false}
        },
        "required": ["pattern"]
      },
      "examples": [
        {
          "description": "Find TODO comments in Python files",
          "call": {
            "pattern": "TODO:",
            "file_type": "py",
            "case_sensitive": false
          }
        },
        {
          "description": "Search for exact function name",
          "call": {
            "pattern": "^def process_data\\(",
            "file_type": "py",
            "case_sensitive": true
          }
        }
      ]
    }

**Impact** : Internal testing at Anthropic showed tool call accuracy improvement from 72% → 90% when adding 3-5 concrete examples per tool. Examples teach usage patterns that schemas cannot express.

### Structured Outputs with Validation

Define exact output formats. Validate tool results before using them in subsequent reasoning.
    
    
    # Pattern: Output validation
    def validate_tool_output(result: dict, schema: dict) -> bool:
        """Verify tool output matches expected structure."""
        required_fields = schema.get("required", [])
        if not all(field in result for field in required_fields):
            return False
        # Type checking, range validation, etc.
        return True
     
    # In agent workflow:
    # 1. Model calls tool
    # 2. Tool returns result
    # 3. Validate result against schema
    # 4. If valid: proceed with result
    # 5. If invalid: retry with corrected parameters or abort

Validation catches errors before they cascade through multi-step workflows.

**See Also** :

  * [Tool Design](/agentic-engineering-book/5-tool-use/1-tool-design) — Tool description patterns and examples
  * [Tool Selection](/agentic-engineering-book/5-tool-use/2-tool-selection) — How naming and descriptions affect selection accuracy



* * *

## Model Upgrade Breakage

New model versions change behavior. What worked yesterday stops working today. This is inevitable—model improvements optimize for aggregate performance, not backward compatibility for specific prompts.

**Observable behavior** : Deploy Opus 4.5 to production. Agent completes tasks reliably. Update to Opus 4.6 when released. Same prompts, same tools, different behavior. Tool selection patterns change, output formats vary, previously reliable workflows fail.

### Workaround: Version Pinning

Pin to specific model versions in production. Test new versions in staging before promotion.

**Pattern: Explicit version control**
    
    
    # Production configuration
    MODEL_VERSION = "claude-opus-4.5-20251101"  # Pinned version
    # Not: "claude-opus-latest"
     
    # Staging configuration for testing
    STAGING_MODEL = "claude-opus-4.6-20251215"  # New version
     
    # Deployment process:
    # 1. Pin production to known-good version
    # 2. Test new version in staging
    # 3. Run regression suite
    # 4. If tests pass, promote new version to production
    # 5. Update production pin

Version pinning trades continuous improvement for stability. The choice depends on whether reliability or latest capabilities matter more.

### Regression Testing

Build evaluation suites that catch behavioral changes. Test not just outcomes but also the path taken—tool sequences, intermediate reasoning, output formats.

**Pattern: Behavioral regression tests**
    
    
    # Test case structure
    test_cases = [
        {
            "name": "file_search_workflow",
            "input": "Find all TODO comments in Python files",
            "expected_tools": ["search_codebase"],  # Which tools used
            "expected_params": {  # Parameter patterns
                "pattern": "TODO:",
                "file_type": "py"
            },
            "expected_format": "markdown_list",  # Output structure
            "min_results": 1
        }
    ]
     
    # Run suite on old and new model versions
    # Flag differences in:
    # - Tool selection patterns
    # - Parameter choices
    # - Output formatting
    # - Success rates

Regression tests don't prevent model changes—they surface the impact so informed decisions can be made about version upgrades.

_[2025-12-10]_ : Spotify's production agent infrastructure runs continuous regression testing against new model releases. Deployment decision: if new version scores >5% better on capability benchmarks but breaks <2% of existing workflows, upgrade proceeds with targeted prompt adjustments. If breakage exceeds 5%, upgrade deferred until prompts can be updated.

**See Also** :

  * [Evaluation](/agentic-engineering-book/8-practices/2-evaluation) — Building test suites for agent systems
  * [Model Selection](/agentic-engineering-book/3-model/1-model-selection) — When to upgrade vs. stay pinned



* * *

## Limitations Practitioners Are Waiting to Overcome

_[2025-12-10]_ : Current pain points observed across production implementations. These are not universal model failures—they represent the edge of current capability where workarounds are costly or incomplete.

### Reasoning Depth Limits

Multi-step planning remains unreliable past 7-10 sequential reasoning steps. Models can execute complex plans when structured externally (via prompts or orchestration), but generating such plans from scratch hits reliability walls.

**Current state** : Extended thinking (o1-style models) improves planning depth but at cost of latency and token consumption. The tradeoff: better reasoning requires more time and tokens.

**What's needed** : Reliable multi-step planning without 10x latency penalty.

### Consistent Output Formatting

Even with detailed format specifications, models occasionally insert preambles, add commentary, or alter structure. The failure rate is low (5-15% depending on model/prompt) but non-zero.

**Current state** : Output validation and retry loops catch most errors. Cost: additional latency and token usage for regeneration.

**What's needed** : Guaranteed format adherence, or at least predictable failure modes that can be programmatically detected before full generation.

### Long-Context Reasoning

Models can receive 200K+ token contexts but don't reason equally well across all tokens. Recency bias and attention dilution mean tokens at position 50,000 have less influence than tokens at position 150,000.

**Current state** : Strategic placement, repetition, and context compaction work around attention limits. Cost: manual context engineering for each use case.

**What's needed** : Uniform attention across full context window, or explicit control over attention weighting.

### Numerical Reasoning

Beyond basic arithmetic (already solved by calculator tools), some tasks require numerical intuition—understanding magnitude, interpolation, trend analysis. Models perform inconsistently.

**Current state** : Simple numeric comparisons work well. Complex numeric reasoning requires extensive examples or external computation.

**What's needed** : Better numeric intuition without requiring specialized tools for every calculation.

* * *

## Anti-Patterns

### Trusting Model Arithmetic

**What it looks like** : Agent performs financial calculations, cost estimation, or statistical analysis without external verification. Results are confidently wrong.

**Why it fails** : Models are not calculators. Arithmetic accuracy degrades with problem complexity. Floating-point operations are especially error-prone.

**Better approach** : Delegate all precise numeric operations to tools. Models interpret requirements and format results; tools compute values.

* * *

### Filling Context to Capacity

**What it looks like** : "We have a 200K token context window, so let's load 190K tokens of documentation, code, and examples. More context is better, right?"

**Why it fails** : Capability degrades with context fill. At 95% utilization, instruction adherence drops, output quality decreases, and error rates spike. The model has access to all the information but can't effectively use it.

**Better approach** : Target 40-60% context utilization. More headroom means better capability. If a task requires more context, restructure it—use retrieval tools, progressive disclosure, or multi-agent delegation.

**See Also** :

  * [Context Management Strategies](../4-context/2-context-strategies.md#frequent-intentional-compaction) — Proactive compaction pattern
  * [Pit of Success](/agentic-engineering-book/9-mental-models/1-pit-of-success) — Designing context as probability landscape



* * *

### Ignoring Version-Specific Behavior

**What it looks like** : Prompt works great in testing with Opus 4.5. Deploy to production using "latest" model version. When Opus 4.6 releases, behavior changes unexpectedly. Tool selection patterns shift, output formats vary, reliability drops.

**Why it fails** : Model updates optimize for aggregate performance, not backward compatibility with specific prompts. Version changes alter probability distributions—same input, different output.

**Better approach** : Pin production to specific model versions. Test new versions in staging with full regression suite before promotion. Understand exactly what changed and update prompts accordingly.

* * *

### Emergency Context Compaction

**What it looks like** : Agent runs until context reaches 95%+ capacity. Output degrades. Solution: compress context to free space, continue working.

**Why it fails** : Quality degradation happens before emergency compaction is triggered. Compressing degraded context doesn't restore lost capability—it preserves the mess.

**Better approach** : Compact proactively at 40-60% utilization, before quality drops. Better yet: scope tasks to fit comfortably within context budgets. If a task balloons, boot a fresh instance with tighter scope.

**See Also** :

  * [Context Management Strategies](../4-context/2-context-strategies.md#managing-context-window-limits) — When to boot vs. compact



* * *

### Assuming Bigger Model = Better Results

**What it looks like** : Task fails with Haiku. Switch to Sonnet without investigating why. Still unreliable. Escalate to Opus. Problem persists. Conclusion: "Even Opus can't do this."

**Why it fails** : Model capability isn't the only variable. Prompt structure, context quality, tool design, and task scope all affect reliability. Upgrading models without debugging other factors wastes capability and cost.

**Better approach** : Default to frontier models for initial development. When failures occur, debug systematically—check prompt clarity, context relevance, tool availability, output validation. Model upgrade is one possible solution, not the first resort.

**See Also** :

  * [Debugging Agents](../8-practices/1-debugging-agents.md#anti-pattern-blame-the-model) — Systematic debugging patterns
  * [Model Selection](1-model-selection.md#when-to-downgrade) — When model changes actually help



* * *

## Connections

  * **To[Tool Use](/agentic-engineering-book/5-tool-use/1-tool-design):** Tool design mitigates limitations—calculator tools solve math failures, retrieval tools reduce hallucination, structured schemas constrain tool use errors. Tool quality determines how effectively workarounds function.

  * **To[Context](/agentic-engineering-book/4-context/2-context-strategies):** Context management addresses window limits and instruction drift. Frequent compaction, strategic placement, and proactive context hygiene prevent degradation before it becomes emergency salvage.

  * **To[Evaluation](/agentic-engineering-book/8-practices/2-evaluation):** Regression testing catches version-specific behavior changes. Evaluation suites make model upgrades measurable decisions rather than blind deployments.

  * **To[Model Selection](/agentic-engineering-book/3-model/1-model-selection):** Understanding limitations informs when to downgrade (small model sufficient for constrained task) vs. when frontier models are necessary (complex reasoning, multi-step planning).

  * **To[Debugging Agents](/agentic-engineering-book/8-practices/1-debugging-agents):** Recognizing limitations prevents misdiagnosis—"model isn't capable" vs. "prompt isn't clear" vs. "context is polluted." Systematic debugging separates model limits from engineering errors.




[PreviousModel Behavior](/agentic-engineering-book/3-model/2-model-behavior)[NextMulti-Model Architectures](/agentic-engineering-book/3-model/4-multi-model-architectures)

[](/)

[](/agentic-engineering-book)

[](https://github.com/jayminwest)

[LinkedIn](https://www.linkedin.com/in/jaymin-west/)

[youtube](https://www.youtube.com/@jaymin-west)

[](https://consulting.jayminwest.com)

[](https://www.skool.com/prompt-to-prod-9369)

[](https://drive.google.com/file/d/1zRVZ8q2swx0erClyknx4X3c4rNrdV-IS/view)
