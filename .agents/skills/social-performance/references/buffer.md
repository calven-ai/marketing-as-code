# Buffer for social-performance

Catalog id `buffer`, source token `buffer`. Buffer's official MCP server
takes OAuth or a personal API key; the vendor page confirms the server
but does not print the endpoint URL, so a person reads it from Buffer's
settings when wiring, and write tools (create, schedule) stay denied
until checked (`integrations/catalog/social.json`). Analytics is a
read; that is all this skill uses.

## What to ask for

Check the server's tool list in the session. Expect, in some spelling:

| Step | Tool family | Notes |
| --- | --- | --- |
| Channels | list channels | One row per connected network (LinkedIn page, X account, and so on); the channel id scopes everything else |
| Posts sent in a range | list posts or "sent updates" with a channel id and date range | Paginate; ask for the statistics object |
| Per-post statistics | the post's `statistics` | Field names differ per network; Buffer normalises impressions, reach, likes, comments, shares, clicks where the network provides them |

## Column mapping

| Snapshot column | Buffer field |
| --- | --- |
| `network` | the channel's service name |
| `post_id` | post id (keep Buffer's, and the network's when returned) |
| `posted_at` | `sent_at` |
| `url` | the network permalink when present |
| `text_start` | first 80 characters of the text |
| `impressions`, `reactions`, `comments`, `reposts`, `clicks` | the statistics object; `reactions` is likes, `reposts` is shares plus reposts |
| `saves` | empty unless the network reports it |
| `followers_at` | from the channel's analytics summary |

Snapshot name: `data/social/snapshots/YYYY-MM-DD-buffer-posts.csv`; the
source token is Buffer's because the numbers come from its sync.

## Cost and limits

Buffer does not bill per call; API rate limits apply. A month is a
handful of calls per channel.

## Quirks

- Statistics lag the network by up to a day; pull after the first of the
  month, not on it.
- Posts published outside Buffer (from the phone, by another tool) are
  absent; list them as untracked in the report, and use the network's
  own export when the gap matters.
- Buffer parks MCP-created posts as drafts or scheduled items; this skill
  creates nothing, and a draft is `publish`'s job with a person's yes.
