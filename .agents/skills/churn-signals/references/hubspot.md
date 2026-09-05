<!-- source: https://raw.githubusercontent.com/HubSpot/agent-cli-skills/main/customer-retention/SKILL.md | license: Apache-2.0 | fetched: 2026-09-04 -->

# HubSpot for churn-signals

The property names and inactivity filters below are condensed from the
source above (HubSpot's own retention guide for its CLI; the repository
ships no NOTICE file). The connection is the remote MCP server (`hubspot`
in `.mcp.json` once wired; catalog entry in `integrations/catalog/crm.json`);
the pull goes through `snapshot-pull`.

## Connection

- Remote MCP (`https://mcp.hubspot.com`, or the `/anthropic` path some
  clients need; confirm when wiring). OAuth at user level; the `manage_*`
  write tools are denied in `.claude/settings.json`. This skill reads only.
- Check the server's tool list in the session; expect a CRM object search
  with property filters, an object read with associations, and on some
  tiers a SQL-style query tool.

## Inactivity signals, as HubSpot filters

| Signal | Property and filter |
| --- | --- |
| no human contact in 60 days | `notes_last_contacted` older than 60 days (calls, notes, meetings) |
| no sales activity at all | `hs_last_sales_activity_date` stale (adds emails and tasks) |
| never contacted | `notes_last_contacted` empty |
| billing at risk | `hs_subscription_status = past_due` on the subscriptions object; `hs_recurring_billing_total` for the amount |
| opted out | `hs_email_optout = true` on the champion |
| no health score | HubSpot has no native one; the team tracks it in a custom property, ask which |

## Objects and fields for the snapshot

Companies with `lifecyclestage = customer`:

| Snapshot column | HubSpot property |
| --- | --- |
| `company`, `domain` | `name`, `domain` |
| `owner` | `hubspot_owner_id`, resolved |
| `arr_band` | the team's ARR property |
| `health` | the team's custom health property |
| `renewal_date` | custom property, or `closedate` of the open renewal deal |
| `last_contact` | `notes_last_contacted` |
| `last_activity` | `hs_last_sales_activity_date` |
| `subscription_status` | `hs_subscription_status` (subscriptions object) |
| `open_high_tickets` | count of tickets with `hs_ticket_priority = HIGH` and `hs_pipeline_stage` open, last 14 days |
| `champion_change` | associated contact with a senior title gone or changed |

Usage comes from `web-analytics`, not HubSpot, unless the team syncs usage
properties to companies.

## Snapshots

`data/crm/snapshots/YYYY-MM-DD-hubspot-customers.csv`,
`data/crm/snapshots/YYYY-MM-DD-hubspot-tickets.csv` and, when the team
uses HubSpot subscriptions,
`data/crm/snapshots/YYYY-MM-DD-hubspot-subscriptions.csv`.

## What the skill does not do here

The source creates follow-up tasks in HubSpot in bulk. This skill files
tasks per `integrations/tasks.md` instead, and never enrols anyone in a
sequence.

## Manual route

Companies > Export filtered to customers with the properties above,
dropped at `data/crm/snapshots/YYYY-MM-DD-hubspot-customers.csv`.
