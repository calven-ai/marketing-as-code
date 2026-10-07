# CRM data quality

**Reads:** `data/crm/snapshots/` (contacts, companies, pipeline),
`reports/recurring/crm/`, `data/ontology/`, `strategy/icp.md`
· **Skills:** `/data-hygiene-audit` counts duplicates, missing fields and
bad stages each month, and `/utm-builder` stops new source data breaking;
these prompts rank the problems by which report they'd break and plan the
fixes around the next big readout.

The QMR is in two weeks and you don't trust the source field. You walk away
knowing which data problems would change a number leadership sees, and a
fix list ordered by that, not by count. The monthly audit gives you the
counts. The prompts tie them to the reports that depend on them.

## Prompts

### Rank problems by the report they'd break

```
Using this repo, rank this month's data problems by the reports they'd distort.

CONTEXT
A thousand contacts with no job title matter less than fifty deals with no source.

READ FROM THE REPO
- The newest audit in reports/recurring/crm/.
- The reports that read the CRM: reports/recurring/pipeline/, reports/qmr/, the latest attribution and win/loss reports in reports/adhoc/.
- The fields each metric needs in data/ontology/metrics.md.

BUILD
- Per problem: count, which metrics and reports use the field, and how much pipeline or how many deals it touches.
- A ranked list: the problems that would move a number leadership sees, first.

OUTPUT
A ranked table with the report each problem affects.

GROUNDING
Cite paths and n. If there's no audit this month, suggest /data-hygiene-audit and stop.
```

### Check the CRM against the ICP

```
Using this repo, check whether our CRM fields can tell us who fits the ICP.

CONTEXT
If tier and segment are empty, every ICP report is guesswork.

READ FROM THE REPO
- The tiers and segment rules in strategy/icp.md.
- The newest companies snapshot in data/crm/snapshots/.
- data/accounts/target-accounts.csv.

BUILD
- Per ICP criterion: which CRM field holds it, and how complete it is.
- Target accounts missing from the CRM or with a different tier there.
- Criteria the CRM can't express at all.

OUTPUT
A short table and the fields to add or fix.

GROUNDING
Cite paths and n. Company-level only; no contact names.
```

### Plan the cleanup before the quarterly review

```
Using this repo, plan the data fixes that need to land before the quarterly review.

FILL IN
- Review date: [date]

CONTEXT
I can get a few hours of someone's time. I want those hours on what changes the review.

READ FROM THE REPO
- The newest audit in reports/recurring/crm/.
- The QMR data checklist in reports/_templates/qmr/data-checklist.md.
- integrations/tasks.md, for where tasks go.

BUILD
- The fixes the QMR checklist depends on, with effort (small, medium, large) and owner.
- What to fix by hand versus with a bulk update in the CRM.
- Tasks filed per integrations/tasks.md.

OUTPUT
A dated fix list and the tasks.

GROUNDING
Cite paths. Agents never edit the CRM; every fix is applied by a person.
```

## Advanced prompts

### Run a pre-mortem on the quarterly numbers

```
Imagine the quarterly review went badly because a number was wrong, and work backwards to which data problem caused it. Use this repo for the reports, the definitions and the audit.

FILL IN
- Quarter: [quarter]

CONTEXT
I'd rather find the embarrassing error now than in the board pack.

FROM THE REPO
- The QMR data checklist in reports/_templates/qmr/data-checklist.md and last quarter's QMR in reports/qmr/.
- The newest audit in reports/recurring/crm/.
- The metric definitions in data/ontology/metrics.md and funnel.md.

METHOD
- Assume it's two weeks after the review and a headline number turned out wrong. Write five plausible stories of how, each tied to a specific field, snapshot or definition.
- For each story: likelihood (from the audit counts) and impact (which number moves, by roughly how much).
- Check each story against the current snapshots: is the condition present right now?
- Rank by likelihood times impact and name the check that would catch each one.

OUTPUT
A ranked table of failure stories with the evidence, the check and the fix, plus the three checks to run before the review.

GROUNDING
Label every number as repo (path and n), mine, or your assumption. A story with no evidence in the repo stays labelled as a hypothesis.
```

## Questions to just ask

- How many duplicate companies are in the CRM this month?
- Which deals have no source?
- What share of companies has no industry or tier?
- Which deals have a close date in the past and are still open?
- How did the last audit compare with the one before?
- Which fields does our MQL definition need that are mostly empty?
- Which target accounts aren't in the CRM?
- Which lifecycle stages in the CRM aren't in our funnel definition?
- How old is the newest contacts snapshot?
- Which fixes from last month's audit are still open?
- Which owner has the most records with missing fields?
