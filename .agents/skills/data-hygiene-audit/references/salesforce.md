# Salesforce fields and checks for the hygiene audit

The pull itself is `snapshot-pull` (`.agents/skills/snapshot-pull/references/salesforce.md`
has the SOQL, routes and limits). This file names the fields each check
reads and the queries that find the records. Field-level security applies:
an empty column may be a permission, say so.

## Fields to request

- Contact: `Id, Email, FirstName, LastName, AccountId, LeadSource,
  OwnerId, CreatedDate, LastModifiedDate, LastActivityDate`, plus the
  org's lifecycle field (custom in most orgs; read the API name from
  `data/ontology/funnel.md` or ask).
- Lead (when the team works leads): `Id, Email, Company, Status,
  LeadSource, OwnerId, IsConverted, CreatedDate, LastActivityDate`.
- Account: `Id, Name, Website, Industry, NumberOfEmployees, Type,
  OwnerId, CreatedDate, ParentId`.
- Opportunity: `Id, Name, AccountId, StageName, Amount, CloseDate,
  OwnerId, LastActivityDate, IsClosed`.

## Checks and the SOQL that finds the records

| Check | Query |
| --- | --- |
| missing field | `WHERE Email = null`, `WHERE AccountId = null`, `WHERE OwnerId = null`; opportunities `WHERE Amount = null OR CloseDate = null` |
| duplicate contacts | `SELECT Email, COUNT(Id) FROM Contact WHERE Email != null GROUP BY Email HAVING COUNT(Id) > 1` (case-insensitive by default) |
| duplicate accounts | `SELECT Website, COUNT(Id) FROM Account WHERE Website != null GROUP BY Website HAVING COUNT(Id) > 1`; normalise `Website` first in the snapshot when the org stores schemes inconsistently; fuzzy `Name` pairs for review |
| lifecycle | `StageName` or the lifecycle field outside the ontology; `Type = 'Customer'` accounts with no `IsWon = true` opportunity; unconverted leads older than the SLA with no owner |
| orphans | contacts with `AccountId = null`; opportunities with no `OpportunityContactRole`; accounts with no contacts and no opportunities |
| stale | `LastActivityDate` past the stage threshold on open opportunities; contacts with `LastModifiedDate < LAST_N_DAYS:365` |
| value normalisation | `LeadSource` values not in `data/ontology/naming.md`; picklist values marked inactive still on records |
| field audit | describe each object (metadata) and flag custom fields with no value on any record |

Do not merge a child account (`ParentId` set) into its parent; propose
the pair for review instead. Duplicate rules and matching rules in Setup
are the prevention half of the fix list: propose them as rules.

## What the fix list proposes, and what a person does

- Merges as `primary,secondary` ids; a person merges in the UI (up to
  three records per merge), keeping the older account as survivor unless
  the report says why not.
- Field edits as a CSV a person loads with Data Loader or
  `sf data update bulk`, after checking the first 50 rows.
- Rules as validation rules, required fields and duplicate rules in
  Setup.

This skill never runs DML: no `sf data update`, no `sf data delete`, no
write tool on either MCP server.
