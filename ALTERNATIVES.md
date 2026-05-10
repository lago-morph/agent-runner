# Interface Alternatives

How a developer (or another agent) actually defines, triggers, observes, and controls a run is the most consequential design choice — more than what's inside the box. Six genuinely distinct options below, then a comparison matrix and a recommendation.

The current `DESIGN.md` is a hybrid of **Alt 6 (comment-first)** with elements of **Alt 2 (GitOps state)** for persistence. That hybrid is reasonable but not the only sensible point in the space.

---

## Alt 1 — GitHub Issues as the database

**Idea.** Each `Run` is a GitHub Issue. Status is a label (`run/queued`, `run/running`, `run/paused`, `run/done`). Checkpoints are comments. The terminal `Result` is a final comment, then the issue is closed. No `state` branch.

**Developer writes** (using an issue template):
```yaml
# .github/ISSUE_TEMPLATE/agent-run.yml
title: "[run] "
labels: ["agent-run", "run/queued"]
body:
  - id: agent
    type: dropdown
    options: [default-claude-coder, reviewer, triager]
  - id: task
    type: textarea
```

**AI sees.** Task = issue body. History = comment thread (already chronological).

**Pros.**
- Zero new UI. Existing GitHub search, mentions, subscriptions, mobile app — all free.
- Cancellation is closing the issue. Pause is a label flip. Cron-friendly: query `is:issue label:run/paused`.
- Audit log is the comment thread, with author attribution.
- Notifications via GH's existing subscription model — no Slack glue needed for v0.
- Cross-repo references (`#123`) work natively.

**Cons.**
- Issue spam. A nightly triage run that fires 100 times/month is 100 issues forever.
- Mixing "tracked work" issues with "ephemeral run" issues confuses human collaborators.
- Issues API has rate limits and pagination; querying 10k historical runs is slow.
- Some orgs disable bot-authored issues or restrict labels.
- Concurrency: writing a label and a comment is two API calls; no transaction.

**Best fit.** Small team, low volume, runs that map 1:1 to tracked work (e.g. "review this PR" runs).

---

## Alt 2 — GitOps file queue

**Idea.** A `Run` is a YAML file committed to `runs/queue/`. A watcher workflow `on: push` to that path picks the file up, moves it to `runs/active/<id>/`, executes it, then moves it to `runs/done/<id>/` with a `result.json` alongside. The repo *is* the database, version-controlled.

**Developer writes.**
```yaml
# runs/queue/refactor-x.yml
agent: default-claude-coder
task: |
  Refactor src/X to use the new API.
  Open a PR titled "refactor: X to new API".
```
Commit on main → enqueued. Or open as a PR if you want approval gates.

**AI sees.** Task = the `task` field. State = `runs/active/<id>/checkpoint.json` if resuming.

**Pros.**
- Fully declarative, replayable, diffable. PR review is a natural approval gate for sensitive runs.
- Versioned history of every run definition.
- Trivially scriptable: generate 50 yamls and `git push` once.
- Watchdog and runner read from the same source of truth (the working tree).
- No bespoke comment grammar to parse.

**Cons.**
- Every run produces 2-3 commits; main branch history gets noisy.
- "Move a file" semantics in CI need locking; concurrent watchers race.
- Human triggers (a comment) need a translator that materializes a yaml file.
- Reading status requires `git log` or a tree walk; less discoverable than labels.
- PRs as enqueue mechanism conflate code review with task submission.

**Best fit.** Scripted/programmatic triggers, batch jobs, cases where the runs themselves should be peer-reviewed.

---

## Alt 3 — Reusable workflow as the public API

**Idea.** The product *is* a reusable workflow. Other repos invoke it with `uses:`. agent-runner contains no triggers itself — it's a library.

**Developer writes** (in *their* repo):
```yaml
# .github/workflows/review.yml in consumer repo
on: pull_request
jobs:
  review:
    uses: lago-morph/agent-runner/.github/workflows/run.yml@v1
    with:
      agent_config: reviewer
      task: "Review ${{ github.event.pull_request.html_url }}"
    secrets:
      claude_oauth_token: ${{ secrets.CLAUDE_OAUTH_TOKEN }}
```

**AI sees.** Whatever the consumer's workflow passes in `with:`.

**Pros.**
- Native GitHub idiom. No vendoring, no submodules.
- Tag-based versioning is built in (`@v1`, `@main`, `@sha`).
- Each consumer holds its own credentials in its own secrets — better blast-radius.
- Trigger logic lives where the events naturally fire (the consumer's repo).
- Marketplace-publishable.

**Cons.**
- **Pause/resume is broken.** When the consumer's workflow is the caller, a paused run can't easily wake the consumer's job back up. State has to live somewhere — but where? agent-runner has no place to write to a foreign repo without elevated tokens.
- Reusable workflows accept only flat scalar inputs — no rich objects, no MCP-config blobs.
- Cross-repo `repository_dispatch` for resume requires a PAT in the consumer with `actions: write`.
- Limit-detection state can't be shared across consumers cleanly.

**Best fit.** Stateless single-shot runs (PR review, security scan). A poor fit for the rate-limit-resume loop, which is the whole point of v1.

---

## Alt 4 — Python (or TS) SDK with thin YAML glue

**Idea.** AgentConfigs and Run definitions are *code*. Workflows are 5-line stubs that call `python -m agent_runner run`.

**Developer writes.**
```python
# agents/reviewer.py
from agent_runner import AgentConfig, MCPServer, run

REVIEWER = AgentConfig(
    name="reviewer",
    model="claude-opus-4-7",
    system_prompt_path="agents/reviewer.md",
    allowed_tools=["Read", "Bash", "WebFetch"],
    mcp_servers=[MCPServer.github()],
    max_turns=30,
)

if __name__ == "__main__":
    result = run(REVIEWER, task=sys.argv[1])
    sys.exit(0 if result.status == "succeeded" else 1)
```

```yaml
# .github/workflows/runner.yml
- run: uv run python -m agent_runner.cli run --config agents/reviewer.py --task "${{ inputs.task }}"
```

**AI sees.** Whatever `run()` passes downstream — fully under code control.

**Pros.**
- Type-checked configs. IDE autocomplete. Refactor with confidence.
- Composition: `REVIEWER.with_extra_tool("WebFetch")`, conditional MCP servers, dynamic system prompts.
- Unit-testable: `pytest agents/test_reviewer.py`.
- One language for orchestration, agent config, and skills.
- Local-first dev loop: same Python runs outside CI.

**Cons.**
- Adds a Python build/lockfile/CI surface to a system whose pitch is "YAML and a token."
- Non-Python users excluded (or you ship a TS variant too — 2x maintenance).
- Reviewing an AgentConfig change is reviewing code, not data; subtler bugs.
- Python imports across consumer repos invite version skew.
- Slightly slower start (interpreter startup, dep resolve) per CI run.

**Best fit.** Power users, complex/dynamic configs, agent set that evolves quickly, teams already on Python.

---

## Alt 5 — MCP server (agent-callable orchestrator)

**Idea.** agent-runner exposes itself as an **MCP server** with tools: `enqueue_run`, `get_run`, `list_runs`, `cancel_run`, `wait_for_run`, etc. Any MCP host (Claude Code, Cursor, another agent's tool list) can drive it.

**Developer writes.** Nothing in agent-runner itself. Configures their MCP host:
```json
{ "mcpServers": { "agent-runner": { "url": "https://my-agent-runner.example.com/mcp" } } }
```
Then in chat: "Use agent-runner to kick off a `reviewer` run on PR 42 and notify me when it's done."

**AI sees.** A first-class tool list. Calls it like any other MCP tool.

**Pros.**
- The most natural interface for AI agents to drive other AI agents.
- Tool grammar is rigorous and self-documenting (input schemas).
- Composable with other MCP servers in the same agent session.
- One interface from CLI (`mcp-cli`), IDE, or programmatic agent.
- Future-proof — MCP is becoming the de-facto AI-tool protocol.

**Cons.**
- **Violates the single-repo, no-external-infra constraint.** You need an always-on server with a URL. CI runners don't host services.
- Auth model is non-trivial: who can call the MCP server, with what credentials?
- Cron and webhook triggers don't speak MCP — you still need a parallel non-MCP surface.
- Operational burden: another service to keep up.
- Limit-resume requires the server to schedule its own re-dispatches.

**Best fit.** v2 — once the CI substrate is solid and primary users are other agents, not humans. Premature for v1.

---

## Alt 6 — Comment-protocol-first (chat-native)

**Idea.** The *only* surface is structured PR/issue comments. State is stored in a `state` branch for resume only — never read by humans directly. (This is closest to current `DESIGN.md`, but pushed harder: no `workflow_dispatch`, no `repository_dispatch` in v1.)

**Developer writes.**
```
@agent-runner run reviewer
> Review the diff for security regressions in src/auth/

@agent-runner status run_ab12
@agent-runner cancel run_ab12
@agent-runner help
```

**AI sees.** Task = the comment body after the directive. Context = surrounding PR/issue.

**Pros.**
- Lowest cognitive load; reads like Slack.
- All interactions live in one threaded view.
- Natural for AIs too — they post comments via the GH API like any other actor.
- Discoverable via `@agent-runner help`.
- Bot-friendly: one comment in, one comment out, no surrounding plumbing.

**Cons.**
- Programmatic triggers (cron, external webhooks) need a translator that fakes a comment or a parallel surface — back to a hybrid.
- Comment grammar drift: every new feature stretches the directive language.
- Markdown fights you for multi-line, structured input.
- Bot/loop prevention is constant whack-a-mole.
- Hard to express a 200-line AgentConfig in a comment — has to reference stored configs.

**Best fit.** Human-in-the-loop work where the trigger is naturally a comment anyway (PR review, issue triage). Pairs well with the `state` branch for resume only, hidden from users.

---

## Comparison matrix

| Axis                      | 1. Issues-DB | 2. GitOps queue | 3. Reusable wf | 4. Python SDK | 5. MCP server | 6. Comment-first |
|---------------------------|--------------|-----------------|----------------|---------------|---------------|------------------|
| Setup cost (consumer)     | Low          | Medium          | Low            | Medium        | High          | Low              |
| Programmatic trigger      | OK           | Great           | Great          | Great         | Great         | Hacky            |
| Human trigger             | Native       | Hacky           | OK             | OK            | Hacky         | Native           |
| Cross-repo                | Hacky        | Hacky           | Native         | OK            | Native        | OK               |
| Persistent state          | Native       | Native          | Hard           | Needs branch  | Server-side   | Needs branch     |
| Pause/resume across CI    | OK           | Great           | **Hard**       | OK            | OK            | OK               |
| AI-callable               | OK           | Hacky           | OK             | OK            | **Native**    | OK               |
| New infra required        | None         | None            | None           | None          | **Server**    | None             |
| Discoverability           | High         | Medium          | Medium         | Low           | High (in IDE) | High             |
| Versioning of configs     | Weak         | Strong          | Strong (tags)  | Strong        | Server-defined | Weak           |
| Concurrency safety        | Medium       | Medium          | High           | High          | High          | Medium           |
| Future-proofing for AI-driven | Medium   | Medium          | Medium         | Medium        | **High**      | High             |

---

## Hybrids worth considering

The strongest real-world designs are usually hybrids. Three that stand out:

### H1 — Comment + State-Branch (current DESIGN.md)
**= Alt 6 + Alt 2 (state only).** Humans use comments; persistence is GitOps. The "queue" is implicit (in-flight Actions runs); only the `state/runs/<id>/` directory is GitOps. Cleanest for v1.

### H2 — Comment + Issues-DB
**= Alt 6 + Alt 1.** Comments still trigger runs, but each run is recorded as an Issue rather than a `state`-branch JSON. Better discoverability; worse at high volume. Strong fit if every run is roughly "tracked work."

### H3 — Reusable workflow + Comment shim
**= Alt 3 + Alt 6.** agent-runner ships a reusable workflow for stateless single-shot runs (great for PR review on every PR, where pause/resume isn't needed) AND a comment-driven path with state branch for long-running interactive runs. Two surfaces, two costs, but covers the most ground.

### H4 — Python SDK + Comment-first frontend
**= Alt 4 + Alt 6.** Comments are the user surface; AgentConfigs are Python. Configs get type safety; users get chat ergonomics. Pays the Python tax once.

---

## Recommendation

For v1 of agent-runner, **stick with H1 (current design)** but make two interface decisions explicit:

1. **AgentConfig representation: JSON files in `agents/` on `main`.** Not Python (Alt 4), not embedded in comments. Plain data, peer-reviewable, copy-pasteable. Upgrade to Python only when configs need conditionals or composition.
2. **Trigger surface: comments + `repository_dispatch` only.** Don't add `workflow_dispatch` UI buttons, don't add an issue-template trigger, don't expose MCP. Two surfaces is enough; one for humans, one for machines.

Reasons:
- H1 is the only option that handles pause/resume well *and* requires no external infrastructure *and* matches how humans currently interact with PRs.
- It composes upward: an MCP server (Alt 5) can be added in v2 as a thin wrapper that issues `repository_dispatch` events. A Python SDK (Alt 4) can be added by reading the same `agents/*.json` files.
- The two paths it forecloses cleanly are Alt 1 (Issues-as-DB) and Alt 3 (Reusable-workflow-as-product). Both are real options if v1 gets uncomfortable.

If at any point during Stage 0–1 the comment-protocol parser feels load-bearing or the `state` branch starts to feel like a real database, **revisit Alt 1**: GH Issues handle 80% of what we're hand-rolling, and we'd give up only programmatic-trigger ergonomics.

If primary users turn out to be other agents rather than humans on PRs, **revisit Alt 5**: the MCP-server framing becomes the right interface, with the CI substrate underneath unchanged.
