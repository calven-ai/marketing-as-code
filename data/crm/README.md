# data/crm/

Pipeline, signup and email-performance pulls from the CRM (HubSpot or
equivalent). See `integrations/README.md`.

## Snapshots

`snapshots/YYYY-MM-DD-<source>-<what>.csv`, immutable. Typical:

- `2026-08-31-hubspot-pipeline.csv`: deals by stage (stages defined in
  `data/ontology/funnel.md`)
- `2026-08-31-hubspot-new-contacts.csv`
- `2026-08-31-hubspot-email-performance.csv`
- `2026-09-15-hubspot-event-x-attendees.csv`: event attendee exports land
  here too

## Rules

- **The PII rule applies hardest here.** Company-level aggregates are safe.
  Individual names and emails only if this repo is private and the team
  logged that decision.
- Lifecycle-stage labels (MQL, SQL, and the rest) mean what
  `data/ontology/metrics.md` says they mean. If the ontology is unfilled,
  ask before analyzing.
