# Customer.io: what to pull and how it maps

Vendor id `customerio`, source token `customerio` (from
`integrations/catalog/marketing-automation.json`). The official remote MCP
server (`customerio` in `.mcp.json`; EU workspaces use the `mcp-eu` host)
covers campaigns, campaign performance, segments and broadcasts. Write
tools exist since spring 2026 and stay denied for this skill; check the
server's tool list in the session for the read tools' exact names. Pull
mechanics live with `snapshot-pull`.

## Vocabulary

Customer.io calls an automated sequence a **campaign** (triggered by an
event, a segment or a date), a one-off send a **broadcast**, and each
email inside either an **action**. Newsletters are broadcasts. Map:

| This repo | Customer.io |
| --- | --- |
| a send | a broadcast, or one action's delivery in a campaign |
| a sequence | a campaign |
| a step | an action (email) inside a campaign, in workflow order |

## Sends (broadcasts)

List broadcasts in the month, then metrics per broadcast:

| Snapshot column | Customer.io metric | Note |
| --- | --- | --- |
| `send_id`, `send_name` | broadcast id, name | |
| `type` | `newsletter` or `campaign` | |
| `sent_at` | triggered date | |
| `sent` | `sent` | |
| `delivered` | `delivered` | |
| `opens` | `opened` (unique) | inflated by prefetch |
| `unique_clicks` | `clicked` (unique) | |
| `replies` | not tracked natively | leave blank, say so |
| `unsubscribes` | `unsubscribed` | |
| `hard_bounces`, `soft_bounces` | `bounced` | one number; put it in `hard_bounces`, note it |
| `spam_complaints` | `spammed` | |

Snapshot: `data/email/snapshots/YYYY-MM-DD-customerio-sends.csv`.

## Sequences (campaigns)

Per campaign, the metrics of each email action for the period, in
workflow order, into
`data/email/snapshots/YYYY-MM-DD-customerio-sequences.csv` with
`sequence,step,send_name,sent,delivered,opens,unique_clicks,replies,unsubscribes,hard_bounces,soft_bounces,spam_complaints`.
Conversions (a campaign goal met) exist per campaign; record them only
if the goal matches an event in `data/ontology/events.md`.

## Manual export

Campaigns > the campaign > Overview > Export, or Broadcasts > the
broadcast > Export, per period. Rename columns as above.

## Limits and quirks

- The App API (the one metrics come from) allows about 10 requests a
  second; the Track API is a different key and is never needed here.
- Metrics can be pulled by period (`day`, `week`, `month`); ask for the
  calendar month to match the report.
- Deliveries to suppressed or unsubscribed people show as `suppressed`,
  not bounces; do not add them to bounces.
