# HubSpot Marketing Hub: what to pull and how it maps

Vendor id `hubspot`, source token `hubspot` (from
`integrations/catalog/marketing-automation.json`). The official remote MCP
server (`hubspot` in `.mcp.json`, one entry serving the `crm` row too)
exposes read tools including `get_marketing_email_analytics`,
`get_content_analytics_report` and `get_campaign_attribution_reports`; the
`manage_*` tools write and stay denied for this skill. Check the server's
tool list in the session; the names above come from the catalog's
caveats and may have moved. Pull mechanics live with `snapshot-pull`.

## Sends

List the marketing emails sent in the month (the marketing email
listing, filtered by send date), then per email the statistics. Map:

| Snapshot column | HubSpot field | Note |
| --- | --- | --- |
| `send_id` | email id | |
| `send_name` | name | |
| `type` | `campaign`, `newsletter`, `automated` | from the email's subscription type or name; say which |
| `sent_at` | publish or send date | ISO date |
| `sent` | `counters.sent` | |
| `delivered` | `counters.delivered` | |
| `opens` | `counters.open` (unique) | inflated by prefetch |
| `unique_clicks` | `counters.click` (unique) | |
| `replies` | `counters.reply` | often 0 for marketing sends; note it |
| `unsubscribes` | `counters.unsubscribed` | |
| `hard_bounces`, `soft_bounces` | `counters.hardbounced`, `counters.softbounced` | |
| `spam_complaints` | `counters.spamreport` | |

Snapshot: `data/email/snapshots/YYYY-MM-DD-hubspot-sends.csv`.

## Sequences and workflows

Automated emails sent by workflows report the same counters per email;
add `sequence` (the workflow name) and `step` (the email's position).
Snapshot: `data/email/snapshots/YYYY-MM-DD-hubspot-sequences.csv` with
`sequence,step,send_name,sent,delivered,opens,unique_clicks,replies,unsubscribes,hard_bounces,soft_bounces,spam_complaints`.
Sales sequences (the Sales Hub feature) are per-rep and per-contact;
they belong to outbound reporting, not here, unless the team asks.

## Manual export

Marketing > Email > the email > Actions > Export, or Marketing > Email >
Analyze > Export for the period. Rename the columns to the snapshot
columns above and drop the file at the path above.

## Limits and quirks

- The API rate limit is per app and per account (bursts of 100 to 150
  requests per 10 seconds on most tiers); a monthly pull is well inside
  it.
- Statistics settle for about 72 hours after a send; pull the month a
  few days after it ends.
- The default attribution for a click to a lifecycle stage is HubSpot's
  own; `data/ontology/funnel.md` decides what counts here.
