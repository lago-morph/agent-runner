# Report 10 — OpenHands provider pagination shapes (GitLab / Bitbucket / Azure DevOps)

**Date:** 2026-05-11
**Author:** Subagent (run 20260511-r4, sub-03)
**Status:** ✅ complete — three required provider files (GitLab, Bitbucket Cloud, Azure DevOps) read end-to-end. One supplementary file (Forgejo `repos.py`) read and included. One supplementary path (`bitbucket_dc/service/repos.py`) returned 404 — Bitbucket Data Center is a single-file stub with no `service/` mixin layout and no `get_paginated_repos` implementation; documented in sources table and excluded from the comparison.

## Lead question

What pagination conventions does each OpenHands git-provider use, and what `_paginate(url, max, ...) -> list[dict]` Protocol would let `agent-runner`'s Stage-4 `ProviderClient` cover all five providers (GitHub baseline + GitLab + Bitbucket Cloud + Azure DevOps + Forgejo) with one default implementation plus per-provider overrides for the cases that genuinely need them?

## 1. GitHub baseline (recap from report 05)

Report 05 §2.1 quoted `_fetch_paginated_repos` from `openhands/app_server/integrations/github/service/repos.py` verbatim. Recap (1-2 paragraphs, see report 05 for the body verbatim):

```python
async def _fetch_paginated_repos(
    self, url: str, params: dict, max_repos: int, extract_key: str | None = None
) -> list[dict]:
    ...
    while len(repos) < max_repos:
        page_params = {**params, 'page': str(page)}
        response, headers = await self._make_request(url, page_params)
        page_repos = response.get(extract_key, []) if extract_key else response
        if not page_repos: break
        repos.extend(page_repos)
        page += 1
        link_header = headers.get('Link', '')
        if 'rel="next"' not in link_header: break
    return repos[:max_repos]
```

The shape: an integer page counter incremented client-side, two termination conditions (empty page OR no `rel="next"` in `Link` header), an optional `extract_key` because GitHub Apps installation endpoints wrap the array in `{"repositories": [...]}`, and a final `[:max_repos]` trim. This is **the loop the other four providers diverge from in distinct, individually surprising ways.**

## 2. GitLab (`openhands/app_server/integrations/gitlab/service/repos.py`)

### 2.1 Signatures

GitLab does **not** define a private `_fetch_paginated_repos` helper. Pagination is *inlined* twice — once in `get_paginated_repos` (single page) and once in `get_all_repositories` (multi-page loop). Verbatim from `get_all_repositories`:

```python
while len(all_repos) < MAX_REPOS:
    params = {
        'page': str(page),
        'per_page': str(PER_PAGE),
        'order_by': order_by,
        'sort': 'desc',  # GitLab uses sort for direction (asc/desc)
        'membership': 1,  # Use 1 instead of True
    }
    response, headers = await self._make_request(url, params)

    if not response:  # No more repositories
        break

    all_repos.extend(response)
    page += 1

    # Check if we've reached the last page
    link_header = headers.get('Link', '')
    if 'rel="next"' not in link_header:
        break
```

### 2.2 Cursor mechanism

**Same as GitHub.** Server-side `Link` header with `rel="next"`, plus client-side `page` counter and a `per_page` knob. GitLab REST returns the array at the top level (no `extract_key` needed). Termination is the same dual condition as GitHub.

### 2.3 Quirks

- **`MAX_REPOS = 1000`, `PER_PAGE = 100`** are hard-coded; GitLab caps `per_page` at 100.
- **`'sort': 'desc'` is direction, not a field.** The sort *field* is named `order_by` on GitLab. The sort *direction* is named `sort`. This is the inverse of GitHub's `sort=updated&direction=desc` and trips up almost every port. There is a small mapping dict (lines 105-110, 142-147) translating GitHub's vocabulary (`'pushed', 'updated', 'created', 'full_name'`) to GitLab's (`'last_activity_at', 'last_activity_at', 'created_at', 'name'`).
- **`'membership': 1` not `True`.** Comment in source: `# Use 1 instead of True`. Suggests the GitLab server rejects Python's `bool` JSON encoding (`true`); needs the integer `1`. Trap.
- **Repository identifier is URL-encoded with `%2F`** in `get_repository_details_from_repo_name`: `encoded_name = repository.replace('/', '%2F')`. GitLab's REST treats `/` in repo paths as a path separator unless escaped.
- **Single-page `get_paginated_repos` has no termination logic** — caller is expected to advance `page` by reading the `Link` header off the returned `Repository.link_header`.

### 2.4 Borrow / skip verdict

**Borrow** the dual-termination loop shape (it's the same as GitHub). **Skip** the `'membership': 1` and `order_by`/`sort` mapping in the *Protocol* — those are GitLab-specific param construction that belongs in the GitLab subclass's `get_paginated_repos`, not in the shared `_paginate` helper. The mechanics of pagination are *identical* to GitHub; the diverging surface is parameter-construction.

## 3. Bitbucket Cloud (`openhands/app_server/integrations/bitbucket/service/repos.py`)

### 3.1 Signatures

Bitbucket Cloud is the **first real divergence.** Pagination lives in a base-class helper `_fetch_paginated_data(url, params, max_items)` (defined in `bitbucket/service/base.py`, not `repos.py`), quoted verbatim:

```python
async def _fetch_paginated_data(
    self, url: str, params: dict, max_items: int
) -> list[dict]:
    """Fetch data with pagination support for Bitbucket API."""
    all_items: list[dict] = []
    current_url = url

    while current_url and len(all_items) < max_items:
        response, _ = await self._make_request(current_url, params)

        # Extract items from response
        page_items = response.get('values', [])
        all_items.extend(page_items)

        # Get next page URL from response
        current_url = response.get('next')

        # Clear params for subsequent requests as they're included in the next URL
        params = {}

    return all_items[:max_items]
```

`get_paginated_repos` (single-page) handles the per-page cursor synthesis differently — it reads `response.get('next', '')` from the **response body**, regex-extracts the `page=N` query param, and synthesizes a fake `Link: <url>; rel="next"` header so the frontend can reuse its GitHub-style parser:

```python
next_link = response.get('next', '')
formatted_link_header = ''
if next_link:
    page_match = re.search(r'[?&]page=(\d+)', next_link)
    if page_match:
        next_page = page_match.group(1)
        formatted_link_header = (
            f'<{workspace_repos_url}?page={next_page}>; rel="next"'
        )
    else:
        formatted_link_header = f'<{next_link}>; rel="next"'
```

### 3.2 Cursor mechanism

**Cursor lives in the response body, not headers.** The Bitbucket Cloud REST v2 paginator returns `{"values": [...], "next": "https://api.bitbucket.org/2.0/repositories/{ws}?page=2", "page": 1, "pagelen": 30}`. The `next` field is a *full URL* including query parameters; the next call is made by passing that URL directly to `_make_request` and **dropping the original `params`** (the URL already encodes them). Termination is "absent or empty `next` field" — single condition, no Link-header-style check.

### 3.3 Quirks

- **Page-size param is `pagelen`, not `per_page`.** Default 30, max 100. Different name from GitHub/GitLab/Forgejo.
- **`page` and `pagelen` are passed as ints, not stringified.** Inconsistent with GitLab which stringifies (`'page': str(page)`). Bitbucket's `httpx` query-string serialization handles both, but the inconsistency would bite a strict-types port.
- **Sort uses a leading-`-` for descending** (`'-updated_on'` for desc). GitHub uses `direction=desc`; GitLab uses `sort=desc`; Bitbucket uses prefix-sigil. Three providers, three conventions for sort direction.
- **No native sort field for `pushed`** — Bitbucket only has `updated_on` and `created_on`. The source maps GitHub's `pushed` → `-updated_on`.
- **Workspace-prefixed URLs.** Repos endpoint is `/repositories/{workspace_slug}`, not `/user/repos`. Bitbucket has no "list all repos for the user" endpoint; you must enumerate workspaces (via `/workspaces`) and fan out. `get_all_repositories` does this fanout; `get_paginated_repos` requires `installation_id` (the workspace slug) be passed in or returns `[]`.
- **The synthesized `formatted_link_header`** is purely for UI consumption — it lets the OpenHands frontend reuse one cursor-extraction code path. **`agent-runner` does not have a frontend that consumes Link headers; we can drop this synthesis entirely** and just expose the raw `next` URL in `Repository.next_page_url` or similar.

### 3.4 Borrow / skip verdict

**Borrow** the body-cursor pattern (`current_url = response.get('next')`; clear `params` on next call) — this is the cleanest of all four loops because the server tells you the literal next URL and you don't have to think about page math. **Skip** the synthesized-Link-header gymnastics — that's frontend-shim debt, not paginator logic.

## 4. Azure DevOps (`openhands/app_server/integrations/azure_devops/service/repos.py`)

### 4.1 Signatures

Azure DevOps is the **most divergent of the four.** There is **no pagination loop at all.** `get_paginated_repos` slices a fully-materialized list:

```python
async def get_paginated_repos(
    self,
    page: int,
    per_page: int,
    sort: str,
    installation_id: str | None,
    query: str | None = None,
) -> list[Repository]:
    """Get a page of repositories for the authenticated user."""
    # Get all repos first, then paginate manually
    # Azure DevOps doesn't have native pagination for repositories
    all_repos = await self.get_repositories(sort, AppMode.SAAS)

    # Calculate pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page

    # Filter by query if provided
    if query:
        query_lower = query.lower()
        all_repos = [
            repo for repo in all_repos if query_lower in repo.full_name.lower()
        ]

    return all_repos[start_idx:end_idx]
```

`get_repositories` itself is a two-step fanout: list all `/_apis/projects?api-version=7.1` (returns `{"value": [...]}`), then for each project list `/{project}/_apis/git/repositories?api-version=7.1`. Hard cap `MAX_REPOS = 1000`. Both calls return everything in one response — no continuation token consulted in `repos.py`.

### 4.2 Cursor mechanism

**There is no cursor.** The repositories endpoints in Azure DevOps Git REST `api-version=7.1` return the full unpaged result set. Pagination, when it exists in Azure DevOps elsewhere, uses a `x-ms-continuationtoken` response header + matching `continuationToken` request param (this *is* documented for the work-items and TFVC APIs but is unused in the repos endpoint here). The mixin's response-shape envelope is `{"value": [...], "count": N}` — same as the rest of the Azure DevOps REST surface — but no `nextLink` is consulted. **Termination = "the API returned everything in one shot, count it client-side."**

### 4.3 Quirks

- **API version is a query param, not a header**: `?api-version=7.1`. Forgetting it returns HTML.
- **Org-and-project hierarchy**: full_name format is `{org}/{project}/{repo}` — three-level, unlike GitHub/GitLab/Bitbucket's two-level `{owner}/{repo}` or `{group}/{repo}`. Caller code that splits on `/` will break.
- **Path components are URL-encoded** via `self._encode_url_component(...)` — Azure project names commonly contain spaces.
- **`is_public=False` hardcoded** for every repo. There is no `is_private` field on the Azure response; the convention is "Azure DevOps repos are private by default."
- **Manual sort happens client-side** (`all_repos.sort(key=lambda r: r.get('updated_date', ''), reverse=True)`) because the API returns unsorted.
- **`get_paginated_repos` re-fetches the entire repo list on every call** — there is no caching. For a 1000-repo organization, paging through to page 10 (per_page=30) requires 10 full list-fetches. Performance bug worth noting on borrow; if ever ported, cache `get_repositories` for the lifetime of the request.

### 4.4 Borrow / skip verdict

**Skip the implementation entirely.** The "pagination" here is client-side list-slicing, not real pagination. **Borrow only the lesson**: any `_paginate(url, max)` Protocol must allow a subclass to short-circuit and return the full list on the first call, then have the base class handle slicing for callers that want a `(page, per_page)` view. This is a shape concern: the Protocol cannot be "yield pages until exhausted" — it must be "return up to `max` items, however many round-trips that takes (possibly zero)." Azure DevOps would implement the Protocol with one round-trip and a slice; everyone else with N round-trips.

## 5. Forgejo (`openhands/app_server/integrations/forgejo/service/repos.py`) — supplementary

Included because report 04 named Forgejo as the sixth provider and the file is small (~110 lines).

### 5.1 Signature and mechanism

Pagination shape from `get_all_repositories` (verbatim):

```python
while len(collected) < max_repos:
    params = {
        'page': str(page),
        'limit': str(per_page),
        'sort': forgejo_sort,
    }
    response, headers = await self._make_request(url, params)
    last_link_header = headers.get('Link')

    page_repos = response if isinstance(response, list) else []
    if not page_repos:
        break

    collected.extend(page_repos)
    if 'rel="next"' not in (last_link_header or ''):
        break

    page += 1
```

**Forgejo is GitHub-shaped** (`Link: rel="next"` + client-side `page` counter, dual termination, top-level array response) **except the page-size param is `limit` not `per_page`.** Forgejo is a Gitea fork; Gitea inherited GitHub's `Link` header convention. This is the easiest non-GitHub provider to add.

### 5.2 Borrow / skip verdict

**Borrow the GitHub helper unchanged**, just rename `per_page` → `limit` in the params dict via a per-provider override. Of the four non-GitHub providers, Forgejo is the one where the `_paginate` Protocol's *default implementation* (GitHub-flavoured) works essentially as-is.

## 6. Comparison table

| Provider | Cursor source | Cursor name | Stop condition | Quirks |
|---|---|---|---|---|
| **GitHub** (baseline) | Response header `Link` with `rel="next"` | `page` (client-side counter) + `per_page` | empty page **OR** no `rel="next"` | Optional `extract_key` for installation-wrapped responses (`{"repositories": [...]}`); response body is the array itself for `/user/repos`. |
| **GitLab** | Response header `Link` with `rel="next"` | `page` (client-side counter) + `per_page` | empty page **OR** no `rel="next"` | `sort` means direction, `order_by` means field — inverse of GitHub. `'membership': 1` (literal int, not `True`). Repo path encoded with `%2F`. Per-page max 100. |
| **Bitbucket Cloud** | Response **body** field `next` (a full URL) | `page` + `pagelen` (NOT `per_page`); on page 2+, the cursor URL embeds the params and request `params` are cleared | absent/empty `next` field (single condition) | `-`-prefix sort sigil for desc (`-updated_on`). Workspace-prefixed URLs (`/repositories/{workspace_slug}`); no global "list my repos" endpoint. Synthesizes a fake `Link: rel="next"` header for UI reuse — drop on borrow. |
| **Azure DevOps** | None | None — full list returned in one response | client-side list exhaustion | `api-version=7.1` query param required. Three-level `{org}/{project}/{repo}` full_name. `is_public=False` hardcoded. `get_paginated_repos` re-fetches and slices on every call (perf trap). Continuation tokens *exist* in the broader Azure DevOps API but are unused in the repos endpoint. |
| **Forgejo** | Response header `Link` with `rel="next"` | `page` + `limit` (NOT `per_page`) | empty page **OR** no `rel="next"` | Gitea-fork; identical convention to GitHub except page-size param name. Top-level array response. |
| **Bitbucket Data Center** | Unknown — no `repos.py` mixin found at expected path | n/a | n/a | `bitbucket_data_center/bitbucket_dc_service.py` is a single-file stub (no `service/` subdirectory). No `_fetch_paginated_*` or `get_paginated_repos` definition on this branch. The `bitbucket_dc/service/repos.py` path returned 404. Documented in sources table. Atlassian's published BDC REST docs use `start` + `limit` + `isLastPage` body fields — distinct from BB Cloud's `next`-URL convention — but this is *not* sourced from the upstream code in this report. |

**Headline divergence:** Bitbucket Cloud puts the cursor in the **body** (a full URL), while GitHub / GitLab / Forgejo put it in the **`Link` header**, and Azure DevOps **has no cursor at all** and forces client-side slicing. Three different cursor *locations* across four providers — the Protocol must accommodate all three.

## 7. Recommended `_paginate` Protocol

### 7.1 The signature

```python
from typing import Protocol, Any, AsyncIterator

class ProviderClient(Protocol):
    """Stage-4 git-provider abstraction (read+write; see report 04 §7.1)."""

    async def _paginate(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        max_items: int = 1000,
        *,
        extract_key: str | None = None,
    ) -> list[dict]:
        """Fetch up to `max_items` items from a paginated endpoint.

        The default implementation walks GitHub-style `Link: rel="next"` headers.
        Subclasses override when the provider uses a different cursor convention.

        Args:
            url: Initial endpoint URL. May be replaced by the server-supplied
                next-page URL on subsequent round-trips.
            params: Initial query parameters. Behavior on subsequent pages is
                provider-specific:
                - GitHub/GitLab/Forgejo: the loop sets `params['page']` (or
                  equivalent) on each iteration and re-sends `params`.
                - Bitbucket Cloud: `params` is cleared after the first call
                  because the next URL embeds them.
                - Azure DevOps: `params` is sent once; no second call.
            max_items: Hard cap on the returned list length. Defaults to 1000
                (matches OpenHands' `MAX_REPOS` ceiling).
            extract_key: If set, dig into `response[extract_key]` to find the
                items array. Required for GitHub Apps installations
                (`{"repositories": [...]}`). Ignored when the response body is
                already an array.

        Returns:
            A list of raw API dicts, length <= max_items. Caller is responsible
            for parsing each dict into a typed value object.
        """
        ...
```

### 7.2 Defaults vs overrides

The *base* `ProviderClient` provides a default `_paginate` matching GitHub / GitLab / Forgejo (it covers 3 of 5 real implementations):

```python
async def _paginate(self, url, params=None, max_items=1000, *, extract_key=None):
    items: list[dict] = []
    params = dict(params or {})
    page = 1
    page_size_param = self.PAGE_SIZE_PARAM  # class attr: 'per_page' | 'limit' | 'pagelen'
    page_param = self.PAGE_PARAM            # class attr: 'page'

    while len(items) < max_items:
        params[page_param] = str(page)
        response, headers = await self._make_request(url, params)

        page_items = (
            response.get(extract_key, []) if extract_key
            else response if isinstance(response, list)
            else response.get('values', [])  # falls through to Bitbucket-shape
        )
        if not page_items:
            break
        items.extend(page_items)

        link_header = headers.get('Link', '')
        if 'rel="next"' not in link_header:
            break
        page += 1

    return items[:max_items]
```

Per-provider override needs:

| Provider | Override needed? | Reason |
|---|---|---|
| GitHub | No | Class attrs `PAGE_PARAM='page'`, `PAGE_SIZE_PARAM='per_page'`. Default works. |
| GitLab | No | Class attrs `PAGE_PARAM='page'`, `PAGE_SIZE_PARAM='per_page'`. Default works (param-construction quirks like `'membership': 1` live in callers, not `_paginate`). |
| Forgejo | No | Class attrs `PAGE_PARAM='page'`, `PAGE_SIZE_PARAM='limit'`. Default works. |
| Bitbucket Cloud | **Yes** | Cursor is body-field `next`, not Link header. Override walks `current_url = response.get('next'); params = {}` until empty. |
| Azure DevOps | **Yes** | No cursor. Override does one round-trip, returns `response['value'][:max_items]`. |
| Bitbucket DC | **Yes (likely)** | If/when implemented: per Atlassian docs, BDC uses `start` + `limit` + body fields `isLastPage` + `nextPageStart`. Override walks them. (Speculative — not sourced from upstream code.) |

### 7.3 Sync vs async, return type, kwargs — design choices

- **`async`.** Matches OpenHands; matches `agent-runner`'s likely httpx adoption; matches the natural concurrency of "post comment + add label + update PR" fanouts in `notify.py`. Sync would force every call site through `asyncio.run()` or block.
- **Return `list[dict]`, not `AsyncIterator[dict]`.** Iterators are theoretically nicer (lazy, no `max_items` cap needed) but they (a) make `try/except` per-page error handling awkward, (b) prevent the trim-after-overshoot pattern that all four implementations use, and (c) don't compose with `await asyncio.gather(...)` for parallel-page fetches (a future optimization). `list[dict]` matches every existing OpenHands implementation and matches GitHub/GitLab REST's "return everything up to N" usage pattern.
- **`max_items` keyword default `1000`.** Matches OpenHands' shared `MAX_REPOS = 1000` ceiling. Callers that want a single page should call the provider's own `get_paginated_repos(page, per_page)` instead of `_paginate`.
- **Class attributes for param names** (`PAGE_PARAM`, `PAGE_SIZE_PARAM`) instead of constructor kwargs. Per-instance config is wrong: every GitHub instance pages by `?page=`. Subclass-level constants match how OpenHands declares `BASE_URL`, `GRAPHQL_URL`, etc.
- **`extract_key` retained**, even though only GitHub uses it. It's free in the default implementation and removing it would force every Bitbucket-shape provider to subclass just to dig out `'values'`. Cheaper to leave as a kwarg and let subclasses pass it.
- **`_paginate` is a private helper, not part of the public Protocol surface.** The public surface is `get_paginated_repos(page, per_page, ...)` — `_paginate` is an implementation aid that subclasses inherit and may override. Marking it private with underscore prefix matches OpenHands' naming and keeps the public Protocol focused on caller-relevant operations (`get_repository`, `post_comment`, etc., per report 04 §7.1).

### 7.4 What this Protocol does *not* try to solve

- **Parallel-page fetching.** A natural future optimization: once the first response tells you total count, fan out N-1 page requests in parallel. Not in v1 — adds a `total_count` requirement that not every provider exposes (Bitbucket Cloud has it as `size`; GitHub doesn't expose it cheaply).
- **Resumable pagination.** Persisting a cursor across process restarts is out of scope; `agent-runner`'s pagination calls are bounded inside a single Run, so a crash retries from page 1.
- **Rate-limit-aware backoff.** Belongs in `_make_request`, not `_paginate`. OpenHands' base `_make_request` raises `RateLimitError` on 429; the paginator just propagates.
- **Streaming consumers.** No `AsyncIterator` return — see §7.3.

## 8. Implementation order — least to most surprising

When `agent-runner` Stage 4 lands a second provider, the order to add them is **least surprising first**, so each new provider exercises one new `_paginate` capability at a time:

1. **Forgejo** — least surprise. The default `_paginate` works with `PAGE_SIZE_PARAM = 'limit'` and one line changed in the params dict. The git-clone URL convention is identical to GitHub (`https://{token}@codeberg.org/{owner}/{repo}.git`, per report 05 §4.2). One subclass, ~50 lines of code, no `_paginate` override. **First non-GitHub provider to ship validates the Protocol's defaults.**
2. **GitLab** — same `_paginate` defaults work; the surprises are *outside* pagination (`%2F` repo encoding; `order_by` vs `sort`; `'membership': 1`). All those live in `get_paginated_repos` parameter construction, not in the shared helper. The GitLab git-URL convention (`https://oauth2:{token}@gitlab.com/...`, per report 05 §4.2) requires a one-line per-provider URL template. **Second provider validates that param-quirks don't leak into `_paginate`.**
3. **Bitbucket Cloud** — first `_paginate` override required, validating that the Protocol's signature accommodates body-cursor providers without the base class having to know about them. Workspace fanout (`get_installations` returning workspace slugs) is a separate concern from `_paginate` itself. Git URL has the `x-token-auth:` username convention (report 05 §4.2). **First override validates the Protocol shape.**
4. **Azure DevOps** — `_paginate` override is "fetch once, slice client-side." Validates the Protocol's allowance for zero-round-trip "pagination." The Azure-specific URL convention (`https://{org}:{PAT}@dev.azure.com/{org}/{project}/_git/{repo}`, with three URL-encoded path components, per report 05 §4.2 / provider.py L347) is the *real* surprise — pagination is the easy part for Azure. **Second override stresses the Protocol's flexibility.**
5. **Bitbucket Data Center** — speculative until upstream actually has a `repos.py` mixin (the path returned 404 on this run; see §6 row and sources table). Per Atlassian's BDC REST docs (NOT sourced from this report's upstream reads), pagination uses `start` + `limit` request params + `isLastPage` + `nextPageStart` response body fields — a *third* cursor convention beyond Link-header and body-URL. URL convention has the `scm/{project.lower()}/{repo}.git` path prefix and URL-encoded credentials (report 05 §4.2). **Save for last; verify upstream shape before designing the override.**

The recommendation: **ship Forgejo first to prove the default works**, then GitLab (still uses the default), then accept the first override (Bitbucket Cloud), then Azure. By the time agent-runner needs BDC, the Protocol has been stress-tested by three real overrides and the spec for BDC's override can be written confidently.

---

## Sources reviewed

| Source URL | Status | Notes |
|---|---|---|
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/gitlab/service/repos.py` | ✅ Full review | 195 lines (~6.6 KB). All five methods read end-to-end (`_parse_repository`, `_parse_gitlab_url`, `search_repositories`, `get_paginated_repos`, `get_all_repositories`, `get_user_groups`, `get_repository_details_from_repo_name`). Pagination quoted verbatim in §2.1. No private `_fetch_paginated_repos` helper — pagination is inlined. |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/bitbucket/service/repos.py` | ✅ Full review | 263 lines (~9.9 KB). All four methods read end-to-end (`search_repositories`, `_get_user_workspaces`, `get_installations`, `get_paginated_repos`, `get_all_repositories`, `get_suggested_tasks`). The synthesized-`Link`-header gymnastics quoted verbatim in §3.1. |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/bitbucket/service/base.py` | 🟡 Targeted (one helper) | Only `_fetch_paginated_data` was extracted — the body-cursor pagination helper that `get_all_repositories` calls. Quoted verbatim in §3.1. Rest of file (auth headers, `_make_request`, etc.) not in scope for this report. |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/azure_devops/service/repos.py` | ✅ Full review | 181 lines (~6.5 KB). All five methods read end-to-end (`search_repositories`, `get_repositories`, `get_all_repositories`, `_parse_repository_response`, `get_paginated_repos`, `get_repository_details_from_repo_name`). The `# Azure DevOps doesn't have native pagination for repositories` comment in `get_paginated_repos` quoted verbatim in §4.1. |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/forgejo/service/repos.py` | ✅ Full review (supplementary) | 110 lines (~3.5 KB). All four methods read (`search_repositories`, `get_all_repositories`, `get_paginated_repos`, `get_repository_details_from_repo_name`). Pagination loop quoted verbatim in §5.1. Confirmed Forgejo is GitHub-shaped except for `limit` vs `per_page` page-size param name. |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/bitbucket_dc/service/repos.py` | ❌ 404 | Path probed at task instruction. Returned HTTP 404 / 14-byte body. The `bitbucket_dc/` directory does not exist on this branch — the actual Bitbucket Data Center service lives at `openhands/app_server/integrations/bitbucket_data_center/bitbucket_dc_service.py` (single-file, no `service/` subdirectory). |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/bitbucket_data_center/bitbucket_dc_service.py` | 🟡 Targeted (grep only) | Confirmed via grep (`async def`, `paginated`, `next`, `start`, `limit`, `isLastPage`) that this file contains no pagination logic — the matches were `__init__`, `__getattr__`, `__call__`, and a `'x-token-auth:'` token-prefix check. BDC has no `get_paginated_repos` or `_fetch_paginated_*` on this branch. Documented in §6 comparison-table row. |
| Report 05 (`research/05-openhands-github-mixins-jira.md`) §2.1 | ✅ Recap reference | The GitHub baseline `_fetch_paginated_repos` quoted in §1 of this report is an abbreviated recap of the verbatim quote in report 05 §2.1. No new GitHub source was fetched — the prior report's read is authoritative. |
| Report 04 (`research/04-openhands-sdk-git-provider.md`) §3, §7.1 | ✅ Recap reference | Read for the existing `GitService` Protocol shape and the `agent-runner` Stage-4 `ProviderClient` proposal that this report's `_paginate` design extends. No new fetch needed; informed §7 entirely. |
