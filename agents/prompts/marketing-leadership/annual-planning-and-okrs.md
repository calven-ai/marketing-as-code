# Annual planning and OKRs

**Reads:** `strategy/`, `reports/qmr/`, `data/ontology/metrics.md` and
`funnel.md`, `memory/decision-log.md`, the plan in `projects/` · **Skill:**
`/marketing-plan` drafts the plan and the OKR table; these prompts feed it
and stress-test it before you commit.

Planning season is when every team brings a wish list and a number. You
need a plan whose targets come from the funnel you actually run, not the
one in last year's deck, and whose risks you've looked at before the board
does. You walk away with inputs `/marketing-plan` can build on, a target
that adds up from the bottom, and a pre-mortem that tells you which bet to
hedge.

## Prompts

### Gather the planning inputs

```
Using this repo, assemble the inputs for next year's marketing plan.

FILL IN
- Plan year: [year]

CONTEXT
I'll run /marketing-plan next. First I want everything it needs on one page, and the gaps named, so the planning meeting argues about choices, not facts.

READ FROM THE REPO
- Everything in strategy/, with each file's last_reviewed date.
- The last four QMRs in reports/qmr/.
- Decision-log entries from the past year in memory/decision-log.md.

BUILD
- What we know: last year's funnel conversion rates by stage, from the QMRs, with the quarter and n.
- What's already committed: launches, budgets, channels dropped, from the decision log.
- What's stale: strategy files past 90 days that the plan would rest on.
- What's missing: every input the plan needs that no file holds.

OUTPUT
A one-page planning brief. Show it here.

GROUNDING
Cite paths. Conversion rates come from the QMRs only, as the ontology defines them. A missing input is listed as a question, never estimated.
```

### Build the target bottom-up

```
Using this repo, work back from the revenue target to what each funnel stage has to deliver.

FILL IN
- Target: [the revenue or pipeline target, and who set it]
- Plan year: [year]

CONTEXT
Leadership gave a top-down number. I want to see what it takes at every stage before I agree to it.

READ FROM THE REPO
- The funnel stages in data/ontology/funnel.md and the metrics in data/ontology/metrics.md.
- Conversion rates and deal sizes from the last four QMRs in reports/qmr/.
- The newest pipeline report in reports/recurring/pipeline/.

BUILD
- Work back from the target through each stage: deals, opportunities, SQLs, MQLs, visitors, using last year's rates.
- The same at last year's best quarter and worst quarter.
- The gap between what the funnel produces today and what the target needs, per stage.

OUTPUT
A table per scenario, then one paragraph: is the target reachable on current rates, and what has to change if not.

GROUNDING
Cite the QMR behind every rate. Use the ontology's stage names. Don't invent a rate improvement; show it as a separate line labelled "assumes".
```

### Review a draft plan against strategy

```
Using this repo, review the draft plan below against our strategy and last year's evidence.

FILL IN
- Draft plan: [paste the plan, or the path of the marketing-plan brief in projects/]

CONTEXT
The plan reads well. I want to know where it quietly contradicts our positioning, our ICP or what we learned.

READ FROM THE REPO
- strategy/positioning.md, strategy/icp.md and strategy/personas.md.
- The last two QMRs in reports/qmr/ and the win/loss report in reports/adhoc/.
- memory/decision-log.md.

CHECK
- Programs aimed at a segment or persona the ICP doesn't prioritise.
- Targets that use a metric data/ontology/metrics.md doesn't define.
- Bets the evidence argues against, and decisions the plan reverses without saying so.

OUTPUT
Findings in a table: plan line, issue, evidence path, suggested fix.

GROUNDING
Cite paths. Findings only, no rewrite unless I ask. A judgment call stays a question for me, not a finding.
```

## Advanced prompts

### Run a pre-mortem on the plan

```
Run a pre-mortem on next year's plan: assume it's December and we missed, and tell me why. Use this repo for the plan, the funnel and last year's misses.

FILL IN
- Plan: [path of the marketing-plan brief in projects/, or paste it]

CONTEXT
Every plan looks achievable in the meeting where it's approved. I want the failure stories while there's still time to hedge.

FROM THE REPO
- The plan's targets and programs.
- Last year's misses and their reasons from the QMRs in reports/qmr/ and project retros in projects/.
- Competitor moves in reports/recurring/competitive/ and stale strategy files flagged in reports/recurring/context/.

METHOD
- Write five distinct failure stories, each a plausible chain from one cause to a missed target: a program underdelivers, a competitor moves, a dependency slips, a definition changes, the team runs out of capacity.
- For each, rate likelihood and impact, and say which early signal would show it in the first 60 days, from a report the repo already produces.
- Name the cheapest hedge for the top two.
- Check whether last year's misses repeat in the new plan.

OUTPUT
A table of failure stories with likelihood, impact, early signal and hedge, then the two changes to make to the plan now.

GROUNDING
Label every number as repo (file path and n), mine, or your assumption. Each failure story cites the evidence that makes it plausible; a story with none is labelled speculative.
```

## Questions to just ask

- What conversion rate from MQL to SQL did we actually get last year?
- Which strategy files would next year's plan rest on that are past 90 days?
- What did we commit to in the decision log that next year's plan has to honour?
- Which OKRs did we hit every quarter last year, and which never?
- How much pipeline did each quarter create last year?
- Which metric in the draft plan isn't defined in the ontology?
- What did last year's plan say we'd stop doing, and did we?
- Which segment in the ICP has no program in the draft plan?
- What's the largest target in the plan with no snapshot to measure it?
- Which project retros from last year recommended something the new plan ignores?
