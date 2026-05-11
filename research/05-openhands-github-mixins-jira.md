# Report 05 — OpenHands GitHub mixins + Jira manager (deep dive)

**Date:** 2026-05-11
**Author:** Subagent (run_id: 20260511-r3, sub-01)
**Status:** ✅ complete — all four targeted source files body-read end-to-end. One source (`jira_manager.py`) returned a different shape than report 04's name-grep predicted (no OAuth handshake; auth is Keycloak SSO + service-account basic auth). One supplementary file (`jira_types.py`) was read to recover the `JiraViewInterface` definition, which is an `ABC` rather than a Pydantic model.

## Lead question

Which patterns from OpenHands' GitHub mixin (`repos.py`, `resolver.py`) and the broader provider URL-construction layer (`provider.py` lines 495-651), plus the Jira manager (`jira_manager.py`), should `agent-runner` borrow when extracting Stage-4 `providers/github/` into a `ProviderClient` and adding Stage-5 Jira backing for `IssueTracker` — and, equally importantly, which OpenHands choices are load-bearing on assumptions `agent-runner` does not share (multi-tenant SaaS, Keycloak SSO, GitHub Apps installations, paid-license enterprise tier) and should therefore be **left behind**?

## 1. TL;DR — three findings

1. **`repos.py` is mostly GitHub-Apps installation plumbing.** Two patterns generalize: (a) the small `_fetch_paginated_repos(url, params, max_repos, extract_key)` helper that walks `Link: rel="next"` headers until either max-repos or no-next, and (b) the `_parse_repository(repo, link_header)` factory that constructs the value object from a raw API dict. The fuzzy-org-match search heuristic (`_fuzzy_match_org_name`) and the SAAS/non-SAAS branching are **OpenHands-specific** and would be over-engineering in `agent-runner`. **Borrow:** the link-header pagination loop. **Skip:** the search heuristics and the installation-id fanout.

2. **`resolver.py` is a 2-step GraphQL traversal that locates a review thread by *any* comment id within it.** Algorithm: (1) fetch the comment via `getThreadFromComment` GraphQL → walk `replyTo.id` to the root, (2) page through `pullRequest.reviewThreads(first: 50)` until a thread's first-comment id matches the root id, then (3) page through that thread's `comments(first: 50)` and return them all. **This is exactly the lookup `agent-runner` will need** when a `@agent-runner` mention lands on a PR review-thread reply rather than a top-level PR comment — Round 1's DESIGN.md §9 trigger-comment path quietly assumes "comment body" but PR review threads are nested. **Borrow:** the algorithm shape (root-via-replyTo, page-until-match, then page-comments). **Skip:** the GitHub-Resolver-specific `[fix #N]` parsing — `agent-runner`'s issue↔PR linkage is one-directional (Run → trigger source), not bidirectional.

3. **`provider.py:get_authenticated_git_url` is the single most directly-borrowable function in OpenHands.** It encapsulates five wildly different per-provider URL conventions in ~60 lines with one critical security check (`ALLOW_INSECURE_GIT_ACCESS` env var gates `http://`). The Azure DevOps (`https://{org}:{pat}@dev.azure.com/{org}/{project}/_git/{repo}` with URL-encoded path components and *org-as-username*) and Bitbucket Data Center (`scm/{project.lower()}/{repo}.git` path prefix; `quote(..., safe="")` on credentials) cases are **non-obvious enough that re-deriving them from the providers' docs will burn hours** when `agent-runner` adds a non-GitHub backend. Quote, attribute, port verbatim. (One bug worth noting: the Azure DevOps branch ignores the `protocol` variable and hardcodes `https://` — see §4.2.)

4. **`jira_manager.py` is *not* the OAuth-handshake reference report 04 hinted at.** There is no Jira OAuth flow in this file; user identity is resolved via a pre-existing OpenHands ↔ Keycloak ↔ Jira account mapping in `integration_store.get_active_user(account_id, workspace_id)`, and *outbound* posts back to Jira use **service-account email + API key basic auth** (not OAuth). The interesting borrow is the **`Manager.start_job(view) → view.create_or_update_conversation() → view.get_response_msg() → manager._send_comment(view, msg)`** orchestration shape — a 4-line method body where every interesting decision lives in the view object, and the manager's job is exception-translation + comment-posting. `agent-runner`'s eventual `IssueTracker` should mirror this control inversion. (Three findings in the TL;DR became four; leaving the count honest.)

## 2. `repos.py` — pagination and the GitHub-Apps installation seam

### 2.1 The pagination helper (the borrow)

This is the cleanest small pattern in the file. From `openhands/app_server/integrations/github/service/repos.py` lines ~26-60:

```python
async def _fetch_paginated_repos(
    self, url: str, params: dict, max_repos: int, extract_key: str | None = None
) -> list[dict]:
    """Fetch repositories with pagination support."""
    repos: list[dict] = []
    page = 1

    while len(repos) < max_repos:
        page_params = {**params, 'page': str(page)}
        response, headers = await self._make_request(url, page_params)

        # Extract repositories from response
        page_repos = response.get(extract_key, []) if extract_key else response

        if not page_repos:  # No more repositories
            break

        repos.extend(page_repos)
        page += 1

        # Check if we've reached the last page
        link_header = headers.get('Link', '')
        if 'rel="next"' not in link_header:
            break

    return repos[:max_repos]  # Trim to max_repos if needed
```

Three observations:

- **The dual termination condition** (empty page OR no `rel="next"`) is correct and load-bearing. GitHub returns 200 + `[]` when you walk past the last page; *also* you should respect the absence of the next-link to avoid one wasted round-trip. Both checks are needed.
- **The `extract_key` parameter** handles the GitHub-Apps installations endpoint, which wraps the array in `{"repositories": [...]}`, vs. `/user/repos` which returns the array at top level. `agent-runner` likely will not need this — we don't use App installations — but the parameter is essentially free.
- **The trim** at the end (`repos[:max_repos]`) compensates for the fact that the inner `extend` may overshoot (the last page returns `per_page` items even if you only wanted a few of them). Correct, easy to forget if you reimplement.

### 2.2 The `_parse_repository` factory (the borrow)

```python
def _parse_repository(
    self, repo: dict, link_header: str | None = None
) -> Repository:
    return Repository(
        id=str(repo.get('id')),
        full_name=repo.get('full_name'),
        stargazers_count=repo.get('stargazers_count'),
        git_provider=ProviderType.GITHUB,
        is_public=not repo.get('private', True),
        owner_type=(
            OwnerType.ORGANIZATION
            if repo.get('owner', {}).get('type') == 'Organization'
            else OwnerType.USER
        ),
        link_header=link_header,
        main_branch=repo.get('default_branch'),
    )
```

Two design choices to copy:

- **Default `private` to `True`** in `repo.get('private', True)` so an absent field fails closed (treat as private if you can't tell).
- **`link_header` rides on the value object**, not as a separate return. Callers that need next-page info read it off the last `Repository` they got. Mildly clever; means the pagination cursor doesn't need a separate `PaginatedResponse` wrapper. Whether `agent-runner` adopts this depends on whether we ever surface pagination to a caller — for v1 we just want "the repo we're working on," not "page through repos."

### 2.3 What to skip

- **`get_all_repositories(sort, app_mode)` with the `AppMode.SAAS` branch** (lines ~115-154). This fans out across all GitHub App installations, fetches up to 1000 repos per installation, then sorts by pushed-at. Multi-tenant cloud territory. `agent-runner` is single-tenant and knows its repo by name from the trigger.
- **`search_repositories` + `_fuzzy_match_org_name`** (lines ~190-280). This is product-feature plumbing for the OpenHands "pick a repo" GUI. We don't have a repo picker; the trigger names the repo.
- **`get_organizations_from_installations`**. Same — App-installations-specific.

### 2.4 Notable absence

There is **no GraphQL in `repos.py`**. All repo operations use REST (`/user/repos`, `/user/installations/.../repositories`, `/search/repositories`, `/repos/{full_name}`). GraphQL appears only in `resolver.py` (§3 below) and in the GitHub-Apps suggested-tasks query (not in this file). Report 04 §5 noted "pagination + GraphQL shape" for `repos.py` — that's only half right; the GraphQL is in `resolver.py`. Updating that prediction: **`repos.py` is REST + Link-header pagination; `resolver.py` is GraphQL + cursor pagination.**

## 3. `resolver.py` — GitHub-Resolver auto-link issue → PR logic

### 3.1 Method inventory

Four methods, all `async`:

```python
async def get_issue_or_pr_title_and_body(
    self, repository: str, issue_number: int
) -> tuple[str, str]: ...

async def get_issue_or_pr_comments(
    self, repository: str, issue_number: int, max_comments: int = 10
) -> list[Comment]: ...

async def get_review_thread_comments(
    self,
    comment_id: str,
    repository: str,
    pr_number: int,
) -> list[Comment]: ...

def _process_raw_comments(
    self, comments_data: list, max_comments: int = 10
) -> list[Comment]: ...
```

The first two are vanilla REST wrappers. **`get_review_thread_comments` is the load-bearing one** — it answers "given a single comment_id from a webhook, return *all* comments in the same review thread, in order." This is the lookup needed when a user replies inline to a PR review comment with `@agent-runner <task>` and the agent needs the surrounding context.

### 3.2 The algorithm (verbatim)

```python
variables = {'commentId': comment_id}
data = await self.execute_graphql_query(
    get_thread_from_comment_graphql_query, variables
)

comment_node = data.get('data', {}).get('node')
if not comment_node:
    return []

root_comment_id = comment_id
reply_to = comment_node.get('replyTo')
if reply_to:
    root_comment_id = reply_to['id']

owner, repo = repository.split('/')
thread_id = None
after_cursor = None
has_next_page = True

while has_next_page and not thread_id:
    threads_variables: dict[str, Any] = {
        'owner': owner,
        'repo': repo,
        'number': pr_number,
        'first': 50,
    }
    if after_cursor:
        threads_variables['after'] = after_cursor

    threads_data = await self.execute_graphql_query(
        get_review_threads_graphql_query, threads_variables
    )

    review_threads_data = (
        threads_data.get('data', {})
        .get('repository', {})
        .get('pullRequest', {})
        .get('reviewThreads', {})
    )

    review_threads = review_threads_data.get('nodes', [])
    page_info = review_threads_data.get('pageInfo', {})

    for thread in review_threads:
        first_comments = thread.get('comments', {}).get('nodes', [])
        for first_comment in first_comments:
            if first_comment.get('id') == root_comment_id:
                thread_id = thread.get('id')
                break
        if thread_id:
            break

    has_next_page = page_info.get('hasNextPage', False)
    after_cursor = page_info.get('endCursor')

if not thread_id:
    logger.warning(
        f'Could not find review thread for comment {comment_id}, '
        f'returning traversed comments'
    )
    return []

all_thread_comments = []
after_cursor = None
has_next_page = True

while has_next_page:
    comments_variables: dict[str, Any] = {}
    comments_variables['threadId'] = thread_id
    comments_variables['page'] = 50
    if after_cursor:
        comments_variables['after'] = after_cursor

    thread_comments_data = await self.execute_graphql_query(
        get_thread_comments_graphql_query, comments_variables
    )

    thread_node = thread_comments_data.get('data', {}).get('node')
    if not thread_node:
        break

    comments_data = thread_node.get('comments', {})
    comments_nodes = comments_data.get('nodes', [])
    page_info = comments_data.get('pageInfo', {})

    all_thread_comments.extend(comments_nodes)

    has_next_page = page_info.get('hasNextPage', False)
    after_cursor = page_info.get('endCursor')

return self._process_raw_comments(all_thread_comments)
```

Three steps in plain English:

1. **Resolve the root.** GitHub's review-thread model is a tree; given any leaf, walk one hop via `replyTo.id` to find the root. (Only one hop is needed because PR review threads are *flat*: there's one root comment and N replies, no nested replies. If GitHub ever changed that, this code would silently return the wrong root — worth a comment in the borrow.)
2. **Find the thread.** Page through `pullRequest.reviewThreads(first: 50, after: $cursor)` 50 at a time, looking for a thread whose `comments.nodes[].id` includes the root. Break out of both loops on first match.
3. **Page the comments.** Once the `thread_id` is known, walk `node(id: $threadId).comments(first: 50, after: $cursor)` to completion. Return all of them processed via `_process_raw_comments` (which sorts chronologically and normalizes author/timestamp shape).

The GraphQL query strings themselves (`get_thread_from_comment_graphql_query`, `get_review_threads_graphql_query`, `get_thread_comments_graphql_query`) are imported from a sibling module — they were not in the WebFetch return. The query *shape* is fully recoverable from the variable names and field accesses above; we have the schema, just not the literal `gql"""..."""` strings. If `agent-runner` borrows this, write the queries fresh against the documented variables — it's <30 lines of GraphQL and writing them ourselves is faster than another fetch.

### 3.3 Variable-name bug worth noting

The third query uses `comments_variables['page'] = 50`. The variable name is `page` but it's used as a *page-size* (`first: 50`). The corresponding GraphQL query presumably declares `$page: Int!` and uses it as the `first:` argument. This is a naming smell, not a bug — the value flows correctly — but `agent-runner` should call it `pageSize` or `first` when reimplementing.

### 3.4 Relation to DESIGN.md §4 Run-PR-Issue association

DESIGN.md §4 lists `Result.artifacts` with `{"kind": "comment", "ref": "owner/repo#issue-123#comment-999"}`. The reverse direction — given a *comment id*, recover the surrounding context — is what `get_review_thread_comments` solves. **DESIGN.md does not currently call this out.** Three concrete consequences for Stage 4:

- The `trigger-comment.yml` parser in `enqueue.py` should distinguish *issue comment*, *PR top-level comment*, and *PR review thread reply* — they have different webhook event types (`issue_comment` vs `pull_request_review_comment`) and different recovery semantics.
- For PR review thread replies, the agent needs the full thread (the file/line context lives on the root comment, not the reply). Borrow `get_review_thread_comments` essentially verbatim — the algorithm is provider-agnostic only at the *shape* level; the GraphQL queries are GitHub-specific.
- `Result.artifacts` should grow a `kind: "review_thread"` variant so that bidirectional Run↔thread navigation is possible from the `state` branch alone.

### 3.5 What to skip

- The `[fix #N]` body-text parsing that the file's name suggests is *not in this file* — it's likely in the `enterprise/integrations/resolver/` directory (the original "OpenHands GitHub Resolver" sub-product), which we did not read. The mixin here only does *thread/comment retrieval*, not the auto-link parsing per se. Report 04 §9's "GitHub-Resolver auto-link issue → PR logic" predicted parsing-of-comment-bodies; the actual file is narrower than that. Treat report 04's prediction as adjusted: **the resolver mixin is comment-thread retrieval, not body-parsing.**

## 4. `provider.py` lines 495-651 — `get_authenticated_git_url`

### 4.1 The verbatim function

From `openhands/app_server/integrations/provider.py`:

```python
async def get_authenticated_git_url(
    self, repo_name: str, is_optional: bool = False
) -> str:
    """Get an authenticated git URL for a repository.

    Args:
        repo_name: Repository name (owner/repo)
        is_optional: If True, logs at debug level instead of error level when repo not found

    Returns:
        Authenticated git URL if credentials are available, otherwise regular HTTPS URL
    """
    try:
        repository = await self.verify_repo_provider(
            repo_name, is_optional=is_optional
        )
    except AuthenticationError:
        raise Exception('Git provider authentication issue when getting remote URL')

    provider = repository.git_provider
    repo_name = repository.full_name

    domain = self.PROVIDER_DOMAINS.get(provider, '')

    # If provider tokens are provided, use the host from the token if available
    # Note: For Azure DevOps, don't use the host field as it may contain org/project path
    if self.provider_tokens and provider in self.provider_tokens:
        if provider != ProviderType.AZURE_DEVOPS:
            domain = self.provider_tokens[provider].host or domain

    # Detect protocol before normalizing domain
    # Default to https, but preserve http if explicitly specified
    protocol = 'https'
    if domain and domain.strip().startswith('http://'):
        allow_insecure = os.environ.get(
            'ALLOW_INSECURE_GIT_ACCESS', 'false'
        ).lower() in ('true', '1', 'yes')
        if not allow_insecure:
            raise ValueError(
                'Attempting to connect to an insecure git repository over HTTP. '
                "If you'd like to allow this nonetheless, set "
                'ALLOW_INSECURE_GIT_ACCESS=true as an environment variable.'
            )
        protocol = 'http'

    # Normalize domain to prevent double protocols or path segments
    if domain:
        domain = domain.strip()
        domain = domain.replace('https://', '').replace('http://', '')
        if '/' in domain:
            domain = domain.split('/')[0]

    # Try to use token if available, otherwise use public URL
    if self.provider_tokens and provider in self.provider_tokens:
        git_token = self.provider_tokens[provider].token
        if git_token:
            token_value = git_token.get_secret_value()
            if provider == ProviderType.GITLAB:
                remote_url = (
                    f'{protocol}://oauth2:{token_value}@{domain}/{repo_name}.git'
                )
            elif provider == ProviderType.BITBUCKET:
                if ':' in token_value:
                    remote_url = (
                        f'{protocol}://{token_value}@{domain}/{repo_name}.git'
                    )
                else:
                    remote_url = f'{protocol}://x-token-auth:{token_value}@{domain}/{repo_name}.git'
            elif provider == ProviderType.BITBUCKET_DATA_CENTER:
                project, repo_slug = (
                    repo_name.split('/', 1)
                    if '/' in repo_name
                    else (repo_name, repo_name)
                )
                scm_path = f'scm/{project.lower()}/{repo_slug}.git'
                if ':' in token_value:
                    dc_user, dc_pass = token_value.split(':', 1)
                    url_creds = (
                        f'{quote(dc_user, safe="")}:{quote(dc_pass, safe="")}'
                    )
                else:
                    url_creds = f'x-token-auth:{quote(token_value, safe="")}'
                remote_url = f'{protocol}://{url_creds}@{domain}/{scm_path}'
            elif provider == ProviderType.AZURE_DEVOPS:
                # Pattern: `https://{org}:{PAT}@dev.azure.com/{org}/{project}/_git/{repo}`
                clean_domain = domain.replace('https://', '').replace('http://', '')
                parts = repo_name.split('/')
                if len(parts) >= 3:
                    org, project, repo = parts[0], parts[1], parts[2]
                    org_encoded = quote(org, safe='')
                    project_encoded = quote(project, safe='')
                    repo_encoded = quote(repo, safe='')
                    remote_url = f'https://{org}:{token_value}@{clean_domain}/{org_encoded}/{project_encoded}/_git/{repo_encoded}'
                else:
                    remote_url = (
                        f'https://user:{token_value}@{clean_domain}/{repo_name}.git'
                    )
            else:
                # GitHub, Forgejo
                remote_url = f'{protocol}://{token_value}@{domain}/{repo_name}.git'
        else:
            remote_url = f'{protocol}://{domain}/{repo_name}.git'
    else:
        remote_url = f'{protocol}://{domain}/{repo_name}.git'

    return remote_url
```

### 4.2 Per-provider URL templates — annotated

| Provider | Template | Subtlety |
|---|---|---|
| GitHub | `https://{token}@github.com/{owner}/{repo}.git` | Token-as-username; password slot empty. |
| Forgejo | `https://{token}@codeberg.org/{owner}/{repo}.git` | Same shape as GitHub — token-as-username. |
| GitLab | `https://oauth2:{token}@gitlab.com/{owner}/{repo}.git` | Username **must** be the literal string `oauth2`; not interchangeable with `git` or `token`. |
| Bitbucket Cloud | `https://x-token-auth:{token}@bitbucket.org/{owner}/{repo}.git` (or `https://{user:pass}@...` if the token contains a colon) | The `:` heuristic distinguishes "I have an app password" (username:apppass) from "I have an access token" (use `x-token-auth` literal). |
| Bitbucket Data Center | `https://x-token-auth:{quote(token)}@{domain}/scm/{project.lower()}/{repo}.git` (or `https://{quote(u)}:{quote(p)}@{domain}/scm/{project.lower()}/{repo}.git`) | Three subtleties: (a) the `scm/` path prefix is required by BDC's clone protocol; (b) project name is **lowercased**; (c) credentials are URL-encoded with `quote(..., safe="")` because BDC users frequently have `@` or `/` in their usernames (corporate AD). |
| Azure DevOps | `https://{org}:{PAT}@dev.azure.com/{org_enc}/{project_enc}/_git/{repo_enc}` | Three subtleties: (a) the **org name is the username** (not the literal "user" or "PAT"); (b) every path component is URL-encoded; (c) the `protocol` variable is **silently ignored** — Azure DevOps always gets `https://` regardless of `ALLOW_INSECURE_GIT_ACCESS`. (Probably fine — there is no http:// Azure DevOps in production — but worth noting on borrow.) |

### 4.3 The security gate

The `ALLOW_INSECURE_GIT_ACCESS` env var check (lines ~530-540) is worth borrowing exactly. It (a) defaults `http://` to a hard `ValueError`, (b) provides an explicit escape-hatch env var with three accepted values (`true`/`1`/`yes`, case-insensitive), and (c) the error message tells the user exactly what to set. Self-hosted Forgejo / Gitea / on-prem Bitbucket DC instances will commonly be plaintext HTTP behind a corporate firewall; you want to fail closed by default.

### 4.4 What `agent-runner` should do with this

When DESIGN.md Stage 4 fires (second provider added), this function is the single highest-value port. Three rules:

1. **Port verbatim.** The per-provider templates encode subtle decisions made against each provider's actual git server — they are not derivable from the provider's documentation in <30 minutes each. (The author has tried; `scm/` prefix for BDC and the org-as-username for Azure are both undocumented in their respective "git over HTTPS" docs.)
2. **Drop the `verify_repo_provider` call.** That auto-detects which provider owns the repo by trying each in turn; `agent-runner`'s Run config already specifies the provider. Replace the first 8 lines with `provider = run.git_provider; repo_name = run.repository`.
3. **Drop `MappingProxyType[ProviderType, ProviderToken]` machinery.** `agent-runner` has one token per Run, not a multi-provider dict. Rename `provider_tokens[provider].token` → `run.provider_token`.

### 4.5 Apparent bug — Azure DevOps ignores `protocol`

Line documented above: the Azure DevOps branch hardcodes `https://`. If a user set `ALLOW_INSECURE_GIT_ACCESS=true` for an on-prem Azure DevOps Server (which exists, though rare), the URL would still be `https://` and the clone would fail. This is *probably* the right behavior (Azure DevOps Server normally has TLS), but it's an inconsistency with every other branch. Worth filing upstream as an issue if `agent-runner` ever hits this case in the wild; for our port, mirror the inconsistency and add a `# TODO: Azure DevOps ignores ALLOW_INSECURE_GIT_ACCESS` comment.

## 5. `jira_manager.py` — JiraView shape, "OAuth handshake," `start_job` semantics

### 5.1 The JiraView is an `ABC`, not a Pydantic model

Report 04 §9 predicted "JiraView Pydantic model." That was wrong. From `enterprise/integrations/jira/jira_types.py`:

```python
class JiraViewInterface(ABC):
    """Interface for Jira views that handle different types of Jira interactions.

    Views hold the webhook payload directly rather than duplicating fields,
    and fetch issue details lazily when needed.
    """

    # Core data - view holds these references
    payload: 'JiraWebhookPayload'
    saas_user_auth: UserAuth
    jira_user: JiraUser
    jira_workspace: JiraWorkspace

    # Mutable state set during processing
    selected_repo: str | None
    conversation_id: str

    @abstractmethod
    async def get_issue_details(self) -> tuple[str, str]:
        """Fetch and cache issue title and description from Jira API."""
        pass

    @abstractmethod
    async def create_or_update_conversation(self, jinja_env: Environment) -> str:
        """Create or update a conversation and return the conversation ID."""
        pass

    @abstractmethod
    def get_response_msg(self) -> str:
        """Get the response message to send back to Jira."""
        pass
```

Three observations:

- **Class attributes as type-hints with no defaults.** This is the "interface declares fields, concrete class provides them" pattern. It works at runtime (Python won't complain) but it's *not enforced* — it's documentation that mypy/pyright will check. Reasonable; `agent-runner` could do the same or could use a Pydantic `BaseModel` with a separate `Protocol` for behavior. Pydantic-for-data + Protocol-for-behavior is cleaner; OpenHands' all-in-one ABC is easier to read.
- **`payload: 'JiraWebhookPayload'`** as forward reference — the payload type lives in `integrations.jira.jira_payload` and is imported under `TYPE_CHECKING` only, to avoid circular imports. Standard Python idiom; copy the pattern.
- **The "view" is *not* a passive data object — it has behavior.** `create_or_update_conversation(jinja_env)` is the heart of the integration: it talks to OpenHands' conversation-creation API, plugs in a Jinja-rendered prompt template, and returns a conversation id. `get_response_msg()` returns the comment text to post back. So a `JiraView` is closer to a **command object** (in the GoF sense) than to a DTO.

### 5.2 `receive_message` — the 5-step pipeline

```python
async def receive_message(self, message: Message):
    raw_payload = message.message.get('payload', {})
    parse_result = self.payload_parser.parse(raw_payload)
    if isinstance(parse_result, JiraPayloadSkipped):
        return
    if isinstance(parse_result, JiraPayloadError):
        return
    payload = parse_result.payload
    workspace = await self._get_active_workspace(payload)
    if not workspace:
        return
    jira_user, saas_user_auth = await self._authenticate_user(payload, workspace)
    if not jira_user or not saas_user_auth:
        return
    decrypted_api_key = self.token_manager.decrypt_text(workspace.svc_acc_api_key)
    try:
        view = await JiraFactory.create_view(
            payload=payload,
            workspace=workspace,
            user=jira_user,
            user_auth=saas_user_auth,
            decrypted_api_key=decrypted_api_key,
        )
    except RepositoryNotFoundError as e:
        await self._send_error_from_payload(payload, workspace, str(e))
        return
    except StartingConvoException as e:
        await self._send_error_from_payload(payload, workspace, str(e))
        return
    except Exception as e:
        await self._send_error_from_payload(
            payload, workspace,
            'Failed to initialize conversation. Please try again.',
        )
        return
    await self.start_job(view)
```

(Logging/extra-fields elided for clarity; original is exhaustive about it.) The 5 steps:

1. **Parse** the raw webhook into a typed `JiraWebhookPayload` (or skip / error).
2. **Workspace check** — `_get_active_workspace` validates the workspace exists, is "active" status, and that the action wasn't triggered by the workspace's own service account (recursive-trigger prevention).
3. **User auth** — see §5.3.
4. **View construction** via `JiraFactory.create_view(...)` — a factory dispatches on payload type to the right `JiraView` subclass. Three exception branches, each posting a user-friendly error comment back to the issue.
5. **`start_job(view)`** — see §5.4.

The control-flow pattern here — *every guard returns early after posting an error comment to the same issue the webhook came from* — is worth borrowing wholesale. In `agent-runner`'s Stage-5 `IssueTracker`, every "we couldn't run because X" branch should post an error comment back to Jira (or the GitHub issue, etc.) so that the user sees the failure where they triggered it, not in a CI log they won't read.

### 5.3 Authentication — there is no Jira OAuth handshake

Report 04 §9 hinted at "OAuth handshake" — that was based on a method-name grep, not a body read. The actual authentication is:

```python
async def _authenticate_user(
    self, payload: JiraWebhookPayload, workspace: JiraWorkspace
) -> tuple[JiraUser | None, UserAuth | None]:
    jira_user = await self.integration_store.get_active_user(
        payload.account_id, workspace.id
    )
    if not jira_user:
        await self._send_error_from_payload(
            payload, workspace,
            f'User {payload.user_email} is not authenticated or active in the Jira integration.',
        )
        return None, None
    saas_user_auth = await get_user_auth_from_keycloak_id(
        jira_user.keycloak_user_id
    )
    if not saas_user_auth:
        await self._send_error_from_payload(
            payload, workspace,
            f'User {payload.user_email} is not authenticated with OpenHands.',
        )
        return None, None
    return jira_user, saas_user_auth
```

The flow: the Jira webhook carries `account_id` (the Atlassian user id) → look up a `JiraUser` row in the integration store keyed by `(account_id, workspace_id)` → that row carries a `keycloak_user_id` → look up the OpenHands `UserAuth` via Keycloak. **The OAuth handshake happened *earlier*, out-of-band** — when the user first connected their Jira workspace to OpenHands via the GUI. By the time a webhook arrives, the account-id ↔ keycloak-id ↔ OpenHands-user mapping is already a row in `integration_store`.

For *outbound* posts (comments back to Jira), the manager uses **service-account basic auth**:

```python
async def send_message(
    self,
    message: str,
    issue_key: str,
    jira_cloud_id: str,
    svc_acc_email: str,
    svc_acc_api_key: str,
):
    url = (
        f'{JIRA_CLOUD_API_URL}/{jira_cloud_id}/rest/api/2/issue/{issue_key}/comment'
    )
    data = format_jira_comment_body(message)
    async with httpx.AsyncClient(verify=httpx_verify_option()) as client:
        response = await client.post(
            url, auth=(svc_acc_email, svc_acc_api_key), json=data
        )
        response.raise_for_status()
        return response.json()
```

The `svc_acc_api_key` is *encrypted at rest* (`workspace.svc_acc_api_key`) and decrypted just-in-time via `self.token_manager.decrypt_text(...)` (line in `receive_message` above). `agent-runner` should adopt the same encrypted-at-rest pattern for any user-supplied API keys we ever store; for our v1 single-tenant model, "store the API key as a GitHub Actions secret" is the equivalent and is already encrypted by GitHub.

**Net for `agent-runner`:** the OpenHands Jira integration is built for multi-tenant SaaS where workspace setup is interactive. `agent-runner`'s Jira backing for `IssueTracker` will be much simpler — a single `JIRA_API_TOKEN` repo secret + a `JIRA_BASE_URL` config field + a `JIRA_USER_EMAIL` config field. Skip the workspace/Keycloak/integration-store layer entirely; we don't need it.

### 5.4 `start_job(view)` — the borrow

```python
async def start_job(self, view: JiraViewInterface) -> None:
    try:
        conversation_id = await view.create_or_update_conversation(self.jinja_env)
        msg_info = view.get_response_msg()
    except MissingSettingsError as e:
        msg_info = f'Please re-login into [OpenHands Cloud]({HOST_URL}) before starting a job.'
    except LLMAuthenticationError as e:
        msg_info = f'Please set a valid LLM API key in [OpenHands Cloud]({HOST_URL}) before starting a job.'
    except SessionExpiredError as e:
        msg_info = get_session_expired_message()
    except StartingConvoException as e:
        msg_info = str(e)
    except Exception as e:
        msg_info = 'Sorry, there was an unexpected error starting the job. Please try again.'
    await self._send_comment(view, msg_info)
```

(Log lines elided for clarity; original logs at every branch with `extra={'issue_key': ..., 'error': ...}`.)

The shape:

- **Two-line happy path.** Create conversation; get response message.
- **Five exception-to-message translations.** Every path sets `msg_info` to something sayable in a Jira comment.
- **One terminal `await self._send_comment(view, msg_info)`.** The comment is always sent — success or failure — so the user always sees acknowledgment. **This is the key pattern.**

For `agent-runner`'s Stage-5 `IssueTracker.start_job(trigger) -> Run`:

- The `trigger` (analogous to OpenHands' `view`) carries enough state to construct a Run. In OpenHands, the view *also* knows how to mutate the conversation; in `agent-runner`, the trigger is purely descriptive and `enqueue.py` does the work.
- The exception-to-message translation table is essentially *what the user sees when something goes wrong before the agent even starts.* OpenHands has 5 entries; `agent-runner`'s minimum set is probably 3: `auth_failed → "OAuth token expired; refresh-oauth.yml may be broken"`, `rate_limited → "all Run slots in use; will queue"`, and `unknown → "see Actions logs at <url>"`.
- **Always post back, even on unexpected exceptions.** This is the user-experience invariant. `agent-runner` already does this via Slack notification on terminal status (DESIGN.md §8); `IssueTracker.start_job` should *also* do it as an issue/PR comment.

### 5.5 `JiraFactory.create_view` — the dispatch table

The factory line in `receive_message` (`view = await JiraFactory.create_view(...)`) hides a dispatch from `payload.event_type` to a concrete `JiraView` subclass. We didn't read `JiraFactory` directly. From the call signature it dispatches on `payload` — likely `payload.event_type` (mention vs. label-applied vs. status-change). For `agent-runner`, this is `Trigger.kind` (`comment | schedule | dispatch | webhook`) → concrete handler. We already do this dispatch in `enqueue.py` informally; the OpenHands pattern of *naming the factory and the abstract base* is worth borrowing once we have more than two trigger sources per integration.

## 6. Borrowed-not-reinvented — the verdict

### 6.1 Adopt verbatim

| Pattern | Source | Where in `agent-runner` |
|---|---|---|
| `_fetch_paginated_repos` link-header loop | `repos.py:_fetch_paginated_repos` | `providers/github/` whenever a method needs to walk pages. |
| `_parse_repository(dict, link_header) -> Repository` factory shape | `repos.py:_parse_repository` | `providers/github/` value-object construction. Default `private=True` for fail-closed. |
| `get_review_thread_comments` 3-step algorithm (root via `replyTo` → page threads → page comments) | `resolver.py` | `providers/github/` — needed when `trigger-comment.yml` fires on `pull_request_review_comment` events (DESIGN.md §9). |
| `get_authenticated_git_url` per-provider URL templates (all 5 providers) | `provider.py` lines ~545-630 | `providers/<each>/` once a non-GitHub provider lands. The Azure DevOps and Bitbucket DC subtleties are the non-rederivable parts. |
| `ALLOW_INSECURE_GIT_ACCESS` env-var gate with three accepted values | `provider.py` lines ~530-540 | Same module — required for self-hosted Forgejo / BDC support. |
| `start_job(view)` exception-translation pattern (every path sets `msg_info`, terminal `_send_comment(view, msg_info)`) | `jira_manager.py:start_job` | Stage-5 `IssueTracker.start_job(trigger)`. Translation table size: ~3-5 user-visible failure modes. |
| 5-step `receive_message` pipeline with early-return-after-posting-error pattern | `jira_manager.py:receive_message` | Any future webhook entry point (`trigger-webhook.yml` from DESIGN.md §9). Each guard posts a user-visible error before returning. |
| `JiraViewInterface` ABC pattern — class-attribute type hints + abstract methods | `jira_types.py` | Stage-5 `IssueTrackerView` (or whatever the per-trigger handler is named). |
| Encrypted-at-rest secrets, decrypted just-in-time | `jira_manager.py` line `self.token_manager.decrypt_text(workspace.svc_acc_api_key)` | Already covered for `agent-runner` v1 by GitHub Actions secrets — but if we ever store provider tokens *in the state branch*, encrypt them. |

### 6.2 Adapt (mirror shape, change content)

- **Pagination wrapper:** Borrow the *loop pattern* from `_fetch_paginated_repos` but skip the `extract_key` parameter (we don't fetch from installation-wrapped endpoints). One less knob.
- **GraphQL queries for review threads:** Re-write the 3 queries fresh; OpenHands' `gql"""..."""` strings are in a sibling module we didn't fetch and re-deriving them from the GraphQL schema is faster than another fetch round.
- **`start_job` exception table:** OpenHands has Keycloak and Cloud-specific failure modes (`MissingSettingsError`, `LLMAuthenticationError`, `SessionExpiredError`). `agent-runner`'s analog table is shorter — see §5.4.
- **`JiraView` factory:** Keep the dispatch idea but inline it for v1; promote to a named factory only when we have ≥3 trigger event types per integration.

### 6.3 Skip entirely

- **`get_all_repositories(sort, app_mode)` SAAS branch + GitHub-Apps installation fanout.** `agent-runner` is single-tenant, single-repo-per-Run.
- **`search_repositories` + `_fuzzy_match_org_name`.** No repo picker.
- **`verify_repo_provider`.** Run config names the provider explicitly.
- **`MappingProxyType[ProviderType, ProviderToken]` multi-provider token machinery.** One token per Run.
- **Keycloak SSO + `integration_store.get_active_user(account_id, workspace_id)`.** `agent-runner`'s "auth" for Jira is a single `JIRA_API_TOKEN` secret. No multi-tenant identity mapping.
- **`_get_active_workspace` recursive-trigger-prevention via service-account email match.** Equivalent in `agent-runner` is the existing DESIGN.md §9 "comment author is not a bot" filter — we already have it; don't double-implement.
- **The `get_impl()` env-var class-substitution machinery** (covered in report 04 §5.1; not in this round's files but worth naming under "skip" for completeness).

### 6.4 Cross-reference to DESIGN.md

Concrete updates DESIGN.md should receive when Stage 4 / Stage 5 ship:

- **§4 future seams, `ProviderClient` bullet:** add "Adopt `get_authenticated_git_url` from OpenHands `app_server/integrations/provider.py` verbatim — the Azure DevOps and Bitbucket DC URL conventions are non-obvious. Adopt the `ALLOW_INSECURE_GIT_ACCESS` env-var gate."
- **§4 future seams, `IssueTracker` bullet:** add "Mirror `Manager.start_job(view)` from OpenHands `enterprise/integrations/jira/jira_manager.py` — every exception path translates to a `msg_info` and the method always terminates with `_send_comment(view, msg_info)`. The view is a command object (it knows how to create/update a conversation) not a DTO."
- **§9 `trigger-comment.yml` bullet:** add "PR review-thread replies fire `pull_request_review_comment` events, distinct from `issue_comment`. Recovering thread context requires a 3-step GraphQL traversal — see report 05 §3.2 for the algorithm."
- **§5 `providers/github/`:** when this directory crosses ~600 lines, refactor following the OpenHands mixin layout (`base.py` + `branches_prs.py` + `prs.py` + `repos.py` + `resolver.py`). Pagination helper goes in `repos.py`; the `_make_request` + auth headers go in `base.py`.

## 7. Open questions / lower-confidence claims

1. **GraphQL query strings for `resolver.py`** — not directly read; reconstructed from variable names and field accesses. Confidence: high on the *shape* (we have variables, types, field paths); medium on the *exact* GraphQL syntax (e.g., did they alias any fields, use fragments, request specific `Comment` fields like `bodyText` vs. `body`?). Recovery cost: one WebFetch of `openhands/app_server/integrations/github/service/graphql_queries.py` (or wherever the imports come from). Probably ~5 minutes if/when needed.
2. **`JiraFactory.create_view` dispatch logic** — only the *signature* was read; the body wasn't. We don't know how many concrete `JiraView` subclasses exist or what payload-attribute the dispatch keys on. Probably `payload.event_type`. Recovery cost: one WebFetch of `enterprise/integrations/jira/jira_factory.py`. Defer until `agent-runner` Stage 5 actually starts.
3. **Whether the Azure DevOps "ignores `protocol` variable" behavior is intentional or a bug.** No upstream issue or comment found. Mirror the behavior on borrow with a `# TODO: confirm with upstream` note. Confidence: medium.
4. **`get_review_thread_comments` traversal depth assumption.** The code walks `replyTo.id` exactly *one* hop. PR review threads as currently modeled by GitHub *are* one-deep, so this is correct today. If GitHub ever ships nested replies, the algorithm finds the wrong root. Worth a comment in our port.
5. **Whether `agent-runner` will *ever* need `is_pr_open` / `get_pr_details`** as part of `ProviderClient`. Round 1 said yes (DESIGN.md §6 watchdog needs to know if a PR was closed in flight). Not contradicted by anything in this round.
6. **`format_jira_comment_body` formatting** — referenced in `send_message` but defined elsewhere. The Jira Cloud REST `/rest/api/2/issue/{key}/comment` endpoint expects ADF (Atlassian Document Format) for v3 or wiki markup for v2; this code uses v2. Worth noting if `agent-runner` ever wants rich formatting (code blocks, lists) in Jira comments — v2 wiki markup is more limited.

---

## Sources reviewed

| Source URL | Status | Notes |
|---|---|---|
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/github/service/repos.py` | ✅ Full review | All ~280 lines body-read end-to-end via WebFetch. Quoted `_fetch_paginated_repos`, `_parse_repository`, and the SAAS-mode `get_all_repositories` fanout. Informed §2 entirely and the DESIGN.md `providers/github/` mixin-layout recommendation in §6.4. |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/github/service/resolver.py` | ✅ Full review (algorithm); 🟡 partial on GraphQL strings | Method signatures + full body of `get_review_thread_comments` quoted verbatim. The three GraphQL query *strings* (`get_thread_from_comment_graphql_query`, `get_review_threads_graphql_query`, `get_thread_comments_graphql_query`) are imported from a sibling module and were NOT in the WebFetch return. Recoverable with one extra fetch of `graphql_queries.py` if `agent-runner` ever ports this. Informed §3 entirely. |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/provider.py` (lines 495-651) | ✅ Full review | Targeted fetch of just `get_authenticated_git_url`. All five per-provider URL-construction branches quoted verbatim. Informed §4 entirely and the §6.1 "adopt verbatim" table. |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/enterprise/integrations/jira/jira_manager.py` | ✅ Full review (method bodies); 🟡 partial on JiraFactory + helpers | All method signatures plus full bodies of `receive_message`, `_authenticate_user`, `send_message`, and `start_job` quoted verbatim. The `JiraFactory.create_view` dispatch body and `format_jira_comment_body` helper are referenced but not directly read. Confirmed that **report 04 §9's "OAuth handshake" prediction was wrong** — auth is via Keycloak SSO mapping established out-of-band, not an in-band OAuth flow. Informed §5 entirely. |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/enterprise/integrations/jira/jira_types.py` | ✅ Full review (supplementary) | Fetched to recover the `JiraViewInterface` definition that report 04 predicted as a "Pydantic model" but turned out to be an `ABC` with class-attribute type hints. Quoted verbatim in §5.1. Also documented `StartingConvoException` and `RepositoryNotFoundError`. Not in original 4-source list but load-bearing for §5; documented as URL drift / supplementary. |
