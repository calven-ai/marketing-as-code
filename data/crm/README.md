# data/crm/

Pipeline, signup, contact and company pulls from the CRM (HubSpot or
equivalent). See `integrations/README.md`. Email performance lives in
`data/email/`, event attendee lists in `data/events/`.

## Snapshots

`snapshots/YYYY-MM-DD-<source>-<what>.csv`, immutable. Typical:

- `2026-08-31-hubspot-pipeline.csv`: deals by stage (stages defined in
  `data/ontology/funnel.md`)
- `2026-08-31-hubspot-new-contacts.csv`
- `2026-08-31-hubspot-closed-deals.csv`: won and lost, with close reason
- `2026-08-31-hubspot-customers.csv`: the customer base, one row per
  account
- `2026-08-31-hubspot-contacts.csv` and `2026-08-31-hubspot-companies.csv`:
  full exports the `data-hygiene-audit` skill reads

## Rules

- **The PII rule applies hardest here.** Company-level aggregates are safe.
  Individual names and emails only if this repo is private and the team
  logged that decision.
- Lifecycle-stage labels (MQL, SQL, and the rest) mean what
  `data/ontology/metrics.md` says they mean. If the ontology is unfilled,
  ask before analyzing.
