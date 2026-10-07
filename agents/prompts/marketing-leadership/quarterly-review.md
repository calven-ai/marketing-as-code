# Quarterly review

**Reads:** `reports/qmr/` (this quarter and the last), `reports/recurring/`,
`projects/*/status.md`, `memory/decision-log.md`, `data/ontology/metrics.md`
· **Skill:** `/qmr` works the data checklist and builds the report and
dashboard; these prompts write the story around it and test it.

The QMR is the one meeting where marketing explains itself to the rest of
the company. The numbers are the easy part once `/qmr` has run. The hard
part is the story: what actually moved, why, what you'd stop, and what
changes next quarter. You walk away with a narrative you can defend line by
line, because every claim points at a snapshot or a decision, and with the
questions the room will ask already answered.

## Prompts

### Write the narrative from the numbers

```
Using this repo, write the narrative section of this quarter's QMR.

FILL IN
- Quarter: [quarter]

CONTEXT
The QMR report and dashboard exist. Leadership reads the first page and skims the rest. They want what moved, why, and what we'll do differently.

READ FROM THE REPO
- This quarter's and last quarter's QMR in reports/qmr/, including their Data used sections.
- The status.md of every project active this quarter in projects/.
- Decision-log entries dated inside the quarter in memory/decision-log.md.

BUILD
- Three headlines: the metric, the change with n, and the one-sentence cause, each tied to a project or decision.
- What we planned and didn't do, and why.
- What we'd stop, with the evidence.
- What changes next quarter, as three commitments with an owner.

OUTPUT
The narrative as Markdown, ready to paste into the report's summary. Under 400 words.

GROUNDING
Cite the snapshot or file behind every number and cause. Don't attribute a change to a program unless a project status or report links them; otherwise say "cause unknown". Name any metric the data checklist left open.
```

### Prepare for the hard questions

```
Using this repo, list the questions the QMR room will ask and draft the answers.

FILL IN
- Quarter: [quarter]
- Who's in the room: [e.g. CEO, CFO, head of sales]

CONTEXT
I want no surprises. Every soft spot in the report gets a question and an honest answer before the meeting.

READ FROM THE REPO
- This quarter's QMR report and data checklist in reports/qmr/.
- The marketing plan's OKR table in projects/ (the marketing-plan folder's status.md).
- The newest pipeline report in reports/recurring/pipeline/.

BUILD
- Per person in the room: the three questions they're most likely to ask, given what they own.
- For each: a two-sentence answer with the file it rests on, or "we don't know yet" and what would tell us.
- Every OKR that missed, with the honest reason.

OUTPUT
A one-page prep sheet, questions grouped by person.

GROUNDING
Cite paths. Don't soften a miss. Where the data checklist shows a gap, the answer says so instead of reaching for a proxy number.
```

### Turn the review into next quarter's changes

```
Using this repo, turn the QMR's findings into proposed changes for next quarter.

FILL IN
- Quarter: [quarter]

CONTEXT
The review is done. I want the commitments it produced written down where they'll be acted on, not left in a slide.

READ FROM THE REPO
- This quarter's QMR in reports/qmr/.
- The marketing plan's brief.md and status.md in projects/.
- integrations/tasks.md, for where tasks go.

BUILD
- Draft decision-log entries for what the review settled, in the format memory/decision-log.md uses.
- The OKR table rows for next quarter that change, old and new side by side.
- One task per commitment, filed per integrations/tasks.md, with an owner and a date.

OUTPUT
A proposal on a branch: the decision-log entries and the status.md change, plus the task list here for me to confirm before filing.

GROUNDING
Draft only what the review actually decided; anything still open stays a question. Don't file a task without my confirmation.
```

## Advanced prompts

### Separate the signal from the season

```
Tell me which of this quarter's changes are real and which are seasonality or noise, before the QMR calls them wins. Use this repo for the quarterly numbers and their history.

FILL IN
- Quarter: [quarter]
- Metrics to test: [e.g. MQLs, pipeline created, win rate, organic sessions]

CONTEXT
A QMR that celebrates a seasonal bump commits next quarter's budget to the wrong program.

FROM THE REPO
- Every past QMR in reports/qmr/ and its Data used snapshots, for as many quarters as exist.
- The monthly figures behind each metric in data/crm/snapshots/ and data/analytics/snapshots/.
- The metric definitions in data/ontology/metrics.md, and any change to them in the decision log.

METHOD
- For each metric, compare this quarter with the same quarter last year and with the trailing four-quarter average.
- Where at least eight quarters exist, decompose into trend and seasonal parts and report the residual. Where fewer exist, say so and fall back to year-over-year.
- For rates, give a binomial interval from the counts; for counts, a Poisson interval.
- Flag any quarter where the metric's definition changed: those comparisons don't count.
- If you can run code, do it in Python and chart each metric with its interval.

OUTPUT
A table: metric, this quarter, expected range from history, verdict (real move, seasonal, noise, can't tell), and the sentence the QMR should use for each.

GROUNDING
Label every number as repo (file path and n), mine, or your calculation. With too little history, the verdict is "can't tell", not a guess.
```

## Questions to just ask

- Which items on this quarter's QMR data checklist are still open?
- Which OKRs did we miss this quarter, and by how much?
- What did we decide this quarter that the QMR doesn't mention?
- Which projects finished this quarter, and which slipped?
- How did pipeline created compare with last quarter, using the ontology's definition?
- Which recurring report shows the biggest change since last quarter?
- What did last quarter's QMR say we'd change, and did we?
- Which numbers in the QMR come from a manual export rather than a wired integration?
- Which program cost the most this quarter, and what did it produce?
- What's the one chart the QMR most needs that the dashboard doesn't have?
