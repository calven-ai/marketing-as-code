# Competitive teardowns

**Reads:** `strategy/competitive/`, `reports/recurring/competitive/`,
`data/accounts/snapshots/` (competitor changes), `data/crm/snapshots/`,
`memory/transcripts/processed/` · **Skills:** `/battlecard` writes and
refreshes the card, `/competitor-watch` tracks what changed each month.
These prompts go deeper on one competitor when a card isn't enough.

A competitor keeps showing up in deals, or a board member asks how you
stack up. The battlecard is a sales tool; a teardown is the full read.
You walk away with what they claim, what changed, where they beat you,
where you beat them, and the deals they touched, all cited. When you're
done, `/battlecard` folds what's new back into the card.

## Prompts

### Pick the competitor for the next teardown

```
Using this repo, tell me which competitor deserves a full teardown next.

CONTEXT
I can do one teardown this month. I want the competitor that costs us most or is moving fastest, not the one people talk about loudest.

READ FROM THE REPO
- The closed-deals snapshot and coded win/loss file in data/crm/snapshots/, for deals and losses per competitor.
- The last three competitor watch reports in reports/recurring/competitive/.
- The last_reviewed date on each battlecard in strategy/competitive/.

BUILD
- A table: competitor, deals in the last two quarters, losses, amount lost, notable changes, card age in days.
- A recommendation with the reason, and the runner-up.

OUTPUT
The table and two sentences.

GROUNDING
Cite paths. Counts come from the snapshots only. If no closed-deals snapshot exists, say which export to drop in data/crm/snapshots/ and rank on changes and card age alone.
```

### Build the full teardown

```
Using this repo, build a full teardown of the competitor below.

FILL IN
- Competitor: [competitor]

CONTEXT
The audience is product marketing, product and sales leadership. They want the honest picture, including where we lose.

READ FROM THE REPO
- The competitor's battlecard in strategy/competitive/.
- Competitor watch reports in reports/recurring/competitive/ and the change snapshots in data/accounts/snapshots/.
- Deals where they appear in data/crm/snapshots/, and the calls for those deals in memory/transcripts/processed/.

BUILD
- What they claim, in their words, quoted from the card.
- What changed in the last two quarters: pricing, packaging, product, positioning.
- Head to head against strategy/positioning.md: where they win, where we win, where it's a draw.
- Their deals with us: count, win rate with n, the drivers, two buyer quotes.
- What buyers say about them on our calls.

OUTPUT
A teardown as report.md in a new reports/adhoc/ folder named for the competitor, on a branch.

GROUNDING
Cite paths. Their pricing and customers only as recorded in the card or a snapshot, never from memory. Mark anything older than 90 days as possibly stale.
```

### Check the battlecard against the teardown

```
Using this repo, compare the competitor's battlecard with what the teardown found.

FILL IN
- Competitor: [competitor]
- Teardown: [paste the teardown, or give its reports/adhoc/ path]

CONTEXT
Cards drift. I want to know what the card gets wrong or misses before reps repeat it.

READ FROM THE REPO
- The battlecard in strategy/competitive/ and the template it follows.
- strategy/positioning.md for our claims on the card.

CHECK
- Claims on the card the teardown contradicts.
- Strengths of theirs the card leaves out.
- Landmines that no longer work because they shipped something.
- Our "we win when" lines with no proof behind them.

OUTPUT
A findings list by severity, then the brief to hand to /battlecard for the refresh.

GROUNDING
Cite both files for every finding. Don't rewrite the card here; that's /battlecard's job.
```

## Advanced prompts

### Red-team us as their product marketer

```
Play the competitor's head of product marketing and write the campaign that beats us. Use this repo for our positioning, our weaknesses and what buyers say about us.

FILL IN
- Competitor: [competitor]

CONTEXT
I know how we pitch against them. I want to see how they'd pitch against us, using our real soft spots, so the card and the talk track hold up.

FROM THE REPO
- Their battlecard in strategy/competitive/, for their strengths and positioning.
- Known weaknesses in strategy/product-brief.md and the objection section of strategy/messaging.md.
- Loss drivers from the coded win/loss file in data/crm/snapshots/ and buyer quotes from memory/transcripts/processed/.

METHOD
- As them: pick the three attacks most likely to land, each tied to a real weakness or loss driver.
- Write their one-liner against us, a comparison table they'd publish, and the question their reps plant.
- Switch sides: for each attack, our best honest response, and whether the card has it.
- Score each attack on how often it would land, from the loss evidence.

OUTPUT
Their campaign on one page, then our response table, then the gaps to fix.

GROUNDING
Label every point as repo (path), or your inference. Their attacks may only use weaknesses the repo records; no invented flaws.
```

### Map their likely next move with a payoff matrix

```
Model the competitor's next strategic move as a game and tell me which response holds up best. Use this repo for their recent moves, our position and the deals we share.

FILL IN
- Competitor: [competitor]
- Moves to consider: [two to four, e.g. a price cut, a free tier, a bundle, entering our core segment]

CONTEXT
Leadership asks "what will they do next and what do we do then". I want an answer that weighs their incentives, not a guess.

FROM THE REPO
- What changed at them in reports/recurring/competitive/ and data/accounts/snapshots/.
- Shared deals and win rates from data/crm/snapshots/.
- Our segments and tiers in strategy/icp.md.

METHOD
- Build a payoff matrix: their moves against our responses (hold, match, reframe, retreat to a segment).
- Score each cell on likely effect on their wins and ours, with the reasoning and the evidence.
- Find each side's best response and any stable outcome.
- Run a sensitivity on the one assumption that changes the answer.

OUTPUT
The matrix, the most likely move, our recommended response and the early signal to watch for.

GROUNDING
Label every number as repo (path and n), mine, or your assumption. Scores are judgements, so say what they rest on.
```

## Questions to just ask

- Which competitor did we lose the most pipeline to last quarter?
- What's our win rate against [competitor], and on how many deals?
- What changed on [competitor]'s pricing page since the last watch report?
- When was the [competitor] battlecard last reviewed?
- What do buyers say about [competitor] on our calls? Quote them.
- Where does [competitor] beat us, according to their card?
- Which segment do we lose to [competitor] in most?
- Which battlecards have a "we win when" line with no proof?
- Which competitors appear in deals but have no battlecard?
- What did we decide the last time [competitor] changed pricing?
- Which keywords do we and [competitor] both rank for?
- Which deals mention two competitors at once?
