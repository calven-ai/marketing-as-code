# Salesforce (source token `salesforce`; category `crm`)

Routes (from `integrations/catalog/crm.json`): the hosted MCP server
`salesforce` (OAuth, Enterprise Edition and above, a person in a session),
the DX server `salesforce-dx` (stdio, reuses `sf org login web`, headless
on a machine that has logged in), or the `sf` CLI in a workflow step:
`sf data query --query "<SOQL>" --result-format csv > <snapshot>`. Field
level security applies to every route, so a missing column may be a
permission, not a gap: say which.

## SOQL per snapshot

Tool names on the hosted server are not verified in the catalog; check the
tool list in the session (a SOQL query tool and a records tool are
expected). The queries are the contract either way.

| `<what>` | SOQL |
| --- | --- |
| pipeline | `SELECT Id, Name, Account.Name, StageName, Amount, CloseDate, CreatedDate, Owner.Name, LeadSource, LastActivityDate FROM Opportunity WHERE IsClosed = false` |
| closed-deals | `SELECT Id, Name, Account.Name, IsWon, Amount, CloseDate, CreatedDate, Owner.Name, LeadSource, Loss_Reason__c FROM Opportunity WHERE IsClosed = true AND CloseDate = LAST_N_DAYS:<n>` |
| new-contacts | `SELECT Id, Account.Name, Lead_Status__c, LeadSource, CreatedDate, Owner.Name FROM Contact WHERE CreatedDate = LAST_N_DAYS:<n>` (or `Lead` with `Status` when the team works leads) |
| contacts, companies | `SELECT Id, Email, FirstName, LastName, Account.Name, LeadSource, Owner.Name, CreatedDate, LastActivityDate FROM Contact` and `SELECT Id, Name, Website, Industry, NumberOfEmployees, Type, Owner.Name, CreatedDate FROM Account` |
| customers | `SELECT Id, Name, Website, Type, Industry, NumberOfEmployees, Owner.Name FROM Account WHERE Type = 'Customer'` |

`Loss_Reason__c`, `Lead_Status__c` and the lifecycle field are custom in
most orgs: read the org's field names from `data/ontology/funnel.md` or ask,
never guess an API name.

## Mapping to the snapshot columns

`deal_id` = `Id`; `stage` = `StageName`; `source` = `LeadSource`;
`last_activity` = `LastActivityDate`; `outcome` = won when `IsWon` is
true, else lost; `lifecycle_stage` = the org's lifecycle field; `size` =
`NumberOfEmployees`; `domain` = `Website` with the scheme stripped.

## Limits and cost

- A query returns up to 2,000 rows per page; the CLI pages for you, the
  API hands back `nextRecordsUrl`. Tables above roughly 50,000 rows go
  through Bulk API 2.0 (`sf data export bulk`).
- API requests are allocated per org per 24 hours (a base plus an
  allowance per user license); one snapshot costs one to a few dozen.
- The DX server's data toolset can run DML; keep `--toolsets orgs,data`
  and never add a write tool.
- Cost: included in the edition.

## Export fallback

Reports > a tabular report with the columns above > Export > Details
Only, CSV. Drop at `data/crm/snapshots/YYYY-MM-DD-salesforce-<what>.csv`
and rename the columns to the snapshot set.
