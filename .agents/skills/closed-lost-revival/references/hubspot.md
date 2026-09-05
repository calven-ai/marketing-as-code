# HubSpot: closed-lost deals, stale proposals, the contacts on them

Wired through the HubSpot MCP server (`integrations/catalog/crm.json`).
Read tools only; check the server's tool list in the session and verify
the pipeline's stage ids and the loss-reason property name once.

## Pulls

| Lane | Object and filter | Properties |
| --- | --- | --- |
| A, closed lost | deals, `dealstage` in the pipeline's closed-lost stages, `closedate` in the last 18 months | `dealname`, `amount`, `closedate`, `closed_lost_reason`, `hs_lastmodifieddate`, `notes_last_contacted`, `hubspot_owner_id`, `hs_analytics_source` |
| A, proposal gone quiet | deals, open, `dealstage` at or past the proposal stage, `notes_last_contacted` older than 60 days | same |
| B, champion moved | the contacts associated with lane A and won deals: `jobtitle`, `company`, `hs_lifecyclestage_customer_date`; the job change itself comes from the alumni snapshot, not from HubSpot | |
| C, engaged then silent | contacts with a reply or a meeting in the engagements read and no activity for 60 days | `hs_last_sales_activity_timestamp`, `hs_email_last_reply_date` |
| exclusions | companies with `lifecyclestage = customer`; contacts with `hs_email_optout = true` or a do-not-contact property the team names | |

`closed_lost_reason` is a free-text or picklist property depending on the
portal; if the team uses a custom one, say which in the report.

## Snapshot

`data/crm/snapshots/YYYY-MM-DD-hubspot-closed-lost.csv`:

```csv
deal_id,domain,company,stage,amount,close_date,closed_lost_reason,last_activity,owner,champion_role,source,pulled_at
```

Include the stale open deals with `stage` set to their current stage so
lane A's two halves sit in one file. `champion_role` is a label, not a
name; add `champion_name,champion_email` only when `repo.private` in
`docs/schema.json` is true.

## Limits

100 records per search page; associations come as a separate call per
deal or as a batch of 100 ids. The route is OAuth, so this is a session
skill, never an unattended one.
