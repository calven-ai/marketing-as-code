# data/seo/

## Canonical

- **`keywords.csv`** — the single source of truth for every keyword this team
  tracks. Columns:

  ```csv
  keyword,intent,target_url,difficulty,volume,current_rank,last_checked,notes
  ```

  Add rows deliberately (a keyword here means "we care about ranking for
  this"); update `difficulty`, `volume`, `current_rank`, `last_checked` from
  fresh pulls.

## Snapshots

`snapshots/YYYY-MM-DD-<source>-<what>.csv`, immutable. Typical:

- `2026-08-31-dataforseo-rankings.csv` — rank check for every keyword in the
  canonical table
- `2026-08-31-dataforseo-keyword-ideas.csv` — research output, pending triage
  into `keywords.csv`

## For agents

- Weekly delta = diff the two most recent ranking snapshots (`weekly-seo`
  skill); write the analysis to `reports/recurring/seo/`, not here.
- Pulls go through DataForSEO — see `integrations/README.md`.
