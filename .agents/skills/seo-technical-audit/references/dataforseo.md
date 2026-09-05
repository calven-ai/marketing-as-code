# DataForSEO for seo-technical-audit

The `dataforseo` MCP server in `.mcp.json`. Names below are the tool
families as the server lists them at version 3.1.1; check the server's tool
list in the session before calling.

## Tool families this skill uses

| Step | Family | Notes |
| --- | --- | --- |
| Per-URL on-page fields | `on_page_instant_pages` | One URL per call; returns status code, canonical, meta robots, title, description, headings, word count, internal and external link counts, duplicate flags, `checks` (a map of pass/fail flags such as `canonical`, `no_title`, `is_https`) |
| Core Web Vitals and performance | `on_page_lighthouse` | One URL per call, mobile by default; read `audits` for LCP, INP or TBT, CLS, and the performance score; slow, so sample rather than crawl |
| Structured data and main content | `on_page_content_parsing` | Returns the parsed page with JSON-LD blocks; use it to list `@type`s |
| Which pages matter | `dataforseo_labs_google_ranked_keywords` for our domain, grouped by URL | Picks the sample by traffic; `dataforseo_labs_google_relevant_pages` lists pages by keyword count |

There is no full-site crawl over MCP in this pin; the on-page task-based
crawler is not exposed. For a whole-blog inbound-link map use the
`scraping-search` route or the manual crawl export.

## Column mapping

| Snapshot column | Source field |
| --- | --- |
| `url` | `items[].url` |
| `status` | `status_code` |
| `indexable` | not `meta.robots` noindex and `checks.canonical` |
| `canonical` | `meta.canonical` |
| `title`, `title_length` | `meta.title`, `meta.title_length` |
| `meta_description` | `meta.description` |
| `h1_count` | length of `meta.htags.h1` |
| `word_count` | `meta.content.plain_text_word_count` |
| `internal_links_in` | filled from the orphan map, not the vendor |
| `internal_links_out` | `meta.internal_links_count` |
| `lcp`, `inp`, `cls` | Lighthouse `audits.largest-contentful-paint`, `interaction-to-next-paint` (or `total-blocking-time` as proxy, say so), `cumulative-layout-shift` |
| `schema_types` | `@type` values from the JSON-LD blocks |

## Cost

Instant pages is billed per page (fractions of a cent); Lighthouse is
billed per run (about a cent). A 20-URL sample is roughly 40 calls and
well under a dollar. Say so in the report.

## Quirks

- Instant pages fetches the page live with a desktop user agent unless
  told otherwise; pass a mobile agent for a second pass if the site
  serves different HTML.
- Lighthouse numbers are lab values, not field data; label them as such.
- A page behind a login or a bot wall returns a status the audit must
  report as a gap, not as an error on the site.
