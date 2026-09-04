# Salesforce: closed-lost opportunities and their contacts

Wired through the hosted Salesforce MCP or the DX server
(`integrations/catalog/crm.json`); query tools only, or
`sf data query --result-format csv`.

## Queries

| Lane | SOQL shape |
| --- | --- |
| A, closed lost | `SELECT Id, AccountId, Account.Website, Account.Name, StageName, Amount, CloseDate, Loss_Reason__c, LastActivityDate, OwnerId, LeadSource FROM Opportunity WHERE IsClosed = true AND IsWon = false AND CloseDate = LAST_N_MONTHS:18` |
| A, proposal gone quiet | `... WHERE IsClosed = false AND StageName IN ('Proposal', 'Negotiation') AND LastActivityDate < LAST_N_DAYS:60` |
| B, contacts on those deals | `SELECT OpportunityId, ContactId, Contact.Title, Role, IsPrimary FROM OpportunityContactRole WHERE OpportunityId IN (...)` |
| C, engaged then silent | `Task` and `Event` rows with a reply or meeting `Type` and no activity in 60 days |
| exclusions | `Account.Type = 'Customer'`, `Contact.HasOptedOutOfEmail = true`, `DoNotCall`, and any custom do-not-contact field |

The loss reason field is org-specific (`Loss_Reason__c` is a common
custom name); ask and record which one you used.

## Snapshot

Same columns as the HubSpot reference, `source` token `salesforce`:
`data/crm/snapshots/YYYY-MM-DD-salesforce-closed-lost.csv`. Derive
`domain` from `Account.Website` (lowercase, scheme stripped) and say so.
`champion_role` from `OpportunityContactRole.Role`; names only in a
private repo.

## Limits

2,000 rows per page; `IN` lists of a few hundred ids; field-level security
may hide the loss reason for some users, which you report as unknown.
