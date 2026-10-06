# Funnel and lead definitions

**Reads:** `data/ontology/` (metrics, funnel, events), `strategy/icp.md`,
`data/crm/snapshots/` (contacts and closed deals), `memory/knowledge/`
· **Skills:** `/lead-lifecycle-spec` writes scoring, routing and the
handoff as an ontology proposal, and `/tracking-spec` keeps the event
taxonomy honest; these prompts find where the definitions leak and test a
threshold before you commit to it.

Sales says the MQLs are junk. Marketing says sales never calls them back.
Both are arguing from definitions nobody wrote down the same way. You walk
away with an MQL, a score and a handoff that are written in
`data/ontology/`, tested against what actually converted, and agreed by
both sides. The skill writes the spec. The prompts find the disagreement
first and pressure-test the numbers after.

## Prompts

### Find where the definitions disagree

```
Using this repo, find every place our funnel terms are defined or used differently.

CONTEXT
Before I change anything, I want to see where we already contradict ourselves.

READ FROM THE REPO
- data/ontology/metrics.md and data/ontology/funnel.md.
- Recent reports in reports/recurring/pipeline/ and reports/qmr/, for how the terms are actually used.
- memory/decision-log.md and memory/knowledge/, for anything decided about MQL, SQL or handoff.

BUILD
- Per term (Signup, MQL, SQL, Opportunity, Pipeline): the ontology definition, how reports compute it, and any decision that says otherwise.
- Terms still marked as template or empty.
- Contradictions, ranked by how many reports they touch.

OUTPUT
A table per term, then the contradictions list.

GROUNDING
Quote each definition with its path and line. Don't fill an empty definition with an industry default; mark it "ask the team".
```

### Measure recent leads against the written criteria

```
Using this repo, check how last period's leads would score against the definitions we have.

FILL IN
- Window: [window]

CONTEXT
I want to know whether the MQL definition on paper matches who sales actually accepted.

READ FROM THE REPO
- The MQL and SQL rows in data/ontology/metrics.md and the scoring proposal if one exists in data/ontology/.
- The newest contacts and closed-deals snapshots in data/crm/snapshots/.
- The tiers in strategy/icp.md.

BUILD
- Leads in the window by: met MQL criteria (yes, no, can't tell), accepted by sales, became an opportunity.
- The criteria that most often fail or can't be evaluated because a field is empty.
- Leads that converted without meeting the criteria, and what they had in common.

OUTPUT
A short table and three findings.

GROUNDING
Cite snapshot paths and n. If the contacts export is missing, say which export to drop in data/crm/snapshots/ and stop. Company-level only; no contact names in the output.
```

### Review the handoff agreement

```
Using this repo, review our marketing-to-sales handoff as written.

FILL IN
- Agreement: [path in memory/knowledge/, or paste it]

CONTEXT
The handoff is where leads go to die. I want the holes before the next pipeline review.

READ FROM THE REPO
- data/ontology/funnel.md, for stage entry and exit rules.
- The newest pipeline report in reports/recurring/pipeline/.

CHECK
- Every stage change has an owner, a trigger and a time limit.
- What happens to a lead sales rejects, and where that's recorded.
- Whether the time limits match what the pipeline report shows.

OUTPUT
Findings, blocking first, then a proposed diff to the agreement on a branch.

GROUNDING
Cite paths. Don't invent an SLA the team never set; propose one and mark it as a proposal.
```

## Advanced prompts

### Backtest a lead score on last year's deals

```
Backtest a proposed lead score on last year's leads and tell me whether it would have found the deals we won. Use this repo for the leads, the outcomes and the ICP.

FILL IN
- Score: [paste the scoring rules, or the path to the scoring proposal in data/ontology/]
- Window: [e.g. the last four quarters]

CONTEXT
A score that looks sensible on a whiteboard can rank our best customers below the junk. I want to know before routing changes.

FROM THE REPO
- Contacts and companies from the newest snapshots in data/crm/snapshots/, with the fields the score uses.
- Closed-won and closed-lost outcomes for the window from the closed-deals snapshot.
- The tiers in strategy/icp.md.

METHOD
- Score every lead in the window with the proposed rules, using only fields that existed at the time.
- Rank leads by score; plot the share of won deals captured against the share of leads called (a gain curve). Report the AUC.
- Compare with the current definition and with ICP tier alone as baselines.
- Find the threshold that captures 80% of wins and say how many leads per week that sends to sales.
- If you can run code, do it in Python and give me the notebook.

OUTPUT
The gain curves, AUC for each option, the recommended threshold with leads per week, and the rules that added nothing.

GROUNDING
Label every number as repo (path and n), mine, or your calculation. Watch for leakage: a field filled after the deal moved isn't a predictor. Say when n is too small.
```

## Questions to just ask

- What does MQL mean in our ontology, exactly?
- Which terms in data/ontology/metrics.md are still template?
- Do our pipeline reports compute SQL the way the ontology says?
- What did we decide about lead scoring, and when?
- Which stage in funnel.md has no exit rule?
- How many leads last month met the MQL definition?
- Which events in events.md have no system named as emitting them?
- Can a lead skip from MQL to Opportunity, per our funnel rules?
- What's the handoff time limit, and where is it written?
- Which fields does our MQL definition need that the contacts export lacks?
- Who owns the funnel definitions, per the decision log?
