<!-- source: https://raw.githubusercontent.com/HubSpot/agent-cli-skills/main/crm-data-quality/SKILL.md | license: Apache-2.0 | fetched: 2026-09-04 -->

# HubSpot fields and checks for the hygiene audit

The pull itself is `snapshot-pull` (`.agents/skills/snapshot-pull/references/hubspot.md`
has the calls and limits). This file names the properties each check
reads and the filters that find the records.

## Properties to request

- Contacts: `email, firstname, lastname, lifecyclestage, hs_lead_status,
  hs_analytics_source, hubspot_owner_id, associatedcompanyid, createdate,
  lastmodifieddate, notes_last_updated`.
- Companies: `name, domain, industry, numberofemployees, lifecyclestage,
  hubspot_owner_id, createdate, num_associated_contacts`.
- Deals: `dealname, dealstage, pipeline, amount, closedate,
  hubspot_owner_id, notes_last_updated`, plus associations to contacts
  and companies.

## Checks and how to find the records

| Check | Filter or method |
| --- | --- |
| missing field | search with the not-has-property operator (`NOT_HAS_PROPERTY`) per required field: `email`, `hubspot_owner_id`, `associatedcompanyid`, `lifecyclestage`; deals `amount`, `closedate` |
| duplicate contacts | pull every contact first, then group by lowercased `email`; grouping one search page misses every pair that crosses a page boundary |
| duplicate companies | group by `domain` (strip `www.` and the scheme); fuzzy pairs by normalised `name` for review |
| lifecycle | `lifecyclestage` values outside `data/ontology/funnel.md`; `customer` with no won deal association; `marketingqualifiedlead` with no owner older than the SLA |
| orphans | contacts with empty `associatedcompanyid`; deals with zero contact or company associations; companies with `num_associated_contacts` = 0 and no deals |
| stale | `notes_last_updated` older than the stage threshold on open deals; contacts with `lastmodifieddate` over a year old |
| value normalisation | `hs_analytics_source` and custom source values not in `data/ontology/naming.md`; company names differing only by case or suffix ("Acme" vs "ACME Corporation") |
| property audit | list properties per object (`GET /crm/v3/properties/<object>`) and flag custom ones with no values on any record or no documented owner |

`hs_date_entered_<stageid>` per stage gives backwards moves and days in
stage when the history is wanted.

## What the fix list proposes, and what a person does in HubSpot

- Merge pairs as `primary,secondary` ids; a person merges in the UI
  (irreversible; the secondary's activity moves to the primary).
- Field edits as `id,property,old,new`; a person applies them, in
  batches of up to 100, after a dry run on the first 50.
- Rules as required properties or validation on the form and the
  pipeline stage; a HubSpot admin sets them.

This skill never calls `manage_*` tools or the update, merge or delete
endpoints; every change is a proposal.
