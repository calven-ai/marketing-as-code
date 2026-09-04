# DataForSEO for ai-share-of-voice

The `dataforseo` MCP server in `.mcp.json`, AI Optimization and LLM
Mentions families. Names are the tool families as the server lists them at
version 3.1.1; check the server's tool list in the session before calling.
The per-prompt runs belong to `brand-monitor`; this skill adds the
aggregate view.

## Tool families this skill uses

| Step | Family | Notes |
| --- | --- | --- |
| Mentions per brand for a keyword set | `ai_opt_llm_ment_agg_metrics` | Filters by keyword or brand, model and date range; returns counts and shares per period |
| Several brands side by side | `ai_opt_llm_ment_cross_agg_metrics` | Ours plus each competitor in one call; the heatmap source |
| Which domains and pages get cited for the category | `ai_opt_llm_ment_top_domains`, `ai_opt_llm_ment_top_pages` | The "who owns what" evidence, and the pages to study in `aeo-page-optimize` |
| Raw mention rows | `ai_opt_llm_ment_search` | For validating a brand match by reading the sentence |
| Filters and models | `ai_optimization_llm_mentions_filters`, `ai_optimization_llm_models`, `ai_opt_llm_ment_loc_and_lang` | Read once per session; keep the model list identical to the previous report |

## Column mapping

`data/seo/snapshots/YYYY-MM-DD-dataforseo-llm-mentions-agg.csv`:

| Column | Source field |
| --- | --- |
| `brand` | the brand or domain you passed |
| `model` | `llm_model` or `platform` in the response |
| `period` | the date bucket returned (month) |
| `mentions` | `mentions_count` or the count field the tool returns |
| `share` | computed here: brand mentions over the sum across the brands in the call |
| `checked` | today's date |

The per-prompt snapshot keeps `brand-monitor`'s columns:
`prompt,model,position,brand,domain,cited_url,we_are_cited`.

## Cost

Mentions and aggregate calls are billed per request, a few cents each; a
run is two to five calls. The expensive part is `brand-monitor`'s prompt
runs, which use the LLM response tools; count them in the report.

## Quirks

- The mentions index is DataForSEO's sample of answers, not the whole of
  ChatGPT; shares are relative within that sample, which is why the
  trend matters more than the level.
- Brand matching is by string; check `ai_opt_llm_ment_search` rows for a
  short or common brand name.
- Models and locations are enumerated; a model the vendor retires breaks
  the history for that column, so note it in the caveats.
