# Report 09 — OpenHands GraphQL queries used by `resolver.py` (verbatim)

**Date:** 2026-05-11
**Author:** Subagent (run_id: 20260511-r4, sub-02)
**Status:** ✅ complete — `queries.py` located and fetched; all three GraphQL strings imported by `resolver.py` quoted verbatim below. The file is *not* `graphql_queries.py` as report 05 hypothesized; it is `openhands/app_server/integrations/github/queries.py` and it contains five query constants (the three resolver imports plus two `suggested_task_*` queries and a `search_branches` query).

## Lead question

What are the literal `gql"""..."""` strings behind the three constants `get_thread_from_comment_graphql_query`, `get_review_threads_graphql_query`, and `get_thread_comments_graphql_query` that `openhands/app_server/integrations/github/service/resolver.py` imports? Report 05 §3 reconstructed the *shape* of these queries from variable names and field accesses, but flagged the literal strings as a 🟡 partial — recoverable with one extra fetch. This report completes that fetch so that any agent-runner port of `get_review_thread_comments` can copy-paste rather than reverse-engineer.

## Where the queries live

Final URL: `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/github/queries.py`

Confirmed via the import statement in `resolver.py` (line 4-9):

```python
from openhands.app_server.integrations.github.queries import (
    ...
    get_thread_from_comment_graphql_query,
    ...
)
```

The directory layout is `openhands/app_server/integrations/github/queries.py` — a sibling of the `service/` sub-package, not inside it. `queries.py` is 153 lines and contains five module-level string constants, all assigned with triple-quoted plain `str` (no `gql""" """` wrapper, no `graphql-core` parsing — they are passed straight through to `execute_graphql_query` which posts them to `https://api.github.com/graphql` as the `query` field of the JSON body).

## Query 1 — `get_thread_from_comment_graphql_query`

```graphql
    query GetThreadFromComment($commentId: ID!) {
        node(id: $commentId) {
            ... on PullRequestReviewComment {
                id
                body
                author {
                    login
                }
                createdAt
                updatedAt
                replyTo {
                    id
                    body
                    author {
                        login
                    }
                    createdAt
                    updatedAt
                }
            }
        }
    }
```

Takes a single `$commentId: ID!` (the GraphQL global node ID of *any* comment in a PR review thread — possibly the trigger comment itself, possibly a reply deep in the chain) and returns that comment plus its immediate `replyTo` parent. Note it returns *only one level up* — `resolver.py` walks the chain by re-issuing this query against `replyTo.id` until `replyTo` comes back null, at which point the most recent non-null result is the root comment of the thread. Both `body` and `author.login` are fetched at both levels even though the resolver only uses the IDs for the walk; the bodies are presumably for log/debug.

## Query 2 — `get_review_threads_graphql_query`

```graphql
query($owner: String!, $repo: String!, $number: Int!, $first: Int = 50, $after: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      reviewThreads(first: $first, after: $after) {
        nodes {
          id
          path
          isResolved
          comments(first: 1) {
            nodes {
              id
              databaseId
              body
              author {
                login
              }
            }
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }
}
```

Lists the review threads on a single PR with cursor pagination (`first: $first, after: $after`, default page size 50). For each thread it returns only `comments(first: 1)` — the *root comment* — because that is all the resolver needs to match the thread by root-comment-id. The thread `id` (a GraphQL node ID) and `path` (the file the thread is anchored to) come along for free. Both `id` (REST comment ID encoded as base64 GraphQL global ID) and `databaseId` (the integer REST id) are returned; the resolver compares against whichever form the input id is in. `isResolved` is fetched but not consulted in the algorithm — it is presumably available for future filtering.

## Query 3 — `get_thread_comments_graphql_query`

```graphql
query ($threadId: ID!, $page: Int = 50, $after: String) {
  node(id: $threadId) {
    ... on PullRequestReviewThread {
      id
      path
      isResolved
      comments(first: $page, after: $after) {
        nodes {
          id
          databaseId
          body
          author { login }
          createdAt
        }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}
```

Once the thread has been located by Query 2, this fetches *all* comments in it (paginated, default page 50) by passing the thread's GraphQL node ID directly into `node(id: $threadId)` and inline-fragment-casting to `PullRequestReviewThread`. Note the variable is named `$page` even though it is a `first:` count, not a page number — slight misnomer but harmless. `createdAt` is included here (unlike Query 2's per-thread root preview) because the resolver needs it to populate the `Comment.created_at` field on the returned `Comment` objects. `updatedAt` is *not* requested; the resolver falls back to `datetime.fromtimestamp(0)` when constructing the value object.

## Port checklist

If `agent-runner` ports the review-thread lookup into Stage-4 `providers/github/`, preserve at minimum:

- **Query 1 → `replyTo` chain walk.** Must fetch `replyTo.id` (and `replyTo` must itself nest `replyTo`-eligible fields if you want to skip a re-fetch — OpenHands chooses to re-fetch). The inline fragment `... on PullRequestReviewComment` is required because `node(id:)` returns the abstract `Node` interface.
- **Query 2 → `comments(first: 1)` per thread.** Returning only the root comment per thread is the whole point — do not bump `first:` on the inner connection or you waste bandwidth. Keep both `id` and `databaseId` so the matcher works whether the trigger comment id arrived as REST integer or GraphQL global ID.
- **Query 2 → `pageInfo { hasNextPage endCursor }`.** Required for the outer loop. Default page size `first: Int = 50` is GitHub's documented sweet spot for `reviewThreads` (max 100, but 50 keeps payload modest when threads are deep).
- **Query 3 → `node(id: $threadId) { ... on PullRequestReviewThread }`.** Same Node-interface caveat as Query 1.
- **Query 3 → request `createdAt` on each comment.** OpenHands uses it for `Comment.created_at`; `updatedAt` is not requested and the value object falls back to epoch-0 — a port should decide whether to add `updatedAt` (one extra field, free) rather than inherit the silent fallback.
- **No fragments, no aliases, no directives.** All three queries are flat — easy to copy verbatim into a Python triple-quoted string and pass through any GraphQL transport. They do *not* require `graphql-core` parsing on the client side.

Cardinality limits to copy as-is unless there is a specific reason not to: `reviewThreads(first: 50)`, `comments(first: 1)` (root preview), `comments(first: $page, after: $after)` with `$page = 50` (full thread page).

## Sources reviewed

| Source | Status | What it informed |
|---|---|---|
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/github/queries.py` | ✅ Full read (153 lines) | All three query strings quoted verbatim above; port checklist; observation that the file is `queries.py` not `graphql_queries.py` (correcting report 05's hypothesis) |
| `https://raw.githubusercontent.com/OpenHands/OpenHands/main/openhands/app_server/integrations/github/service/resolver.py` (imports section, lines 1-11) | ✅ Spot read | Confirmed the import path and constant names; resolved the file location after the original `graphql_queries.py` guess 404'd |
| `research/05-openhands-github-mixins-jira.md` §3 | ✅ Re-read | Source of the 🟡 deferred row this report closes; cross-checked field names (`replyTo.id`, `databaseId`, `pageInfo.hasNextPage/endCursor`) — all match the verbatim strings |
