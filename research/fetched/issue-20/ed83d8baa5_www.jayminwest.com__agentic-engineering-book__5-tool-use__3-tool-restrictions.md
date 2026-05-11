


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

# Tool Restrictions and Security

Tool restrictions aren't just about capability—they're security boundaries. Treat tool access like production IAM: deny-all by default, allowlist only what each agent needs.

* * *

## Tool Restrictions as Security Boundaries

_[2025-12-09]_ : In multi-agent systems, tool restrictions aren't just about capability—they're security boundaries. Treat tool access like production IAM: deny-all by default, allowlist only what each subagent needs.

**Principle** : Each subagent should have the minimum tool set required for its role. This isn't just defense-in-depth—it also helps the agent stay focused on its domain by reducing distraction from irrelevant capabilities.

**Common Patterns** :

Role | Tools | Rationale  
---|---|---  
Reviewer/Analyzer | Read, Grep, Glob | Read-only; can't accidentally modify files  
Test Runner | Bash, Read, Grep | Execute tests and read results; no file editing  
Builder/Implementer | Read, Edit, Write, Grep, Glob | Full modification access for implementation  
Orchestrator | Task, Read, Glob | Routes work, has minimal direct access  
Scout/Explorer | Read, Grep, Glob, WebFetch | Discovery only, no modification  
  
**Implementation** : In Claude Agent SDK, configure via YAML frontmatter (`tools: [Read, Grep, Glob]`) or the programmatic `tools` array. Filesystem definitions in `.claude/agents/*.md` make permissions visible and auditable.

**Anti-Pattern** : Giving all agents full tool access "for flexibility." This is the fastest path to unsafe autonomy. Instead:

  * Require explicit confirmation for sensitive actions (git push, infrastructure changes)
  * Restrict agents to relevant directories when possible
  * Log tool usage for auditability



**Production Lesson** : Permission sprawl compounds. Start restrictive and expand only when you hit actual blockers. It's much easier to grant additional permissions than to clean up after an agent with too much access does something unexpected.

**See Also** :

  * [Orchestrator Pattern: Capability Minimization](../7-patterns/3-orchestrator-pattern.md#capability-minimization) — How tool restriction becomes an architectural forcing function for delegation



**Sources** : [Subagents in the SDK - Claude Docs](https://platform.claude.com/docs/en/agent-sdk/subagents), [Claude Agent SDK Best Practices](https://skywork.ai/blog/claude-agent-sdk-best-practices-ai-agents-2025/), [Best practices for Claude Code subagents](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)

* * *

## MCP Tool Declarations in Frontmatter

_[2025-12-09]_ : MCP (Model Context Protocol) tools extend agent capabilities beyond native tools. Declaring them in YAML frontmatter follows a consistent pattern across projects.

**Naming Convention** : `mcp__<server>__<tool>`

  * Double underscores separate the three components
  * Server names can include hyphens: `mcp__firecrawl-mcp__firecrawl_scrape`
  * Examples: 
    * `mcp__playwright__browser_navigate` (browser automation)
    * `mcp__supabase__execute_sql` (database operations)
    * `mcp__kotadb__search_code` (custom code search)



**Two Frontmatter Fields** (context-dependent):

  * **`tools:`** — Used in agent definitions to declare capabilities
  * **`allowed-tools:`** — Used in commands to restrict available tools



**Mixed Declarations** : MCP tools combine naturally with native tools:
    
    
    tools: mcp__playwright__browser_click, mcp__firecrawl-mcp__firecrawl_scrape, Write, Read, Edit

**Role-Based MCP Assignment** : Different agents get different MCP tool subsets:

Role | MCP Tools | Purpose  
---|---|---  
Scout | `search_code`, `list_recent_files` | Read-only exploration  
Builder | `search_code`, `analyze_change_impact` | Implementation support  
Validator | `browser_navigate`, `browser_snapshot`, `browser_click` | UI verification  
Scraper | `firecrawl_scrape`, `firecrawl_search` | Documentation fetching  
  
**Permission Patterns at Settings Level** : Glob patterns control MCP access without per-tool whitelisting:
    
    
    {
      "permissions": { "allow": ["mcp__kotadb__*", "mcp__playwright__*"] },
      "enableAllProjectMcpServers": true
    }

**Multi-Instance Pattern** : Some projects separate staging and production:

  * `mcp__kotadb-staging__search_code`
  * `mcp__kotadb-production__search_code`



**Gap** : Frontmatter only references tools by name—server configuration (endpoints, auth, schemas) happens elsewhere (`.mcp.json`, environment variables, or external config). The declaration pattern is separate from the instantiation pattern.

**See Also** :

  * [Claude Code: Subagent System](../10-practitioner-toolkit/1-claude-code.md#subagent-system) — How MCP tools integrate with subagent definitions
  * [Orchestrator Pattern: Tool Assignment](../7-patterns/3-orchestrator-pattern.md#tool-assignment) — Role-based MCP tool assignment in multi-agent workflows



* * *

## Wildcard Permission Patterns

_[2026-01-11]_ : Claude Code 2.1.0 introduced wildcard pattern matching for Bash tool permissions. This enables more flexible permission policies that reduce prompt fatigue while maintaining security boundaries.

**Syntax:** `Bash(<pattern>)` where `*` matches any characters

**Examples:**

Pattern | Matches | Use Case  
---|---|---  
`Bash(npm *)` | `npm install`, `npm run build`, `npm test` | Package management  
`Bash(git *)` | `git status`, `git commit`, `git push` | Version control  
`Bash(docker compose *)` | `docker compose up`, `docker compose down` | Container orchestration  
`Bash(pytest *)` | `pytest tests/`, `pytest -v` | Test execution  
`Bash(make *)` | `make build`, `make clean`, `make deploy` | Build automation  
  
**Configuration in settings.json:**
    
    
    {
      "permissions": {
        "allow": [
          "Bash(npm *)",
          "Bash(git status)",
          "Bash(git diff *)",
          "Bash(git add *)",
          "Bash(git commit *)",
          "Bash(pytest *)"
        ],
        "deny": [
          "Bash(git push *)",
          "Bash(rm -rf *)"
        ]
      }
    }

**Security Considerations:**

Wildcards expand the permission surface. Apply least-privilege principles:

  * **Prefer specific patterns:** `Bash(npm run test)` over `Bash(npm *)`
  * **Combine allow and deny:** Allow broad patterns, deny dangerous subsets
  * **Test coverage:** Verify patterns match intended commands before production use



**Anti-Pattern: Over-Broad Wildcards**
    
    
    {
      "permissions": {
        "allow": ["Bash(*)"]
      }
    }

This effectively disables Bash permission prompts entirely—equivalent to `--dangerously-skip-permissions` for shell commands. Defeats the purpose of permission controls.

**Sources:** [Claude Code Changelog 2.1.0](https://code.claude.com/docs/en/changelog)

* * *

## Permission Bypass Vulnerabilities

_[2026-01-17]_ : Security fixes in Claude Code 2.1.6-2.1.7 revealed attack surfaces in permission patterns that warranted documentation.

### Line Continuation Injection

Shell allows command continuation with backslash. This can bypass single-line permission checks:
    
    
    # Approved permission: Bash(git add)
    # Attack vector:
    git add \
    && rm -rf /  # Continuation executes without restriction

**Mitigation:** Claude Code 2.1.7 validates across line continuations, treating the entire multi-line command as a single unit for permission matching.

### Glob Expansion Escapes

Wildcard patterns can expand beyond intended scope:
    
    
    # Approved: Bash(rm temp/*)
    # Risk: rm temp/* expands to include unexpected files
    #       if temp/ contains symlinks or unexpected entries

**Mitigation:** Prefer explicit paths over wildcards for destructive operations. Filesystem state at execution time determines actual expansion.

### Best Practices for Secure Permissions

  1. **Prefer exact matches** over wildcards: `Bash(git status)` not `Bash(git *)`
  2. **Test patterns in isolation** before production deployment
  3. **Layer defenses** : combine allow-lists with explicit deny-lists
  4. **Audit filesystem separately** from permission string validation
  5. **Log all permission decisions** for post-incident analysis



### Testing Permission Enforcement

Before trusting a permission pattern, verify behavior in a sandboxed environment:
    
    
    # Test script: verify permission actually blocks
    test_cases = [
        ("git add .\n&& rm -rf /", "should_block"),  # line continuation
        ("rm ../outside/*", "should_block"),          # path traversal
        ("git status", "should_allow"),               # exact match
    ]

Run permission tests in isolation before production use. Permission validation and filesystem state are separate concerns—test both.

* * *

## Leading Questions

  * How do you test that tool restrictions are actually enforced?
  * What happens when an agent needs temporary elevated permissions?
  * How do you handle tool access in development vs. production?
  * When should tools fail loudly vs. silently when permission is denied?
  * How do you audit tool usage patterns to detect permission issues?



* * *

## Connections

  * **To[Tool Selection](/agentic-engineering-book/5-tool-use/2-tool-selection):** Restrictions affect what's selectable
  * **To[Scaling Tools](/agentic-engineering-book/5-tool-use/4-scaling-tools):** MCP deployment patterns intersect with security
  * **To[Orchestrator Pattern](/agentic-engineering-book/7-patterns/3-orchestrator-pattern):** Delegation as security enforcement
  * **To[Production Concerns](/agentic-engineering-book/8-practices/4-production-concerns):** Security in production environments



[PreviousTool Selection and Routing](/agentic-engineering-book/5-tool-use/2-tool-selection)[NextScaling Tool Use](/agentic-engineering-book/5-tool-use/4-scaling-tools)

[](/)

[](/agentic-engineering-book)

[](https://github.com/jayminwest)

[LinkedIn](https://www.linkedin.com/in/jaymin-west/)

[youtube](https://www.youtube.com/@jaymin-west)

[](https://consulting.jayminwest.com)

[](https://www.skool.com/prompt-to-prod-9369)

[](https://drive.google.com/file/d/1zRVZ8q2swx0erClyknx4X3c4rNrdV-IS/view)
