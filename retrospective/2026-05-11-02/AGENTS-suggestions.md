# AGENTS.md suggestions — 2026-05-11-02

These are proposed additions to the project's agents file (typically `AGENTS.md` at the repo root). Each section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for doing it, grounded in something that happened (or nearly happened).

Decide each on its own merits. Skip ones that don't apply to your operating posture; copy-paste the ones that do.

---

## Suggestion 1: Verbatim-slug rule for external content references

### Proposed addition

> **Verbatim-slug rule.** When `research/PLAN.md` (or any plan document) names external content by chapter/section title, cite the verbatim URL slug from a previously-fetched index page, with the URL. Do NOT paraphrase. The dispatcher's English-language paraphrase of "Chapter 5: Tools" is not authoritative evidence — only `5-tool-use` from a fetched `…/5-tool-use.md` is. Before opening any `[fetch-urls]` issue, every chapter slug in the URL list must either match a slug already present in `research/fetched/` or be the target of a separate probe issue.
>
> *Grounded in: three consecutive slug-paraphrase failures in Rounds 3, 4, 5 (chapter 7 was `7-patterns` not `7-architecture`; chapter 5 was `5-tool-use` not `5-tools`; chapters 2 and 3 were inverted as `2-prompt` and `3-model`).*

### Why this earns its place in your agents file

The lesson encoded in three successive PLAN.md updates failed to prevent the fourth recurrence. Inline reminders read as conversational; rules in AGENTS.md read as enforceable. Round 3 burned issue #15 entirely (20+ URLs, all returning 404 stubs). Round 4 caught it at the probe step (saved ~3 min wall time + ~20 URL fetches). Round 5 caught it at probe but only because the previous round's lesson had been encoded in the brief — without that, the silent-404 from `2-models` would have looked like a successful 200-OK fetch and the wrong-slug body fetches would have all silent-404'd too. Marginal cost of the rule: one extra `git grep` against `research/fetched/` before opening a fetch issue. Marginal benefit: prevents a category of failure that has hit three sessions in a row.

---

## Suggestion 2: SPA silent-404 detection

### Proposed addition

> **SPA silent-404 detection.** A fetched page from a JavaScript-rendered single-page application that returns 200-OK but has an `.md` (html2text) body under 8 KB containing only the site's navigation skeleton (no chapter-title H1 or comparable substantive heading) is a 404 in disguise. Treat the URL as ❌ Unavailable. Either the slug is wrong (most common) or the page doesn't exist. Do not assume content existence from HTTP status alone for JS-rendered sites.
>
> *Grounded in: issue #21 probe of `2-models` and `3-prompting` slugs, both returned 200-OK with ~6 KB nav-only skeletons.*

### Why this earns its place in your agents file

Without this rule, silent 404s look like successful fetches and propagate empty content into the dispatcher's reading queue. The subagent that catches it at drain step does so because they read the file body; one that trusts the per-URL summary's "HTTP 200, 6234 bytes" line does not. The rule converts the implicit "read the body, don't trust the status" practice into an explicit detection criterion. Marginal cost: one `wc -c` + one `grep` per fetched file. Marginal benefit: stops fabricated-from-empty-content claims before they reach a written report.

---

## Suggestion 3: `isolation: "worktree"` mandatory for parallel fanout

### Proposed addition

> **Always dispatch parallel subagents with `isolation: "worktree"`.** Concurrent Agent calls that share the dispatcher's working directory race on `git checkout <sub-branch>` and contaminate each other's branches — files committed onto the wrong sub-branch, untracked files leak between sibling workdirs, the merge phase becomes a manual cherry-pick exercise. The `isolation: "worktree"` parameter gives each subagent its own git-worktree on its assigned branch and these collisions cannot happen. The cost is one extra parameter per Agent call.
>
> *Grounded in: codified in `.claude/skills/parallel-subagent-fanout/SKILL.md` after Round-2's cross-workdir contamination; Rounds 3, 4, 5 confirmed zero contamination with worktree isolation across 7 parallel-or-serial dispatches.*

### Why this earns its place in your agents file

The skill encodes it, but the skill is consulted only when invoked. AGENTS.md is consulted at session start. Rounds 3 + 4 + 5 dispatched 7 subagents across 3 fanout rounds; zero merge cleanup at the integration layer. The Round-2 baseline (no isolation) required cherry-picking just the report files because branches had been stomped. Marginal cost: 1 line per Agent call. Marginal benefit: 0 merge-cleanup work, 0 lost commits, 0 confusion about which sub-branch a file landed on.

---

## Suggestion 4: GitHub MCP scope is repo-locked

### Proposed addition

> **GitHub MCP tools (`mcp__github__*`) are scoped to `lago-morph/agent-runner` only.** Any cross-repo work — reading issues in `anthropics/claude-code-action`, searching code in `OpenHands/OpenHands`, listing releases in any other repo — must go through `WebFetch` against the appropriate URL (typically `raw.githubusercontent.com` for files, `github.com/<org>/<repo>/issues/<N>` for issues, `github.com/<org>/<repo>/releases` for releases). Calls to `mcp__github__*` targeting other repos will fail.
>
> *Grounded in: Round 3 sub-03 (OAuth refresh watch) had to fall back to WebFetch for `anthropics/claude-code-action/issues/727` and the releases page after `mcp__github__issue_read` was unavailable cross-repo.*

### Why this earns its place in your agents file

A subagent that doesn't know the scope policy wastes a tool call discovering it. Round 3 sub-03 worked around the constraint inline but cost time and noise. Marginal cost: one rule line. Marginal benefit: subagents reach for the right tool first.

---

## Suggestion 5: Repeat-round sub-branch naming

### Proposed addition

> **Repeat-fanout sub-branch naming.** When a feature branch has already had a fanout run merged AND the sandbox proxy blocks `git push origin --delete` (common in CI-runner environments), the prior `<feature>--sub-NN` branches remain on origin. For a second fanout run from the same feature branch, use suffix `<feature>--r<N>-sub-NN` (where `<N>` is the round number) to avoid collisions with the still-present prior round's branches.
>
> *Grounded in: Round 4 used `--r4-sub-NN` because `--sub-NN` from Round 3 still existed on origin; Round 5 used `--r5-sub-NN`.*

### Why this earns its place in your agents file

Branch-name collisions on origin produce confusing `git push -u origin <branch>` failures (or worse, silent overwrites if force-pushed). The convention is small and self-documenting in `git log --all --oneline --decorate`. Marginal cost: name discipline. Marginal benefit: clean origin namespace + audit-friendly branch names.

---

## Suggestion 6: `.fetch-work/urls.txt` merge conflicts union-merge

### Proposed addition

> **`.fetch-work/urls.txt` merges by union.** When a sub-branch merges multiple `fetched/issue-N` branches in sequence (each of which rewrote `.fetch-work/urls.txt` with only its own URL list), the merge conflicts on this file. The canonical resolution is union — keep ALL historical URL lines so the manifest preserves provenance across the lifetime of the sub-branch.
>
> *Grounded in: Round 4 r4-sub-01 had two fetched-branch merges, both produced conflicts on `.fetch-work/urls.txt`, both resolved by union; Round 5 r5-sub-01 had three fetched-branch merges with the same conflict and the same resolution.*

### Why this earns its place in your agents file

Without this rule, a subagent might pick `--ours` (loses prior URL evidence) or `--theirs` (loses new URL evidence). Both are wrong; union is right and consistent with the manifest's purpose (record what was originally fetched). Marginal cost: 30 seconds of conflict resolution. Marginal benefit: persistent fetch provenance.

---

## Suggestion 7: `mcp__github__issue_write` label re-application does NOT re-fire workflow

### Proposed addition

> **Label re-application via `mcp__github__issue_write update` does NOT re-fire `issues.labeled` workflows.** If a workflow needs retriggering on an existing issue, open a *new* issue with the same labels rather than mutating the old one. `workflow_dispatch` is also available where the workflow definition supports it. Do NOT attempt to retrigger via label-remove-then-readd cycles; the action either does not fire on the second add or fires in a state the workflow author didn't intend.
>
> *Grounded in: Round 3 issue #16 — a retry of issue #15 with corrected slugs via body edit + label re-application — never fired a follow-up workflow run, despite `gh issue view 16` showing the correct body and labels. Recovered by opening fresh issue #17.*

### Why this earns its place in your agents file

The intuitive recovery path (edit body, re-apply label) fails silently. Without this rule, a future agent will repeat the recovery attempt and waste a round-trip. Marginal cost: one rule. Marginal benefit: skips an inert recovery path.

---

## Suggestion 8: Sandbox proxy blocks `git push --delete` — UI cleanup needed

### Proposed addition

> **Sandbox proxy environments return HTTP 403 on `git push origin --delete`.** Do NOT retry with backoff — this is not a transient network failure, it's a permission boundary. Surface stale-branch lists to the user as "needs UI cleanup" and move on. Branches that the dispatcher cannot delete remain on origin until the user deletes them via the GitHub UI.
>
> *Grounded in: every fanout round in this session (3, 4, 5) accumulated sub-branches and `fetched/issue-N` branches that the dispatcher could not delete; user UI cleanup is the established workaround.*

### Why this earns its place in your agents file

Without this rule, an agent will retry deletes with exponential backoff thinking the proxy is rate-limiting, consuming a full minute or more per stale branch. Marginal cost: one rule line. Marginal benefit: stops a class of failed-retry loops.

---

## Suggestion 9: Lead-merge discipline in fanout

### Proposed addition

> **In a parallel-subagent-fanout run, only the lead dispatcher merges sub-branches.** Subagents must NOT open PRs against the feature branch and must NOT merge sub-branches into the feature branch themselves. Subagents commit and push to their sub-branch only; the lead agent then merges in plan order (not arrival order) per the `parallel-subagent-fanout` skill.
>
> *Grounded in: all 7 sub-branch dispatches across Rounds 3, 4, 5 followed this discipline successfully; zero merge conflicts at the integration layer.*

### Why this earns its place in your agents file

Without this rule, two subagents could open PRs against the same target branch and trigger CI conflicts, or a subagent could merge its own work and the lead agent loses the plan-order discipline. Marginal cost: one bullet in each subagent brief. Marginal benefit: deterministic integration order + reproducible run reports.

---

## Suggestion 10: `mcp__github__issue_write` auto-creates unknown labels

### Proposed addition

> **`mcp__github__issue_write` with an unknown `labels: [...]` value auto-creates the label** (default color `#ededed`). No separate label-bootstrap step is needed when introducing a new workflow-driving label like `fetch-urls`. Just pass it on issue creation; the label appears in the repo's label set after the first issue lands.
>
> *Grounded in: the `fetch-urls` label was auto-created by the first issue in this repo's history that referenced it; documented in `.claude/skills/research-pipeline/SKILL.md`.*

### Why this earns its place in your agents file

A subagent that doesn't know this might call `mcp__github__create_label` (which doesn't exist in this MCP) or skip the labeling step entirely (which breaks workflow gating). Marginal cost: zero (just documents existing behavior). Marginal benefit: subagents don't go searching for a label-creation tool that doesn't exist.

---

## Suggestion 11: Per-fanout state-discipline contract

### Proposed addition

> **Every fanout run produces a `harness/runs/<run_id>/` triple.** Files: `state.json` (subtask statuses, PRs, tests deltas), `plan.yaml` (the approved decomposition), and `report.md` (post-merge run report with summary table + merge log + deviations + lessons). The triple lands on the feature branch in the same commit that updates `research/INDEX.md` and `research/PLAN.md`. This is non-optional even for single-subtask "fanouts" — the trace value of the state.json + report.md pair is worth the overhead.
>
> *Grounded in: Rounds 3, 4, 5 each landed the full triple, and a fourth retrospective session reading just the triples could reconstruct the work without consulting the research reports themselves.*

### Why this earns its place in your agents file

Without this rule, a fanout discipline lapses to "merge and forget" and the audit trail dies on a feature branch that gets merged or rebased. Marginal cost: ~5 min writing the run report. Marginal benefit: permanent reproducibility.

---

## Suggestion 12: Probe-then-body fetch pattern as default

### Proposed addition

> **When external content slugs are not authoritatively known, the fetch workflow is two issues, not one.** Open `[fetch-urls] <topic> indexes (probe)` with only the chapter-index URLs first; after the workflow merges, parse the index `.md` files for verbatim subchapter slugs; then open `[fetch-urls] <topic> bodies` with the verified subchapter URLs. The added wall time (~3-5 min for the probe round trip) is small versus the cost of body-fetching against wrong slugs (a whole fetch issue's worth of silent-404s).
>
> *Grounded in: Round 4 r4-sub-01 generalized this from Round 3's lesson; Round 5 r5-sub-01 used it and caught the chapter-2/3 inversion at probe step.*

### Why this earns its place in your agents file

Without this rule, single-shot fetches against unverified slugs produce both 404s and silent-404s in the same issue, making the failure mode hard to diagnose. Marginal cost: one extra fetch round trip (~3-5 min) when slugs aren't verified. Marginal benefit: prevents catastrophic-but-silent body-fetch failures.

---

## Suggestion 13: Close fetch-urls issues at drain step

### Proposed addition

> **At session end / "drain", close all `fetch-urls`-labeled issues whose content has been merged into the working line.** Use `state_reason: completed` for issues whose workflow succeeded and whose fetched content landed on a working branch. Use `state_reason: not_planned` for issues whose workflow never fired, or whose content was abandoned (e.g., superseded by a probe-then-body retry). Leave open ONLY issues that are genuinely in-flight as of session end.
>
> *Grounded in: 9 `fetch-urls` issues (#15–#23) opened during this overnight session; all closed in the drain step with appropriate state_reasons.*

### Why this earns its place in your agents file

Open issues on a repo are an attention surface. Issues whose work is done but state is still open create false signal — a future maintainer scans them looking for actionable items. Marginal cost: one `mcp__github__issue_write` per closed issue (parallelizable in a single message). Marginal benefit: clean issue tracker + clear audit boundary between "in-flight" and "wrapped" work.
