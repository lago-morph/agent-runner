#!/usr/bin/env python3
"""Extract URLs from the issue body env var BODY.

The body MUST contain a JSON value at the top (either a JSON array of
URL strings, or a JSON object with a "urls" key whose value is an array
of URL strings). Anything that isn't valid JSON at the start of the body
is ignored. Free-form prose, session-URL footers, or context notes
*below* the JSON are ignored too.

Accepted shapes:

  ["https://example.com", "https://other.example/page"]

  {"urls": ["https://example.com", "https://other.example/page"]}

The JSON may optionally be wrapped in a ```json ... ``` fenced code
block (which renders better in the GitHub issue UI). If a fenced block
is present anywhere in the body, it wins over any bare JSON; this lets
authors put prose at the top of the issue and the URL list below in a
fenced block if they prefer.

URLs are validated minimally: must be strings, must start with http://
or https://, length <= 2048. Duplicates dropped (first occurrence wins).
Surrounding whitespace stripped.

Exit code: always 0. If parsing fails or no URLs are produced, stdout
is empty and the workflow's url-count step takes the no_urls path.
"""
from __future__ import annotations

import json
import os
import re
import sys
from typing import Any

BODY = os.environ.get("BODY", "")
MAX_URL = 2048

# Fenced ```json``` block, anywhere in the body. Non-greedy.
_FENCED = re.compile(r"```json\s*\n(.*?)\n```", flags=re.DOTALL)


def _parse_json(body: str) -> Any | None:
    """Return the parsed JSON value from the body, or None if no parse.

    Strategy:
      1. If a ```json``` fenced block is present, parse its contents.
      2. Else, if the body (after lstrip) starts with `{` or `[`, parse
         the leading JSON value via raw_decode (stops at end of value).
      3. Else, return None.
    """
    m = _FENCED.search(body)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError as e:
            print(f"Fenced JSON block failed to parse: {e}", file=sys.stderr)
            return None

    stripped = body.lstrip()
    if not stripped or stripped[0] not in "{[":
        return None
    try:
        value, _ = json.JSONDecoder().raw_decode(stripped)
        return value
    except json.JSONDecodeError as e:
        print(f"Top-of-body JSON failed to parse: {e}", file=sys.stderr)
        return None


def _urls_from_value(value: Any) -> list[str]:
    if isinstance(value, list):
        items = value
    elif isinstance(value, dict) and isinstance(value.get("urls"), list):
        items = value["urls"]
    else:
        return []

    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        if not isinstance(item, str):
            continue
        u = item.strip()
        if not u or len(u) > MAX_URL:
            continue
        if not (u.startswith("http://") or u.startswith("https://")):
            continue
        if u in seen:
            continue
        seen.add(u)
        out.append(u)
    return out


def main() -> int:
    value = _parse_json(BODY)
    if value is None:
        print(
            "No JSON found in issue body "
            "(expected an array of URLs or {'urls': [...]}).",
            file=sys.stderr,
        )
        return 0
    urls = _urls_from_value(value)
    for u in urls:
        print(u)
    print(f"Extracted {len(urls)} URLs from JSON.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
