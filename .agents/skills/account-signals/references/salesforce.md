# Salesforce: contacts, activities and opportunities per target account

Wired either through the hosted Salesforce MCP server or the local DX server
(`integrations/catalog/crm.json`). Both expose SOQL; the hosted route is
OAuth, the DX route reuses `sf org login web`. The `sf` CLI
(`sf data query --result-format csv`) is the unattended path. Check the
server's tool list in the session; the DX data toolset can run DML, so use
query tools only.

## Queries (adapt object and field names to the org)

| Purpose | SOQL shape |
| --- | --- |
| accounts in scope | `SELECT Id, Name, Website, Industry, NumberOfEmployees, OwnerId FROM Account WHERE Website IN (...)` |
| contacts and roles | `SELECT Id, AccountId, Title, Email, HasOptedOutOfEmail FROM Contact WHERE AccountId IN (...)` |
| activity, 90 days | `SELECT WhoId, WhatId, ActivityDate, Subject, Type FROM Task WHERE AccountId IN (...) AND ActivityDate = LAST_N_DAYS:90` and the same on `Event` |
| open pipeline | `SELECT AccountId, StageName, Amount, CloseDate, OwnerId FROM Opportunity WHERE IsClosed = false AND AccountId IN (...)` |
| campaign responses | `SELECT ContactId, CampaignId, Status, CreatedDate FROM CampaignMember WHERE ...` |

Match accounts by domain from `Website` after lowercasing and stripping
the scheme; Salesforce has no canonical domain field unless the org added
one, so say which field you matched on.

## Column mapping

Write the same columns as the HubSpot reference:
`domain,company,contact_id,role,seniority,lifecyclestage,last_email_click,
last_meeting,last_reply,last_contacted,optout,owner,pulled_at`, `source`
token `salesforce`. Map `Task.Type` and `Event` rows to `last_meeting`,
`last_reply` and `last_contacted`; email clicks only exist if a marketing
automation tool writes them back, otherwise leave the column empty and say
so in the report.

## Limits

SOQL `IN` lists are practical up to a few hundred ids; queries return
2,000 rows per page. Field-level security applies, so a missing column may
be a permission, not an absence; report it as unknown.
