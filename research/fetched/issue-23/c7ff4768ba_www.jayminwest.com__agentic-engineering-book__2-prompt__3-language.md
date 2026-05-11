


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

# Prompt Language

The specific words, grammar, and sentence structure used in prompts significantly impact agent behavior. Language choice affects how models parse instructions, interpret constraints, and generate output. This chapter examines evidence-grounded linguistic patterns that improve prompt effectiveness.

* * *

## Verb Semantics

The verbs chosen for instructions shape model behavior more than most other linguistic elements.

### Declarative vs. Imperative

Recent research reveals that verb mood (declarative vs. imperative) affects reasoning quality differently based on task type.

**Declarative statements** describe facts or states without issuing direct commands:
    
    
    The output follows JSON schema format.
    Analysis identifies security vulnerabilities.
    Test coverage reaches 80% minimum.
    

**Imperative commands** issue direct instructions:
    
    
    Format output as JSON schema.
    Identify security vulnerabilities.
    Achieve 80% test coverage.
    

**Evidence from SatLM Study (arxiv:2305.09656):**

The SatLM research tested declarative vs. imperative prompts across multiple reasoning benchmarks. Results showed **declarative prompts outperform imperatives by ~23%** on complex reasoning tasks like logical inference and mathematical problem-solving.

The researchers hypothesize this occurs because declarative framing encourages models to construct internal representations of the desired state, rather than executing procedural steps. For reasoning-heavy tasks, state-based thinking appears more effective than step-based execution.

### Task-Type Dependency

Verb mood effectiveness varies by task category:

Task Type | Preferred Mood | Example | Rationale  
---|---|---|---  
Reasoning | Declarative | "The solution minimizes edge cases" | Encourages state-based thinking  
Sequential | Imperative | "Parse input, validate schema, return result" | Clear procedural steps  
Tool-Calling | Imperative | "Search codebase for references" | Direct action invocation  
Creative | Declarative | "The narrative maintains consistent tone" | Establishes constraints without rigidity  
  
**Implementation Guidance:**

For multi-phase workflows, use declarative framing for high-level goals and imperative for operational steps:
    
    
    ## Goal (Declarative)
    The implementation meets these criteria:
    - Code follows existing patterns
    - Changes preserve backward compatibility
    - Test coverage validates edge cases
     
    ## Workflow (Imperative)
    1. Read existing implementation files
    2. Identify integration points
    3. Implement changes following detected patterns
    4. Run test suite and verify coverage

### Hierarchical Verb Progression

Complex tasks benefit from verb hierarchies that structure reasoning:
    
    
    # Shallow (single-level)
    Analyze the code for bugs.
     
    # Hierarchical (multi-level)
    1. Analyze the codebase structure
    2. Extract component dependencies
    3. Identify potential failure points
    4. Update documentation with findings

The hierarchical approach creates explicit intermediate steps, reducing cognitive load and improving output quality. Research on chain-of-thought prompting suggests that visible reasoning steps improve accuracy, even when the model already performs implicit reasoning.

### Bare Imperatives vs. Hedged Requests

Frontier models parse bare imperatives more reliably than hedged phrasing:
    
    
    # Effective (bare imperative)
    Validate input before processing.
     
    # Ineffective (hedged request)
    Could you maybe try to validate the input if possible?

Hedging introduces ambiguity. The model must interpret whether "could you" is requesting permission, suggesting optionality, or emphasizing importance. Bare imperatives eliminate this ambiguity.

**Exception:** When genuine optionality exists, use conditional phrasing explicitly:
    
    
    If input validation fails, attempt recovery.
    If recovery succeeds, continue processing.
    If recovery fails, halt and report error.

* * *

## Specificity Calibration

Modern frontier models (GPT-4.1, Claude 3.5+, Gemini 2.0) follow instructions with high literal fidelity. This shifts optimal prompting strategy toward greater specificity.

### Literal Interpretation Behavior

_[2025-12-26]_ : Earlier models (GPT-3.5, Claude 2.x) often inferred implicit requirements. Frontier models require explicit specification. Example:
    
    
    # Implicit (worked on older models)
    Create a React component for user profiles.
     
    # Explicit (required for frontier models)
    Create a React component for user profiles that:
    - Accepts userId prop
    - Fetches user data from /api/users/:id
    - Displays loading state during fetch
    - Handles error state with retry button
    - Uses TypeScript with proper types
    - Follows existing component patterns in src/components/

The older implicit prompt relied on the model filling gaps with "reasonable defaults." Frontier models skip inference and implement only what's explicitly stated, often asking clarifying questions when requirements are ambiguous.

### The DETAIL Framework

Research by arxiv:2512.02246 examined specificity impact across task categories:

Task Category | Specificity Gain | Details  
---|---|---  
Mathematical | +0.47 accuracy | Step-by-step constraints, intermediate validation  
Decision-Making | +0.02 accuracy | Minimal benefit from added detail  
Code Generation | +0.31 accuracy | API signatures, error handling, test requirements  
Creative Writing | -0.12 quality | Over-specification reduces natural flow  
  
**Goldilocks Principle:** Specificity helps when tasks have objective correctness criteria. Over-specification harms tasks requiring creative flexibility.

**Calibration Strategy:**

Be specific on:

  * Required output format (schema, structure, delimiters)
  * Constraints and boundaries (what NOT to do)
  * Success criteria (how to know when done)
  * External dependencies (APIs, file paths, data sources)



Remain flexible on:

  * Implementation approach (unless patterns must be followed)
  * Intermediate reasoning steps (unless chain-of-thought required)
  * Stylistic choices within defined boundaries



### Optimal Prompt Length

Google research on prompt optimization found **~21 words (with context)** as optimal length for many tasks. This metric combines:

  * Instruction clarity (enough words to be unambiguous)
  * Cognitive load (few enough to parse easily)
  * Context efficiency (leaves room for examples/data)



This isn't a hard rule—complex tasks require longer prompts. The finding suggests that concise, precise language outperforms verbose explanations.

**Anti-Pattern:**
    
    
    So basically what I'm trying to say is that the output should be formatted
    in a way that makes it easy to parse, like maybe JSON or something similar,
    because we need to be able to process it downstream, and it would be really
    helpful if you could make sure it's valid JSON...

**Better:**
    
    
    Output valid JSON matching this schema: {schema}

The anti-pattern uses 47 words to convey what the better version states in 7.

* * *

## Constraint Framing

How constraints are phrased significantly impacts adherence and agent behavior.

### The Pink Elephant Problem

InstructGPT research revealed that **negative constraints backfire at scale**. When prompts say "never do X," models become more likely to do X as conversation length increases.

The hypothesis: negative phrasing creates semantic association. The model must represent the forbidden action to understand the constraint, increasing activation of that concept in its attention mechanism.

**Evidence:** 16x.engineer analysis showed **performance degradation with negative constraints** in long-context scenarios. Prompts with "NEVER use global variables" produced more global variable usage than prompts without the constraint.

### Positive Constraint Reformulation

Convert negative constraints to positive requirements:

Negative (Backfires) | Positive (Effective)  
---|---  
Never use global state | Use dependency injection for state management  
Don't expose internal errors | Return user-friendly error messages  
Never modify files without reading | Read file contents before editing  
Don't create new patterns | Follow existing patterns in the codebase  
  
The positive version specifies desired behavior rather than forbidden behavior, avoiding semantic activation of the unwanted pattern.

### Permission Hierarchy Pattern

For complex constraint systems, use explicit permission hierarchies:
    
    
    ## Constraint Hierarchy (highest priority first)
     
    **PRESERVE (always maintain):**
    - Existing API contracts
    - Backward compatibility
    - Test coverage levels
     
    **APPEND (add when needed):**
    - New functionality
    - Documentation updates
    - Additional test cases
     
    **REMOVE (only if explicit criteria met):**
    - Deprecated code (marked deprecated >6 months)
    - Unused imports (verified by static analysis)
    - Redundant comments (outdated or obvious)
     
    **NEVER:**
    - Breaking changes without migration path
    - Reducing test coverage
    - Exposing security vulnerabilities

This hierarchy provides clear decision rules. The agent knows what takes precedence when constraints conflict.

### Constraint Ordering Effects

Constraint placement affects adherence:

**Most effective ordering:**

  1. Critical/blocking constraints first
  2. Important guidelines second
  3. Stylistic preferences last


    
    
    # CRITICAL CONSTRAINTS - NEVER VIOLATE
    - Zero data loss
    - Maintain authentication/authorization
    - Pass all existing tests
     
    # IMPORTANT GUIDELINES
    - Follow existing code patterns
    - Add tests for new functionality
    - Update documentation
     
    # STYLE PREFERENCES
    - Use TypeScript strict mode
    - Prefer functional patterns
    - Keep functions under 50 lines

The model weights earlier content more heavily. Placing critical constraints first ensures they receive maximum attention.

* * *

## Structural Language Patterns

The delimiters and formatting conventions used in prompts affect parsing and adherence.

### Model-Specific Delimiter Preferences

**Claude (Anthropic):**

  * **Primary:** XML-style tags (`<instructions>`, `<context>`, `<examples>`)
  * **Rationale:** Claude's training included explicit XML parsing. Documentation confirms preferential handling.
  * **Example:**


    
    
    <task>
    Analyze the codebase for security issues.
    </task>
     
    <constraints>
    Focus on authentication and authorization.
    Report severity levels: critical, high, medium, low.
    </constraints>
     
    <output_format>
    JSON array of findings with: file, line, severity, description.
    </output_format>

**GPT (OpenAI):**

  * **Primary:** Markdown headers (`###`), horizontal rules (`---`), code fences (`````)
  * **Rationale:** OpenAI's documentation emphasizes Markdown. Models parse it reliably.
  * **Example:**


    
    
    ### Task
    Analyze the codebase for security issues.
     
    ---
     
    ### Constraints
    - Focus on authentication and authorization
    - Report severity levels: critical, high, medium, low
     
    ---
     
    ### Output Format
    ```json
    [
      {"file": "...", "line": 0, "severity": "...", "description": "..."}
    ]
    
    
    **Format variance impact:** Research shows **up to 40% accuracy variance** in smaller models based solely on delimiter choice. Frontier models are more robust but still show preference-based performance differences.
    
    ### Recommended Structural Order
    
    Consistent section ordering improves instruction adherence:
    
    1. **Context** - Background information needed
    2. **Task** - What to accomplish
    3. **Constraints** - Boundaries and restrictions
    4. **Output Format** - Expected structure/schema
    5. **Examples** - Concrete demonstrations (if needed)
    
    This order mirrors natural cognitive processing: understand situation → understand goal → understand limits → understand success criteria → see examples.
    
    ---
    
    ## Role and Persona Framing
    
    Role-based prompting (e.g., "You are an expert security engineer") remains common despite mixed evidence.
    
    ### Persona Effectiveness Research
    
    EMNLP 2024 study (arxiv:2311.10054) tested 162 different personas across 2,410 questions:
    
    **Key Finding:** Personas "do not improve performance" on factual or reasoning tasks. In 30% of cases, persona framing **decreased accuracy**.
    
    **Why personas fail:**
    - Irrelevant details compete for attention in context window
    - Models lack internal role-based reasoning pathways
    - Persona details can introduce biased reasoning patterns
    
    **When personas help:**
    - Creative writing tasks requiring specific tone/style
    - Customer-facing outputs needing particular voice
    - Exploratory brainstorming requiring perspective shifts
    
    **Evidence:** The same study found **LLM-generated personas outperform human-written personas** when persona framing is genuinely beneficial. LLMs identify relevant expertise markers more reliably than humans guess them.
    
    ### Effective Role Framing Pattern
    
    When role framing is justified, use minimal, task-relevant framing:
    
    ```markdown
    # Over-specified (ineffective)
    You are a senior security engineer with 15 years of experience in financial
    services, specializing in cryptographic implementations and threat modeling,
    who has worked at major banks and led security teams...
    
    # Minimal (effective when role matters)
    Focus on security implications, particularly authentication and authorization.
    

The minimal version specifies the domain focus without elaborate backstory. The model doesn't benefit from fictional experience claims.

* * *

## Chain-of-Thought Language

Chain-of-thought (CoT) prompting emerged as a major technique for improving reasoning. Recent research shows its effectiveness varies significantly by model generation.

### The "Let's Think Step by Step" Effect

Original research (Kojima et al., 2022) showed adding "Let's think step by step" improved math reasoning from **18% to 79% accuracy** on certain benchmarks.

**Critical context:** This research used non-reasoning-optimized models. The dramatic improvement came from explicitly requesting reasoning that wasn't default behavior.

### Reasoning Model Era

_[2025-12-26]_ : Modern reasoning-optimized models (GPT-4.1, Claude 3.5+, o1) perform internal reasoning by default. Explicit CoT prompting shows diminishing returns.

**Wharton 2025 Research (SSRN):**

  * CoT prompting increases response time **20-80%** on reasoning models
  * Accuracy gain is **minimal to zero** on tasks within model capability
  * Explicit CoT helps primarily when debugging reasoning failures



**When CoT still helps:**

  * Debugging incorrect outputs (seeing reasoning reveals errors)
  * Tasks requiring specific reasoning format (e.g., legal analysis structure)
  * Explaining decisions to humans (transparency requirement)



**When to skip CoT:**

  * Straightforward tasks within model capability
  * Time/cost-sensitive applications
  * Model already demonstrates correct reasoning



### Invalid Reasoning Examples

Fascinating research by arxiv:2212.10001 found that **invalid CoT examples work nearly as well as valid ones** for improving performance. When few-shot examples contained logically flawed reasoning steps that reached correct conclusions, models achieved similar accuracy gains as with valid reasoning examples.

This suggests CoT's primary benefit isn't teaching reasoning logic but rather activating reasoning mode. The presence of step-by-step structure, regardless of step validity, triggers more careful processing.

* * *

## Model-Specific Language Patterns

Different model families respond optimally to different linguistic conventions.

### Claude (Anthropic)

**Effective patterns:**

  * XML tags for structure (`<instructions>`, `<examples>`, `<constraints>`)
  * Explicit scaffolding with clear section boundaries
  * Prefills for output format control (provide initial output text)
  * `<format>` tags wrapping expected output structure



**Example prefill pattern:**
    
    
    Generate a commit message for these changes.
     
    Output format:
    <commit_message>

The model completes starting from `<commit_message>`, naturally following the structure.

**Anthropic documentation:** docs.anthropic.com/claude/docs/prompt-engineering explicitly recommends XML tags and prefills.

### GPT (OpenAI)

**Effective patterns:**

  * Markdown structure with `###` headers
  * "Let's think step by step" for non-reasoning models
  * Sentence labels for hallucination reduction
  * System message for persistent behavioral rules



**Sentence label pattern (reduces hallucination):**
    
    
    For each claim:
    [CLAIM]: State the claim
    [EVIDENCE]: Provide supporting evidence
    [CONFIDENCE]: Rate confidence (high/medium/low)

The explicit labeling forces grounding of claims in evidence, reducing hallucination rates.

**OpenAI documentation:** cookbook.openai.com emphasizes Markdown and system/user message separation.

### Gemini (Google)

**Effective patterns:**

  * Precision over persuasion in phrasing
  * Temperature=1.0 required for Gemini 2.0 (lower values degrade quality)
  * Context-last ordering (key information at end of prompt)
  * Explicit output schema definition



**Context-last example:**
    
    
    Task: Summarize the key findings.
     
    [Long document content here...]
     
    Focus on: security vulnerabilities and performance bottlenecks.

The final line provides focus after context, leveraging recency bias.

**Google documentation:** ai.google.dev/docs/prompting-strategies documents these patterns.

* * *

## Anti-Patterns

### Over-Hedging

**Pattern:**
    
    
    Perhaps it might be worth considering possibly trying to maybe implement
    something that could potentially help with this issue if feasible.
    

**Problem:** Introduces ambiguity. Model uncertain whether action is required.

**Better:**
    
    
    Implement error recovery for network timeout scenarios.
    

### Anthropomorphization

**Pattern:**
    
    
    I know you're very smart and capable, so please use your intelligence to
    carefully analyze this complex problem and apply your expertise to find
    the optimal solution.
    

**Problem:** Zero informational content. Wastes tokens and context budget.

**Better:**
    
    
    Analyze for security vulnerabilities. Prioritize authentication issues.
    

### Implicit Negation

**Pattern:**
    
    
    Avoid global state, don't use mutable data structures, never expose internals.
    

**Problem:** Pink elephant effect—semantic activation of forbidden patterns.

**Better:**
    
    
    Use dependency injection, prefer immutable data structures, return sanitized errors.
    

### Format Ambiguity

**Pattern:**
    
    
    Return the results in a nice readable format.
    

**Problem:** "Nice" and "readable" undefined. Model guesses format.

**Better:**
    
    
    Return JSON array of objects with fields: id, name, status, timestamp.
    

### Role Overloading

**Pattern:**
    
    
    You are a world-class expert in security, performance, architecture, UX,
    accessibility, and business strategy with decades of experience in...
    

**Problem:** Dilutes focus. Model has no clear priority hierarchy.

**Better:**
    
    
    Prioritize security analysis. Note performance issues as secondary findings.
    

* * *

## Connections

  * **[Prompt Structuring](/agentic-engineering-book/2-prompt/2-structuring):** Language patterns work in conjunction with structural organization. Clear structure amplifies effective language; poor structure undermines it.

  * **[Model Behavior](/agentic-engineering-book/3-model/2-model-behavior):** Language effectiveness varies by model architecture. Understanding model-specific behaviors helps calibrate language choices.

  * **[Context Strategies](/agentic-engineering-book/4-context/2-context-strategies):** Language used to frame injected context affects how models utilize external information.




* * *

## References

### Academic Papers

  * **SatLM: Declarative Prompting** \- arxiv:2305.09656 Demonstrated 23% improvement with declarative phrasing on reasoning tasks.

  * **DETAIL Framework: Prompt Specificity Impact** \- arxiv:2512.02246 Quantified specificity gains across task categories (+0.47 math, +0.02 decision-making).

  * **"When A Helpful Assistant Is Not Really Helpful"** \- EMNLP 2024, arxiv:2311.10054 Tested 162 personas, found no improvement on factual/reasoning tasks.

  * **Understanding What Matters in Chain-of-Thought** \- arxiv:2212.10001 Showed invalid reasoning examples work nearly as well as valid ones.

  * **Wharton Prompting Science Reports 2025** \- SSRN Found 20-80% time increase for minimal accuracy gain with CoT on reasoning models.




### Official Documentation

  * **Anthropic Claude Best Practices** docs.anthropic.com/claude/docs/prompt-engineering Documents XML tag preference, prefill patterns, and structural conventions.

  * **OpenAI GPT-4.1 Prompting Guide** cookbook.openai.com Covers Markdown structure, system messages, and chain-of-thought patterns.

  * **Google Gemini Prompting Strategies** ai.google.dev/docs/prompting-strategies Details temperature requirements, context ordering, and precision phrasing.




### Practitioner Sources

  * **Simon Willison - Prompt Engineering** simonwillison.net (blog posts on practical prompt patterns)

  * **Eugene Yan - Prompting Fundamentals** eugeneyan.com (case studies and pattern documentation)

  * **Ethan Mollick - Two Paths to Prompting** oneusefulthing.org (research translation and practical guidance)

  * **Pink Elephant Problem Analysis** 16x.engineer (negative constraint failure modes)




* * *

## Open Questions

  * **Verb mood interaction effects:** How do declarative/imperative choices interact with model-specific architectural differences? Does this vary between autoregressive models and models with reasoning traces?

  * **Specificity saturation point:** At what level of detail does added specificity stop improving accuracy and start introducing brittleness? How task-dependent is this threshold?

  * **Cross-model language portability:** Can prompts be written in model-agnostic language, or does optimization always require model-specific tuning? What's the performance cost of portability?

  * **Constraint hierarchy complexity limits:** How many levels of permission hierarchy can models track reliably before confusion emerges?

  * **Negative constraint duration:** Is the pink elephant effect immediate or does it emerge only in long conversations? What's the interaction between context length and negative constraint reliability?




[PreviousPrompt Structuring](/agentic-engineering-book/2-prompt/2-structuring)[NextModel](/agentic-engineering-book/3-model)

[](/)

[](/agentic-engineering-book)

[](https://github.com/jayminwest)

[LinkedIn](https://www.linkedin.com/in/jaymin-west/)

[youtube](https://www.youtube.com/@jaymin-west)

[](https://consulting.jayminwest.com)

[](https://www.skool.com/prompt-to-prod-9369)

[](https://drive.google.com/file/d/1zRVZ8q2swx0erClyknx4X3c4rNrdV-IS/view)
