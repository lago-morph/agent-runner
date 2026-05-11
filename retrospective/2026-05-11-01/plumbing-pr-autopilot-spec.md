# Spec: `plumbing-pr-autopilot`

## Intent

Low-risk "plumbing" PRs — skill edits, config tweaks, dependency bumps, doc fixes — that have no architectural significance and pass a clean status check should not require the user to be in the merge loop. This skill packages the open → subscribe → check-status → merge → sync flow as one autonomous routine so an agent can finish a plumbing change without yet another round-trip. The session evidence is that this exact sequence ran twice (PR #9 and PR #10), four tool calls each, with identical structure and identical outcomes.

Grounded in: PR #9 (`cfde00e` — subscribe-pr-default-on policy flip) and PR #10 (`adc5c9b` — self-retrospective upstream sync). Both PRs were opened, subscribed-to, found clean on first parallel status read, merged, and the local main fast-forwarded — all within the same tool-call shape.

## Trigger

### Direct triggers — activate immediately

- "Merge this PR if CI passes"
- "Autopilot PR #N"
- "Finish PR #N if it's clean"
- The skill is invoked at the tail end of another skill (e.g., `upstream-skill-sync`) after a PR has just been opened.

### Proactive triggers

- A plumbing-style PR is open and the user has explicitly authorised self-merge for similar work earlier in the session.
- A PR is open, the agent created it, and it is clearly low-risk (skill files, config files, docs only — no source code, no schema migrations, no auth, no CI workflows).

### Negative triggers — do NOT activate

- PR touches source code, schema migrations, IAM/auth, CI pipelines, dependency upgrades crossing a major version, or anything in `/security/`, `/auth/`, or files matching `*.lock`. Plumbing means plumbing.
- The agent has no prior authorisation pattern for self-merging in this session and the user has not asked.
- The PR has open review threads — even resolved ones if the latest is non-author and unresolved.
- The PR has failing or in-progress CI checks.

## Inputs

- `PR_NUMBER` — the integer PR number.
- `OWNER` / `REPO` — repository coordinates (default to working repo).
- `LOCAL_BASE_BRANCH` (default `main`) — branch to fast-forward after merge.
- `MERGE_METHOD` (default `merge`) — one of `merge`, `squash`, `rebase`.

## Outputs

- One `subscribe_pr_activity` call.
- One parallel batch of three `pull_request_read` calls (`get_check_runs`, `get_reviews`, `get_review_comments`).
- One `merge_pull_request` call if status is clean.
- One `git checkout <LOCAL_BASE_BRANCH> && git pull` to sync local.
- Inline acknowledgement when the auto-unsubscribe webhook arrives.

If status is not clean, the skill stops at the status check and reports findings to the user.

## Workflow

1. **Subscribe to PR activity** via `mcp__github__subscribe_pr_activity`. This must happen even though the rest of the flow is synchronous — the webhook-driven auto-unsubscribe at merge time is what tells the user (and the agent) that the loop closed.

2. **Read three status surfaces in parallel** with one tool-batch message:
   - `mcp__github__pull_request_read method=get_check_runs`
   - `mcp__github__pull_request_read method=get_reviews`
   - `mcp__github__pull_request_read method=get_review_comments`
   Parallel is mandatory — they are independent, and the harness will charge serial latency otherwise.

3. **Evaluate clean-status criteria** (all must hold):
   - `check_runs.total_count == 0` or every run's `conclusion == "success"`.
   - `reviews == []` or every review's `state == "APPROVED"` (no `CHANGES_REQUESTED`).
   - `review_threads.totalCount == 0` or every thread's `isResolved == true`.

4. **If clean**: call `mcp__github__merge_pull_request` with `MERGE_METHOD`. Capture the returned merge SHA.

5. **Sync local base branch**:
   ```bash
   git checkout <LOCAL_BASE_BRANCH>
   git pull origin <LOCAL_BASE_BRANCH>
   ```
   Verify fast-forward by checking `git log --oneline -1` matches the merge SHA returned in step 4.

6. **Wait for the auto-unsubscribe webhook**. Do not poll — the webhook arrives as a `<github-webhook-activity>` message. When it does, acknowledge it briefly (one short sentence) and end the turn. If the webhook does not arrive within the same turn, do not block — proceed to summary; the webhook will arrive eventually and is informational.

7. **If not clean** at step 3: stop, do not merge. Report exactly which surface flagged (check failure / change-request review / unresolved thread). Hand back to the user for next steps. Stay subscribed — the user may want to fix and re-run the autopilot.

## Concrete examples

### Example 1: PR #9 (subscribe-pr-default-on)

- `PR_NUMBER=9`, defaults otherwise.
- Step 1: subscribed.
- Step 2 (parallel reads): `check_runs=0`, `reviews=[]`, `review_threads=0`.
- Step 3: clean.
- Step 4: merged via `mcp__github__merge_pull_request` → returned `67337d4`.
- Step 5: `git checkout main && git pull` fast-forwarded `cfde00e..67337d4`.
- Step 6: auto-unsubscribe webhook arrived; acknowledged.
- Total tool calls: 1 subscribe + 3 parallel reads + 1 merge + 1 bash sync = **6 tool calls** for end-to-end PR closure.

### Example 2: PR #10 (self-retrospective sync)

- `PR_NUMBER=10`, defaults otherwise.
- Step 1: subscribed.
- Step 2 (parallel reads): `check_runs=0`, `reviews=[]`, `review_threads=0`.
- Step 3: clean.
- Step 4: merged → `104043b`.
- Step 5: `git pull` fast-forwarded `adc5c9b..104043b`.
- Step 6: auto-unsubscribe arrived.
- Total tool calls: 6.

Both runs hit the same call shape with no branching — strong signal that the flow is tight.

### Example 3: hypothetical not-clean case

- `PR_NUMBER=N`, defaults otherwise.
- Step 1: subscribed.
- Step 2 (parallel reads): `check_runs.total_count == 2`, one failing.
- Step 3: NOT clean.
- Step 4: skipped.
- Step 5: skipped.
- Output: "PR #N has 1 failing check (`lint`). Not merging. Subscription remains active so the next push will refresh status here."
- Stay subscribed; do not unsubscribe — the user may push a fix.

## Anti-patterns

- **Subscribing without the parallel status read.** Subscription alone is necessary but not sufficient — you must close the loop with an explicit clean-status assertion. The webhook stream eventually surfaces failures but on a delay; the explicit read is the gate.
- **Serial status reads.** Three sequential `pull_request_read` calls is 3× the latency of one parallel batch.
- **Polling for the auto-unsubscribe webhook.** The webhook arrives when it arrives. If it's not in the current turn, move on; do not `sleep`.
- **Auto-merging PRs that touch source code, schema, CI, or auth.** Plumbing means plumbing. The cost of an unauthorised merge to production code is asymmetric — measure twice.
- **Treating `check_runs.total_count == 0` as a CI gap that should block.** In repos with no PR-triggered workflows, zero checks is the *correct* state. The clean-status predicate is `(no runs) OR (all runs passing)`, not `runs > 0 AND all passing`. If you require positive CI coverage, that's a project policy that belongs in an ADR, not in this skill.
- **Decision-flip-flopping in chain-of-thought before the merge call.** The Opus 4.7 chain-of-thought is visible. Either the criteria pass and you merge, or they don't and you stop. Don't litigate "should I merge?" in the open after the criteria already decided it.

## Acceptance criteria

1. Tool-call count for a clean run is exactly 6 (subscribe + 3 parallel reads + merge + bash sync). Deviations indicate a bug or a non-plumbing PR slipping through.
2. Local base branch fast-forwards to the merge SHA from step 4 with no merge conflict and no extra commits.
3. The auto-unsubscribe webhook is acknowledged exactly once if it arrives in the same turn (not echoed twice, not ignored).
4. If status is not clean, the skill exits without calling `merge_pull_request` and produces a one-paragraph report naming the failing surface and the failing items.
5. No `git push` is required — the skill operates entirely server-side via the MCP merge call plus a local pull.

## Files this skill creates / modifies

- None on disk in the working tree. The skill only mutates the GitHub PR state and the local checkout of `<LOCAL_BASE_BRANCH>`.