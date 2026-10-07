# Pipeline reporting

**Reads:** `data/crm/snapshots/` (pipeline, new contacts, closed deals),
`data/analytics/snapshots/`, `data/ontology/`, `reports/recurring/pipeline/`
· **Skills:** `/pipeline-report` writes the weekly report and the monthly
forecast, `/web-analyst` the web side, and `/snapshot-pull` fetches what's
missing; these prompts explain the numbers before someone else does.

It's Monday and the pipeline number dropped. You walk away knowing why:
which stage moved, which segment or source drove it, and whether it's real
or a data artifact. The skill produces the weekly report. The prompts below
dig into the change it shows, prep you for the meeting, and stress-test the
forecast.

## Prompts

### Explain this week's change

```
Using this repo, explain what drove the change in this week's pipeline report.

FILL IN
- Report: [path in reports/recurring/pipeline/, or "the newest"]

CONTEXT
I'll be asked "why" in the pipeline meeting. I want the answer in three lines and the evidence behind it.

READ FROM THE REPO
- The report and the one before it in reports/recurring/pipeline/.
- The pipeline snapshots they cite in data/crm/snapshots/.
- Stage definitions in data/ontology/funnel.md.

BUILD
- The headline change and its size.
- A decomposition: how much came from new pipeline, stage movement, closed deals, slipped close dates, and deleted or re-staged records.
- The segment or source that accounts for most of it.

OUTPUT
Three lines I can say out loud, then a table with the decomposition.

GROUNDING
Cite snapshot paths and n. If part of the change is a data artifact (a bulk re-stage, a missing field), say so plainly.
```

### Read the funnel by source

```
Using this repo, show conversion at each funnel stage by lead source for the window below.

FILL IN
- Window: [window]

CONTEXT
I want to know which sources produce leads that actually progress, not just volume.

READ FROM THE REPO
- The newest new-contacts, pipeline and closed-deals snapshots in data/crm/snapshots/.
- data/ontology/funnel.md and data/ontology/metrics.md.
- The source naming rules in data/ontology/naming.md.

BUILD
- A table: source, leads, MQL, SQL, Opportunity, Won, with conversion between each stage and n.
- Sources whose labels break the naming rules, counted separately.
- The two sources with the biggest gap between volume and conversion.

OUTPUT
The table and two findings.

GROUNDING
Compute stages only as the ontology defines them. Mark any cell under n of 20 as "too few". If a snapshot is missing, say which one to pull with /snapshot-pull.
```

### Prep for the pipeline review

```
Using this repo, prepare me for this week's pipeline review.

CONTEXT
Thirty minutes, sales and marketing in the room. I want the numbers, the risks and the decisions to ask for.

READ FROM THE REPO
- The newest pipeline report in reports/recurring/pipeline/.
- Open decisions and recent entries in memory/decision-log.md.
- Status of active campaigns in projects/.

BUILD
- Pipeline versus target, with the trend over the last four reports.
- Three risks with the evidence.
- Two decisions to ask for, each with the options.

OUTPUT
A one-page brief.

GROUNDING
Cite paths. Don't forecast beyond what the monthly report states.
```

## Advanced prompts

### Forecast the quarter with Monte Carlo

```
Forecast where pipeline and bookings land this quarter as a distribution, not a single number. Use this repo for open pipeline, historical stage conversion and cycle times.

FILL IN
- Quarter: [quarter]
- Target: [the number]

CONTEXT
The weighted pipeline number assumes every deal behaves like an average. I want the range and the odds of hitting target.

FROM THE REPO
- Open deals with stage, amount and close date from the newest pipeline snapshot in data/crm/snapshots/.
- Historical stage-to-won conversion and days to close from closed-deals snapshots over the last four quarters.
- Pipeline and stage definitions in data/ontology/metrics.md and funnel.md.

METHOD
- Estimate per stage: win probability (Beta from historical counts) and days to close (empirical distribution).
- For each open deal, simulate win or loss and close date, 10,000 runs. Count only wins that close inside the quarter.
- Add new pipeline created and won inside the quarter from the historical rate, with its own uncertainty.
- Report P10, P50, P90 and the probability of hitting target. Show which deals swing the result most.
- If you can run code, do it in Python and give me the script.

OUTPUT
The distribution as P10, P50, P90, the probability of target, the ten deals that matter most, and one chart.

GROUNDING
Label every number as repo (path and n), mine, or your assumption. Don't treat close dates as reliable if history shows they slip; model the slip.
```

## Questions to just ask

- What's pipeline versus target this week?
- Which stage lost the most deals since last week?
- How much pipeline did marketing source this quarter, per our ontology?
- Which lead source converts best from MQL to SQL?
- How long does a deal sit in each stage, on average?
- Which open deals have a close date in the past?
- How fresh is the newest pipeline snapshot?
- What did the last monthly forecast say, and how close was it?
- Which segment grew pipeline most this quarter?
- How many new contacts came in last week by source?
- Which sources break our naming rules?
- What did the last four pipeline reports flag as risks?
