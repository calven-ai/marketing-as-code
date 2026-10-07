# Budget allocation

**Reads:** `projects/*/campaign.md` (the plan per campaign),
`data/ads/snapshots/` (spend and the finance export), `data/crm/snapshots/`,
`reports/recurring/ads/` · **Skills:** `/budget-pacing` answers "are we on
pace"; `/attribution-analysis` answers "what drives pipeline". These prompts
decide where the next dollar goes.

Someone just asked you to cut 15% or to place an extra chunk of budget by
Friday. You don't want to defend it with last-click charts and gut feel.
You walk away with spend and pipeline per program from the repo, the cost
of what each program produced, and a recommendation with the risk shown as
a range, not a single confident number.

## Prompts

### Show cost and return per program

```
Using this repo, show what each program cost and what it produced over the window below.

FILL IN
- Window: [window]

CONTEXT
Before I move any money I want one table: spend in, pipeline out, per program.

READ FROM THE REPO
- Planned budget per campaign in each projects/ campaign.md.
- Actual spend from the newest ads and finance snapshots in data/ads/snapshots/.
- Pipeline and closed-won by source from data/crm/snapshots/, read through data/ontology/metrics.md.

BUILD
- A table: program, planned spend, actual spend, pipeline created, closed-won, cost per opportunity, pipeline per dollar.
- Which attribution view the pipeline numbers use, from the newest attribution report if one exists.
- Programs with spend but no way to tie pipeline to them.

OUTPUT
The table and a three-line read. Show it here.

GROUNDING
Cite the snapshot behind every number. Never estimate spend you couldn't read. If finance's invoices and the platform spend disagree, show both.
```

### Plan a cut

```
Using this repo, propose how to cut the budget by the amount below with the least damage to pipeline.

FILL IN
- Cut: [amount or percent]
- Protected: [programs leadership won't touch, or "none"]

CONTEXT
I need a defensible cut by the end of the week, with what we lose stated plainly.

READ FROM THE REPO
- The cost and return per program, from the newest pacing report in reports/recurring/ads/ and data/crm/snapshots/.
- Commitments in memory/decision-log.md: contracts, events, launches already promised.
- Active projects and their status in projects/.

BUILD
- Rank programs by pipeline per dollar, lowest first, skipping the protected ones and anything contractually committed.
- Cut in that order until the amount is reached, and estimate the pipeline lost at each program's own rate.
- Flag cuts that break a launch or a commitment in the decision log.

OUTPUT
A cut list with pipeline at risk, then a draft decision-log entry for me to approve.

GROUNDING
Cite paths. The pipeline-at-risk estimate uses each program's own historical rate and says so. Don't log the decision until I confirm it.
```

## Advanced prompts

### Simulate the reallocation before you make it

```
Simulate three budget splits for next quarter and tell me which one I should fund, with the risk. Use this repo for spend, pipeline per program and the funnel rates.

FILL IN
- Budget: [next quarter's total]
- Splits to test: [three allocations across programs, or "propose three"]

CONTEXT
Every allocation looks good with a point estimate. I want to see the spread, because a program with a great average and a wide spread can still sink the quarter.

FROM THE REPO
- Spend and pipeline per program per month from data/ads/snapshots/ and data/crm/snapshots/, as many months as exist.
- Funnel conversion rates and deal sizes from the QMRs in reports/qmr/.
- Saturation hints: programs where the pacing reports show rising cost per opportunity as spend grew.

METHOD
- Per program, fit pipeline per dollar from the monthly history as a distribution (lognormal if positive and skewed), with diminishing returns where the history shows them.
- Run a Monte Carlo of 10,000 quarters per split: draw each program's return, apply the funnel rates to get closed-won.
- Report the median, the 10th and 90th percentiles and the probability of hitting the target per split.
- Run a sensitivity: which program's assumption moves the answer most.
- If you can run code, do it in Python and hand me the notebook and a chart of the three distributions.

OUTPUT
A table per split: median pipeline and revenue, P10, P90, probability of hitting target. Then the split I should fund and the one assumption to check first.

GROUNDING
Label every number as repo (file path and n), mine, or your assumption. A program with fewer than three months of history gets a wide, stated assumption, not a fitted distribution.
```

## Questions to just ask

- How much have we spent this month against plan, by campaign?
- Which program has the lowest pipeline per dollar this quarter?
- Where do finance's invoices and the ad platform's spend disagree?
- Which campaigns in projects/ have no budget in their campaign.md?
- What did we commit to spending in the decision log that hasn't been spent?
- How has cost per opportunity moved on our biggest paid channel over the last six months?
- Which programs produce pipeline we can't tie to spend?
- What would we lose if we paused [campaign] for a month?
- Which program grew spend fastest this year, and did pipeline follow?
- How much budget is left for the quarter?
