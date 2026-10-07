# DataForSEO for aeo-page-optimize

The `dataforseo` MCP server in `.mcp.json`, AI Optimization family. Names
are the tool families as the server lists them at version 3.1.1; check the
server's tool list in the session before calling. `brand-monitor` owns the
prompt runs; this skill asks it for two views.

## Tool families this skill uses

| Step | Family | Notes |
| --- | --- | --- |
| Who is cited for a prompt right now | `ai_optimization_llm_response` (or `ai_optimization_chat_gpt_scraper` for ChatGPT with web search) | One call per prompt per model; the most expensive family, so only for the two to five prompts this page targets, and only when the weekly snapshot is stale |
| Which pages the engines pull from for a topic | `ai_opt_llm_ment_top_pages`, `ai_opt_llm_ment_top_domains` | Keyword or brand scoped; shows the competing pages whose structure to read |
| How often a brand is mentioned for a keyword set | `ai_opt_llm_ment_search`, `ai_opt_llm_ment_agg_metrics` | The before-and-after check a month after publishing |
| Which models exist | `ai_optimization_llm_models` | Use the models the last report used, for comparable history |
| Search demand inside AI assistants | `ai_optimization_keyword_data_search_volume` | AI-search volume for the prompt's keywords, when prioritising which prompt to write for |

## What to record

Nothing new: snapshots are immutable and a re-ask is evidence for the
report, not a snapshot row. The weekly `*-aeo-results.csv` from
`scripts/aeo_track.py` gives `mentioned`, `cited_paths` and
`cited_domains` per prompt and engine; the `*-aeo-answers.csv` beside it
gives the answer text and every source URL, the pages to study.

## Cost

LLM response calls are billed per model call and cost more than any Labs
call; the mentions tools are billed per request. Five prompts on two
models is ten expensive calls; say so before running and prefer the
weekly snapshot when it is under two weeks old.

## Quirks

- Answers vary run to run; one call is a sample, the weekly history is
  the signal.
- The response tools return the answer text and the cited sources;
  brand mentions without a link need matching by name, and a name can be
  a false match (a word, a person).
