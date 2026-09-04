# data/email/

Email and marketing-automation performance pulls (HubSpot, Customer.io, or
whatever sends the team's email). Fed by the `marketing-automation`
integration category (`integrations/catalog/marketing-automation.json`).
See `integrations/README.md`. Email performance used to be described under
`data/crm/`; it lives here now, and `data/crm/` keeps pipeline and contacts.

## Snapshots

`snapshots/YYYY-MM-DD-<source>-<what>.csv`, immutable, named per
`data/README.md`. Typical:

- `2026-08-31-hubspot-sends.csv`: sends, opens, clicks and unsubscribes by
  campaign
- `2026-08-31-customerio-sequences.csv`: per-step performance of the
  automated sequences

The `email-performance` skill writes here. `lifecycle-map` and `qmr` read.

## Rules

- Load `data/ontology/` first. A click or a reply counts toward a lifecycle
  stage only where `data/ontology/funnel.md` says so.
- The PII rule from `data/`: aggregate by send or sequence. Recipient-level
  rows only if this repo is private and the team logged that decision.
