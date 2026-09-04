# HubSpot for advocacy-program

What this skill reads from the HubSpot remote MCP server (`hubspot` in
`.mcp.json` once wired; catalog entry in `integrations/catalog/crm.json`).
The pull itself goes through `snapshot-pull`; this file says which objects
and fields to ask for.

## Connection

- Remote MCP (`https://mcp.hubspot.com`, or the `/anthropic` path some
  clients need; confirm on the day it is wired). OAuth at user level, so
  the server can do whatever the signed-in user can: the `manage_*` write
  tools are denied in `.claude/settings.json`. This skill only reads.
- Works on every HubSpot tier. Custom Sensitive Data properties are not
  exposed.

## Objects and fields

Check the server's tool list in the session; expect a CRM object search
and a CRM object read, plus a SQL-style query tool on some tiers.

Companies, filtered to `lifecyclestage = customer`:

| Snapshot column | HubSpot property |
| --- | --- |
| `company` | `name` |
| `domain` | `domain` |
| `industry` | `industry` |
| `size` | `numberofemployees` |
| `owner` | `hubspot_owner_id` (resolve to a name) |
| `customer_since` | `closedate` of the first won deal, or `hs_lastmodifieddate` of the stage change |
| `arr_band` | `annualrevenue`, or the custom ARR property the team uses |
| `health` | a custom property (HubSpot has no native health score); ask the team which |
| `nps` | a custom property, or join from `data/reviews/snapshots/` by domain |
| `renewal_date` | a custom property, or the close date of the open renewal deal |
| `escalation` | open tickets with high priority, from the tickets object |

Contacts are read only to find the champion for the ask (`jobtitle`,
`hs_email_optout`); their names stay out of any public copy.

## Snapshot

`data/crm/snapshots/YYYY-MM-DD-hubspot-customers.csv`, one row per
company, the columns above. Rows without a health value keep the column
empty; the skill reports them as a gap.

## Manual route

Contacts or Companies > Export, filtered to customers, with the columns
above, dropped at `data/crm/snapshots/YYYY-MM-DD-hubspot-customers.csv`.
