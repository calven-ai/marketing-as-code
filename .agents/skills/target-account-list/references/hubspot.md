<!-- source: https://raw.githubusercontent.com/HubSpot/agent-cli-skills/main/data-enrichment/SKILL.md | license: Apache-2.0 | fetched: 2026-09-04 -->

# HubSpot: the exclusion lists and the dedupe key

Wired through the HubSpot MCP server (`integrations/catalog/crm.json`).
Check the server's tool list in the session; the read tools search CRM
objects by property filters. Never call a `manage_*` tool from this skill.

## What to pull

| Purpose | Object | Filter | Snapshot |
| --- | --- | --- | --- |
| customers to exclude | companies | `lifecyclestage = customer` | `data/crm/snapshots/YYYY-MM-DD-hubspot-customers.csv` |
| lost accounts to exclude | deals, with associated company | `dealstage` in the closed-lost stages of the pipeline; add `closed_lost_reason` | `data/crm/snapshots/YYYY-MM-DD-hubspot-closed-lost.csv` |
| existing target accounts | companies | a list or a custom property the team names | compare against `data/accounts/target-accounts.csv` |

Columns for the customers snapshot: `domain,company,lifecyclestage,owner,
close_date,source,pulled_at`. For closed-lost: `domain,company,deal_name,
amount,closed_lost_reason,close_date,owner,source,pulled_at`. Company-level
only; contacts do not belong in this skill.

## The dedupe key (from the source)

HubSpot's natural key for companies is `domain`, for contacts `email`, both
matched exactly after lowercasing. Lowercase every domain before comparing
snapshot rows with `target-accounts.csv`; a mixed-case duplicate is the most
common reason an exclusion is missed.

## If the team asks to write the list back

This skill does not write to HubSpot. If a person wants the tiered list in
the CRM, hand them the CSV and note the source's rules: verify property
names with the properties list first (never hard-code them), run a dry run,
and check the per-record result before trusting the import. An upsert
leaves unspecified fields alone, but a write-back can overwrite populated
ones; that is a human's call.

## Limits

Search calls page at 100 records; OR-filters are capped at 5 filter groups
per call, so split a long domain list into chunks.
