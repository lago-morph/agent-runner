# Report 01 — Prior art: Agentic Engineering book, Overstory, OpenHands

**Date:** 2026-05-11
**Author:** Lead agent
**Status:** ✅ complete (OpenHands git-provider abstraction depth is 🟡 — source layout has shifted since the earlier landscape scan and the GitService interface was not trivially relocatable in the current `main`)

## Lead question

What concrete patterns, abstractions, and operational lessons from the Jaymin West "Agentic Engineering" book, the Overstory CLI-agent orchestrator (`github.com/jayminwest/overstory`), and OpenHands (`github.com/All-Hands-AI/OpenHands`) should inform `agent-runner`'s v1 design — distinguishing between (a) interfaces worth adopting verbatim, (b) patterns worth adapting given that `agent-runner` runs in CI rather than on a developer laptop, (c) components mature enough to vendor rather than reimplement, and (d) design choices we should explicitly differ from? Capture a follow-up cluster list for deeper investigation.

## 1. Verdict in three sentences

The Agentic Engineering book validates `agent-runner`'s core bet — *use an existing full agentic harness (Claude Code) and instrument the surrounding system* — and gives us a vocabulary for `agent-runner`'s job ("the harness is the control system around the model"). Overstory and OpenHands are real, mature implementations of nearby ideas, but **neither is a candidate to vendor**: Overstory is local-execution / tmux / Bun and explicitly subscription-aware but designed for 5-15 concurrent agents on a developer laptop; OpenHands is BYO-API-key with a SaaS-flavored deployment model. **Both are inspiration sources for interface shape, not dependencies.** The book's most pointed advice for the scale tier `agent-runner` actually operates at (1-5 concurrent agents in CI) is "use Claude Code's built-ins; factory thinking is premature."

## 2. The harness frame (AE book §6) maps directly onto `agent-runner`

The book establishes that **`Agent = Model + Harness`**, where the harness is "everything around the model that makes it an agent." `agent-runner` is, in this taxonomy, a harness composed of two layers:

1. The **inner harness** is Claude Code itself (which carries Anthropic's defaults for prompt shape, tool inventory, context management, session memory, sub-agent delegation — Raschka's six-component stack).
2. The **outer harness** is `agent-runner`'s CI orchestration: trigger logic, state persistence across rate-limit windows, OAuth refresh, notification, run accounting.

The book's strongest applicable claims:

- **"Default to an existing full agentic harness for most work. Building a harness from scratch is a significant investment. Claude Code, Codex, and equivalent tools ship with Anthropic's harness defaults already set. Start there."** This is exactly `agent-runner`'s thesis. The book is the third independent voice (after `anthropics/claude-code-action` itself and the earlier landscape scan) recommending the path we're already on.
- **Fowler's guides-and-sensors decomposition** (§6/4): the harness is a *control system*, not passive scaffolding. *Guides* intervene **before** agent actions (feedforward); *sensors* observe results and steer subsequent behavior (feedback). Each can be **computational** (deterministic, e.g. a regex limit-detector) or **inferential** (a model-judged review). For `agent-runner` this is a useful framing because our rate-limit detector, our `max_turns` cap, and our timeout are all *computational guides*; the agent's self-reported transcript summary is a *computational sensor*; and an LLM-judged "did this PR actually do what was asked" check (if we add one) would be an *inferential sensor*.
- **Harness Engineering loop** (§6/5, Hashimoto's coinage Feb 5 2026): when an agent makes a mistake, engineer the surrounding system so that mistake cannot recur. Failure classification taxonomy: *model / context / prompt / harness / tool*. We should adopt this classification when logging run failures so that follow-ups produce harness fixes rather than prompt patches.
- **Trajectory capture as infrastructure, not nice-to-have** (§6/5, Schmid's thesis). Every session through a well-instrumented harness produces training data, evaluation data, and edge-case documentation. **`agent-runner` should log structured run records from day one** — Run/Result JSON in the state branch (already in DESIGN.md §4) covers this if we capture token usage, attempts, exit signals, and a transcript hash.
- **The harness is the primary security boundary** (§6/6). The model does not enforce permissions — the harness does. For `agent-runner`: the `allowed_tools` whitelist in `AgentConfig`, the `permissions` block in the Actions workflow, and the secret-scope decisions are *the* security layer. The book is unambiguous that this is not a model concern.

## 3. Where in the book's scale tiers `agent-runner` sits

The AE book's chapter 10/5 lays out a scale ladder for agent-orchestration systems. The two rows relevant to `agent-runner`:

| Tier | Agent count | Book's recommended infrastructure |
|---|---|---|
| **Solo** | 1-5 | None — use Claude Code's built-in Agent Teams |
| **Workshop** | 6-12 | Merge strategy, basic supervision (Overstory / Gas Town tier) |

`agent-runner` is Solo-tier in any realistic v1: one agent per CI run, a handful of concurrent runs per repo, kicked off by comments or cron. The book's explicit recommendation for Solo-tier is "use Claude Code's built-ins" — don't build an orchestration layer.

**Implication for `agent-runner`**: defer supervisor agents, merge queues, sub-orchestrators, and any other multi-agent coordination until there is concrete demand. Single-agent-per-run is the v1 contract. This is execution-layer scope discipline, not aspiration: the question of whether multiple agents should ever cooperate inside one logical task belongs to the sister "software factory" research effort, not here.

## 4. Scope note — software-factory analysis is out of scope here

The AE book's chapter 9/7 ("Software Factories") and the broader factory-readiness framing belong to a separate research and specification effort the user is running elsewhere. `agent-runner`'s scope is narrower and specific: **a general execution-layer for running agents under a Claude Max subscription via CI**, with the rate-limit-resume loop and the OAuth-in-secrets pattern as its load-bearing differentiators. Factory-scale validation patterns (StrongDM holdout sets, Digital Twin Universe), Shapiro's five-level framework, the circularity critique, and the talent-pipeline / liability discussion are all interesting and were partly read (chapter 9/7 is in the sources table for citation completeness), but they do not drive any decision in this repo. They are deferred to the sister research effort.

What chapter 9/7 *does* contribute to `agent-runner` is one orthogonal observation that survives the scope cut: **anti-pattern: "premature factory infrastructure"** — building supervisor agents, merge queues, multi-agent coordination, and other orchestration scaffolding before the scale demands it. The applicable consequence here is to keep `agent-runner` v1 deliberately minimal: single agent per run, no orchestration layer, no supervisor agents, no merge automation. That conclusion is also supported by Overstory's STEELMAN.md (see §5).

## 5. Overstory: what to take, what to ignore

Overstory ([github.com/jayminwest/overstory](https://github.com/jayminwest/overstory), 31K LOC TypeScript/Bun, 912 tests) is the closest existing thing to a CLI-agent orchestrator. After deep-reading the README, `CLAUDE.md`, `STEELMAN.md`, `src/runtimes/types.ts`, `registry.ts`, `claude.ts`, and `mail/client.ts`:

### What's genuinely worth borrowing

| Pattern | Where in Overstory | What we'd do in `agent-runner` |
|---|---|---|
| **`AgentRuntime` interface shape** | `src/runtimes/types.ts` — ~20 methods covering spawn-command building, headless spawn, config deployment, readiness detection, transcript parsing, event streaming | When we hit Stage 4 of DESIGN.md (extract runtime abstraction), borrow the method *names* and the *headless vs. interactive split* (`buildSpawnCommand` vs. `buildDirectSpawn`). Don't reimplement all 20 methods — we only need 3-4 for CI use. |
| **`headless: true` declaration on adapters** | Same file; orchestrator checks for `buildDirectSpawn()` before calling it | This is exactly how CI-substrate works: we always use the headless path. The adapter API in our future `AgentRuntime` should make headless the default and treat interactive as an optional capability. |
| **`AgentEvent` NDJSON stream from headless agents** | `src/runtimes/types.ts`; parsed by each adapter's `parseEvents()` | Claude Code's `--output-format stream-json` already emits this. Our run.py should consume it for live progress + accurate token accounting rather than parsing logs post-hoc. |
| **Two-layer agent definition** (base `.md` + dynamic overlay `CLAUDE.md`) | `agents/` (base) + `.overstory/.../CLAUDE.md` (per-run overlay) | Mirrors our `AgentConfig` (static base) + per-run prompt (dynamic). We're already doing roughly this; the Overstory naming is a useful convention. |
| **Subscription-aware cost model** | README compares Overstory ("Subscription, fixed monthly cost") vs. Gas Town ("API tokens, ~$100/hr") | First public system I've seen that *names* subscription-vs-API as a design axis. Validates `agent-runner`'s OAuth-token-in-secrets approach as an established pattern, not a hack. |

### What to explicitly *not* borrow

- **Tmux-based interactive sessions, `Bun.spawn`, per-agent git worktrees, SQLite mailbox with WAL mode and broadcast addressing.** All of these assume a long-lived local process. CI runners are ephemeral; jobs come and go. Don't import an architecture designed around the wrong execution model.
- **Multi-agent swarm patterns.** Overstory's *own author* wrote `STEELMAN.md` as a serious argument against multi-agent swarms — citing a real example where "a 20-agent swarm consumed 8M tokens ($60) while a single agent consumed 1.2M tokens ($9)" for comparable work. Other arguments in that doc: "architectural drift" (parallel work produces inconsistent naming, duplicated utilities, conflicting assumptions), compounding failure rates at integration boundaries, and forensic-reconstruction debugging across distributed worktrees. **For `agent-runner` v1 this is decisive: single sequential agent only.**
- **17-command CLI surface (`overstory sling`, `mail send`, `merge`, etc.).** Right scope for a developer-laptop power tool; wrong scope for a CI-driven orchestrator where the trigger surface is "comment a PR" and "cron."

### The STEELMAN.md callout deserves its own paragraph

Overstory's author argues *against his own design*. The quoted token-cost gap (8M vs 1.2M for similar work) is direct empirical evidence that the multi-agent approach is expensive without being proportionally productive. The deeper argument — that parallel agents produce architectural drift that escapes test coverage — is the most credible single source of "don't build multi-agent v1" reasoning I've encountered. This is a reusable artifact: if/when we're tempted to add multi-agent coordination, re-read STEELMAN.md first.

## 6. OpenHands: limited but real takeaways

OpenHands ([github.com/All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)) is open source, mature, and BYO-API-key. Its README emphasizes a vendor-led product surface (SDK / CLI / Local GUI / Cloud / Enterprise) and "Sign in with GitHub or GitLab" cloud onboarding. The earlier landscape scan called out a `GitService` protocol abstracting GitHub/GitLab/Bitbucket/Azure DevOps/Forgejo, but in the current `main` the top-level `/openhands/` directory shows `{analytics, app_server, server}` — the integration layer appears to have been refactored, possibly into the separate `software-agent-sdk/` package that the README points at via `docs.openhands.dev/sdk`. **I'm marking the GitService abstraction as 🟡 reconstructed** for this report; the *concept* is well-attested but the current code path is not where I expected it.

### What we can take from OpenHands at the concept level

- **Multi-platform git auth as a product axis**: "sign in with GitHub or GitLab" is unified in the user experience and split internally. This is the right shape for `agent-runner`'s future Stage 4 provider seam. The interface name `GitService` is good; the methods presumably look like `list_pull_requests`, `get_pr_diff`, `post_comment`, etc.
- **The SDK / CLI / GUI / Cloud / Enterprise product split**: useful taxonomy for `agent-runner`'s eventual surface area. v1 is "the workflow in this repo." A future v2 might be a Python package (the SDK), a CLI (`agent-runner run`), and that's likely the right ceiling.
- **What we won't borrow**: OpenHands is API-key-first and SaaS-flavored. The multi-tenant control plane, the enterprise auth model, the docker-deployment posture — all wrong for the "single repo holds everything" decision we already locked in.

The OpenHands research depth gap is small enough that I'd defer chasing the actual `GitService` code to a Stage-4-trigger future-research task rather than another fetch round now.

## 7. Adopt / Adapt / Differ / Defer matrix

The actionable summary:

| Item | Source | Verdict | When |
|---|---|---|---|
| `Agent = Model + Harness` framing for our docs | AE book §6 | **Adopt** verbatim | Now (update DESIGN.md introduction) |
| Guides / sensors decomposition (with computational/inferential split) | AE book §6/4 | **Adopt** as the mental model for `agent-runner`'s control elements (rate-limit detector, max-turns cap, transcript parser, future review-agent) | Now (DESIGN.md §11 failure-mode section) |
| Failure classification taxonomy (model / context / prompt / harness / tool) | AE book §6/5 | **Adopt** as a structured field in Run JSON when a run fails | Stage 2 (state schema) |
| Trajectory capture as infrastructure (token usage, transcript hash, agent events) | AE book §6/5 + Overstory `AgentEvent` | **Adopt** — log structured run records from day one | Stage 1 |
| `AgentRuntime.buildDirectSpawn` naming + headless-as-default | Overstory `src/runtimes/types.ts` | **Adopt** as the interface shape when we extract Stage 4 | Stage 4 only |
| Two-layer agent definition (static base + dynamic overlay) | Overstory + already in DESIGN.md | **Adopt** — formalize the convention | Stage 1 |
| Stream-json output parsing in run.py | Claude Code CLI native + Overstory `parseEvents` | **Adopt** — `--output-format stream-json` instead of post-hoc log parsing | Stage 1 |
| Multi-platform `GitService` abstraction | OpenHands (🟡 reconstructed) | **Adapt** when we extract Stage 4 — borrow the *name* and the *unified-method-set* idea | Stage 4 only |
| "Default to existing harness; don't build a new one" | AE book §6 + own DESIGN.md | **Already adopted** — current design wraps `claude-code-action` | Already done |
| Multi-agent swarm orchestration | Overstory STEELMAN.md (negative source) | **Differ** — explicit non-goal in v1 | Indefinite defer |
| Tmux interactive sessions, `Bun.spawn`, local worktrees | Overstory `src/worktree/manager.ts` | **Differ** — wrong execution model for CI | Never |
| SaaS control plane, multi-tenant deployment | OpenHands | **Differ** — explicit non-goal | Never |
| Supervisor agents, merge queues, multi-agent coordination | Overstory + AE book §9/7 "premature factory infrastructure" anti-pattern | **Defer** — premature at our scale tier | Until concrete demand appears |
| Vendor / fork Overstory or OpenHands wholesale | — | **Don't** — both wrong execution model for CI | Never |

## 8. Specific design-doc updates this round implies

Items to fold into DESIGN.md and ALTERNATIVES.md in a follow-up commit (probably in a separate PR after this report lands):

1. **DESIGN.md introduction**: add a one-paragraph harness-framing block citing the book. `agent-runner` is the *outer* harness; Claude Code is the *inner* harness; together they form Anthropic's `claude-code-action` recommendation.
2. **DESIGN.md §11 (failure modes)**: re-label the existing list using the book's failure taxonomy (model / context / prompt / harness / tool). Add OAuth-refresh failures under "harness."
3. **DESIGN.md §4 (Run JSON)**: add a `failure_classification` field (one of the five categories) when status is `failed`. Add `transcript_hash` for trajectory capture. Already have `tokens_used`.
4. **DESIGN.md §5 (run.py)**: specify `--output-format stream-json` invocation explicitly, with `parse_events` as the consumer. Borrow the NDJSON `AgentEvent` shape from Overstory's types as a reference for what fields to expect.
5. **DESIGN.md §10 (roadmap)**: append a v1 scale assumption — single agent per run, no orchestration layer, no supervisor / merge / multi-agent coordination. The reason is execution-layer scope discipline (the sister "software factory" effort is where multi-agent design questions are handled).
6. **ALTERNATIVES.md "Recommendation" section**: add an explicit "do NOT vendor Overstory or OpenHands" entry under "Things we considered and rejected" with one-line reasons (wrong execution model; wrong auth model; wrong scale tier).
7. **A new short doc — `LESSONS.md` or appendix in DESIGN.md** — capturing the three single-line maxims from this round:
   - "The harness is the primary security boundary."
   - "Default to an existing harness; build the outer ring."
   - "Single agent until scale demands otherwise (see Overstory STEELMAN.md)."

## 9. Round-1 future-research candidates (execution-layer scope only)

Promoted to PLAN.md "Future research" section. Brief here; justifications belong in PLAN.md. Multi-agent and software-factory clusters are deferred to the sister research repo and explicitly *not* tracked here.

- **AE book §6/2 (The Harness Stack), §6/4 (Harness as Control System), §6/5 (Harness Engineering), §6/6 (Security/Permissions/Trust)** — the full subchapters, not just the overview I read. Decision-relevant for the run-state machine, the guides/sensors framing, and the security boundary documentation.
- **AE book §8/3 (Cost and Latency), §8/4 (Production Concerns)** — operational lessons; likely contains rate-limit-handling discussion and cost-tracking patterns directly applicable to `agent-runner`'s execution layer.
- **OpenHands software-agent-sdk** at `software-agent-sdk/` — find the actual `GitService` implementation; what does the interface look like in code? Decision-relevant if/when we add a second git provider.
- **claude-code-action OAuth refresh community forks** (`grll/claude-code-login`, `claude-code-action-with-oauth`, anthropics/claude-code-action#727) — directly load-bearing for Stage 0 (proof of auth). Should be read *before* implementing `refresh-oauth.yml`.

---

## Sources reviewed

| Source URL | Status | Notes |
|---|---|---|
| `https://www.jayminwest.com/agentic-engineering-book` | ✅ Full review | Fetched via workflow (issue #5); full TOC and book intro. Used for §2 framing, §3 scale-tier mapping, and discovering chapter URLs for the second fetch round. |
| `https://www.jayminwest.com/agentic-engineering-book/6-harnesses` | ✅ Full review | Chapter 6 overview. Subchapter "Key concepts" bullets carried most of the substance for §2 (harness frame, control system, security boundary, trajectory capture). Full subchapter texts not read — see future-research. |
| `https://www.jayminwest.com/agentic-engineering-book/9-mental-models/7-software-factories` | ✅ Full review | Chapter 9/7. The Shapiro five-level table, StrongDM patterns, scale-transition signal diagram, anti-patterns, code-quality critique (CodeRabbit / Veracode / METR), and historical lineage all informed §3, §4. |
| `https://www.jayminwest.com/agentic-engineering-book/10-practitioner-toolkit/5-multi-agent-workspace-managers` | ✅ Full review (targeted: Overstory section + comparison tables) | Chapter 10/5. The Overstory architecture summary, the Overstory-vs-Gas-Town comparison table, and the scale-tier infrastructure table all informed §3 and §5. Gas Town content noted for future research; not read in full. |
| `https://raw.githubusercontent.com/jayminwest/overstory/main/README.md` | ✅ Full review | Section headings (Install, Architecture, Runtime Adapters, etc.), 11-runtime list, SQLite mailbox + worktree mentions. Informed §5. |
| `https://raw.githubusercontent.com/jayminwest/overstory/main/CLAUDE.md` | ✅ Full review (targeted: architecture + runtime + mailbox sections) | Deeper architecture: tech stack, orchestrator model, runtime modes (headless vs tmux), messaging protocol message types and priorities, worktree management at `.overstory/worktrees/{agent-name}/`. Informed §5. |
| `https://raw.githubusercontent.com/jayminwest/overstory/main/STEELMAN.md` | ✅ Full review | The author's own steel-man against multi-agent swarms: 20-agent vs 1-agent token cost example, architectural drift, compounding failure modes, forensic debugging. Load-bearing for §5 and the v1 "single agent only" decision. |
| `https://raw.githubusercontent.com/jayminwest/overstory/main/src/runtimes/types.ts` | 🟡 Reconstructed (interface names extracted, not all bodies) | `AgentRuntime`, `SpawnOpts`, `DirectSpawnOpts`, `ReadyState`, `OverlayContent`, `HooksDef`, `TranscriptSummary`, `ConnectionState`, `AgentEvent`, `RpcProcessHandle`, `RuntimeConnection`. Method bodies not quoted; method *count* (~20) and the optional-method pattern (orchestrator checks for `buildDirectSpawn()` before calling) are the load-bearing facts. Informed §5 adopt-matrix row 1. |
| `https://raw.githubusercontent.com/jayminwest/overstory/main/src/runtimes/registry.ts` | ✅ Full review (interface portion) | Factory map `Map<string, () => AgentRuntime>`, `getRuntime(name?, config?, capability?)` signature, fallback chain (explicit name → capability config → default → hardcoded "claude"). Informed §5 adopt-matrix row 1. |
| `https://raw.githubusercontent.com/jayminwest/overstory/main/src/runtimes/claude.ts` | ✅ Full review (public surface) | Method list: `buildSpawnCommand`, `buildDirectSpawn`, `detectReady`, `deployConfig`, `parseEvents`, `parseTranscript`, `buildPrintCommand`, `buildEnv`, `getTranscriptDir`. The `buildDirectSpawn` argv for headless mode (`"-p --output-format stream-json --input-format stream-json --verbose --strict-mcp-config --permission-mode bypassPermissions"`) is directly applicable to `agent-runner`'s `run.py`. Informed §5 and §8 item 4. |
| `https://raw.githubusercontent.com/jayminwest/overstory/main/src/mail/client.ts` | ✅ Full review (interface portion) | `createMailClient(store)`, MailClient methods (send, sendProtocol, check, list, reply, etc.). SQLite schema is in `store.ts` (not read). Informed §5 "what to NOT borrow." |
| `https://github.com/jayminwest/overstory` (repo root file browser) | ✅ Full review | Top-level dirs: `.canopy/`, `.claude/`, `.github/`, `.mulch/`, `.overstory/`, `.pi/`, `.sapling/`, `.seeds/`, `agents/`, `docs/`, `scripts/`, `src/`, `templates/`, `ui/`. Confirmed scope. |
| `https://github.com/jayminwest/overstory/tree/main/src/runtimes` | ✅ Full review | 11 runtime adapter pairs (one `.ts` + one `.test.ts` each), plus `types.ts`, `registry.ts`, `connections.ts`, `headless-connection.ts`, `pi-guards.ts`, `__fixtures__/`. Confirmed the runtime-adapter surface is ~10 files per adapter * 11 adapters = sizable. |
| `https://raw.githubusercontent.com/All-Hands-AI/OpenHands/main/README.md` | ✅ Full review | Product surface (SDK / CLI / Local GUI / Cloud / Enterprise), GitHub + GitLab cloud auth. No `GitService` details at README level. Informed §6 (note: GitService details are 🟡, source-layout-shifted). |
| `https://github.com/All-Hands-AI/OpenHands/tree/main` | ✅ Full review (top-level only) | Top-level dirs: `.agents`, `.devcontainer`, `.github`, `.openhands`, `.vscode`, `containers`, `dev_config`, `enterprise`, `frontend`, `kind`, `openhands-ui`, `openhands`, `scripts`, `skills`, `tests`. No top-level `integrations/`. Informed §6 (note: the integrations layer has been refactored). |
| `https://github.com/All-Hands-AI/OpenHands/tree/main/openhands` | ✅ Full review (directory only) | `/openhands/` contains `analytics/`, `app_server/`, `server/`, `__init__.py`, `py.typed`, `version.py`. No `integrations/`, `providers/`, or `git_service/` at this level. Informed §6 GitService 🟡 reconstruction. |
| `https://github.com/All-Hands-AI/OpenHands/tree/main/openhands/server` | ✅ Full review (directory only) | `config/`, `__init__.py`, `__main__.py`, `app.py`, `listen.py`, `middleware.py`, `shared.py`, `static.py`, `types.py`. Not where git-provider integration lives. Confirmed GitService is elsewhere — likely the separate `software-agent-sdk/` package mentioned in the README. Deferred to future research. |
| OpenHands `GitService` / `ProviderHandler` (multi-platform git abstraction) | 🟡 Reconstructed from earlier landscape-scan finding | The abstraction's *existence and scope* (GitHub / GitLab / Bitbucket / Azure DevOps / Forgejo) is well-attested in the earlier scan. The current code path was not relocated in this round. §6 commentary stands at the concept level; the interface signature has not been read. Recover by inspecting `software-agent-sdk/` once that package is located. |
| `https://www.jayminwest.com/agentic-engineering-book` (sub-chapters 6/1 through 6/7 in detail, 7/3, 7/4, 7/11, 8/3, 8/4) | ⏳ Pending | Not yet fetched. Deferred to future-research cluster "AE book operational chapters." Used overview-level material in this report. |
