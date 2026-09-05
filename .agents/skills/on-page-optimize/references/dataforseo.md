# DataForSEO for on-page-optimize

The `dataforseo` MCP server in `.mcp.json`. Names are the tool families as
the server lists them at version 3.1.1; check the server's tool list in the
session before calling. The SERP and ranked-keyword pulls belong to
`seo-analyst`; this file says which of its pulls this skill asks for.

## Tool families this skill uses

| Step | Family | Notes |
| --- | --- | --- |
| Top 10 for the keyword | `serp_organic_live_advanced` | `depth: 10`, location and language from the ontology; read `items[]` of type organic for url, title, description, and the feature types present (people_also_ask, featured_snippet, ai_overview) |
| What the URL ranks for | `dataforseo_labs_google_ranked_keywords` with the page URL | Sort by volume times a CTR curve (`page-verdict.md`) to find the page's real primary keywords |
| Same-domain competition | `dataforseo_labs_google_ranked_keywords` for our domain, filtered to the target keyword | Any second URL of ours in the top 20 is cannibalisation |
| The page's current fields | `on_page_instant_pages` | Title, description, headings, word count, canonical, internal links; one call |
| Volume and difficulty for a new keyword | `dataforseo_labs_google_keyword_overview` | Only when the row is missing from `keywords.csv`; propose the row, do not insert it |

## Column mapping for the SERP snapshot

`data/seo/snapshots/YYYY-MM-DD-dataforseo-serp.csv` with columns
`keyword,position,url,title,type,features,checked`:

| Column | Source field |
| --- | --- |
| `position` | `rank_absolute` |
| `url`, `title` | `url`, `title` |
| `type` | your label from the title and URL: guide, template, comparison, product page, listicle |
| `features` | the non-organic `items[].type` values on that SERP, joined with `;` |

## Cost

A live SERP page costs a fraction of a cent; a Labs call a cent or two.
One page is two to four calls. Say so.

## Quirks

- The SERP tool returns the whole page of items, not only organic; filter
  by `type`.
- Ranked keywords for a URL is exact-match on the URL string; pass the
  canonical form.
