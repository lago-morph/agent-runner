# agent-runner — Design

Status: draft, v1 scope.
Audience: the author and future contributors deciding whether to extend or replace this.

## 1. What this is

A system for orchestrating runs of CLI-based AI coding agents (Claude Code initially) under **subscription auth** rather than API-key auth. The execution substrate is **GitHub Actions**, because that is where a Claude Max OAuth token can be stored as a secret without leaving the user's machine and without exposing it to a third-party SaaS.

The system lets a user:

- Define an "agent run" (what to run, on what input, with what config).
- Trigger runs from PR/issue comments, cron, manual dispatch, or external webhook.
- Have runs that hit a 5-hour or weekly rate limit **pause and resume automatically** when the window expires, without losing context.
- Receive notifications when runs complete or fail.

It is not an attempt to compete with CodeRabbit, Greptile, or Devin — those are vendor-billed SaaS. The differentiator is: **your subscription, your runner, your code.**

## 2. Goals and non-goals

### v1 goals

1. End-to-end happy path: a comment of the form `@agent-runner <task>` on a PR or issue triggers a Claude Code run inside a GitHub Actions job, results posted back to the thread.
2. Rate-limit resilience: when Claude Max returns a 5-hour or weekly limit error, the run is checkpointed and resumed automatically once the window expires.
3. OAuth token refresh: the Max OAuth token is refreshed before it expires, without manual intervention.
4. One notification sink: Slack webhook (other sinks deferred).
5. Single-repo deployment: clone, set secrets, push — no external services.

### Explicit non-goals for v1

- GitLab, Jira, Linear, Forgejo, Bitbucket support. Seams will be named, not built.
- Codex / ChatGPT subscription support. The auth model is officially discouraged in CI by OpenAI; revisit later.
- A web UI or dashboard. The "UI" is the GitHub repo — issues, PRs, the `state` branch, and Actions logs.
- Multi-tenant SaaS. Each user runs their own copy.
- An MCP server registry. Users configure MCP servers per-AgentConfig.
- A skills marketplace. Skills are paths in the user's repo.

## 3. Why CI is the substrate (the core bet)

The Anthropic-published `anthropics/claude-code-action` accepts a `claude_code_oauth_token` produced by `claude setup-token`. That token authenticates against the user's Max subscription. Putting it in a GitHub Actions secret is the only ergonomic way today to:

- Run an agent from a trigger that isn't a human at a terminal.
- Keep credentials out of any third-party orchestration SaaS.
- Get a free, durable, versioned execution log (Actions runs + the `state` branch).

The cost: each CI job is **ephemeral**. Anything that needs to survive across job boundaries — paused-run state, OAuth refresh tokens, the queue of pending runs — must be persisted externally. We persist to a Git branch inside this same repo (see §6).

## 4. Concepts (the abstract layer)

These are the only types in v1. Each is a JSON document, not (yet) a typed in-memory object — keeping it as JSON in Git makes the system inspectable and forkable without code changes.

### `AgentConfig`

```json
{
  "id": "default-claude-coder",
  "agent": "claude-code",
  "model": "claude-opus-4-7",
  "system_prompt_ref": "agents/coder.md",
  "allowed_tools": ["Read", "Edit", "Bash", "WebFetch"],
  "mcp_servers": [{ "name": "github", "config_ref": "mcp/github.json" }],
  "skills": ["security-review", "review"],
  "max_turns": 50
}
```

Stored at `agents/<id>.json` on `main`. Referenced by id from a `Run`.

### `Trigger`

A normalized representation of what kicked off a run. Three v1 sources, all collapsed to the same shape:

```json
{
  "kind": "comment | schedule | dispatch | webhook",
  "source_ref": "owner/repo#PR-123#comment-456 | cron:0 9 * * * | ...",
  "payload": { /* original event JSON, for context */ },
  "actor": "github-username | system",
  "created_at": "2026-05-10T19:44:00Z"
}
```

### `Run`

```json
{
  "id": "run_2026-05-10_a3f1c2",
  "status": "queued | running | paused_rate_limit | succeeded | failed | cancelled",
  "agent_config_id": "default-claude-coder",
  "trigger": { /* Trigger */ },
  "task": "free-form prompt or structured input",
  "attempts": [
    {
      "n": 1,
      "started_at": "...",
      "ended_at": "...",
      "outcome": "completed | rate_limited | error",
      "actions_run_url": "https://github.com/.../actions/runs/123",
      "tokens_used": { "input": 12345, "output": 6789 }
    }
  ],
  "resume_at": "2026-05-11T00:44:00Z",
  "checkpoint_ref": "runs/run_2026-05-10_a3f1c2/checkpoint.json"
}
```

### `Result`

The terminal artifact of a `Run`:

```json
{
  "run_id": "run_2026-05-10_a3f1c2",
  "status": "succeeded | failed | cancelled",
  "summary": "Markdown summary posted back to trigger source",
  "artifacts": [
    { "kind": "pr", "ref": "owner/repo#PR-789" },
    { "kind": "comment", "ref": "owner/repo#issue-123#comment-999" },
    { "kind": "branch", "ref": "agent/run_2026-05-10_a3f1c2" }
  ],
  "token_usage": { "input": 80000, "output": 40000 }
}
```

### Future seams (named, not built)

The following will become interfaces when a second concrete backend exists. **Not earlier.**

- `ProviderClient` — abstract over GitHub vs. GitLab vs. Forgejo for issue/PR/comment operations. Today: only `providers/github/`.
- `IssueTracker` — abstract over GitHub Issues vs. Jira vs. Linear. Today: GitHub Issues, in-line.
- `Notifier` — abstract over Slack vs. Mattermost vs. Teams vs. email. Today: a single function `notify_slack(...)`.
- `AgentRuntime` — abstract over Claude Code vs. Codex vs. Aider. Today: a single function `run_claude_code(...)`.

When extracting these, look at OpenHands' `GitService` and Overstory's `AgentRuntime` for prior-art shapes. Don't invent.

## 5. Components

```
.github/workflows/
  trigger-comment.yml      # on: issue_comment, pull_request_review_comment
  trigger-schedule.yml     # on: schedule
  trigger-dispatch.yml     # on: workflow_dispatch, repository_dispatch
  runner.yml               # on: workflow_dispatch (called by triggers)
  watchdog.yml             # on: schedule (*/10 * * * *)
  refresh-oauth.yml        # on: schedule (every 6h)

agents/
  coder.md                 # system prompts
  reviewer.md
  default-claude-coder.json # AgentConfig

scripts/
  enqueue.py               # called by triggers; writes run.json to state branch, dispatches runner.yml
  run.py                   # called by runner.yml; loads run.json, invokes claude-code-action, writes checkpoint or result
  watchdog.py              # called by watchdog.yml; finds paused runs whose resume_at has passed, re-dispatches runner.yml
  notify.py                # called from run.py; posts to Slack webhook
  detect_limit.py          # parses claude-code-action output for rate-limit signatures

providers/github/          # all GitHub API calls live here. Nothing else imports octokit / PyGithub.
```

The `state` branch is an orphan branch that holds:

```
runs/<run_id>/
  run.json
  checkpoint.json          # only present when status == paused_rate_limit
  result.json              # only present when status is terminal
  attempt-1.log
  attempt-2.log
queue/
  pending.json             # FIFO of runs awaiting first dispatch (rare; mostly we dispatch immediately)
```

Concurrency: each run owns its own directory; cross-run conflicts are impossible. Within a run, only one workflow writes at a time (the runner job, or the watchdog when re-dispatching). We use `git push` with `--force-with-lease` and retry on conflict.

## 6. The hard part: rate-limit resume

This is the differentiator. Sequence:

1. `runner.yml` fires for `run_X`. It checks out `main`, the `state` branch into `./_state`, and runs `scripts/run.py`.
2. `run.py` loads `_state/runs/run_X/run.json`. If `checkpoint.json` exists, it includes the checkpoint's `last_assistant_message` and modified-file list as context for the resumed prompt.
3. `run.py` invokes `claude-code-action` (via composite step or direct CLI), capturing stdout/stderr.
4. After the action exits, `detect_limit.py` scans the captured output for known signatures:
   - `"5-hour limit reached"` / `"resets at <time>"`
   - Weekly limit messages
   - HTTP 429-equivalent surfaced by the CLI
5. **Three outcomes:**
   - **Completed normally** → write `result.json`, set `status=succeeded`, post Slack/PR notification, done.
   - **Rate-limited** → write `checkpoint.json` (extracted from the run's transcript and any modified files committed to a per-run branch `agent/run_X`), set `status=paused_rate_limit`, set `resume_at` from the parsed reset time (fallback: now + 5h or now + 7d), commit `_state`, exit 0. **Do not fail the job** — failure would surface as a noisy red X.
   - **Other error** → set `status=failed`, write `result.json` with stderr excerpt, notify, exit 0.
6. `watchdog.yml` runs every 10 minutes. `watchdog.py` lists `runs/*/run.json` with `status=paused_rate_limit`, filters where `resume_at <= now()`, and dispatches `runner.yml` for each (capped at N concurrent to avoid burning the new window all at once).

### Open problems for v1

- **Faithful checkpoints.** The Claude Code CLI has a `--resume` / `-c` flag, but issue anthropics/claude-code#36320 reports state-reload bugs. Two fallbacks: (a) commit any in-progress file changes to `agent/run_X` and pass them as context on resume, (b) prepend a synthesized "here is what you did so far" message. Start with (b); add (a) after the first end-to-end run that needs it.
- **Limit detection is parsing CLI output.** This is brittle. Centralize in `detect_limit.py` with a small test corpus; add new signatures as we see them. Cite the existing community parsers (`claude-auto-resume`, the dev.to "Smart Resume" wrapper) and steal their regexes.
- **Watchdog reaping the same run twice.** Use a lease: when watchdog dispatches, it writes `dispatched_at` to `run.json` and won't re-dispatch within the next 30 minutes. The runner clears the lease when it picks the run up.

## 7. Auth and token refresh

- Repo secrets:
  - `CLAUDE_CODE_OAUTH_TOKEN` (short-lived, refreshed by `refresh-oauth.yml`)
  - `CLAUDE_OAUTH_REFRESH_TOKEN` (long-lived; used only by the refresh workflow)
  - `AGENT_RUNNER_PAT` (fine-grained PAT with `secrets: write` on this repo, so the refresh workflow can update `CLAUDE_CODE_OAUTH_TOKEN`)
  - `SLACK_WEBHOOK_URL`
- `refresh-oauth.yml` runs every 6 hours, calls Anthropic's OAuth refresh endpoint, and writes the new access token back into the repo secret via the GitHub API.
- Reference: [grll/claude-code-login](https://github.com/grll/claude-code-login), [claude-code-action-with-oauth](https://github.com/marketplace/actions/claude-code-action-with-oauth). Do not reimplement; either vendor or wrap.
- This is the **single biggest operational risk**. If refresh breaks, every run breaks. Treat it as a tier-1 component with its own monitoring (a heartbeat run that posts "auth healthy" to Slack daily).

## 8. Notifications

v1 is one function:

```python
def notify_slack(webhook_url: str, run: Run, result: Result | None) -> None: ...
```

Called from `run.py` on terminal status, and from `watchdog.py` if a run has been paused longer than 8 days (which means weekly limit + something else went wrong).

When a second sink is added (Mattermost, Teams, email), extract `Notifier` interface. Not before.

## 9. Triggers in detail

### `trigger-comment.yml`

- `on: issue_comment` and `on: pull_request_review_comment`.
- Filters: comment body starts with `@agent-runner` (configurable), comment author is in an allow-list (repo collaborators by default — prevents random GitHub users from spending your tokens), comment author is not a bot (loop prevention).
- Parses `@agent-runner <agent_config_id> <task>`; defaults to `default-claude-coder` if no id given.
- Calls `enqueue.py` which writes `run.json` and dispatches `runner.yml`.

### `trigger-schedule.yml`

- `on: schedule` with crons defined in `schedules.yml` (a list of `{cron, agent_config_id, task}`).

### `trigger-dispatch.yml`

- `on: workflow_dispatch` (manual button) and `on: repository_dispatch` (external webhook via PAT).
- This is how cross-repo and cross-system triggering works in v1: another repo's workflow calls `gh api repos/.../dispatches` with an event payload.

## 10. Roadmap

**Stage 0 — proof of auth** (1 day)
- One workflow, one secret, one composite step that calls `claude-code-action` with a hardcoded prompt and posts the result as a comment. Confirms OAuth-in-CI works on the user's account.

**Stage 1 — happy path** (2-3 days)
- `trigger-comment.yml` + `runner.yml` + minimal `run.py` + `enqueue.py`. No state branch yet; runs are stateless. Confirms the trigger → run → reply loop.

**Stage 2 — state and watchdog** (3-5 days)
- Introduce the `state` orphan branch, `Run`/`Result` JSON, `watchdog.yml`, `detect_limit.py`. Hand-trigger a rate limit (or simulate by stubbing the limit detector) and verify the resume loop end-to-end.

**Stage 3 — auth refresh** (1-2 days)
- `refresh-oauth.yml`, healthcheck heartbeat. After this, the system can run unattended for a week.

**Stage 4 — extract abstractions, only as needed**
- A second `AgentConfig` (e.g. a reviewer prompt with different tools) — no abstraction needed.
- A second notification sink — extract `Notifier`.
- A second provider (GitLab) — extract `ProviderClient`. Look at OpenHands' design.
- A second runtime (Codex, Aider) — extract `AgentRuntime`. Look at Overstory's design.

## 11. Failure modes worth naming up front

- **OAuth refresh dies silently.** Mitigated by daily heartbeat; otherwise every workflow starts failing 6-24 hours later with auth errors.
- **Limit-detection regex stops matching after a CLI update.** Mitigated by a test corpus and an alert when a run exits with a non-zero code from the action but the detector reports "completed normally."
- **Watchdog re-dispatches a run that's already running.** Mitigated by the lease in §6.
- **Comment-trigger spam.** Allow-list of authors; per-actor rate limit (max N runs per hour).
- **Cost from runaway runs.** Hard cap on `max_turns` per AgentConfig and a per-run wall-clock timeout in `runner.yml`.
- **Token in logs.** `claude-code-action` masks the token, but `run.py` must never `set -x` after loading it; verify with a deliberate test.

## 12. Prior art relied on

- [`anthropics/claude-code-action`](https://github.com/anthropics/claude-code-action) — the auth shim.
- [`grll/claude-code-login`](https://github.com/grll/claude-code-login) — OAuth refresh in CI.
- [`terryso/claude-auto-resume`](https://github.com/terryso/claude-auto-resume) — limit-detection regexes (local-only, but the parsing logic transfers).
- [`jayminwest/overstory`](https://github.com/jayminwest/overstory) — pluggable `AgentRuntime` shape (reference for Stage 4).
- [OpenHands `GitService`](https://github.com/OpenHands/OpenHands) — provider abstraction shape (reference for Stage 4).
- [`awslabs/cli-agent-orchestrator`](https://github.com/awslabs/cli-agent-orchestrator) — cron + webhook + notification plugin model (reference for v2).

## 13. Open questions

1. Do we want the agent's working tree to be on a per-run branch (`agent/run_X`) inside the same repo, or in a separate "workspace" repo? Per-run branch is simpler for v1; a workspace repo isolates blast radius and is probably right for v2.
2. How should runs be cancelled? A label on a tracking issue? A comment `@agent-runner cancel run_X`? Defer until needed.
3. Should `result.json` summaries be posted as PR review comments (with line refs) or as plain issue/PR comments? Plain comments for v1; review comments require structured output from the agent.
4. What's the test strategy? At minimum: `detect_limit.py` has a corpus of real CLI outputs; `run.py` is dry-runnable against a stub `claude-code-action`.
