# `.github/scripts/`

Helpers for the `fetch-blocked-urls.yml` workflow.

| File | Purpose |
|---|---|
| `extract_urls.py` | Parse the issue body (from env var `BODY`) and emit one URL per line. Accepts a JSON array of URL strings or `{"urls": [...]}` object — either bare at the top of the body or inside a ```` ```json ```` fenced block. Everything outside the JSON is ignored. |
| `fetch_urls.sh` | Iterate `.fetch-work/urls.txt`, curl each URL (30s timeout, browser-ish UA, redirect-following), save raw HTML + html2text markdown into `research/fetched/issue-<N>/`, and write a per-URL summary to `.fetch-work/summary.md`. |

See `.github/workflows/fetch-blocked-urls.yml` for the wiring, and `.claude/skills/fetch-blocked-urls/SKILL.md` for the trigger / security model.

## Local test

```bash
# Bare JSON array at top:
BODY='["https://example.com","https://example.org"]' \
  python3 .github/scripts/extract_urls.py

# JSON object with urls key, free-form prose ignored below:
BODY=$'{"urls":["https://example.com"]}\n\nContext: ignored.' \
  python3 .github/scripts/extract_urls.py

# Fenced ```json``` block (preferred for issue UI rendering):
BODY=$'```json\n["https://example.com"]\n```' \
  python3 .github/scripts/extract_urls.py
```

```bash
mkdir -p .fetch-work
echo "https://example.com" > .fetch-work/urls.txt
ISSUE_NUMBER=0 bash .github/scripts/fetch_urls.sh
ls research/fetched/issue-0/
```
