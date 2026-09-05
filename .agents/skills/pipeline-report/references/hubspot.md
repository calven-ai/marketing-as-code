<!-- source: https://raw.githubusercontent.com/HubSpot/agent-cli-skills/main/sales-reporting/SKILL.md | license: Apache-2.0 | fetched: 2026-09-04 -->

# HubSpot fields for the pipeline report

The pull itself is `snapshot-pull` (`.agents/skills/snapshot-pull/references/hubspot.md`
has the calls, paging and limits). This file says which deal properties
the report computes from and how HubSpot's stage model maps onto
`data/ontology/funnel.md`.

## Deal properties

| Report needs | Property | Notes |
| --- | --- | --- |
| stage | `dealstage` (id) + `pipeline` | resolve ids to labels through the pipelines endpoint once per run; a portal can have several pipelines, report each or say which one |
| amount | `amount` | string in the API; empty means unvalued, count it and say so |
| close date | `closedate` | overdue when before today on an open deal |
| created | `createdate` | pipeline created this period = `createdate` in the period |
| open or closed | `hs_is_closed`, `hs_is_closed_won` | strings `"true"` / `"false"`; lost = closed and not won |
| owner | `hubspot_owner_id` | resolve through owners once |
| source | `hs_analytics_source` (+ `_data_1`, `_data_2`) | HubSpot's original source; marketing-sourced is decided by `data/ontology/naming.md`, not by the label alone |
| last activity | `notes_last_updated` or `hs_lastmodifieddate` | stale = no activity past the stage threshold |
| stage entry dates | `hs_date_entered_<stageid>` | one property per stage; the basis for days per stage and velocity |
| close reason | `closed_lost_reason`, `closed_won_reason` | free text in many portals |

## Stage model

Stage probabilities live on the pipeline stage (`metadata.probability`
in the pipelines response). Use them only if `data/ontology/funnel.md`
says the team has calibrated them; otherwise compute stage-to-close from
`closed-deals` and treat the portal's defaults as unverified.

## Filters the report uses

- Open pipeline: `hs_is_closed = false`.
- Closed in period: `hs_is_closed = true` and `closedate` in range.
- Won: `hs_is_closed_won = true`; win rate = won / (won + lost) over
  the same range.
- Revenue by close month: sum of `amount` for won deals grouped by the
  month of `closedate`.
- Closing in the next 7 days: open deals with `closedate` inside the
  window, the list a manager asks for first.

Search and list calls cap at 100 rows; a count from one page is wrong.
Marketing-influenced pipeline needs the campaign attribution read tool or
the contact's `hs_analytics_*` touches joined by association; when the
portal has neither, report it as a gap rather than an estimate.
