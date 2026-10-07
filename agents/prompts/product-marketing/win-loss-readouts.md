# Win/loss readouts

**Reads:** `data/crm/snapshots/` (closed deals and the coded file),
`memory/transcripts/processed/`, `strategy/competitive/`, the last win/loss
report in `reports/adhoc/` · **Skill:** `/win-loss` codes the deals and
writes the analysis; these prompts turn it into a readout people act on.

Leadership, sales and product want to know why deals were won and lost this
quarter, what changed since last time, and what to do about it. You walk
away with a readout: the win rate and its movement, the drivers with the
buyer's own words, the competitor read, the product gaps ranked by money at
stake, and three recommendations each owner accepts. Run `/win-loss` first
if this period hasn't been coded yet; everything below reads its output.

## Prompts

### Build the headline read

```
Using this repo, build the first page of the win/loss readout for the period below.

FILL IN
- Period: [quarter]

CONTEXT
The audience is leadership, sales and product in a 30-minute meeting. They want why we won and lost, what changed, and what to fix.

READ FROM THE REPO
- The win/loss report for this period and the one before it in reports/adhoc/.
- The coded deals file and the closed-deals snapshot for the period in data/crm/snapshots/.
- What win rate means in data/ontology/metrics.md.

BUILD
- The headline: win rate, deals won and lost, pipeline won and lost, each with the change from last period and n.
- Coverage: how many decided deals have a call on record, and which segments rest on fewer than five deals.
- The five drivers that decided the most deals, won and lost, each with one verbatim line and the transcript it came from.

OUTPUT
One page, numbers in a table, quotes cited. Show it here; I'll paste it.

GROUNDING
Cite the file path behind every number and quote. Compute rates only as the ontology defines them. If the period isn't coded yet, stop and tell me to run /win-loss.
```

### Read win/loss by competitor

```
Using this repo, write the competitor section of the win/loss readout.

FILL IN
- Period: [quarter]

CONTEXT
Leadership wants to know which competitors we beat, which beat us, and on what.

READ FROM THE REPO
- The coded deals file and closed-deals snapshot for the period in data/crm/snapshots/.
- Every battlecard in strategy/competitive/.
- The calls for deals lost to the top two competitors in memory/transcripts/processed/.

BUILD
- A table: competitor, deals, won, lost, win rate with n, the top driver we lose to them on.
- For the two competitors costing us most: what buyers said, in their words.
- Per battlecard: where it already answers that driver and where it doesn't.

OUTPUT
One page, then a list of battlecards that need a refresh with the reason.

GROUNDING
Cite paths. Mark any competitor with fewer than five deals as "too few to read". Never infer a competitor's move from a loss.
```

### Rank the product gaps that cost deals

```
Using this repo, rank the product gaps that cost us deals in the period below.

FILL IN
- Period: [quarter]

CONTEXT
Product wants gaps ranked by money at stake, with the buyer's words, not the loudest rep's.

READ FROM THE REPO
- Deals coded "capability gap" as primary or secondary driver in the coded deals file in data/crm/snapshots/.
- Their calls in memory/transcripts/processed/.
- What we claim the product does in strategy/product-brief.md.

BUILD
- A table: gap, deals touched, won and lost, amount at stake, competitors that have it per their battlecard.
- Under each of the top three: two verbatim lines and the deal they came from.
- Any gap the product brief says we already cover: flag it as a messaging problem, not a product one.

OUTPUT
The ranked table and quotes, ready to paste into the readout.

GROUNDING
Cite paths. Amount at stake counts won and lost deals; say so. A deal with no call on record is counted from the CRM reason and marked.
```

### Assemble the readout and its follow-ups

```
Using this repo, assemble the win/loss readout from the sections below and propose what follows from it.

FILL IN
- Period: [quarter]
- Sections: [paste the headline, competitor and product-gap sections]

CONTEXT
One document for the leadership meeting, plus the changes the findings imply.

READ FROM THE REPO
- memory/decision-log.md, for anything already decided on these drivers.
- integrations/tasks.md, for where follow-ups go.

BUILD
- One-paragraph summary: what changed and why.
- The numbers table, why we win, why we lose, competitors, product gaps.
- Three recommendations with an owner each: marketing, product, sales.
- Draft decision-log entries for anything the readout settles, and tasks per integrations/tasks.md for each recommendation.

OUTPUT
The readout as report.md in the period's reports/adhoc/ win/loss folder, on a branch. Slides if I say deck.

GROUNDING
Change nothing in the numbers or quotes. Every recommendation traces to a driver in the sections. Don't log a decision nobody made: draft it and ask.
```

## Advanced prompts

### Test whether the win-rate move is real

```
Tell me whether this period's win-rate change is a real shift or noise before I put it on a slide. Use this repo for the win rates, their sample sizes and the drivers behind them.

FILL IN
- Period: [quarter]
- Prior belief: [what leadership thinks caused the change, or "none"]

CONTEXT
Every readout gets a headline like "win rate up six points". On thirty deals that can be chance. If I present noise as a trend, product and sales act on it for a quarter.

FROM THE REPO
- Won and lost counts for this period and the one before, overall, by segment and by competitor, from the closed-deals snapshots in data/crm/snapshots/.
- The primary drivers for both periods from the coded deals files.
- How data/ontology/metrics.md defines win rate (does no-decision count?).

METHOD
- Treat each win rate as a Beta posterior from its wins and losses with a flat prior. Give the 90% credible interval per period and the probability the true rate went up.
- Repeat per segment and competitor. Flag moves that clear 80% probability and those that don't.
- Update the prior belief: given how the drivers shifted, is the stated cause more or less likely?
- Work out how many more decided deals it would take to call the headline move at 90%.
- If you can run code, simulate it in Python and plot the two posteriors.

OUTPUT
A table: metric, last period, this period, credible interval, probability of a real increase, verdict (real, likely, noise). Then the one sentence to say in the readout and the one not to.

GROUNDING
Label every number as repo (file path and n), mine, or your calculation. Don't call anything a trend that fails the threshold.
```

### Replay the lost deals with one gap fixed

```
Replay last period's lost deals as if we'd fixed one thing, and tell me how many would have flipped. Use this repo for the lost deals, their coded drivers and the buyers' words.

FILL IN
- Period: [quarter or two]
- Fixes to test: [two to four, e.g. the missing integration, a cheaper entry tier, a security review pack]

CONTEXT
Product, pricing and sales each want next quarter's investment. I want the counterfactual: which fix would have won back the most revenue, deal by deal.

FROM THE REPO
- Lost deals with amount and competitor from the closed-deals snapshot in data/crm/snapshots/.
- Primary and secondary drivers and evidence paths from the coded deals file.
- The calls behind them in memory/transcripts/processed/.

METHOD
- For each lost deal and each fix, judge whether the fix removes the deciding driver: flip, maybe or no, quoting the evidence.
- A deal with two deciding drivers flips only if the fix removes both.
- Weight flip as 0.7 and maybe as 0.3 (assumptions I can change) and sum recovered revenue per fix.
- Check overlap so no deal counts twice.
- If you can run code, write the deal-by-fix grid as a CSV with the weights as inputs.

OUTPUT
Fixes ranked by expected recovered revenue, the grid behind it, and the deals no fix would have saved.

GROUNDING
Label every number as repo (file path and n), mine, or your assumption. Every flip cites its evidence path. A deal with no call and a vague CRM reason is "unknown", not a guess.
```

## Questions to just ask

- What was our win rate last quarter, and how many deals is it based on?
- Why did we lose to [competitor] this quarter? Quote the calls.
- Which product gap cost the most pipeline this year?
- Which closed deals have no call in the transcripts?
- What did buyers say about price in the deals we lost?
- Which driver grew most since the last win/loss report?
- Which deals did we win despite losing on price, and what outweighed it?
- How does win rate in [segment] compare with the rest?
- Which lost deals have a CRM close reason the call contradicts?
- Which battlecards haven't been touched since we last lost to that competitor?
- What do buyers praise in won deals that our messaging never mentions?
- Which decisions in the decision log came out of a win/loss finding, and did anything change after?
