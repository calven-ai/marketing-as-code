<!-- source: https://raw.githubusercontent.com/HubSpot/agent-cli-skills/main/audience-targeting/SKILL.md | license: Apache-2.0 | fetched: 2026-09-04 -->

# HubSpot: contacts, engagement and deals per target account

Wired through the HubSpot MCP server (`integrations/catalog/crm.json`).
Check the server's tool list in the session; expect object search with
property filters, association listing and an engagements read. Never call a
`manage_*` tool from this role. The property names below are condensed from
the source; verify them against the properties list once per session.

## Properties that carry the signal

| Group | Properties |
| --- | --- |
| lifecycle | `lifecyclestage`, `hs_lead_status`, `hubspot_owner_id` |
| engagement recency | `hs_email_last_open_date`, `hs_email_last_click_date`, `notes_last_contacted`, `hs_last_sales_activity_timestamp` |
| compliance | `hs_email_optout` (exclude `true` from any outreach list) |
| role | `jobtitle` (token match with `~`: `director`, `vp`, `chief`, `head`) |
| firmographic (company) | `domain`, `industry`, `numberofemployees`, `annualrevenue`, `country` |
| pipeline | `num_associated_deals` (0 is net new) |

The token-match operator matches whole words, not substrings. Filters
inside one group are AND; separate groups are OR, capped at 5 per call.

## Pull order

1. Companies by `domain` in the target list, chunks of 5 OR filters, to get
   company ids.
2. Contacts associated with each company (associations list, then one
   batch read), with the properties above.
3. Engagements (emails, meetings, calls, notes) for the last 90 days per
   company; page views only if the HubSpot tracking code is the team's
   analytics source, otherwise they come from `web-analytics`.
4. Open deals per company for the stage and the owner.

## Column mapping

`data/crm/snapshots/YYYY-MM-DD-hubspot-contacts.csv`:

```csv
domain,company,contact_id,role,seniority,lifecyclestage,last_email_click,last_meeting,last_reply,last_contacted,optout,owner,pulled_at
```

`role` is a label you derive from `jobtitle` against `strategy/personas.md`
(economic buyer, technical buyer, champion, procurement). Names and emails
only when `repo.private` in `docs/schema.json` is true; add `name,email`
columns then, never otherwise.

## Limits

Search returns 100 per page; batch reads take 100 ids. The route is OAuth,
so an unattended run needs the private-app script route in the catalog.
