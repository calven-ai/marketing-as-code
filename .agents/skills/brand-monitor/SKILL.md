---
name: brand-monitor
description: Track how AI answer engines and LLMs mention us and our competitors, using the DataForSEO MCP's AI optimization and LLM mentions tools against the prompt set in data/seo/prompts.csv. Use when asked "are we cited by ChatGPT", "who gets recommended for X", "run the AEO check", or for the recurring mentions report.
---

# Brand monitor

Answer engines (ChatGPT, Perplexity, Google's AI answers) recommend
vendors by name. This skill checks, for a fixed set of prompts, who gets
cited and whether we are among them, and keeps the history so the trend is
visible.

Needs: the DataForSEO MCP server (`dataforseo` in `.mcp.json`, credentials
`DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` in `.env`, which you never
read yourself), specifically its AI optimization tools: LLM mentions
search, top domains and top pages, and the LLM response / ChatGPT scraper
tools. Without it, say so and stop; there is no manual export for this.

Run it by hand on the cadence the team picks (monthly is plenty; answer
engines vary run to run), or as an agent in GitHub Actions on a schedule
if the team has opted into that mode (`docs/operating-model.md`); the
DataForSEO server is key-based, so it works headless.

## The prompt set

`data/seo/prompts.csv` is canonical. Columns:

```csv
prompt,persona,stage,category,notes
```

Each row is a question a buyer would actually type into an AI assistant.
Add rows deliberately (in a PR with a one-line reason); never rewrite a
prompt in place, because history only compares if the prompt stays the
same. Retire a prompt by noting it in `notes`, not by deleting the row.

## Procedure

1. **Load `strategy/positioning.md`** (our name, category, the competitors
   we care about) and `strategy/competitive/` for the competitor list.
2. **Run the prompt set.** For each prompt in `prompts.csv`, ask the LLM
   response tool for the model(s) the team tracks (ask which, or use what
   the last report used) and record the brands and domains cited. Use the
   LLM mentions search, top domains, and top pages tools for our brand and
   each competitor to see where mentions come from.
3. **Save the snapshot** before analysing:
   `data/seo/snapshots/YYYY-MM-DD-dataforseo-llm-mentions.csv` with stable
   columns `prompt,model,position,brand,domain,cited_url,we_are_cited`.
   One row per cited brand per prompt per model. Never edit an old
   snapshot.
4. **Write the report** to `reports/recurring/mentions/YYYY-MM-DD.md` from
   `reports/_templates/report.md`:
   - Answer: for how many prompts we are cited, by which model, and who
     leads overall.
   - Evidence: a table, one row per prompt, columns per model, cell = the
     brands cited in order, ours in bold. A second table: competitor, count
     of prompts cited, delta vs the previous report.
   - Caveats: answer engines vary run to run; one snapshot is a sample, the
     trend across snapshots is the signal.
   - Data used: the snapshot path(s).
5. **Suggest, do not decide.** End with the prompts where a competitor is
   cited and we are not, and which existing `content/` piece (grep by
   `channel` and `status`) or new piece could earn the citation. The human
   picks.

## Worked example

Prompt "What is the best tool for running a marketing team from a Git
repository?", run against two models: model A cites competitor X, Y, and
us in third place; model B cites X and Z, not us. Snapshot rows: five
lines. Report: cited by 1 of 2 models for this prompt; X leads (2 of 2);
gap on model B; suggested piece: the published guide in
`content/2026-08-marketing-as-code-guide/`, if it exists, should mention
the category term explicitly.

## Rules

- Never invent a citation. If a tool returns nothing for a prompt, the
  cell says "no answer returned".
- Report the number of tool calls and their approximate cost.
- Competitor names in the report come from `strategy/competitive/`; a new
  name you see in answers goes into an "unknown players" line, not into the
  competitor list.
