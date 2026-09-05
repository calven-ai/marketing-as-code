# Salesforce: closed deals for win/loss

What the win/loss skill needs from Salesforce, and where it lives. The
pull runs through `snapshot-pull`; check the server's tool list in the
session for the exact tool names (a SOQL query tool is the usual route).
`integrations/catalog/crm.json` carries the caveats: the hosted MCP is
edition-gated, and the whole server stays denied for writes until the
write tools are checked.

## Objects and fields

`Opportunity` is the object; `Account` gives the company.

| Field | Holds | Snapshot column |
| --- | --- | --- |
| `Id` | Opportunity id | `deal_id` |
| `Account.Name`, `Account.Website` | The account | `company` |
| `Amount` | Deal value | `amount` |
| `CloseDate` | Close date | `close_date` |
| `StageName`, `IsClosed`, `IsWon` | Outcome; `IsWon` true is won, `IsClosed` true and `IsWon` false is lost | `outcome` |
| a loss reason field (often `Loss_Reason__c`, sometimes a standard picklist the org enabled) | The rep's reason | `reason_crm` |
| a competitor field (`Competitor__c`, or the `OpportunityCompetitor` related list) | Named competitor | `competitor` |
| `Account.Industry`, `Account.NumberOfEmployees`, or a custom segment or tier field | Segment | `segment`, `tier` |
| `Owner.Name` | Owner | `owner` |
| `LeadSource` | Original source | `source` |

Custom fields end in `__c` and differ per org; ask the team which ones
carry reason, competitor and tier, and write them into `data/ontology/`
so the next run does not ask again. An empty column is reported as "the
CRM does not record this", never filled in.

## Query shape

Select the fields above from `Opportunity` where `IsClosed = true` and
`CloseDate` falls inside the period, ordered by `CloseDate`. Keep the
result under the query row limit by paging on `Id` or by month, and say
how many queries you ran.

## Quirks

- A sandbox org has its own endpoint; make sure the pull is against the
  org the team reports from.
- `StageName` values are org-specific; the ontology's funnel maps them to
  the stages the report uses.
- Opportunity history (`OpportunityHistory`) gives the real stage dates
  when the close date was backfilled; useful for the timeline check in
  the win/loss procedure.
- Contact roles and activities carry personal data; the win/loss
  snapshot stays at company level.
