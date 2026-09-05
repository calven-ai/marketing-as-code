# Salesforce touch and source fields

The pull is `snapshot-pull` (`.agents/skills/snapshot-pull/references/salesforce.md`).
This file names where Salesforce keeps first touch, last touch and
campaign influence, so the three views come from what the org records.

## Source fields

| View | Fields |
| --- | --- |
| first touch | `Lead.LeadSource` (set at creation, carried to `Contact.LeadSource` on conversion); `Campaign.Name` of the lead's first `CampaignMember` by `CreatedDate`; the org's custom `First_Touch_*__c` fields when a marketing automation tool writes them (Marketo, HubSpot and Pardot each add their own; read the names from the object describe) |
| last touch | the latest `CampaignMember` before the opportunity's `CreatedDate`; custom `Last_Touch_*__c` fields when present |
| opportunity source | `Opportunity.LeadSource` (often copied from the contact, sometimes edited by the rep, say which) and `Opportunity.CampaignId` (the primary campaign source) |
| self-reported | a custom field on Lead the form writes (ask) |

`LeadSource` is a picklist the org defines; map its values to
`data/ontology/naming.md`, never the other way.

## Campaign influence (the multi-touch view)

- Primary campaign source: `Opportunity.CampaignId`, 100% credit to one
  campaign; the default "influenced" report in most orgs.
- Customizable Campaign Influence (Setup, needs enabling): the
  `CampaignInfluence` object holds one row per campaign and opportunity
  with `Influence` (a percentage) per model (`CampaignInfluenceModel`:
  primary campaign, even distribution, first touch, last touch, or
  custom). When enabled, pull
  `SELECT OpportunityId, CampaignId, Campaign.Name, Influence, ModelId FROM CampaignInfluence WHERE OpportunityId IN (<ids>)`
  and save it as `data/crm/snapshots/YYYY-MM-DD-salesforce-attribution.csv`
  with `model,channel,campaign,deals,amount`; say which model.
- Without it, build the touch snapshot from contact roles and campaign
  members:
  `SELECT OpportunityId, ContactId FROM OpportunityContactRole WHERE OpportunityId IN (<ids>)`,
  then
  `SELECT ContactId, CampaignId, Campaign.Name, Campaign.Type, CreatedDate, FirstRespondedDate FROM CampaignMember WHERE ContactId IN (<ids>)`,
  keeping members whose `CreatedDate` precedes the opportunity's close.

## Touch snapshot

`deal_id,contact_id,touch_date,source,medium,campaign,position`: `source`
and `medium` from `Campaign.Type` mapped through `naming.md`, `campaign`
from `Campaign.Name`, `position` first or last for the lead-source rows
and `middle` for campaign memberships. Contact ids only; no names or
emails in a public repo. Opportunities with no contact roles have no
touches: a gap, counted.
