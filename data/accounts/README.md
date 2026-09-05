# data/accounts/

Target-account intelligence for ABM: prospect lists, account research,
enrichment outputs.

## Canonical

- **`target-accounts.csv`**: the account list the team is actively working.
  Columns:

  ```csv
  company,domain,tier,owner,status,notes
  ```

  `tier` is 1, 2 or 3 as defined under Segment Tiers in
  [`strategy/icp.md`](../../strategy/icp.md). `status` is one of prospect,
  engaged, customer or lost. The two rows it ships with are examples;
  replace them with yours.

## Snapshots

`snapshots/YYYY-MM-DD-<source>-<what>.csv`, immutable. Typical:

- `2026-08-31-apify-alumni.csv`: people who left the target accounts, one
  row per person, with the actor ID that found them (`researcher` skill)
- `2026-08-31-apify-linkedin-activity.csv`: scraped social activity for
  target accounts (`researcher` skill)
- `2026-08-31-apollo-firmographics.csv`: enrichment output, named after
  the vendor that produced it
- `2026-08-31-repo-engagement.csv`: engagement per target account, computed
  in-repo from the other domains (`account-signals` skill)
- `2026-08-31-repo-partner-candidates.csv`: accounts that look like partners
  rather than buyers, computed in-repo
- `2026-08-31-web-competitor-changes.csv`: what changed on competitor
  websites since the last pull (`competitor-watch` skill)

## Rules

- Research individuals only in a B2B, account-context way, and keep personal
  data out of any public copy (the PII rule from `data/`). A snapshot with
  names or profile URLs belongs in a private repo only.
- Research is read-only. No agent contacts anyone it finds here.
