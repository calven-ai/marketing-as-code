# DataForSEO for keyword-cluster

The `dataforseo` MCP server in `.mcp.json` (pinned package, see
`integrations/README.md`). Tool names below are the families as the server
lists them at version 3.1.1; check the server's tool list in the session
before calling, and read `references/dataforseo.md` in `seo-analyst`, which
owns the pulls this skill reuses.

## Tool families this skill uses

| Step | Family | Notes |
| --- | --- | --- |
| Expand seeds | `dataforseo_labs_google_keyword_ideas`, `dataforseo_labs_google_keyword_suggestions`, `dataforseo_labs_google_related_keywords` | One call per seed per family; `limit` caps rows; pass `location_name` and `language_code` from the ontology |
| Volume and difficulty for the survivors | `dataforseo_labs_google_keyword_overview`, `dataforseo_labs_bulk_keyword_difficulty` | Up to 700 keywords per call for overview; bulk difficulty is cheaper when you only need KD |
| Intent | `dataforseo_labs_search_intent` | Returns a label and probability per keyword; keep the label, note low probabilities in the report |
| SERP top 10 | `serp_organic_live_advanced` | One call per keyword, `depth: 10`; the overlap pass is the cost driver, state the count first |
| Which of our pages ranks already | `dataforseo_labs_google_ranked_keywords` for our domain | Fills `target_url` for existing pages |

Location codes come from `serp_locations`; language from the ontology or
the human, never a default you picked.

## Column mapping

| Snapshot column | Source field |
| --- | --- |
| `keyword` | `keyword` |
| `volume` | `keyword_info.search_volume` |
| `difficulty` | `keyword_properties.keyword_difficulty` |
| `intent` | `search_intent_info.main_intent`, else the word signals |
| `serp_urls` (working file, not the snapshot) | `items[].url` from the SERP call, top 10 organic only |
| `target_url` | `ranked_serp_element.serp_item.url` for our domain, or the proposed path |

## Cost

Labs calls are billed per request (roughly a cent or two each for up to
1,000 rows); live SERP calls are billed per page. A 40-keyword cluster run
is about 45 calls. Report the count and the approximate spend in the
report's Caveats section.

## Quirks

- Keyword ideas returns rows for the whole category, including brands we
  do not own; drop branded terms before clustering.
- The server returns JSON, not CSV; write the snapshot yourself with a
  header row and stable columns.
- Volumes are monthly averages over twelve months; a seasonal term looks
  smaller than it is in season.
