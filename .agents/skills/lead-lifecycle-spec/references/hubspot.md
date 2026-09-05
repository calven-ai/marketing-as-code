# HubSpot: the backtest pull

Wired through the HubSpot MCP server (`integrations/catalog/crm.json`).
Read tools only; check the server's tool list in the session and verify
property names against the properties list once.

## What the backtest needs

| Purpose | Object and properties |
| --- | --- |
| last quarter's leads with outcomes | contacts: `createdate`, `lifecyclestage`, `hs_lifecyclestage_mql_date`, `hs_lifecyclestage_salesqualifiedlead_date`, `hs_lead_status`, `jobtitle`, `hubspot_owner_id`, plus the fit properties on the associated company (`industry`, `numberofemployees`, `annualrevenue`, `country`) |
| the engagement that preceded them | `hs_email_last_click_date`, `num_notes`, `hs_analytics_num_page_views`, `hs_analytics_num_visits`, form submissions and meeting engagements from the engagements read |
| won and lost deals with reasons | deals: `dealstage`, `amount`, `closedate`, `closed_lost_reason`, `hs_analytics_source`, associated contact and company |

Existing scores, if the team already has them: `hubspotscore` (the classic
score property) and any custom score properties.

## Snapshots

`data/crm/snapshots/YYYY-MM-DD-hubspot-contacts.csv`:
`contact_id,domain,role,created,mql_date,sql_date,lead_status,owner,
industry,headcount,revenue,country,clicks_90d,page_views,visits,meetings,
source,pulled_at`. Add `name,email` only when `repo.private` in
`docs/schema.json` is true.

`data/crm/snapshots/YYYY-MM-DD-hubspot-closed-lost.csv`:
`deal_id,domain,company,stage,amount,close_date,closed_lost_reason,source,
owner,pulled_at`; include won deals with `stage` set so the backtest has
both sides.

## Writing the model back

Not from this skill. When the team adopts the spec, a person builds the
score in HubSpot's scoring properties or workflows; note in the hand-over
that the MCP's `manage_*` tools are denied by default and stay so.
