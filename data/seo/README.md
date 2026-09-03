# data/seo/

## Canonical

- **`keywords.csv`**: the single source of truth for every keyword this team
  tracks. Columns:

  ```csv
  keyword,intent,target_url,difficulty,volume,current_rank,last_checked,notes
  ```

  Add rows deliberately (a keyword here means "we care about ranking for
  this"); update `difficulty`, `volume`, `current_rank`, `last_checked` from
  fresh pulls. The three rows it ships with are examples; replace them with
  yours. `scripts/seo_snapshot.py` refreshes volume and difficulty for every
  row and saves the pull as a snapshot.

- **`prompts.csv`**: the canonical prompt set for AI answer-engine (AEO)
  tracking: the questions a buyer types into ChatGPT or Perplexity for
  which we want to be cited. Columns:

  ```csv
  prompt,persona,stage,category,notes
  ```

  Never rewrite a prompt in place (history only compares if the wording is
  stable); retire one via `notes`. The `brand-monitor` skill runs it.

## Snapshots

`snapshots/YYYY-MM-DD-<source>-<what>.csv`, immutable. Typical:

- `2026-08-31-dataforseo-rankings.csv`: rank check for every keyword in the
  canonical table
- `2026-08-31-dataforseo-keyword-ideas.csv`: research output, pending triage
  into `keywords.csv`
- `2026-08-31-dataforseo-llm-mentions.csv`: one row per brand cited per
  prompt per model (`brand-monitor` skill)

## For agents

- Weekly delta = diff the two most recent ranking snapshots (`weekly-seo`
  skill); write the analysis to `reports/recurring/seo/`, not here.
- Pulls go through DataForSEO (see `integrations/README.md`). Keyword and
  rank pulls: `seo-analyst`; AI answer-engine mentions: `brand-monitor`.
