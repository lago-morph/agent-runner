


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

# Plan-Build-Review Pattern

A workflow pattern that separates specification from implementation, with optional research phase and feedback loops where production experience continuously improves the process itself.

* * *

## Core Insight

_[2025-12-10]_ : **Bad research compounds exponentially.** One flawed architectural assumption in the Research phase leads to a misguided plan, which generates thousands of lines of incorrect code. Research quality has massive leverage on all downstream outcomes.

The core pattern has three phases (Plan-Build-Improve), with an optional Research phase for complex domains. The four-command expert pattern (Research-Plan-Build-Improve) creates a learning loop where each phase builds on validated understanding:

  1. **Research** \- Understand the problem space, codebase structure, and dependencies
  2. **Plan** \- Creates detailed specifications grounded in research findings
  3. **Build** \- Implements according to the research-backed spec
  4. **Improve** \- Analyzes what happened and updates the Research/Plan/Build expertise



The Improve phase closes the loop by extracting learnings from actual production usage and updating the expert's knowledge base across all commands, making each iteration smarter than the last.

* * *

## How It Works

### The Learning Loop
    
    
        Research (with Expertise)
             ↓
        Plan (with Expertise)
             ↓
        Build (with Expertise)
             ↓
        Production Experience
             ↓
        Improve (updates Expertise)
             ↓
        (feeds back to Research/Plan/Build)
    

### Key Characteristics

  * **Mutable Expertise Sections** : Unlike workflows, the Expertise sections in Research/Plan/Build commands are designed to evolve
  * **Experience-Driven Evolution** : Learnings come from real production usage, not theory
  * **Self-Improving System** : Each cycle makes the next iteration better
  * **Persistent Knowledge** : Insights are captured in the prompts themselves, not lost in conversation history



* * *

## The Research Phase

_[2025-12-10]_ : Research is the foundation that determines everything downstream. Before planning what to build, you need to understand:

  * **Codebase structure** : Where does relevant code live? What are the existing patterns?
  * **Dependencies** : What does this component depend on? What depends on it?
  * **Problem causes** : What actually broke? What's the root cause vs. symptoms?
  * **Constraints** : What can't change? What assumptions must hold?



### Research as Artifact Generation

The output of research isn't just understanding—it's **concise summary documents** that capture findings:
    
    
    # Research Summary: Feature X Implementation
     
    ## Current Architecture
    - Component Y handles Z via pattern P
    - Dependencies: A, B, C (see /path/to/code)
     
    ## Problem Root Cause
    - Symptom: Users report timeout
    - Cause: Unbounded retry loop in module M
    - Evidence: /path/to/logs, line 234
     
    ## Constraints
    - Cannot change API contract (external clients)
    - Must maintain backward compatibility with v1.x
     
    ## Recommended Approach
    Based on architecture analysis, approach 2 (async queue)
    fits existing patterns better than approach 1 (sync retry).

These artifacts serve two purposes:

  1. **Grounding** : Plan phase references concrete findings, not assumptions
  2. **Validation** : Team can review research conclusions before building begins



### The Exponential Compounding Problem

Why research deserves a dedicated phase:

Research Quality | Plan Accuracy | Lines of Wrong Code | Cost to Fix  
---|---|---|---  
Excellent | 95% | ~50 | Hours  
Good | 80% | ~500 | Days  
Poor | 50% | ~5,000 | Weeks  
Terrible | 10% | Complete rewrite | Months  
  
A 10-minute research mistake can create a 10-week refactoring disaster. The leverage is asymmetric—investing in research quality pays exponential dividends.

### What Good Research Looks Like

**Good:**

  * "Module X uses pattern Y (see lines 45-67 in file.py)"
  * "Dependency graph shows A→B→C, change must start at C"
  * "Root cause: race condition between handlers (reproduced in test)"



**Bad:**

  * "The code probably does something with databases"
  * "I think this component is important"
  * "We should investigate the authentication system"



Good research is specific, sourced, and falsifiable. Bad research is vague and ungrounded.

* * *

## Implementation in Claude Code

In Claude Code's slash command system, this pattern is implemented through expert command sets:
    
    
    .claude/commands/experts/[domain]-expert/
         [domain]_expert_research.md  # Has ## Expertise section
         [domain]_expert_plan.md      # Has ## Expertise section
         [domain]_expert_build.md     # Has ## Expertise section
         [domain]_expert_improve.md   # Updates the Expertise sections
    

The Improve command:

  1. Analyzes recent git changes
  2. Identifies successful patterns and learnings
  3. Updates ONLY the Expertise sections in Research/Plan/Build commands
  4. Keeps workflow sections stable



### Research Command Structure

A typical Research expert command:
    
    
    ## Workflow
     
    1. **Understand the Requirement**
       - What problem are we solving?
       - What's the scope?
     
    2. **Explore the Codebase**
       - Use Glob/Grep to find relevant files
       - Read key components
       - Map dependencies
     
    3. **Analyze the Problem**
       - Identify root causes
       - Distinguish symptoms from causes
       - Document constraints
     
    4. **Generate Research Summary**
       - Create concise summary document
       - Include specific file paths and line numbers
       - State conclusions with evidence
     
    ## Expertise
     
    *[2025-12-10]*: (Accumulated learnings about researching this domain)

* * *

## When to Use This Pattern

### Good Fit

**Complex, knowledge-intensive domains:**

  * Multi-step workflows requiring specialized understanding
  * Tasks where learning from experience is valuable
  * Situations where patterns emerge over time
  * When you want prompts to improve with use



**Indicators you need this pattern:**

  * Repeatedly solving similar problems in the same domain
  * Accumulating domain-specific best practices
  * Need for consistent approach across team/project
  * High cost of mistakes (research phase prevents compounding errors)



### Poor Fit

**Simple or one-off tasks:**

  * Single-file changes with clear requirements
  * Domains with fixed, unchanging requirements
  * When expertise doesn't accumulate meaningfully
  * Tasks simple enough that planning overhead exceeds benefit



**When simpler approaches work:**

  * Ad-hoc changes with no pattern reuse
  * Exploratory work where learning isn't transferable
  * Domains where external documentation is comprehensive and stable



* * *

## Scale-Adaptive Execution

_[2026-02-06]_ : Not every task requires full Research-Plan-Build-Improve. BMAD-METHOD demonstrates **scale-adaptive intelligence** —the framework adjusts depth based on task complexity, from quick-fix to enterprise governance.

### The Spectrum
    
    
    Bug Fix              Small Feature       New Product          Enterprise System
       ↓                      ↓                   ↓                      ↓
    Quick Flow          Partial Planning    Full Planning       Compliance Planning
    (3 steps)           (4 steps)           (6 steps)           (8+ steps)
    

**Quick Flow** (Bug fixes, refactoring, prototypes):
    
    
    /quick-spec → /dev-story → /code-review
    

Skip Research, Analysis, Architecture. Get to code fast.

**Standard Flow** (Features, enhancements):
    
    
    Research → Plan → Build → Review
    

The base pattern described in this chapter.

**Full Planning** (New products, major features):
    
    
    Research → Product Brief → PRD → Architecture →
    Epics/Stories → Sprint Planning → Dev → Review
    

Add business analysis and structured requirements.

**Enterprise** (Compliance-required, multi-team):
    
    
    Research → Product Brief → Stakeholder Review → PRD →
    Architecture → Security Review → Implementation Plan →
    Readiness Assessment → Build → QA → Release Gates → Retrospective
    

Add approval gates, compliance artifacts, governance.

### How Framework Decides

**Context-aware recommendations** based on:

  * **Task type** : "fix bug" → Quick Flow, "new authentication system" → Full Planning
  * **Domain complexity** : Simple CRUD → Standard, Medical diagnostic system → Enterprise
  * **Regulatory requirements** : Internal tool → Standard, HIPAA-covered → Enterprise
  * **Team size** : Solo dev → Quick Flow, 5-team effort → Enterprise



**Example decision logic:**
    
    
    User: "Implement real-time notifications"
        ↓
    Framework analyzes:
    - "real-time" → system architectural concern (not bug fix)
    - "notifications" → new feature, not enhancement
        ↓
    Recommends: Full Planning
    - Research existing notification systems
    - Create PRD defining notification taxonomy
    - Design architecture (WebSockets vs SSE)
    - Plan implementation in phases
    

### Benefits of Scale-Adaptive Approach

**Prevents over-planning:** Don't spend 4 hours planning a 30-minute bug fix. Quick Flow gets you to solution fast.

**Prevents under-planning:** Don't write 5,000 lines of code for a "new authentication system" without architecture. Full Planning prevents compounding errors.

**Matches investment to risk:**

  * Low risk → minimal planning
  * Medium risk → standard planning
  * High risk → comprehensive planning with gates



### When to Override Framework Recommendations

**Use lighter process when:**

  * Prototyping to validate feasibility
  * Strict time constraints (ship fast, refine later)
  * Low-stakes exploratory work
  * Team has deep domain expertise (less research needed)



**Use heavier process when:**

  * Regulatory compliance required
  * Changes affect many teams
  * Mistakes are expensive to fix
  * Learning for future projects (invest in documentation)



### Integration with Self-Improving Experts

Scale-adaptive execution pairs with self-improving experts:

**Pattern:** Framework recommends process depth, expert improves recommendations over time.

**Learning loop:**

  1. Framework recommends Quick Flow for "add field to API"
  2. Implementation reveals need for database migration (should have been Standard Flow)
  3. Improve phase captures: "Field additions requiring schema changes → Standard Flow"
  4. Future similar tasks get better recommendation



### Practical Implementation

**In prompts:**
    
    
    ## Workflow Selection
     
    Based on task analysis, use:
    - **Quick Flow** if: Bug fix, refactoring, prototype, < 2 hours estimated
    - **Standard Flow** if: Feature, enhancement, system change, 2-8 hours
    - **Full Planning** if: New subsystem, major feature, multi-team, > 8 hours
    - **Enterprise** if: Compliance required, security-critical, production infrastructure

**In orchestrators:**
    
    
    def select_workflow_depth(task: str, context: dict) -> WorkflowDepth:
        """Recommend workflow depth based on task complexity."""
        complexity_score = analyze_task_complexity(task, context)
     
        if complexity_score < 2:
            return WorkflowDepth.QUICK_FLOW
        elif complexity_score < 5:
            return WorkflowDepth.STANDARD
        elif complexity_score < 8:
            return WorkflowDepth.FULL_PLANNING
        else:
            return WorkflowDepth.ENTERPRISE

### Production Evidence

BMAD-METHOD (34.5k stars) demonstrates this at scale:

  * 68 workflows covering spectrum from quick-fix to enterprise
  * Automatic workflow recommendation via `/bmad-help`
  * Scale-adaptive intelligence distinguishes SaaS app from medical system
  * Community validation across diverse project types



### Trade-Offs

Approach | Planning Time | Risk Mitigation | Flexibility  
---|---|---|---  
**Always Quick Flow** | Minimal | Low (skips critical planning) | High  
**Always Full Planning** | High | High (prevents errors) | Low (overhead for simple tasks)  
**Scale-Adaptive** | Variable (matches task) | Appropriate (risk-matched) | High (right tool for job)  
  
### Open Questions

  * Can complexity analysis be automated reliably, or does it require human judgment?
  * What factors beyond task type should influence workflow depth? (team experience, codebase maturity, time pressure)
  * How to handle edge cases where task seems simple but has hidden complexity?
  * Does scale-adaptive intelligence improve with machine learning, or is rule-based sufficient?



* * *

## Connections

  * **To[Prompts/Structuring](/agentic-engineering-book/2-prompt/2-structuring)**: Scale-adaptive execution requires prompts that can handle variable workflow depth
  * **To[Claude Code](/agentic-engineering-book/10-practitioner-toolkit/1-claude-code)**: Implementation via expert command sets with workflow selection logic
  * **To[Evaluation](/agentic-engineering-book/8-practices/2-evaluation)**: How to measure if workflow depth recommendations are accurate?
  * **To[Context Management](/agentic-engineering-book/4-context)**: Heavier workflows generate more artifacts—context management strategies must scale with workflow depth
  * **To[Specs as Source Code](/agentic-engineering-book/9-mental-models/3-specs-as-source-code)**: BMAD's living artifacts methodology demonstrates full-spectrum documentation from quick-spec to enterprise governance



* * *

## Related Patterns

  * **ReAct Loop** : Similar feedback structure but at inference time, not across sessions
  * **Human-in-the-Loop** : Review phase could involve human validation
  * **Multi-Agent** : Multiple experts could each use Research-Plan-Build-Improve internally



[PreviousPatterns](/agentic-engineering-book/7-patterns)[NextSelf-Improving Expert Commands](/agentic-engineering-book/7-patterns/2-self-improving-experts)

[](/)

[](/agentic-engineering-book)

[](https://github.com/jayminwest)

[LinkedIn](https://www.linkedin.com/in/jaymin-west/)

[youtube](https://www.youtube.com/@jaymin-west)

[](https://consulting.jayminwest.com)

[](https://www.skool.com/prompt-to-prod-9369)

[](https://drive.google.com/file/d/1zRVZ8q2swx0erClyknx4X3c4rNrdV-IS/view)
