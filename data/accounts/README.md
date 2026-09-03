# data/accounts/

Target-account intelligence for ABM: prospect lists, account research,
enrichment outputs.

## Canonical

- **`target-accounts.csv`** — the account list the team is actively working.
  Columns:

  ```csv
  company,domain,tier,owner,status,notes
  ```

## Snapshots

`snapshots/YYYY-MM-DD-<source>-<what>.csv`, immutable. Typical:

- `2026-08-31-apify-alumni.csv` — people who left the target accounts, one
  row per person, with the actor ID that found them (`researcher` skill)
- `2026-08-31-apify-linkedin-activity.csv` — scraped social activity for
  target accounts (`researcher` skill)
- `2026-08-31-enrichment-firmographics.csv`

## Rules

- Research individuals only in a B2B, account-context way, and keep personal
  data out of any public copy — same PII rule as the rest of `data/`. A
  snapshot with names or profile URLs belongs in a private repo only.
- Research is read-only: no agent contacts anyone it finds here.
