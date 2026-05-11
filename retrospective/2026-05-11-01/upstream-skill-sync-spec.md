# Spec: `upstream-skill-sync`

## Intent

Skills in this repo originate from upstream skill libraries (currently `lago-morph/software-factory` and historically `lago-morph/ai-skills`). When the upstream releases an updated version of a skill, the local copy needs to be replaced — file-for-file — to match the upstream layout, including deletions of files the upstream dropped. The operation is not strictly mechanical: per-file diffs, dropped-file detection, optional session-mirror, and the project's required PR workflow all have to compose. This skill packages that composition so future syncs are predictable and reviewable.

Grounded in: PR #10 (commit `adc5c9b`) updating `self-retrospective` from upstream. The substantive part of the work was straightforward once the workflow was settled, but settling the workflow ate disproportionate decision overhead.

## Trigger

### Direct triggers — activate immediately

- "Update the `<skill-name>` skill from upstream"
- "Grab the update [for `<skill-name>`] and install it"
- "Sync `<skill-name>` to the latest upstream"
- "Pull `<skill-name>` from `<upstream-url>`"

### Proactive triggers

- The user pastes a GitHub URL pointing inside a `.claude/skills/<name>/` directory of a known upstream repo.
- The user says a skill's wording or behavior is "stale" and references a known upstream.

### Negative triggers — do NOT activate

- The user is **authoring** a new skill from scratch — use a skill-authoring spec instead, not this sync flow.
- The user is **editing** a local skill to diverge from upstream intentionally — this skill assumes upstream is the source of truth.
- The user only wants to read the upstream version, not install — fetch and show, do not branch/commit.

## Inputs

- `SKILL_NAME` — the directory name under `.claude/skills/` (e.g., `self-retrospective`).
- `UPSTREAM_URL` — the upstream repository (e.g., `https://github.com/lago-morph/software-factory`). The skill directory is assumed to live at `.claude/skills/<SKILL_NAME>/` in the upstream too.
- `MIRROR_TO_SESSION` (optional, default false) — if true, also copy to `~/.claude/skills/<SKILL_NAME>/` so the running harness picks up the change without a session restart.

## Outputs

- File replacements in `.claude/skills/<SKILL_NAME>/` matching upstream exactly (additions, modifications, deletions).
- Optional mirror at `~/.claude/skills/<SKILL_NAME>/`.
- One commit on a feature branch `claude/update-<SKILL_NAME>-skill`.
- One pushed branch.
- One open PR titled `Update <SKILL_NAME> skill to upstream <owner>/<repo>` with a body listing every changed file with size deltas and the upstream commit URL.

The skill does **not** auto-merge the PR by default; merging is the user's call (or a separate plumbing-PR-autopilot invocation).

## Workflow

1. **Shallow-clone the upstream into `/tmp`**:
   ```bash
   git clone --depth 1 "$UPSTREAM_URL" "/tmp/<repo-name>"
   ```
   Do NOT use WebFetch per-file or the GitHub MCP server's `get_file_contents` — both add friction relative to a one-shot clone. The GitHub MCP server in particular is typically allow-listed to the working repo only, so it cannot read arbitrary upstreams.

2. **Enumerate upstream and local file sets** for `.claude/skills/<SKILL_NAME>/`:
   ```bash
   find /tmp/<repo-name>/.claude/skills/<SKILL_NAME> -type f
   find .claude/skills/<SKILL_NAME> -type f
   ```
   Compute three sets: `to_replace` (in both), `to_add` (upstream only), `to_delete` (local only).

3. **Diff `to_replace` files** to confirm there are real differences. If a file is byte-identical, leave it untouched (do not stage a no-op change). Use `diff -q` or `cmp -s`.

4. **Create the feature branch** off the current branch (typically `main`):
   ```bash
   git checkout -b claude/update-<SKILL_NAME>-skill
   ```

5. **Apply changes**: `cp` upstream files over `to_replace` and `to_add`; `rm` `to_delete`. Do not preserve `to_delete` files — the upstream dropping a file is an intentional layout decision and must be mirrored.

6. **If `MIRROR_TO_SESSION` is true**: also copy each upstream file into `~/.claude/skills/<SKILL_NAME>/` and `rm` matching `to_delete` entries there. Create the directory if needed. Do **not** commit this mirror — it is ephemeral.

7. **Verify file sizes match** across three locations (upstream / repo / session-mirror if applicable) before committing. A size mismatch is a copy error.

8. **Cleanup**: `rm -rf /tmp/<repo-name>` once verification passes.

9. **Commit, push, open PR**:
   ```bash
   git add .claude/skills/<SKILL_NAME>/
   git commit -m "Update <SKILL_NAME> skill to upstream <owner>/<repo>"
   git push -u origin claude/update-<SKILL_NAME>-skill
   ```
   Open PR via `mcp__github__create_pull_request`. Body must include: (a) summary of behavior change, (b) per-file size delta table, (c) list of deleted files with a one-line reason ("upstream release dropped them"), (d) upstream URL, (e) note about session-mirror if applicable.

10. **Stop** — do not auto-merge. Surface the PR URL to the user. If the user requests autopilot, hand off to `plumbing-pr-autopilot` as a separate invocation.

## Concrete examples

### Example 1: PR #10 — `self-retrospective` sync from `lago-morph/software-factory`

- Inputs: `SKILL_NAME=self-retrospective`, `UPSTREAM_URL=https://github.com/lago-morph/software-factory`, `MIRROR_TO_SESSION=true`.
- File-set diff:
  - `to_replace`: `SKILL.md` (12,735 → 17,307 bytes), `spec/SPEC.md` (9,662 → 12,061 bytes).
  - `to_add`: none.
  - `to_delete`: `README.md`, `spec/README.md`.
- Branch: `claude/update-self-retrospective-skill`.
- Commit: `adc5c9b` — "Update self-retrospective skill to upstream lago-morph/software-factory".
- Mirror: created `~/.claude/skills/self-retrospective/SKILL.md` and `~/.claude/skills/self-retrospective/spec/SPEC.md`. Harness re-scanned and surfaced the new description string.
- PR: #10, opened with size-delta table and dropped-files note. Merged via separate plumbing-PR-autopilot pass.

### Example 2: hypothetical sync where upstream adds a new file

- Inputs: `SKILL_NAME=research-pipeline`, `UPSTREAM_URL=https://github.com/lago-morph/software-factory`, `MIRROR_TO_SESSION=false`.
- File-set diff (hypothetical):
  - `to_replace`: `SKILL.md` (size unchanged but `diff -q` reports differences).
  - `to_add`: `scripts/probe-sources.sh` (new in upstream).
  - `to_delete`: none.
- Step 3 catches the no-content `SKILL.md` change and proceeds; step 5 copies both files; PR body lists `scripts/probe-sources.sh` as new with size and permissions noted.

## Anti-patterns

- **Using WebFetch or `mcp__github__get_file_contents` for arbitrary upstream files.** WebFetch is per-URL and slow over multiple files; the GitHub MCP server is typically allow-listed to the working repo. `git clone --depth 1` is faster and unambiguous about which commit you got.
- **Skipping the deletion mirror.** Upstream dropped a file → drop it locally. Keeping a "harmless" stale README in the local skill dir produces drift that compounds over future syncs.
- **Committing the `~/.claude/` mirror.** That path is outside the working tree; even if it weren't, it's session-ephemeral and must not enter version control.
- **Auto-merging the resulting PR from inside this skill.** Sync is one decision; merging is another. Keep them separate so a user reviewing the diff has a window.
- **Trusting the upstream tree URL to enumerate files.** Browsing `github.com/<owner>/<repo>/tree/<ref>/<path>` does not give you a deterministic file list in a sandbox WebFetch context (HTML parsing, redirects, rate limits). Clone instead.
- **Re-fetching the upstream more than once per sync.** One clone, one verification pass, one cleanup. If the work loops back, that means a previous step failed — debug it, don't re-clone blindly.

## Acceptance criteria

1. The repo's `.claude/skills/<SKILL_NAME>/` is byte-identical to the upstream's `.claude/skills/<SKILL_NAME>/` at the cloned ref after the PR merges.
2. The PR body contains a per-file size-delta table that matches what `git diff --stat` reports.
3. `/tmp/<repo-name>` no longer exists after the skill finishes.
4. If `MIRROR_TO_SESSION` was true, the running harness's skill-list reflects the updated description string (verifiable in the next system-reminder skill-list block).
5. The PR is left open for the user to merge; the skill does not call `mcp__github__merge_pull_request`.

## Files this skill creates / modifies

- `.claude/skills/<SKILL_NAME>/**` — replaced and deleted as needed to match upstream.
- `~/.claude/skills/<SKILL_NAME>/**` — mirrored if `MIRROR_TO_SESSION` is true (not in version control).
- One new git branch `claude/update-<SKILL_NAME>-skill` with a single commit.
- One new open PR.