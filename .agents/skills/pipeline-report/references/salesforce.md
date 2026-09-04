# Salesforce fields for the pipeline report

The pull itself is `snapshot-pull` (`.agents/skills/snapshot-pull/references/salesforce.md`
has the SOQL, routes and limits). This file says which Opportunity fields
the report computes from and how Salesforce's stage model maps onto
`data/ontology/funnel.md`.

## Opportunity fields

| Report needs | Field | Notes |
| --- | --- | --- |
| stage | `StageName` | picklist; `ForecastCategoryName` (Pipeline, Best Case, Commit, Omitted, Closed) is the forecast view, separate from the stage |
| amount | `Amount` | null means unvalued; `ExpectedRevenue` is `Amount * Probability`, report it as the CRM's own weighted view |
| probability | `Probability` | defaults from the stage picklist; the team may override per deal |
| close date | `CloseDate` | overdue when before today on an open deal |
| created | `CreatedDate` | pipeline created this period |
| open or closed | `IsClosed`, `IsWon` | lost = closed and not won |
| owner | `Owner.Name` | |
| source | `LeadSource` | on the opportunity; the contact's or lead's `LeadSource` may differ, say which one you used |
| last activity | `LastActivityDate` | stale = no activity past the stage threshold |
| stage entry dates | `OpportunityHistory` (`StageName`, `CreatedDate`, `Amount`, `CloseDate`, `Probability`) | one row per change: velocity, days per stage, push counts, amount changes all come from here |
| campaign | `CampaignId`, `Campaign.Name`; `OpportunityContactRole` joined to `CampaignMember` | primary campaign source for sourced pipeline; contact roles plus campaign membership for influenced pipeline |
| close reason | a custom field in most orgs | read the API name from the ontology or ask |

## SOQL the report adds

- Stage history for velocity:
  `SELECT OpportunityId, StageName, CreatedDate, CloseDate, Amount FROM OpportunityHistory WHERE OpportunityId IN (<ids>) ORDER BY OpportunityId, CreatedDate`
- Influenced pipeline:
  `SELECT OpportunityId, Contact.Id FROM OpportunityContactRole WHERE OpportunityId IN (<ids>)`
  then `SELECT ContactId, Campaign.Name, Campaign.Type FROM CampaignMember WHERE ContactId IN (<ids>)`
- Closing in the next 7 days:
  `... WHERE IsClosed = false AND CloseDate = NEXT_N_DAYS:7`

Multi-currency orgs return `Amount` in the record currency with
`CurrencyIsoCode`; convert with the org's dated rates or report per
currency, never mix. `RecordType` separates new business from renewals in
many orgs; check before computing win rate on the whole table.
