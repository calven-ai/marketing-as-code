# DataForSEO for the SEO analyst

The `seo-data` category wired to DataForSEO: the `dataforseo` MCP server
(`dataforseo-mcp-server`, pinned in `.mcp.json`) with `DATAFORSEO_LOGIN`
and `DATAFORSEO_PASSWORD` in the environment, never read by you. The
weekly pulls do not go through the MCP at all: `scripts/seo_snapshot.py`
writes `data/seo/snapshots/YYYY-MM-DD-dataforseo-volume.csv` and
`scripts/seo_rank_track.py` writes the `-serp` and `-serp-results`
snapshots from the same API.

Tool names below are the server's names as of `3.1.1`; the connected
server's tool list is authoritative when a name has moved. Most tools take
`keywords` (a list) or `keyword` (one), `target` (a domain, no scheme),
`location_name` and `language_code`, and a `limit`.

## Tool families, by question

| Question | Tool family | Notes |
| --- | --- | --- |
| volumes and difficulty for the keyword list | `dataforseo_labs_google_keyword_overview`; `keywords_data_google_ads_search_volume` for Google Ads volumes; `dataforseo_labs_bulk_keyword_difficulty` for difficulty alone | up to 700 keywords per Labs request, 1,000 for Google Ads |
| our current ranks | `dataforseo_labs_google_ranked_keywords` with `target` = our domain | one request per domain; filter to the `keywords.csv` set afterwards |
| a live check for one keyword between runs | `serp_organic_live_advanced`, one keyword per request | the tracker uses depth 30 with `load_async_ai_overview`; find our domain in `items` |
| who owns the SERPs for a keyword set | `dataforseo_labs_google_serp_competitors` with the `keywords` list | returns domains ranked by visibility across the set |
| ideas when asked to expand | `dataforseo_labs_google_keyword_ideas` (category-level), `dataforseo_labs_google_keyword_suggestions` (contains the seed), `dataforseo_labs_google_related_keywords` | keep `limit` to what the report will show |
| history for a keyword | `dataforseo_labs_google_historical_keyword_data` | monthly volumes back several years |

## Location and language

Every request carries one `location_name` (`"United States"`, `"United
Kingdom"`, `"Germany"`) and one `language_code` (`en`, `de`). They come
from `data/ontology/` or the person asking, never from a default you
picked; mixing them across a snapshot makes the deltas meaningless.
`serp_locations` resolves a place to its exact name when unsure.

## Cost

DataForSEO bills per request and, for Labs tools, per returned row:
roughly a cent per Labs request plus a fraction of a cent per row, a few
tenths of a cent per live SERP page (the tracker estimates $0.0075 per
keyword at depth 30 with the AI Overview), and a few cents per Google Ads
search volume batch. A weekly rankings check for one domain is one Labs
request; a keyword-ideas pull with `limit: 100` is one request and a
hundred rows. State the count and the rough total in every report; the
account balance is visible at app.dataforseo.com.

## Mapping to the snapshot columns

Snapshots keep `keyword,volume,difficulty,rank,url,checked`.

| Column | From |
| --- | --- |
| `keyword` | `keyword` (the request's keyword, spelled as in `keywords.csv`) |
| `volume` | `keyword_info.search_volume` (Labs) or `search_volume` (Google Ads) |
| `difficulty` | `keyword_properties.keyword_difficulty` (Labs) or the bulk difficulty tool's `keyword_difficulty` |
| `rank` | `ranked_serp_element.serp_item.rank_group` (ranked keywords) or the `rank_group` of our domain's item in a live SERP; empty when we do not rank |
| `url` | the same item's `url`; empty when we do not rank |
| `checked` | the pull date, `YYYY-MM-DD` |

The tracker's `-serp` snapshot reads the live SERP directly: `rank` and
`url` from our best `organic` item's `rank_group`, `aio` from an
`ai_overview` item, `aio_cited` and `aio_cited_paths` from its
`references`, `paa` from `people_also_ask`, `top10_domains` and
`top10_brands` (labelled by the brands table, data/seo/brands.csv, when it exists) from the organic items
ranked 1 to 10. `-serp-results` keeps one row per organic result, AI
Overview reference, People Also Ask question and related search
(`keyword_id,kind,position,domain,url,title,brand,checked`).

Snapshot names by pull: `-volume` (the script), `-serp` and
`-serp-results` (the tracker), `-rankings`,
`-keyword-overview`, `-serp-competitors` (columns `keyword,domain,rank,url,checked`),
`-keyword-ideas`.
