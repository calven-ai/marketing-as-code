# X for social-performance

Catalog id `x`, source token `x`. The hosted server at X's MCP endpoint
authenticates with the team's own developer credentials; the open-source
`xmcp` server runs locally with a bearer token. Check the server's tool
list in the session: the survey confirmed search, user and engagement
tools, and posting over MCP is not confirmed. Write tools stay denied
until a person checks them (`integrations/catalog/social.json`).

## What to ask the server for

| Step | Tool family (names vary by server) | Notes |
| --- | --- | --- |
| The account's posts for the month | user timeline or "posts by user" with a start and end time | Paginate; ask for `public_metrics` and `non_public_metrics` (impressions need the account's own auth) |
| Per-post engagement | the same call's metrics object | `impression_count`, `like_count`, `reply_count`, `retweet_count`, `quote_count`, `bookmark_count`, `url_link_clicks`, `user_profile_clicks` |
| Followers at month end | user lookup with `public_metrics` | `followers_count` |

## Column mapping

| Snapshot column | X field |
| --- | --- |
| `post_id` | `id` |
| `posted_at` | `created_at` |
| `url` | `https://x.com/<handle>/status/<id>` |
| `text_start` | first 80 characters of `text` |
| `impressions` | `non_public_metrics.impression_count` |
| `reactions` | `public_metrics.like_count` |
| `comments` | `public_metrics.reply_count` |
| `reposts` | `retweet_count` plus `quote_count` |
| `clicks` | `non_public_metrics.url_link_clicks` |
| `saves` | `public_metrics.bookmark_count` |
| `followers_at` | `followers_count` at pull time |

## The manual route

X Analytics (analytics.x.com or the Creator dashboard), Export data for
the month, saved as `data/social/snapshots/YYYY-MM-DD-x-posts.csv` with
X's column names kept.

## Cost and limits

API tier limits apply per call and per month; the free tier is too small
for a month of posts on an active account, and full-archive search needs
a paid tier. State the call count; a month is usually two to five
paginated calls.

## Quirks

- Non-public metrics are only available for the authenticated account's
  own posts, and only for recent posts (about 30 days); pull monthly or
  the impressions are gone.
- Threads are separate posts; join them by the conversation id and
  report the first post's numbers as the thread's.
- Replies to other accounts are posts too; filter them out of the
  format tables or label them.
