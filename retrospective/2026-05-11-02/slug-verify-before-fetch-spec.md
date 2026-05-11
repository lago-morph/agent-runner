# Spec: `slug-verify-before-fetch`

## Intent

Stop the dispatcher from burning fetch issues on wrong URL slugs. Across three consecutive fanout rounds (3, 4, 5) in `agent-runner`, the lead dispatcher's paraphrase of an external content site's chapter/section titles produced wrong URL slugs three times — costing one whole bad-slug fetch issue (#15: all 404s), one silent-404 probe (#21: 200-OK with nav-skeleton-only body), and an inversion of two chapters (#22 corrected when the dispatcher's brief swapped chapter 2 "Prompt" and chapter 3 "Model"). Each round encoded a "verify slugs first" note in the PLAN.md process notes; each subsequent round still hit the same failure mode. The fix is to convert the inline reminder into a tool-enforced pre-flight: any dispatch that will open a `[fetch-urls]` issue with URLs containing slugs the dispatcher cannot point to a previously-fetched index for **must first probe at least one URL of the intended pattern**, and the probe must explicitly check for SPA silent-404 (200-OK + nav-skeleton-only).

## Trigger

**Direct trigger:** any planned `mcp__github__issue_write` call with title prefix `[fetch-urls]` whose body contains URLs the agent cannot trace to a previously-committed `research/fetched/issue-N/<index>.md` file.

**Proactive trigger:** when reading a `research/PLAN.md` "Future research" cluster whose description names external chapters/sections by *title* (English words), not by *verbatim slug* (the URL-path token).

**Negative trigger (skip the skill):** if the cluster description cites a verbatim slug AND quotes the URL from a previously-fetched index file in the same commit history, the slugs are already verified — no probe needed.

## Inputs

1. The dispatcher's planned URL list for the fetch issue.
2. The repo's `research/fetched/` directory (to check for prior index fetches that already authoritatively list the slugs).
3. The external content site's TOC or index URL pattern (the dispatcher's best guess of where slugs are listed).

## Outputs

1. **Either:** a verified slug list, ready for the body-fetch issue, with each slug traceable to a fetched index file committed in the repo.
2. **Or:** one or more `[fetch-urls]` probe issues whose body contains only chapter-index URLs (≤ 50). Their fetch results, once merged, become the authoritative source for downstream body-fetch issues.

The skill never produces a body-fetch issue without a verified slug list backing it.

## Workflow

1. **Inspect the planned URL list.** For each URL, identify the "chapter slug" — the URL-path token directly under the content-site root (e.g., `7-patterns` in `…/agentic-engineering-book/7-patterns/1-plan-build-review`).

2. **Search for prior authoritative evidence.** Run `git grep -l '<slug>' research/fetched/ research/INDEX.md`. If a previously-merged fetched index page contains the slug verbatim, mark the slug verified. If a previously-merged report's "Sources reviewed" table lists a URL with the exact slug AND status ✅, mark verified.

3. **For unverified slugs, do NOT open the body-fetch issue yet.** Instead, construct a probe issue:
   - Title: `[fetch-urls] <topic> indexes (probe)` — the word "probe" or "indexes" in the title is mandatory.
   - Body: one URL per line, only the chapter-index URLs (e.g., `…/agentic-engineering-book/7-patterns` without subchapter suffix).
   - Labels: `["fetch-urls"]`.

4. **Open the probe issue** via `mcp__github__issue_write` method=create.

5. **Wait for the fetched branch** via `git ls-remote --exit-code --heads origin fetched/issue-N`. Cap wait at 15 minutes; expected wall time is 3-5 min.

6. **Merge the fetched branch** into the working branch: `git fetch origin fetched/issue-N && git merge --no-ff origin/fetched/issue-N`.

7. **Validate each fetched index page for SPA silent-404** (this is the second half of the skill — see anti-patterns):
   - If the `.md` body is < 8 KB AND contains only the site's navigation skeleton (typically the chapter-list sidebar with no chapter-title H1 or substantive body content), the slug is wrong. The probe failed silently. The URL must be retried with a corrected slug; if no corrected slug is known, mark the cluster blocked and surface to the user.
   - If the `.md` body has substantive content (≥ 8 KB AND a chapter-title H1 or comparable structural element), the slug is verified.

8. **Extract subchapter slugs from each verified index file** by parsing the `.md` for in-page anchor links or sidebar entries pointing to subchapter URLs.

9. **Construct the body-fetch issue** with the verified subchapter URLs. Now and only now, open the body-fetch issue.

10. **In the resulting report's "Sources reviewed" table**, mark any silent-404 probe URLs as ❌ with a note explaining the failure mode — these are evidence and should not be silently dropped.

## Concrete examples

### Example 1 — slug-verification catches an inversion

`agent-runner` PLAN.md Round-5 cluster: "AE book chapters 1, 2, 3 — Chapter 2 (Models) and Chapter 3 (Prompting)."

Dispatcher's first instinct: open one fetch issue with URLs `…/1-foundations`, `…/2-models`, `…/3-prompting`. The slugs are unverified — no prior fetched index contains `2-models` or `3-prompting`.

Skill says: probe first. Probe issue #21 opens with the three index URLs. Workflow runs. Merging the fetched branch reveals:
- `1-foundations.md` is 16 KB with a chapter-title H1 — slug verified.
- `2-models.md` is ~6 KB containing only the chapter-list sidebar (no chapter title, no body) — silent-404 detected.
- `3-prompting.md` is ~6 KB, same pattern — silent-404 detected.

The probe surfaces the real chapter names by reading the chapter-1 sidebar (which lists all chapters): chapter 2 is `2-prompt` (singular), chapter 3 is `3-model` (singular). The brief had them swapped. A corrected probe issue #22 confirms `2-prompt` and `3-model` are real. Body-fetch issue #23 with verified slugs succeeds for all 10 URLs at HTTP 200.

Without the skill: the dispatcher would have opened one issue with 20+ URLs containing two wrong slugs. The fetch would have appeared to succeed (200-OKs throughout); only post-merge reading would have caught the empty pages, and 10+ URLs of subchapter probes against wrong parent slugs would all have silent-404'd too.

### Example 2 — slug-verification skipped because slugs are already verified

A later round adds a cluster reading more subchapters of chapter 7 (`7-patterns`). The dispatcher planned URLs include `…/7-patterns/12-something-new`. The skill runs the search: `git grep -l '7-patterns' research/fetched/` finds `research/fetched/issue-17/<hash>__7-patterns.md` and `research/fetched/issue-17/<hash>__7-patterns__1-plan-build-review.md`. Slug `7-patterns` is verified. The new subchapter slug `12-something-new` is unverified, but the parent is. Skill recommendation: probe the chapter-7 index ONCE more (in case new subchapters have been added since issue-17), then proceed. If the dispatcher prefers to skip the probe (parent-slug-verified is a strong signal), they may proceed with a `--no-probe-known-parents` override, accepting that any new subchapter URLs might 404 individually but won't silent-404 catastrophically.

## Anti-patterns

- **Trusting English chapter titles in PLAN.md.** "Chapter 5: Tools" sounds authoritative. The actual URL slug is `5-tool-use`. Always verify against a fetched index.
- **Trusting your own paraphrase.** Even after Round 3 encoded "verify slugs first" in PLAN.md process notes, Round 4 still hit the same failure mode because the cluster description was the dispatcher's own paraphrase. The fix is to encode the *verbatim slug* in the cluster description, not the chapter title.
- **Skipping SPA silent-404 detection.** A 200-OK response is not evidence of a successful fetch on JavaScript-rendered single-page applications. The skill's step 7 is mandatory, not optional.
- **Treating the probe issue as overhead.** A probe issue costs ~3-5 min wall time and one fetch-workflow run. A bad body-fetch costs the same wall time plus the engineering work of debugging why the body content looks like a navigation menu.
- **Merging the silent-404 fetched branch and immediately deleting the evidence.** Keep the failed-fetch `.md` files in the report's "Sources reviewed" table as ❌ with a note. They're the verbatim record of the failure mode and prevent the lesson from rotting.

## Acceptance criteria

1. The skill activates on any `[fetch-urls]` issue creation whose URL list contains slugs not verified by a prior fetched index file or a prior ✅ report row.
2. The probe issue is opened with title containing "probe" or "indexes" — the word is mandatory for downstream tooling that may filter on it.
3. The merge-then-validate step rejects fetched files with < 8 KB body AND no chapter-title H1, marking them as silent-404.
4. The body-fetch issue is never opened until at least one verified-index file exists for each chapter-slug in the URL list.
5. Failed-fetch evidence (silent-404 .md files) is retained in the report's "Sources reviewed" table as ❌ rows, not silently dropped.

## Files this skill creates / modifies

- `.github/scripts/fetch_urls.sh` — optional enhancement: add a post-fetch line to the per-URL summary tagging responses where bytes < 8 KB AND body matches nav-skeleton pattern.
- The skill itself does not write report files — it gates the dispatcher's fetch-issue-opening behavior.
- The dispatcher's `research/<report>.md` "Sources reviewed" table — the skill's outputs feed into this table's ❌ rows.
