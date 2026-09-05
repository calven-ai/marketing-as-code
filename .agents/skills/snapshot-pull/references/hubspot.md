<!-- source: https://raw.githubusercontent.com/HubSpot/agent-cli-skills/main/bulk-operations/SKILL.md | license: Apache-2.0 | fetched: 2026-09-04 -->

# HubSpot (source token `hubspot`; categories `crm`, `marketing-automation`)

Routes (from `integrations/catalog/crm.json`): the remote MCP server
`hubspot` (OAuth, a person in a session), or a stdlib script with a
private-app token `HUBSPOT_ACCESS_TOKEN` for unattended pulls (copy
`scripts/seo_snapshot.py`). The `hs` CLI is developer tooling and exports
no CRM data. Deny `mcp__hubspot__manage_*`; this skill only reads.

## Calls per snapshot

Read tool names vary by server version: check the tool list in the session
(search or list objects, get pipelines, marketing email analytics). The
API behind them is CRM v3 search: `POST /crm/v3/objects/<object>/search`.

| `<what>` | Object and filter | Properties to request |
| --- | --- | --- |
| pipeline | deals, `hs_is_closed = false` | `dealname, dealstage, amount, closedate, createdate, hubspot_owner_id, hs_analytics_source, notes_last_updated, pipeline` |
| closed-deals | deals, `closedate` in period | same plus `hs_is_closed_won, closed_lost_reason, closed_won_reason` |
| new-contacts | contacts, `createdate` in period | `lifecyclestage, hs_analytics_source, hs_analytics_source_data_1, associatedcompanyid, hubspot_owner_id, createdate` |
| contacts, companies | all records | contacts: `email, firstname, lastname, lifecyclestage, hs_analytics_source, hubspot_owner_id, createdate, lastmodifieddate`; companies: `name, domain, industry, numberofemployees, lifecyclestage, hubspot_owner_id, createdate` |
| customers | companies, `lifecyclestage = customer` | `name, domain, hs_lastmodifieddate, industry, numberofemployees, hubspot_owner_id` |
| sends (email) | marketing email statistics | `name, publishDate, sent, delivered, open, click, unsubscribed, bounce` |

Resolve `dealstage` and `pipeline` ids to labels once through the
pipelines endpoint (`GET /crm/v3/pipelines/deals`) and owner ids through
`GET /crm/v3/owners`; write labels into the snapshot, ids in a spare
column only when a report needs them. `hs_is_closed` and
`hs_is_closed_won` come back as the strings `"true"` and `"false"`.

## Mapping to the snapshot columns

`deal_id` = record `id`; `company` = the associated company's `name`
(request associations, or pull companies and join on id); `source` =
`hs_analytics_source`; `last_activity` = `notes_last_updated`;
`stage` = the pipeline stage label; `owner` = the owner's name or email
(email only in a private repo).

## Limits and cost

- Search and list return at most 100 records per call; page with the
  `after` cursor to the end. A single page is never the whole table, and
  a count read from one page is wrong.
- Search returns at most 10,000 results per query; split a larger pull by
  `createdate` ranges.
- Private-app rate limits are per account (on the order of 100 requests
  per 10 seconds, with a daily allowance by tier); a 429 means wait and
  retry the same page.
- Batch read (`/batch/read`) takes up to 100 ids per call; never fetch
  records one id at a time.
- Cost: included in the subscription; the MCP server works on any tier.

## Export fallback

Deals: Sales > Deals > Export (CSV, all properties above). Contacts and
companies: Contacts > Export. Email: Marketing > Email > Analyze > Export.
Drop at `data/crm/snapshots/YYYY-MM-DD-hubspot-<what>.csv` (email at
`data/email/snapshots/YYYY-MM-DD-hubspot-sends.csv`) and rename the
columns to the snapshot set before a report reads it.
