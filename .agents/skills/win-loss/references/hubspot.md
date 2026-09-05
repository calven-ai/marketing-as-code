<!-- source: https://raw.githubusercontent.com/HubSpot/agent-cli-skills/main/sales-reporting/SKILL.md | license: Apache-2.0 | fetched: 2026-09-04 -->
<!-- NOTICE: the source repository carries no NOTICE file (checked 2026-09-04). -->

# HubSpot: closed deals for win/loss

What the win/loss skill needs from HubSpot, and where it lives. The pull
itself runs through `snapshot-pull`; this file says which objects and
fields to ask for and how they land in the snapshot. Check the server's
tool list in the session for the exact tool names; the catalog entry in
`integrations/catalog/crm.json` lists the write tools to keep denied.

## Objects and properties

Deals are the object. Properties to request:

| Property | Holds | Snapshot column |
| --- | --- | --- |
| `hs_object_id` | Deal id | `deal_id` |
| `dealname` | Deal name | (not exported; use the company) |
| associated company `name`, `domain` | The account | `company` |
| `amount` | Deal value, a numeric string | `amount` |
| `closedate` | Close date | `close_date` |
| `dealstage` and `pipeline` | Stage ids; map with the pipeline's stage list | (used to filter) |
| `hs_is_closed`, `hs_is_closed_won` | Strings `"true"` or `"false"` | `outcome` |
| `closed_lost_reason`, `closed_won_reason` | Free text or a picklist the team defined | `reason_crm` |
| `hubspot_owner_id` | Owner id; resolve through the owners list | `owner` |
| `hs_analytics_source` or the team's source property | Original source | `source` |
| a custom competitor property (often `competitor` or `primary_competitor`) | Named competitor | `competitor` |
| a custom segment or tier property, or the company's `numberofemployees` and `industry` | Segment | `segment`, `tier` |

Competitor and segment are not standard properties. Ask the team which
property carries them (`data/ontology/` should say); if none does, the
column stays empty and the report says the CRM does not record it.

## Filters

- Won: `hs_is_closed_won` equals `true`.
- Lost: `hs_is_closed` equals `true` and `hs_is_closed_won` is not `true`.
- Period: `closedate` between the period's start and end.

The source's CLI shape, for a script route: search deals with a filter
expression and a property list, list pipeline stages to map stage ids to
names, and list owners to resolve owner ids. Numeric properties come back
as strings and need converting before any sum.

## Quirks

- The HubSpot MCP is OAuth and user-scoped: it can read whatever the
  signed-in person can. It cannot run unattended.
- Paging: keep page sizes at 100 and say how many pages you fetched.
- `closed_lost_reason` is only as good as the team's discipline; the
  transcript coding in the win/loss skill exists because of that.
- Calls and notes live on engagements associated with the deal; the
  transcripts category is the better source for what buyers said.
