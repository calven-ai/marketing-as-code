# CRM fields

Open this at step 1 when profiling an export or querying a connected CRM. Column names differ per CRM and per company; match on meaning, then confirm with the person once.

| Needed for | Look for a column like | Notes |
| --- | --- | --- |
| Deal identity | Deal ID, Opportunity ID, Record ID, Deal name | Keep the ID; use the company name only for display |
| Account | Company, Account name, Associated company | Company level only; drop contact names and emails |
| Stage | Stage, Deal stage, Stage name, Pipeline stage | Stage values are company-specific; map them in step 2 |
| Outcome | Is won, Is closed, Closed won reason, a won or lost stage | A closed flag with won false is lost; never take the outcome from notes |
| Competitor | Competitor, Primary competitor, Competitors (multi-select), a related competitor list | Often free text: normalize in step 3. Sometimes only in notes; if so, mark the source "notes" |
| Loss reason | Loss reason, Closed lost reason, Reason lost | The rep's reason, coded against the taxonomy in step 6 |
| Dates | Create date, Close date, Date entered <stage>, stage history | Stage history gives real cycle and loss stage; a backfilled close date is common, so check it against the history |
| Amount | Amount, Deal value, ARR, ACV | Say which one, and the currency |
| Segment | Industry, Employees, Segment, Tier, Region | Use only what exists; never derive size from the company name |
| Owner | Deal owner, Opportunity owner | For process patterns only; report by team, not by person, unless asked |
| Source | Lead source, Original source | Optional pattern cut |

## Exports that help most

Ask for: closed deals in the period with every column above, plus a stage history export (one row per deal per stage change with its date) when the CRM offers one. Most CRMs export stage history separately from the deals list; it is what turns "loss stage" from "not recorded" into a number.

## From a connected CRM

Query closed deals with a close date in the period, the fields above, ordered by close date. Page through results rather than truncating, and say how many queries you ran. Read only: never change a record.
