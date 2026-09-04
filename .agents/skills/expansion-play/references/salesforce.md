# Salesforce for expansion-play

What this skill reads from Salesforce when it fills the `crm` category
(catalog entry in `integrations/catalog/crm.json`). The pull goes through
`snapshot-pull`.

## Connection

The route the catalog lists (MCP server or CLI with SOQL). Check the
server's tool list in the session; expect a SOQL query tool. Writes stay
denied; this skill reads.

## Objects and fields

| Snapshot column | Salesforce field |
| --- | --- |
| `company`, `domain` | `Account.Name`, `Account.Website` |
| `owner` | `Account.Owner.Name` |
| `arr_band` | the team's ARR field, often on `Contract` or a custom Account field |
| `plan`, `seats_bought` | `Contract` line items, or custom fields; ask which |
| `health` | custom field, or a success platform's score synced to Account |
| `renewal_date` | `Contract.EndDate`, or the open renewal `Opportunity.CloseDate` |
| `customer_since` | earliest won `Opportunity.CloseDate` |
| `contacts_engaged` | Contacts per Account with activity in 90 days (`LastActivityDate`) |
| `champion_change` | a Contact whose `Title` changed recently, or a new senior Contact |

Open expansion deals, to exclude accounts sales is already working:

```
SELECT Account.Name, Name, StageName, Amount, CloseDate
FROM Opportunity WHERE IsClosed = false AND Type = 'Existing Customer - Upgrade'
```

Adjust `Type` to the team's picklist values.

## Snapshots

`data/crm/snapshots/YYYY-MM-DD-salesforce-customers.csv` and
`data/crm/snapshots/YYYY-MM-DD-salesforce-pipeline.csv`.

## Manual route

Two Salesforce reports (Accounts of type customer; open opportunities of
the expansion type) exported as CSV and dropped under
`data/crm/snapshots/` with the names above.
