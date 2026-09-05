# Customer.io (source token `customerio`; category `marketing-automation`)

Routes (from `integrations/catalog/marketing-automation.json`): the remote
MCP server `customerio` (OAuth after an admin enables MCP in Workspace
Settings; `mcp-eu.customer.io` for EU workspaces), or a stdlib script with
an App API key `CUSTOMERIO_APP_API_KEY` for unattended pulls (copy
`scripts/seo_snapshot.py`). The server can write (campaigns, segments,
broadcasts) and its write tool names are not verified: deny the whole
server's writes and only read here. No CLI.

## Calls per snapshot

Tool names are not verified in the catalog; check the tool list in the
session (list campaigns, campaign metrics, broadcasts, segments). The App
API behind them:

| `<what>` | Endpoint |
| --- | --- |
| sends | `GET /v1/broadcasts` for the list, then `GET /v1/broadcasts/<id>/metrics?period=days&steps=<n>` per broadcast in the period; newsletters are broadcasts |
| sequences | `GET /v1/campaigns` for the list, `GET /v1/campaigns/<id>/actions` for the steps, `GET /v1/campaigns/<id>/actions/<action_id>/metrics` per step |
| campaigns (summary) | `GET /v1/campaigns/<id>/metrics?period=days&steps=<n>` for one row per campaign |

Metrics come back as arrays per period step; sum them across the period
the snapshot covers and record the period in the report.

## Mapping to the snapshot columns

`campaign` = the broadcast or campaign name; `send_date` = the broadcast's
`sent_at` (for a campaign row, the period end); `sends` = `sent`;
`delivered` = `delivered`; `opens` = `opened`; `clicks` = `clicked`;
`unsubscribes` = `unsubscribed`; `bounces` = `bounced`; `conversions` =
`converted` where the campaign has a goal. Aggregates only, never
recipient-level rows.

## Limits and cost

- The App API allows on the order of 10 requests per second per key; a
  workspace with 40 campaigns costs about 40 metric calls for `sequences`.
- Metrics are computed per workspace, so a team with several workspaces
  pulls one snapshot per workspace and names it `<what>-<workspace>`.
- Cost: included in the plan.

## Export fallback

Campaigns or Broadcasts > the campaign > Metrics > Export, or Reporting >
Deliverability > Export (CSV), per period. Drop at
`data/email/snapshots/YYYY-MM-DD-customerio-<what>.csv` and rename the
columns to the snapshot set.
