# DataForSEO AI Optimization for the brand monitor

The `ai-visibility` category wired to DataForSEO AI Optimization: the same
`dataforseo` MCP server the SEO analyst uses (`.mcp.json`, credentials
`DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` in the environment, never
read by you), through its AI optimization tools. Names below are the
server's as of `3.1.1`; the connected server's tool list is authoritative
when a name has moved.

## Tool families

| Job | Tool family | Notes |
| --- | --- | --- |
| which models are available | `ai_optimization_llm_models` | run once; pick the model ids the team tracks and keep them stable across reports |
| ask a model a prompt and read the answer with its citations | `ai_optimization_llm_response` (`prompt`, `model_name`, optional `web_search: true`) | one request per prompt per model; the answer text plus `citations` or `annotations` with URLs |
| the same for ChatGPT with live search | `ai_optimization_chat_gpt_scraper` (`ai_optimization_chat_gpt_scraper_locations` for the location list) | slower and dearer than the LLM response tool; use for the handful of prompts where the live product answer matters |
| where a brand is mentioned across LLM answers | `ai_optimization_llm_mentions_search` (`keywords` = the brand and its aliases; `ai_optimization_llm_mentions_filters` lists the filters) | one request per brand: ours and each competitor |
| which domains and pages the models cite for a topic | `ai_optimization_llm_mentions_top_domains`, `ai_optimization_llm_mentions_top_pages` | the "where do citations come from" tables |
| counts over time | `ai_optimization_llm_mentions_aggregated_metrics` and the cross-model variant | the trend line when the team wants one beyond the snapshot diffs |
| how often a prompt is asked | `ai_optimization_keyword_data_search_volume` | AI search volume for a prompt; useful when adding rows to `prompts.csv` |

Location and language, where a tool takes them, come from `data/ontology/`
or the person asking, the same rule as the SEO analyst.

## Cost

Each LLM response call is billed per request plus the model's own token
price; the ChatGPT scraper costs several times more per prompt. Mentions
search, top domains and top pages are billed per request plus per row.
A monthly run is therefore prompts x models LLM response calls plus one
mentions search per tracked brand; say the count and the rough total in
the report, and ask before running a prompt set that has grown past a
few dozen rows.

## Mapping to the snapshot columns

Snapshots keep `prompt,model,position,brand,domain,cited_url,we_are_cited`,
one row per cited brand per prompt per model.

| Column | From |
| --- | --- |
| `prompt` | the `prompts.csv` row, verbatim |
| `model` | the `model_name` sent |
| `position` | the order in which the brand appears in the answer text, 1 first |
| `brand` | the brand as named in the answer; ours and the `strategy/competitive/` names, everything else kept as written for the "unknown players" line |
| `domain` | the registrable domain of the citation, or of the brand when the answer names it without a link |
| `cited_url` | the citation URL when the answer carries one, else empty |
| `we_are_cited` | `true` or `false` for the prompt and model, repeated on every row of that pair |

A prompt with no answer or no brands gets one row with `brand` empty and
`we_are_cited` `false`, so the report can say "no answer returned" rather
than lose the prompt.
