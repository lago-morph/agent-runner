# Report 04 — OpenHands SDK git-provider abstraction

**Date:** 2026-05-11
**Author:** Subagent (run_id: 20260511-r2, sub-03)
**Status:** ✅ complete — abstraction relocated to `openhands/app_server/integrations/`. The `GitService` Protocol and `ProviderHandler` orchestrator both exist and were read end-to-end. Round-1 report 01's 🟡-reconstructed marker on the OpenHands GitService is now upgraded to ✅ for the Stage-4 design loop.

## Lead question

Where in the current `All-Hands-AI/OpenHands` (or successor `software-agent-sdk`) repo does the git-provider abstraction live, and what is its actual interface signature — class name, method list, parameter shapes, return types — that `agent-runner`'s eventual `ProviderClient` for GitLab/Jira backends should mirror?

## 1. TL;DR — three sentences

1. The abstraction was **not removed**, but it was **relocated** and the GitHub org **renamed**: it now lives at `github.com/OpenHands/OpenHands` (formerly `All-Hands-AI/OpenHands`) under `openhands/app_server/integrations/`, with the canonical Protocol named `GitService` (in `service_types.py`) and a multi-provider orchestrator class `ProviderHandler` (in `provider.py`).
2. **The SDK was split into a sibling repo** at `github.com/OpenHands/software-agent-sdk` — but that sibling is the *agent-loop* SDK (LLM, Agent, Conversation, Tool); the **git-provider integration code stayed in the main OpenHands repo's `app_server`** (the local-GUI / cloud server). So Round-1's intuition that the abstraction had moved to a sibling SDK was wrong: it moved within the same repo, from `openhands/integrations/` to `openhands/app_server/integrations/`.
3. Six concrete providers ship today (GitHub, GitLab, Bitbucket, Bitbucket Data Center, Forgejo, Azure DevOps); each is composed from feature-mixins (`*BranchesMixin`, `*PRsMixin`, `*ReposMixin`, `*FeaturesMixin`, `*ResolverMixin`) plus a `BaseGitService` ABC. **Jira / Linear / Slack are a *separate* abstraction** (`Manager[ViewT]` in `enterprise/integrations/manager.py`) — they're issue-tracker integrations, not git providers. `agent-runner`'s Stage-4 split should mirror this: `ProviderClient` ≠ `IssueTracker`.

## 2. Locating the abstraction — what I searched and what I found

### 2.1 Path discovery

Round 1's report 01 said:

> "the top-level `/openhands/` directory shows `{analytics, app_server, server}` — the integration layer appears to have been refactored, possibly into the separate `software-agent-sdk/` package"

That guess was half-right (org renamed, SDK split out) and half-wrong (the git-provider code didn't move to the SDK; it moved into `app_server/`). The actual current path:

```
openhands/app_server/integrations/
├── service_types.py              # the Protocol + Pydantic models + exceptions
├── provider.py                   # ProviderHandler + ProviderToken
├── github/
│   ├── github_service.py         # GitHubService (assembled from mixins)
│   └── service/
│       ├── __init__.py           # exports the mixins
│       ├── base.py               # GitHubMixinBase (auth, _make_request, get_user)
│       ├── branches_prs.py       # GitHubBranchesMixin + ...
│       ├── features.py           # GitHubFeaturesMixin
│       ├── prs.py                # GitHubPRsMixin
│       ├── repos.py              # GitHubReposMixin
│       └── resolver.py           # GitHubResolverMixin
├── gitlab/
│   ├── gitlab_service.py
│   └── service/{base,branches,prs,repos}.py
├── bitbucket/bitbucket_service.py
├── bitbucket_data_center/bitbucket_dc_service.py
├── forgejo/forgejo_service.py
└── azure_devops/azure_devops_service.py
```

I confirmed each path with HEAD requests against `raw.githubusercontent.com/OpenHands/OpenHands/main/<path>`; all returned HTTP 200. I then fetched and read `service_types.py` (332 lines) and `provider.py` (651 lines) end-to-end, plus `github/github_service.py` (105 lines) and `github/service/base.py` (163 lines) for the implementation pattern.

### 2.2 Org rename

`github.com/All-Hands-AI/OpenHands` redirects to `github.com/OpenHands/OpenHands`. The README at the new location has been rewritten and explicitly distinguishes five product surfaces: SDK (sibling repo), CLI (sibling repo), Local GUI (this repo's `openhands/app_server/`), Cloud (deployment of the GUI), Enterprise (this repo's `enterprise/` directory, source-available with paid license after one month).

The git-provider integrations are **part of the GUI / Cloud server**, not the agent SDK. This is structurally informative for `agent-runner`: the OpenHands team draws their boundary at "what does the agent need to *call*" (SDK) vs. "what does the *web app* need to talk to GitHub/GitLab/etc. for" (`app_server/integrations/`). For us, `ProviderClient` lives on the orchestration side too — it's the harness's responsibility, not the agent's.

### 2.3 Reachability notes

`api.github.com/repos/.../git/trees/main?recursive=1` returned 403 (rate-limited unauthenticated requests). All `raw.githubusercontent.com/OpenHands/OpenHands/main/<path>` fetches worked. No fetch workflow needed.

## 3. Interface signature — `GitService` Protocol

From `openhands/app_server/integrations/service_types.py` (lines 235-332). Quoted verbatim:

```python
class GitService(Protocol):
    """Protocol defining the interface for Git service providers"""

    def __init__(
        self,
        user_id: str | None = None,
        token: SecretStr | None = None,
        external_auth_id: str | None = None,
        external_auth_token: SecretStr | None = None,
        external_token_manager: bool = False,
        base_domain: str | None = None,
    ) -> None:
        """Initialize the service with authentication details"""
        ...

    async def get_latest_token(self) -> SecretStr | None:
        """Get latest working token of the user"""
        ...

    async def get_user(self) -> User:
        """Get the authenticated user's information"""
        ...

    async def search_repositories(
        self,
        query: str,
        per_page: int,
        sort: str,
        order: str,
        public: bool,
        app_mode: AppMode,
    ) -> list[Repository]:
        """Search for public repositories"""
        ...

    async def get_all_repositories(
        self, sort: str, app_mode: AppMode
    ) -> list[Repository]:
        """Get repositories for the authenticated user"""
        ...

    async def get_paginated_repos(
        self,
        page: int,
        per_page: int,
        sort: str,
        installation_id: str | None,
        query: str | None = None,
    ) -> list[Repository]:
        """Get a page of repositories for the authenticated user"""
        ...

    async def get_suggested_tasks(self) -> list[SuggestedTask]:
        """Get suggested tasks for the authenticated user across all repositories"""
        ...

    async def get_repository_details_from_repo_name(
        self, repository: str
    ) -> Repository:
        """Gets all repository details from repository name"""

    async def get_branches(self, repository: str) -> list[Branch]:
        """Get branches for a repository"""

    async def get_paginated_branches(
        self, repository: str, page: int = 1, per_page: int = 30
    ) -> PaginatedBranchesResponse:
        """Get branches for a repository with pagination"""

    async def search_branches(
        self, repository: str, query: str, per_page: int = 30
    ) -> list[Branch]:
        """Search for branches within a repository"""

    async def get_pr_details(self, repository: str, pr_number: int) -> dict:
        """Get detailed information about a specific pull request/merge request"""
        ...

    async def is_pr_open(self, repository: str, pr_number: int) -> bool:
        """Check if a PR is still active (not closed/merged)."""
        ...
```

### 3.1 Method count and shape summary

`GitService` is a `typing.Protocol` (structural — anything matching the shape qualifies, no inheritance required) with **13 methods** (1 constructor + 12 async methods). Notable shape facts:

- **All operational methods are `async`.** No sync API. This matches the `app_server`'s overall FastAPI/httpx design.
- **Authentication is constructor-injected** (`token`, `external_auth_id`, `external_auth_token`, `base_domain`). No per-call auth parameter. This is a strong choice — auth state lives on the service instance for its lifetime.
- **`base_domain` is the self-hosted seam.** GitHub Enterprise, self-hosted GitLab, self-hosted Bitbucket DC, Forgejo on Codeberg or elsewhere all flow through the same `base_domain` parameter. Default-domain fallback is in `ProviderHandler.PROVIDER_DOMAINS`.
- **`UserGitInfo` (aliased as `User`), `Repository`, `Branch`, `Comment`, `SuggestedTask`** are Pydantic v2 `BaseModel` value objects defined in the same file (lines 120-168). `Branch` carries `name`, `commit_sha`, `protected`, `last_push_date`. `Repository` carries `id`, `full_name`, `git_provider`, `is_public`, `stargazers_count`, `pushed_at`, `owner_type`, `main_branch`, etc.
- **No `create_pr`, `post_comment`, `merge_pr`, `close_issue`, or any *write* operations on the Protocol.** This is the most important shape observation for `agent-runner`. The `GitService` Protocol is **read-only**. Write operations live elsewhere — concrete services have their own `create_*` methods that aren't part of the Protocol contract.
- **`get_pr_details` returns a `dict`** — raw API response — not a typed model. This is an explicit escape hatch for provider-specific fields.

### 3.2 Companion abstractions

In the same file (`service_types.py`):

```python
class BaseGitService(ABC):
    @property
    def provider(self) -> str: ...                # subclasses must override

    @abstractmethod
    async def _make_request(
        self, url: str,
        params: dict | None = None,
        method: RequestMethod = RequestMethod.GET,
    ) -> tuple[Any, dict]: ...                    # returns (json_body, link_headers)

    def _truncate_comment(self, comment_body: str, max_comment_length: int = 500) -> str: ...

class InstallationsService(Protocol):
    async def get_installations(self) -> list[str]:
        """Get installations for the service; repos live underneath"""
        ...
```

`BaseGitService` is an ABC the concrete classes inherit; it standardizes the HTTP call shape (`_make_request(url, params, method)` returning a `(body, headers)` tuple). `InstallationsService` is a *separate* Protocol layered on top of GitService for providers that have an "installations" or "workspaces" concept (GitHub Apps, Bitbucket workspaces, Bitbucket DC projects, Azure DevOps organizations). GitLab uses a different concept (`get_user_groups`) and is *not* an `InstallationsService`.

### 3.3 ProviderType enum

```python
class ProviderType(Enum):
    GITHUB = 'github'
    GITLAB = 'gitlab'
    BITBUCKET = 'bitbucket'
    BITBUCKET_DATA_CENTER = 'bitbucket_data_center'
    FORGEJO = 'forgejo'
    AZURE_DEVOPS = 'azure_devops'
    ENTERPRISE_SSO = 'enterprise_sso'
```

`ENTERPRISE_SSO` is included in the enum but does not have a corresponding `*ServiceImpl` in the `service_class_map` (see §4 below) — it's a distinct authentication-only flow.

### 3.4 Exception hierarchy

`AuthenticationError`, `UnknownException`, `RateLimitError`, `ProviderTimeoutError`, `ResourceNotFoundError` — all subclass `ValueError`. **Worth borrowing as-is**: `agent-runner`'s `providers/github/` already needs at least `AuthenticationError`, `RateLimitError`, and `ResourceNotFoundError`; using the same names would mean less translation when reading both codebases side-by-side.

## 4. `ProviderHandler` — the multi-provider orchestrator

`provider.py` defines `ProviderHandler`, a **non-abstract** orchestrator class that fans out to the per-provider `GitService` instances. It is the layer above `GitService`. Method inventory:

```python
class ProviderHandler:
    PROVIDER_DOMAINS: dict[ProviderType, str] = {
        ProviderType.GITHUB: 'github.com',
        ProviderType.GITLAB: GITLAB_HOST,
        ProviderType.BITBUCKET: 'bitbucket.org',
        ProviderType.FORGEJO: 'codeberg.org',
        ProviderType.AZURE_DEVOPS: 'dev.azure.com',
    }

    def __init__(
        self,
        provider_tokens: PROVIDER_TOKEN_TYPE,        # MappingProxyType[ProviderType, ProviderToken]
        external_auth_id: str | None = None,
        external_auth_token: SecretStr | None = None,
        external_token_manager: bool = False,
        session_api_key: str | None = None,
        sid: str | None = None,
    ): ...

    @property
    def provider_tokens(self) -> PROVIDER_TOKEN_TYPE: ...

    def get_service(self, provider: ProviderType) -> GitService: ...

    async def get_user(self) -> User: ...
    async def _get_latest_provider_token(self, provider: ProviderType) -> SecretStr | None: ...

    # Per-provider installation-list fanouts
    async def get_github_installations(self) -> list[str]: ...
    async def get_bitbucket_workspaces(self) -> list[str]: ...
    async def get_bitbucket_dc_projects(self) -> list[str]: ...
    async def get_github_organizations(self) -> list[str]: ...
    async def get_gitlab_groups(self) -> list[str]: ...
    async def get_azure_devops_organizations(self) -> list[str]: ...

    # Aggregated cross-provider operations
    async def get_repositories(
        self, sort: str, app_mode: AppMode,
        selected_provider: ProviderType | None,
        page: int | None, per_page: int | None,
        installation_id: str | None,
    ) -> list[Repository]: ...
    async def get_suggested_tasks(self) -> list[SuggestedTask]: ...
    async def search_branches(
        self, selected_provider: ProviderType | None,
        repository: str, query: str, per_page: int = 30,
    ) -> list[Branch]: ...
    async def search_repositories(
        self, selected_provider: ProviderType | None,
        query: str, per_page: int, sort: str, order: str, app_mode: AppMode,
    ) -> list[Repository]: ...
    async def verify_repo_provider(
        self, repository: str,
        specified_provider: ProviderType | None = None,
        is_optional: bool = False,
    ) -> Repository: ...                              # auto-detects which provider owns a repo
    async def get_branches(
        self, repository: str,
        specified_provider: ProviderType | None = None,
        page: int = 1, per_page: int = 30,
    ) -> PaginatedBranchesResponse: ...
    async def get_authenticated_git_url(
        self, repo_name: str, is_optional: bool = False,
    ) -> str: ...                                     # builds the https URL with embedded token

    # Internal helpers
    def _is_repository_url(self, query: str, provider: ProviderType) -> bool: ...
    def _deduplicate_repositories(self, repos: list[Repository]) -> list[Repository]: ...
    @classmethod
    def get_provider_env_key(cls, provider: ProviderType) -> str: ...
```

Construction-time wiring — the `service_class_map`:

```python
self.service_class_map: dict[ProviderType, type[GitService]] = {
    ProviderType.GITHUB: GithubServiceImpl,
    ProviderType.GITLAB: GitLabServiceImpl,
    ProviderType.BITBUCKET: BitBucketServiceImpl,
    ProviderType.BITBUCKET_DATA_CENTER: BitbucketDCServiceImpl,
    ProviderType.FORGEJO: ForgejoServiceImpl,
    ProviderType.AZURE_DEVOPS: AzureDevOpsServiceImpl,
}
```

### 4.1 `ProviderHandler` shape observations

- **It's a *handler*, not a *registry*.** The class both (a) maps provider → service class and (b) implements all the cross-provider fanout logic. There's no smaller "registry" abstraction; the dict is just an instance attribute.
- **Multi-provider repository search and aggregation are first-class.** A single `agent-runner` repo will only ever have one git provider per Run, so we don't need the cross-provider fanout that drives `get_repositories(selected_provider=None)`. **For our Stage 4, the right shape is closer to a registry-of-one-per-Run** than to OpenHands' multi-provider `ProviderHandler`.
- **`get_authenticated_git_url(repo_name)` is load-bearing.** This builds the HTTPS-with-embedded-token URL for `git clone` / `git push`. It branches on provider for the username convention (`oauth2:<token>@` for GitLab, `x-token-auth:<token>@` for Bitbucket, `<token>@` for GitHub/Forgejo, `<org>:<pat>@` for Azure DevOps). **`agent-runner` will need this exact function** when we add a non-GitHub backend; we should adopt the method name and the per-provider URL template directly.
- **`verify_repo_provider(repository)` does provider auto-detection.** Useful for OpenHands' multi-provider users; **not relevant for `agent-runner`** because each Run already names its provider.
- **OAuth refresh is in-band**, via `_get_latest_provider_token(provider)` calling `WEB_HOST/api/refresh-tokens?provider=...&sid=...`. The refresh URL is a separate service the OpenHands cloud runs. `agent-runner` already plans its own `refresh-oauth.yml` workflow (DESIGN.md §7); the OpenHands pattern is informative — `provider` and `sid` are the only inputs needed — but the *transport* differs (we'd refresh in CI, they refresh in a long-lived service).

## 5. Implementation surface — what concrete providers exist and how big they are

Sizes via `Content-Length` header from raw.githubusercontent.com:

| Provider | Top-level `*_service.py` | Mixins under `service/` | Total file count | Total bytes |
|---|---:|---|---:|---:|
| GitHub | 105 lines (3.2 KB) | base, branches_prs, features, prs, repos, resolver (6 files, ~40 KB) | 7 | ~43 KB |
| GitLab | 3.6 KB | base, branches, prs, repos (4 files, ~21 KB) | 5 | ~25 KB |
| Bitbucket (cloud) | 2.9 KB | (no separate mixins) | 1 | 2.9 KB |
| Bitbucket Data Center | 3.9 KB | (no separate mixins) | 1 | 3.9 KB |
| Forgejo | 1.6 KB | (no separate mixins) | 1 | 1.6 KB |
| Azure DevOps | 10.0 KB | (no separate mixins) | 1 | 10.0 KB |

**GitHub is the canonical and largest implementation.** Its mixin breakdown is informative for `agent-runner`'s eventual structure inside `providers/github/`:

- `base.py` (~5.7 KB) — `GitHubMixinBase(BaseGitService, HTTPClient)`. Contains `_make_request`, `_get_headers`, `execute_graphql_query`, `get_user`, `get_user_emails`, `verify_access`. **This is the shape to mirror in `providers/github/base.py` if we ever break our existing single-file provider out.**
- `branches_prs.py` (~5.8 KB) — branch + paginated branch listing + search.
- `prs.py` (~4.4 KB) — PR-only operations.
- `features.py` (~4.1 KB) — feature-flagged or app-mode-conditional methods.
- `repos.py` (~11.6 KB) — repository CRUD-and-discovery (largest mixin).
- `resolver.py` (~8.2 KB) — GitHub-Resolver-specific behavior (auto-link issue → PR resolution, `[fix #N]` parsing).

GitHub's `__init__.py` for `service/` exports five mixins; `github_service.py` then composes them:

```python
class GitHubService(
    GitHubBranchesMixin,
    GitHubFeaturesMixin,
    GitHubPRsMixin,
    GitHubReposMixin,
    GitHubResolverMixin,
    BaseGitService,
    GitService,
    InstallationsService,
):
    ...
    BASE_URL = 'https://api.github.com'
    GRAPHQL_URL = 'https://api.github.com/graphql'

    @property
    def provider(self) -> str:
        return ProviderType.GITHUB.value
```

Note the **mixin ordering**: feature mixins first, then `BaseGitService`, then the two Protocols (`GitService`, `InstallationsService`) for type-checker satisfaction. Python MRO resolves `_make_request` to whichever mixin defines it (here, `GitHubMixinBase` via `base.py`).

### 5.1 Customization seam — `get_impl()` pattern

The bottom of `github_service.py`:

```python
github_service_cls = os.environ.get(
    'OPENHANDS_GITHUB_SERVICE_CLS',
    'openhands.app_server.integrations.github.github_service.GitHubService',
)

def get_github_service_impl():
    global _github_service_impl
    if _github_service_impl is None:
        _github_service_impl = get_impl(GitHubService, github_service_cls)
    return _github_service_impl

class _GitHubServiceImplProxy:
    def __getattr__(self, name): ...
    def __call__(self, *args, **kwargs): ...

GithubServiceImpl: type[GitHubService] = _GitHubServiceImplProxy()
```

Applications can substitute their own `GitHubService` subclass via the `OPENHANDS_GITHUB_SERVICE_CLS` env var. The `get_impl()` helper resolves a fully-qualified class name to a class object. **`agent-runner` does not need this seam in v1** — we'd only want it if a user wanted to inject a custom GitHub mock or wrap our calls with extra logging. Defer until concrete demand.

## 6. Issue trackers are a *separate* abstraction

`agent-runner`'s DESIGN.md §4 lists `ProviderClient` (git) and `IssueTracker` (Jira/Linear) as two separate future seams. **The OpenHands codebase confirms this split is correct.** Issue-tracker / chat integrations live in `enterprise/integrations/` and use a *different* abstraction:

```python
# enterprise/integrations/manager.py
class Manager(ABC, Generic[ViewT]):
    manager_type: SourceType

    @abstractmethod
    async def receive_message(self, message: Message): ...

    @abstractmethod
    def send_message(self, message: str, *args: Any, **kwargs: Any): ...

    @abstractmethod
    async def start_job(self, view: ViewT) -> None: ...
```

Concrete subclasses: `JiraManager(Manager[JiraViewInterface])` (in `enterprise/integrations/jira/jira_manager.py`, ~14 KB), and similar managers for Slack, Linear, etc.

**Three observations for `agent-runner`'s Stage-4 split:**

1. **The git-provider abstraction (`GitService` / `ProviderHandler`) is read-and-act-on-repos. The issue-tracker abstraction (`Manager[ViewT]`) is bidirectional-message-passing.** They have nothing in common at the Protocol level. `agent-runner` should likewise have two unrelated interfaces.
2. **The `Manager.start_job(view)` shape is the integration → agent-runner trigger.** This is exactly the Slack-mention-or-Jira-ticket-comment flow. `agent-runner`'s eventual `IssueTracker` shape should expose a `start_job` semantic that the workflow trigger calls into.
3. **Jira is in `enterprise/`, not `openhands/`.** The Jira/Linear integrations are paid-license territory in OpenHands. We can read the *interface shape* (it's MIT-licensed code in a public repo) but should not vendor the implementation — the license forbids running it for more than a month without a paid license.

## 7. Mapping to `agent-runner` Stage 4 — adopt / adapt / differ

DESIGN.md §4 names four future seams. Restated against what we now know:

| `agent-runner` seam | OpenHands counterpart | Verdict |
|---|---|---|
| `ProviderClient` (GitHub vs GitLab vs Forgejo for issue/PR/comment ops) | `GitService` Protocol (`openhands/app_server/integrations/service_types.py`) + `ProviderHandler` orchestrator | **Adopt-and-trim.** See §7.1 below. |
| `IssueTracker` (Jira / Linear / GitHub Issues) | `Manager[ViewT]` ABC (`enterprise/integrations/manager.py`) | **Adapt** the `start_job(view)` semantic; **don't** vendor concrete managers (license + multi-tenant assumptions). |
| `Notifier` (Slack / Mattermost / Teams / email) | Not a single OpenHands interface — implemented inside Slack/Linear `Manager` subclasses' `send_message` | **Differ.** Keep as a flat `Notifier` Protocol with one method `send(text, channel)`; do not couple it to issue-tracker abstraction. |
| `AgentRuntime` (Claude Code / Codex / Aider) | Overstory's `AgentRuntime` (per Round 1) | **Adopt** Overstory shape per Round 1; OpenHands has no analogous abstraction at the *runtime-process* level (their SDK is the runtime, full stop). |

### 7.1 Concrete `ProviderClient` proposal for Stage 4

When a second git provider arrives, extract `ProviderClient` from `providers/github/` with this shape (mirroring `GitService` but trimmed to what `agent-runner` actually does):

```python
class ProviderClient(Protocol):
    """Read-and-write git-provider operations agent-runner needs."""

    def __init__(
        self,
        token: SecretStr,
        base_domain: str | None = None,    # for self-hosted GitLab/Forgejo
    ) -> None: ...

    # --- read operations (mirror GitService directly) ---
    async def get_user(self) -> User: ...
    async def get_repository(self, repo_name: str) -> Repository: ...
    async def get_pr_details(self, repo_name: str, pr_number: int) -> dict: ...
    async def is_pr_open(self, repo_name: str, pr_number: int) -> bool: ...
    async def get_branches(self, repo_name: str) -> list[Branch]: ...

    # --- write operations (NOT in GitService Protocol — we add them) ---
    async def post_comment(self, repo_name: str, issue_or_pr_number: int, body: str) -> Comment: ...
    async def create_pr(
        self, repo_name: str,
        head: str, base: str,
        title: str, body: str,
        draft: bool = False,
    ) -> dict: ...
    async def update_pr(self, repo_name: str, pr_number: int, **fields) -> dict: ...
    async def add_label(self, repo_name: str, issue_or_pr_number: int, label: str) -> None: ...

    # --- git-clone URL with embedded credentials (load-bearing for run.py) ---
    def get_authenticated_clone_url(self, repo_name: str) -> str: ...
```

Adopt verbatim from OpenHands:
- The `Protocol` (not ABC) approach — duck-typing keeps testing easy.
- Pydantic value objects: `User`, `Repository`, `Branch`, `Comment`. Steal field-for-field; small enough to retype.
- The exception hierarchy: `AuthenticationError`, `RateLimitError`, `ProviderTimeoutError`, `ResourceNotFoundError`, `UnknownException` — all subclassing `ValueError`.
- The `base_domain` constructor parameter for self-hosted instances.
- `get_authenticated_clone_url` (renaming from `get_authenticated_git_url`) and the per-provider URL templates from `provider.py` lines 549-647.

Adapt (differ in shape):
- **Drop `ProviderHandler`-style multi-provider fanout.** `agent-runner` is single-provider-per-Run. The "registry" reduces to `ProviderClient.from_run_config(run)`. No `get_repositories(selected_provider=None)` cross-provider aggregation.
- **Add write operations** (`post_comment`, `create_pr`, etc.) directly onto `ProviderClient`. The OpenHands Protocol is read-only because writes are scattered across mixins and the GUI — `agent-runner`'s mental model of "the provider client" is the thing that does both reads and writes.
- **Fewer methods overall.** OpenHands' `GitService` has 13 methods because the GUI needs repository search, suggested tasks, paginated branches, etc. `agent-runner` only needs: `get_user`, `get_repository`, `get_pr_details`, `is_pr_open`, `get_branches`, `post_comment`, `create_pr`, `update_pr`, `add_label`, `get_authenticated_clone_url`. **10 methods, not 13.**
- **`async` is fine** but consider: our `run.py` is sync today. If we adopt async, every call site needs an event loop. Probably worth it; matches OpenHands and matches the natural concurrency of comment + label + PR-update fanouts in `notify.py`.

Differ explicitly:
- **Don't adopt `get_impl()` env-var customization.** Premature flexibility for our v1 and v2 use cases.
- **Don't adopt the mixin decomposition for v1.** Keep `providers/github/__init__.py` as a single-file implementation. Refactor into `base.py` + `branches_prs.py` + `prs.py` + `repos.py` mixins **only if** the file crosses ~600 lines, mirroring the GitHub directory size in OpenHands.
- **Don't put Jira / Linear under `ProviderClient`.** They go under `IssueTracker` per DESIGN.md §4 — mirrors OpenHands' `Manager[ViewT]` split.

### 7.2 What to write into DESIGN.md §4 once Stage 4 lands

Two-sentence addition under the "Future seams" bullet on `ProviderClient`:

> The shape mirrors OpenHands' `GitService` Protocol (`openhands/app_server/integrations/service_types.py`) — async methods, constructor-injected token + optional `base_domain`, Pydantic value objects, exceptions subclassing `ValueError`. We trim the OpenHands surface from 13 methods to ~10 and add the write operations (`post_comment`, `create_pr`, `update_pr`, `add_label`) that OpenHands keeps off the Protocol.

And under `IssueTracker`:

> Mirrors OpenHands' `enterprise/integrations/manager.py` `Manager[ViewT]` ABC — bidirectional message passing (`receive_message`, `send_message`) plus `start_job(view)`. `IssueTracker` is *not* a `ProviderClient`; the two abstractions are unrelated and should not share base classes.

## 8. What changed since Round 1

Three corrections to report 01 §6:

1. **Path:** "the integration layer appears to have been refactored, possibly into the separate `software-agent-sdk/` package" → **wrong**. The integration layer was refactored to `openhands/app_server/integrations/` *within the same repo*. The `software-agent-sdk/` package contains agent-loop primitives (LLM, Agent, Conversation, Tool), no git providers.
2. **Org:** the repo is now `OpenHands/OpenHands`, not `All-Hands-AI/OpenHands`. Old URLs redirect; raw URLs work under both forms during the transition window.
3. **Status:** the GitService row in report 01's Sources table can be upgraded from 🟡 Reconstructed to ✅ Full review. Interface is now read end-to-end and quoted in §3 above.

No need to *edit* report 01 (round 1 is closed); this report supersedes the relevant claims and the index entry will (when next updated) reference both.

## 9. Open follow-ups (not promoted to PLAN.md by this subagent — dispatcher-owned)

For the lead agent / dispatcher to decide whether to promote:

- **Read the GitHub mixins end-to-end** if/when we extract our own `providers/github/` into multiple files. `repos.py` (~11.6 KB) is the canonical pagination + GraphQL shape; worth borrowing patterns. `resolver.py` is the GitHub-Resolver auto-link issue→PR logic — possibly inspirational for our own Run/Issue association.
- **Inspect `enterprise/integrations/jira/jira_manager.py`** when we add Jira support. It's 14 KB and includes workspace management, OAuth handshake, and the `start_job` semantic. Read for the JiraView shape and the `_authenticate_user` + `_get_active_workspace` pattern.
- **`get_authenticated_git_url`** in `provider.py` (lines 495-651) is worth re-reading when we wire our second provider. The Azure DevOps and Bitbucket DC URL-construction logic has subtleties (URL-encoding, `scm/` path prefix for DC, org-as-username for Azure) that are easy to get wrong.
- **The `software-agent-sdk` repo** at `github.com/OpenHands/software-agent-sdk` is unrelated to the git-provider abstraction *but* is the actual agent-loop SDK. If `agent-runner` ever moves off `claude-code-action` toward an SDK-based runner, this is the reference implementation.

---

## Sources reviewed

| Source URL | Status | Notes |
|---|---|---|
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/README.md` | ✅ Full review | Confirmed org rename (All-Hands-AI → OpenHands), the SDK/CLI/Local GUI/Cloud/Enterprise product split, and the `software-agent-sdk` sibling-repo pointer. Informed §1 and §2.2. |
| `https://raw.githubusercontent.com/OpenHands/software-agent-sdk/main/README.md` | ✅ Full review | Confirmed the SDK is the agent-loop layer (LLM, Agent, Conversation, Tool, FileEditorTool, TerminalTool, TaskTrackerTool) — NOT the git-provider layer. Quick-start example quoted. Informed §1 and §2.2. |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/service_types.py` | ✅ Full review | The `GitService` Protocol, `BaseGitService` ABC, `InstallationsService` Protocol, `ProviderType` enum, `TaskType`, `OwnerType`, `SuggestedTask`, `User`/`UserGitInfo`, `Branch`, `PaginatedBranchesResponse`, `Repository`, `Comment`, exception hierarchy, `RequestMethod` enum. 332 lines, all read. Informed §3 entirely. |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/provider.py` | ✅ Full review | `ProviderToken`, `CustomSecret`, `ProviderHandler` (the orchestrator). 651 lines, read end-to-end including the `get_authenticated_git_url` per-provider URL templates. Informed §4 and §7.1. |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/github/github_service.py` | ✅ Full review | The mixin-composition pattern; 105 lines. Quoted in §5 verbatim including the `get_impl()` proxy. Informed §5 and §5.1. |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/github/service/__init__.py` | ✅ Full review | Confirmed the five mixin exports (`GitHubMixinBase`, `GitHubBranchesMixin`, `GitHubFeaturesMixin`, `GitHubPRsMixin`, `GitHubReposMixin`, `GitHubResolverMixin`). Informed §5 mixin breakdown. |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/github/service/base.py` | ✅ Full review | `GitHubMixinBase(BaseGitService, HTTPClient)` — `_make_request`, `_get_headers`, `execute_graphql_query`, `get_user_emails`, `verify_access`, `get_user`. 163 lines, all read. Informed §5 and §3.2. |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/enterprise/integrations/manager.py` | ✅ Full review | `Manager(ABC, Generic[ViewT])` — `receive_message`, `send_message`, `start_job(view)`. 36 lines. Informed §6 entirely. |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/enterprise/integrations/types.py` | 🟡 Targeted (header + class signatures via grep) | 81 lines; informed §6 confirmation that types are SourceType / Message / etc. (issue-tracker concepts, distinct from git ProviderType). Not deeply parsed. |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/enterprise/integrations/jira/jira_manager.py` | 🟡 Targeted (method-list grep, not body-read) | `JiraManager(Manager[JiraViewInterface])` with `receive_message`, `_get_active_workspace`, `_authenticate_user`, `start_job`, `send_message`, `_send_comment`, `_send_error_from_payload`, `get_workspace_name_from_payload`. 14 KB. Quoted method names in §6 and §9. Body not deeply parsed; deferred to a future-research follow-up if/when `agent-runner` adds Jira. |
| `https://api.github.com/repos/OpenHands/OpenHands/git/trees/main?recursive=1` | ❌ Unavailable | HTTP 403 (unauthenticated rate limit). Worked around by probing candidate raw URLs; no fetch workflow needed. Documented in §2.3. |
| `https://api.github.com/repos/OpenHands/software-agent-sdk/git/trees/main?recursive=1` | ❌ Unavailable | HTTP 403 (same reason). Not load-bearing for this report — SDK README §1 source was sufficient to confirm SDK scope is agent-loop, not git providers. |
| HEAD-only probes against `raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/{gitlab,bitbucket,bitbucket_data_center,forgejo,azure_devops}/...` | ✅ Status + Content-Length only | Confirmed file presence and approximate sizes for §5's per-provider table. File bodies not read; sizes are sufficient for the "implementation surface" question and `agent-runner` does not need to mirror these implementations directly. |
| `https://docs.openhands.dev/sdk` | ❌ Unavailable (not attempted) | Not needed once the source paths were located. The README at the SDK repo root was sufficient. Recoverable with a single WebFetch if a future report needs it. |
