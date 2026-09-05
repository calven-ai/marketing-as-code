# DataForSEO for backlink-analysis

The `dataforseo` MCP server in `.mcp.json`, Backlinks API family. Names
are the tool families as the server lists them at version 3.1.1; check the
server's tool list in the session before calling.

## Tool families this skill uses

| Step | Family | Notes |
| --- | --- | --- |
| Our profile top line | `backlinks_summary` | Backlinks, referring domains, dofollow and nofollow counts, referring IPs and subnets, new and lost counts; one call per target |
| Referring domains | `backlinks_referring_domains` | One row per domain with `rank`, `backlinks`, `first_seen`, `lost_date`; use `limit` and `order_by` rank descending; filter `dofollow` where asked |
| Anchors | `backlinks_anchors` | Anchor text with counts; classify locally (branded, exact commercial, partial, generic, naked URL, image) |
| Trend | `backlinks_timeseries_new_lost_summary` | Monthly new and lost backlinks and domains for the last six to twelve months |
| Recent losses | `backlinks_bulk_new_lost_referring_domains` | Last 30 days per target |
| The gap | `backlinks_domain_intersection` | Targets are the competitors; exclude our domain; returns domains linking to N of them |
| Rank and spam for a batch | `backlinks_bulk_ranks`, `backlinks_bulk_spam_score` | Up to 1,000 domains per call; run once on the prospect set |
| Who else competes for links | `backlinks_competitors` | Domains sharing referring domains with ours; a check on the competitor list from `strategy/competitive/` |

`backlinks_available_filters` lists the filterable fields when a query
needs narrowing.

## Column mapping

| Snapshot column | Source field |
| --- | --- |
| `target` | the domain the row describes (ours), or the competitors it links to for a gap row |
| `referring_domain` | `domain` |
| `domain_rank` | `rank` (0 to 1,000 scale) |
| `backlinks`, `dofollow` | `backlinks`, `backlinks_dofollow` or the boolean |
| `first_seen`, `last_seen` | `first_seen`, `last_seen` |
| `anchor` | most frequent `anchor` for the domain |
| `spam_score` | `backlinks_spam_score` from the bulk call |

## Cost

Backlink calls are billed per request, a few cents each, with a per-row
component on large `limit` values. A full profile plus a two-competitor
gap is under ten calls. State the count.

## Quirks

- `rank` is DataForSEO's own scale, not Moz DA or Ahrefs DR; never mix
  scales in one table.
- Subdomains count separately unless `include_subdomains` is set; say
  which you used.
- Intersection returns page-level and domain-level modes; this skill uses
  domain level.
