# LinkedIn (organic page) for social-performance

Catalog id `linkedin-organic`, source token `linkedin`. There is no
official LinkedIn MCP server, and community servers use unofficial APIs
or browser automation that breach LinkedIn's terms; do not wire them
(`integrations/catalog/social.json`). Two routes:

## Route 1: the manual export (default)

A page admin opens the company page, Analytics, Content (or Updates),
sets the date range to the month, and exports. LinkedIn produces a
spreadsheet with one sheet of metrics per day and one of per-post
metrics; save the per-post sheet as CSV at
`data/social/snapshots/YYYY-MM-DD-linkedin-posts.csv`, keeping LinkedIn's
column names in the file and mapping them in the report.

| Snapshot column | LinkedIn export column |
| --- | --- |
| `post_id` | the post URL's activity id |
| `posted_at` | Created date |
| `url` | Post link |
| `text_start` | Post title (the first line) |
| `impressions` | Impressions |
| `reactions` | Reactions (Likes in older exports) |
| `comments` | Comments |
| `reposts` | Reposts (Shares) |
| `clicks` | Clicks |
| `saves` | not exported for pages; leave empty |
| `followers_at` | from the Followers sheet, the month-end total |

Follower demographics in the export are aggregates; do not copy the
visitor or follower sheets that name people into the repo.

## Route 2: through a scheduling tool

Buffer, Hootsuite, Typefully and Taplio read page analytics through
LinkedIn's official partner API. When one is wired, its `references/`
file (`buffer.md` here) maps its fields; the source token in the snapshot
name is that tool's (`buffer`), not `linkedin`, because the numbers come
from its sync and can lag a day.

## Quirks

- Impressions are counted differently for page posts and for posts
  employees share; the export covers page posts only.
- Video views and document (carousel) page views are separate columns
  when present; record them in `text_start`'s notes or a `notes` column,
  not as clicks.
- Exports cover a rolling window of up to twelve months; pull monthly so
  history never has a gap.
- The API does not expose "saves" for pages; a save count in a report
  came from somewhere else and needs its source stated.
