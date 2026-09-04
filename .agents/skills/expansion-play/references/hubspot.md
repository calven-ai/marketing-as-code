# HubSpot for expansion-play

What this skill reads from the HubSpot remote MCP server (`hubspot` in
`.mcp.json` once wired; catalog entry in `integrations/catalog/crm.json`).
The pull goes through `snapshot-pull`; this file names the objects and
fields.

## Connection

- Remote MCP (`https://mcp.hubspot.com`, or the `/anthropic` path some
  clients need; confirm when wiring). OAuth at user level; the `manage_*`
  write tools are denied in `.claude/settings.json`. This skill only reads.
- Check the server's tool list in the session; expect a CRM object
  search, an object read with associations, and on some tiers a SQL-style
  query tool that joins companies to deals in one call.

## Objects and fields

Companies with `lifecyclestage = customer`:

| Snapshot column | HubSpot property |
| --- | --- |
| `company`, `domain` | `name`, `domain` |
| `owner` | `hubspot_owner_id`, resolved to a name |
| `arr_band` | the team's ARR property (custom), else `annualrevenue` |
| `plan`, `seats_bought` | custom properties, or from the subscriptions object (`hs_recurring_billing_total`, `hs_subscription_status`) |
| `health` | the team's custom health property; HubSpot has none natively |
| `renewal_date` | custom property, or `closedate` of the open renewal deal |
| `customer_since` | first won deal's `closedate` |
| `contacts_engaged` | count of associated contacts with activity in 90 days (`hs_last_sales_activity_date`) |
| `champion_change` | a contact whose `jobtitle` changed, or a new contact with a senior title |

Deals, to exclude accounts already in play: open deals with the team's
expansion pipeline or deal type (`dealtype = existingbusiness` in the
default setup), `dealstage`, `amount`, `closedate`.

Usage comes from `web-analytics`, not from HubSpot, unless the team syncs
usage properties to companies; ask which properties before reading them.

## Snapshots

`data/crm/snapshots/YYYY-MM-DD-hubspot-customers.csv` and
`data/crm/snapshots/YYYY-MM-DD-hubspot-pipeline.csv` (the same shape the
pipeline report uses, so one pull serves both).

## Manual route

Companies > Export filtered to customers, and Deals > Export filtered to
open expansion deals, dropped under `data/crm/snapshots/` with the names
above.
