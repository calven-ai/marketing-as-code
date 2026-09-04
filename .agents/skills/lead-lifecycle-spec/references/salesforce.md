# Salesforce: the backtest pull

Wired through the hosted Salesforce MCP or the DX server
(`integrations/catalog/crm.json`); both run SOQL, and `sf data query
--result-format csv` is the scriptable path. Query tools only.

## Queries

| Purpose | SOQL shape |
| --- | --- |
| leads and their fate | `SELECT Id, CreatedDate, Status, Title, Industry, NumberOfEmployees, Country, LeadSource, IsConverted, ConvertedDate, ConvertedOpportunityId, OwnerId FROM Lead WHERE CreatedDate = LAST_N_DAYS:90` |
| activity before conversion | `SELECT WhoId, ActivityDate, Type, Subject FROM Task WHERE WhoId IN (...)` plus `CampaignMember` rows for form and event responses |
| won and lost with reasons | `SELECT Id, AccountId, StageName, Amount, CloseDate, IsWon, Loss_Reason__c, LeadSource, OwnerId FROM Opportunity WHERE IsClosed = true AND CloseDate = LAST_N_DAYS:90` |

The loss reason field is org-specific (often a custom picklist); ask which
one the team uses and name it in the snapshot's hand-over. Existing scores
live in custom fields or in a scoring add-on; read them as data.

## Snapshots

Same columns as the HubSpot reference, `source` token `salesforce`:
`data/crm/snapshots/YYYY-MM-DD-salesforce-contacts.csv` (leads and
converted contacts) and `YYYY-MM-DD-salesforce-closed-lost.csv` (won and
lost opportunities with the reason). Names and emails only in a private
repo.

## Limits

2,000 rows per query page; field-level security may hide a column, so a
missing value is "unknown", not zero. The hosted route is OAuth; the
unattended path is the `sf` CLI in a workflow step.
