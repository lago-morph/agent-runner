# Spec: `session-end-cleanup-checklist`

## Intent

When a session ends (user says "drain", "wrap up", "we're done") or a major PR has just merged, walk the session's accumulated artifacts and surface a structured cleanup checklist *before* the dispatcher signs off. In the 2026-05-11 overnight session, the lead agent's initial drain step missed two cleanup targets: the `fetched/issue-18` branch (the user had to manually ask "Is it safe to delete?") and the leftover `research/fetched/issue-21/` directory under main after PR #24 merged (the user had to say "There are still things in a subdirectory of reports"). Both omissions are detectable mechanically — the skill walks the same git+filesystem terrain the user inspected and produces the list the dispatcher should have offered.

## Trigger

**Direct triggers:**
- User says: "drain", "wrap up", "session is over", "we're done", "clean up".
- A PR the dispatcher authored gets merged into `main`.

**Proactive triggers:**
- Before any natural session-end communication ("ready to sign off", "anything else").
- After committing the final retrospective for a session.

**Negative trigger (skip):**
- The session opened zero issues, zero PRs, zero feature branches. Nothing to clean up.

## Inputs

1. The current repo's git state (local + `origin`).
2. The set of issue numbers, PR numbers, and branch names the dispatcher created or modified this session — gathered from the conversation transcript or, if unavailable, from `git log --author=…` heuristics and `mcp__github__list_issues` filters.
3. The current default-branch HEAD (typically `origin/main`).
4. The runtime environment's deletion-capability flags — specifically, whether `git push origin --delete` returns HTTP 403 against this remote (sandbox-proxy environments do).

## Outputs

A single structured checklist surfaced to the user, grouped by cleanup category. Each item has: identifier, current state, recommended action, and the runtime obstacle (if any) preventing the dispatcher from doing it autonomously.

The skill **does not silently delete things.** Branch and issue cleanup is presented as a list for the user to approve or override; only on explicit "do it" instruction does the dispatcher act.

## Workflow

1. **Enumerate issues.** Call `mcp__github__list_issues` with `state: OPEN`, `labels: ["fetch-urls"]` (or other workflow-driving labels in use). For each, check whether its workflow has produced a fetched branch and whether that branch has been merged into the dispatcher's working line. Open + workflow-complete + merged = candidate for closure as `completed`. Open + workflow-incomplete + superseded = candidate for closure as `not_planned`.

2. **Enumerate sub-branches.** Run `git branch -r | grep -E '<feature-branch>--(r[0-9]+-)?sub-[0-9]+'`. For each, check whether it has been merged into the feature branch (`git branch -r --merged <feature-branch>`). Merged sub-branches are candidates for deletion.

3. **Enumerate fetched/issue-N branches.** Run `git branch -r | grep -E '^origin/fetched/issue-[0-9]+$'`. Cross-reference with the feature-branch merge log (`git log --merges`) — branches whose content has been merged are candidates for deletion. Branches whose content was NEVER merged (e.g., abandoned single-shot fetches superseded by probe-then-body retries) are candidates for `not_planned` issue closure and branch deletion both.

4. **Enumerate leftover content in `research/fetched/`** (or equivalent ephemeral-content directories). For each subdirectory:
   - If the corresponding report cites only the source URLs (not local snapshots) AND the report's "Sources reviewed" table is ✅ for those URLs, the directory is a candidate for `git rm`.
   - If the directory is failed-fetch evidence (silent-404 files etc.) AND already documented in the report and run-report, it's a *judgement call* item — surface to the user with both options.
   - If the directory is NOT yet referenced in any committed report, do NOT recommend deletion. Surface as "in-flight content needing report-write or explicit abandonment."

5. **Test branch deletion capability** with one trial: try `git push origin --delete <some-merged-sub-branch>` and capture the exit code. If 0, the environment supports deletion — the dispatcher can do all branch deletes autonomously after user approval. If 403/non-zero, mark all branch-deletes as "needs UI cleanup by user" and DO NOT retry.

6. **Construct the checklist** as a single message to the user, grouped:
   - **Issues to close (completed):** numbered list with one line each.
   - **Issues to close (not_planned):** numbered list, justification per item.
   - **Branches to delete (merged sub-branches):** numbered list, marked with "needs UI cleanup" if the proxy blocks deletion.
   - **Branches to delete (fetched/issue-N, content already merged):** same.
   - **Leftover content directories:** per-directory, with the recommended action and an "ask user" flag where it's a judgement call.
   - **Followup PRs needed (e.g., for `git rm` cleanup commits):** explicit list.

7. **Await user instruction.** Execute deletions/closures the user approves; do not act unilaterally on anything past step 6.

## Concrete examples

### Example 1 — overnight session end with sandbox-proxy

After 3 fanout rounds + retrospective, user says "drain." Skill output:

> **Issues to close as `completed`:** #15, #17, #19, #20, #21, #22, #23 (fetch-urls workflow ran and content was merged into the feature branch).
> **Issues to close as `not_planned`:** #16 (workflow didn't re-fire after label re-application; superseded by #17), #18 (single-shot attempt superseded by probe-then-body #19+#20).
> **Branches to delete (needs UI cleanup — sandbox proxy blocks deletion):**
> - `claude/parallelize-with-subagents-p4Opo--sub-{01,02,03}`
> - `claude/parallelize-with-subagents-p4Opo--r4-sub-{01,02,03}`
> - `claude/parallelize-with-subagents-p4Opo--r5-sub-01`
> - `fetched/issue-{15,17,19,20,21,22,23,18}`
> **Leftover content (post-PR-merge):** `research/fetched/issue-21/` (6 files; silent-404 evidence — already documented in report 11's Sources Reviewed table and `harness/runs/20260511-r5/report.md`). Recommend `git rm`; ask user to confirm.

User reviews; says "close the issues, delete the fetched content." Skill closes the 9 issues via `mcp__github__issue_write` and opens a cleanup branch with the `git rm`.

### Example 2 — small session with no fetched content

Single-PR session ended with all work merged. Skill output:

> **Nothing to clean up.** All branches created in this session are merged and deleted. No open issues. No leftover content directories.

Total cost: 4 tool calls. The skill is cheap when there's nothing to do.

## Anti-patterns

- **Acting without surfacing the list.** Even when branch deletion is technically possible, the dispatcher must surface the list and wait for user approval. Silent deletion is the wrong default.
- **Re-trying a blocked operation in a loop.** When `git push --delete` returns 403, do NOT retry with backoff. The sandbox proxy is not a transient network failure; it's a permission boundary. Surface the branch list as "needs UI cleanup" and move on.
- **Closing fetch-urls issues whose workflow output is NOT merged.** The skill must verify that the fetched/issue-N branch's content has actually landed on the feature branch (`git log --merges | grep "fetched/issue-N"`) before recommending `state_reason: completed`. An open fetch issue whose branch was never merged should be `not_planned` (the work was abandoned) or stay open (the work is genuinely in flight).
- **Deleting content that's the only copy of evidence.** Silent-404 evidence under `research/fetched/issue-N/` is documentation. Before recommending `git rm`, confirm the report's "Sources reviewed" table fully captures what the files would have shown.
- **Forgetting open PRs.** Any branch that has an open PR against `main` (or against the feature branch) is NOT a candidate for deletion — surface it as "PR open, awaiting review/merge."

## Acceptance criteria

1. The skill runs at every user-signaled session-end (drain/wrap-up/we're done) and at every dispatcher-authored PR merge.
2. The checklist is a single grouped message; no per-item conversation rounds before the list lands.
3. Items marked "needs UI cleanup" are not retried by the dispatcher; the user gets the list and acts in the GitHub UI.
4. No deletion is executed without explicit user approval.
5. Fetch-urls issues are closed only after verifying their content was merged (or explicitly abandoned).
6. Leftover content directories surface with both options (keep as evidence vs delete) when the call is non-obvious.

## Files this skill creates / modifies

- The skill writes nothing to disk by default. Cleanup actions (branch deletes, `git rm`) happen only after user approval, and those write through normal git commit/push.
- An optional `retrospective/<date>-<seq>/cleanup-checklist.md` artifact may be written when the skill runs as part of a retrospective, capturing the list for audit.
