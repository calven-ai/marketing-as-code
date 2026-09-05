# DataForSEO for content-decay-monitor

The `dataforseo` MCP server in `.mcp.json`. Names are the tool families
as the server lists them at version 3.1.1; check the server's tool list in
the session before calling. The rankings pull is the same one
`seo-analyst` makes weekly; reuse its snapshot when it is fresh enough.

## Tool families this skill uses

| Step | Family | Notes |
| --- | --- | --- |
| Every keyword our domain ranks for | `dataforseo_labs_google_ranked_keywords` | Target is our domain; `limit` up to 1,000; filter `ranked_serp_element.serp_item.rank_absolute` under 21 for the top-20 view, or keep all and filter locally |
| Pages by ranking share | `dataforseo_labs_google_relevant_pages` | One row per URL with keyword count and estimated traffic; a cheap second view when the keyword list is long |
| Rank history for one keyword | `dataforseo_labs_google_historical_rank_overview` | Only for a page the team asks about; the monthly snapshots are the normal history |

## Column mapping

`data/seo/snapshots/YYYY-MM-DD-dataforseo-rankings.csv`:

| Column | Source field |
| --- | --- |
| `keyword` | `keyword_data.keyword` |
| `volume` | `keyword_data.keyword_info.search_volume` |
| `rank` | `ranked_serp_element.serp_item.rank_absolute` |
| `url` | `ranked_serp_element.serp_item.relative_url` joined to the host |
| `checked` | today's date |

Unattended runs produce the same file through `scripts/seo_snapshot.py`'s
pattern; the columns are what the diff step keys on, so keep them.

## Cost

One Labs call per 1,000 rows, a cent or two. The monthly run is one or two
calls.

## Quirks

- The vendor's "estimated traffic" is a model; use sessions from
  `web-analytics` for traffic and rank from here.
- `relative_url` includes the query string on some rows; normalise before
  diffing by URL.
- A keyword absent from the new snapshot but present in the old one fell
  out of the top 100, not to zero volume.
