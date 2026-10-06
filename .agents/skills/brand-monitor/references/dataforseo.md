# DataForSEO for the brand monitor

The `ai-visibility` category wired to DataForSEO. Credentials are
`DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` in the environment or `.env`,
read only by scripts and the MCP server, never by you.

## The weekly collection: `scripts/aeo_track.py`

One live call per active prompt per engine, United States and English by
default (`--location`, `--language`). Costs per call as measured on
2026-09-29; `--estimate` multiplies them out, and each row records what
was actually billed in `cost_usd`.

| Engine | Endpoint | Model | About $ per call |
| --- | --- | --- | --- |
| `chatgpt` (default) | `ai_optimization/chat_gpt/llm_scraper/live/advanced`, what a logged-out user sees | the web UI's | 0.004 |
| `google_ai_mode` (default) | `serp/google/ai_mode/live/advanced` | AI Mode | 0.004 |
| `claude` (default) | `ai_optimization/claude/llm_responses/live`, `web_search: true` | `claude-haiku-4-5` | 0.025 |
| `perplexity` | `ai_optimization/perplexity/llm_responses/live` | `sonar` | 0.007 |
| `gemini` | `ai_optimization/gemini/llm_responses/live` | `gemini-3.5-flash` | 0.085 |
| `google_aio` | `serp/google/organic/live/advanced`, the AI Overview block | n/a | 0.004 |

The default three cost about $0.033 a prompt, so 30 prompts run about $1
and 120 about $4. The others are opt-in through `--engines`; Google AI
Overviews belong to keyword SERPs (`seo-analyst`), so add `google_aio`
only on purpose. A ChatGPT answer that is only a preamble is retried once
and both costs are counted. An answer under 500 characters with no
sources counts as unanswered and stays out of n.

## Snapshot columns

`*-aeo-results.csv`, one row per prompt and engine:
`prompt_id,engine,model,answered,mentioned,position,cited_self,cited_paths,cited_domains,brands,category_phrase,answer_chars,cost_usd,error,prompts_sha,brands_sha`.
`position` is our rank among tracked brands by first appearance (1 =
named first), empty when not named; `cited_paths` are our own site paths;
`cited_paths`, `cited_domains` and `brands` are `|`-separated; the two
hashes mark definition changes. `*-aeo-answers.csv` holds
`prompt_id,engine,text,sources,fan_out` (text cut at 8,000 characters,
up to 40 sources and 20 fan-out queries). Fan-out queries are prompt and
keyword candidates.

## Ad-hoc checks through the MCP server

The `dataforseo` server in `.mcp.json` (pinned `3.1.1`; its tool list is
authoritative when a name moves). Ten calls at most a run.

| Job | Tool |
| --- | --- |
| re-ask one prompt on one model | `ai_optimization_llm_response` (`model_name`, `web_search: true`); `ai_optimization_llm_models` lists models |
| the same on ChatGPT's web UI | `ai_optimization_chat_gpt_scraper` |
| where a brand is mentioned across LLM answers | `ai_opt_llm_ment_search`, `ai_opt_llm_ment_top_domains`, `ai_opt_llm_ment_top_pages` |
| mention counts over time | `ai_opt_llm_ment_agg_metrics`, `ai_opt_llm_ment_cross_agg_metrics` |
| how often a prompt is asked | `ai_optimization_keyword_data_search_volume` |

LLM response calls are billed per request plus the model's tokens;
mentions endpoints per request plus per row. Note each call and its cost
under Evidence.
