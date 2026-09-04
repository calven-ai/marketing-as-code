# Salesforce for churn-signals

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
| `arr_band` | the team's ARR field |
| `health` | custom field, or a success platform's score synced to Account |
| `renewal_date` | `Contract.EndDate`, or the open renewal `Opportunity.CloseDate` |
| `last_contact` | `Account.LastActivityDate` (latest task or event) |
| `subscription_status` | from `billing` when wired; else a custom field |
| `open_high_tickets` | `Case` with `Priority = 'High'` and `IsClosed = false`, last 14 days |
| `champion_change` | a Contact with a senior `Title` marked inactive or gone |

Sample SOQL for the inactivity filter:

```
SELECT Name, Owner.Name, LastActivityDate
FROM Account WHERE Type = 'Customer' AND LastActivityDate < LAST_N_DAYS:60
```

And for tickets:

```
SELECT Account.Name, COUNT(Id) FROM Case
WHERE IsClosed = false AND Priority = 'High' AND CreatedDate = LAST_N_DAYS:14
GROUP BY Account.Name
```

## Snapshots

`data/crm/snapshots/YYYY-MM-DD-salesforce-customers.csv` and
`data/crm/snapshots/YYYY-MM-DD-salesforce-tickets.csv`.

## Manual route

Two Salesforce reports (customer Accounts with the fields above; open
high-priority Cases by Account) exported as CSV, dropped under
`data/crm/snapshots/` with the names above.
