# Salesforce for advocacy-program

What this skill reads from Salesforce when it fills the `crm` category
(catalog entry in `integrations/catalog/crm.json`). The pull goes through
`snapshot-pull`; this file names the objects and fields.

## Connection

- The route the catalog lists for Salesforce (an MCP server or a CLI with
  SOQL). Check the server's tool list in the session; expect a SOQL query
  tool and object describe. Write tools stay denied; this skill reads.

## Objects and fields

Accounts, filtered to `Type = 'Customer'` (or the team's equivalent
picklist value; ask when unsure):

| Snapshot column | Salesforce field |
| --- | --- |
| `company` | `Account.Name` |
| `domain` | `Account.Website` |
| `industry` | `Account.Industry` |
| `size` | `Account.NumberOfEmployees` |
| `owner` | `Account.Owner.Name` |
| `customer_since` | earliest `Opportunity.CloseDate` where `IsWon = true` |
| `arr_band` | the ARR field the team uses (custom, often on Account or a Contract) |
| `health` | a custom field, or the success platform's score synced to Account |
| `nps` | a custom field, or join from `data/reviews/snapshots/` by domain |
| `renewal_date` | `Contract.EndDate`, or the open renewal `Opportunity.CloseDate` |
| `escalation` | open `Case` records with high priority per Account |

Sample SOQL, to adapt to the team's fields:

```
SELECT Name, Website, Industry, NumberOfEmployees, Owner.Name
FROM Account WHERE Type = 'Customer'
```

Contacts are read only to find the champion (`Title`, `HasOptedOutOfEmail`).

## Snapshot

`data/crm/snapshots/YYYY-MM-DD-salesforce-customers.csv`, one row per
account, the columns above; empty cells stay empty and are reported as
gaps.

## Manual route

A Salesforce report on Accounts with the fields above, exported as CSV,
dropped at `data/crm/snapshots/YYYY-MM-DD-salesforce-customers.csv`.
