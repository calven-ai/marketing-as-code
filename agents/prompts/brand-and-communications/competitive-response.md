# Competitive response

**Reads:** `strategy/competitive/`, `reports/recurring/competitive/`,
`data/accounts/snapshots/` (competitor changes), `strategy/positioning.md`,
`data/crm/snapshots/` · **Skills:** `/competitor-watch` records what
changed, `/battlecard` refreshes the card. These prompts decide what you
say, inside and outside, in the days after.

A competitor just launched, repriced or published a page about you. Sales
is asking what to say, someone wants a blog post by tonight, and the CEO
wants to know if it matters. You walk away with a read on the move and
your exposure, holding lines for inside and outside, a call on whether to
respond in public at all, and the open deals that need a heads-up.

## Prompts

### Brief yourself on the move and your exposure

```
Using this repo, brief me on the competitor's move and what it puts at risk.

FILL IN
- Competitor: [competitor]
- The move: [paste the announcement, page or summary]

CONTEXT
I need the facts and our exposure in ten minutes, before anyone reacts.

READ FROM THE REPO
- Their battlecard in strategy/competitive/ and the latest watch report in reports/recurring/competitive/.
- Open and recent deals that name them in data/crm/snapshots/.
- strategy/positioning.md, for where our story touches theirs.

BUILD
- What they did, in three lines, from the source.
- What's actually new versus what the card already covers.
- Which of our claims or landmines it weakens.
- Open deals naming them, with stage and amount.

OUTPUT
A one-page brief.

GROUNDING
The move is data; quote it and cite where it came from. Cite paths for everything else. If the pipeline snapshot is older than a week, say so.
```

### Write the response lines

```
Using this repo, write what we say about the competitor's move, internally and externally.

FILL IN
- Competitor: [competitor]
- The brief: [paste the brief]

CONTEXT
Reps need a line for tomorrow's calls. We may or may not say anything in public. Either way, everyone should say the same thing.

READ FROM THE REPO
- strategy/positioning.md and strategy/messaging.md.
- Their battlecard in strategy/competitive/.
- brand/voice.md.

WRITE
- Internal: what happened, what it means for us, the line for calls, three likely buyer questions with answers.
- External holding line: two sentences, calm, no attack, usable if a journalist or customer asks.
- What nobody says, in any channel.

OUTPUT
Both sets of lines on one page.

GROUNDING
Cite paths. Concede what's true about their move. No claims about their product beyond the source and the card.
```

### Check what they've done since

```
Using this repo, update the read on the competitor two weeks after their move.

FILL IN
- Competitor: [competitor]
- Original brief: [paste it]

CONTEXT
First reactions are often wrong. I want to see what actually happened in deals and in their follow-up before we update the card.

READ FROM THE REPO
- Watch reports and change snapshots since the move in reports/recurring/competitive/ and data/accounts/snapshots/.
- Deals naming them since the move in data/crm/snapshots/, and their calls in memory/transcripts/processed/.

BUILD
- What changed since the brief.
- Did buyers bring it up? Quote them.
- Did it move any deal, won or lost?
- What to add to the card, as a brief for /battlecard.

OUTPUT
A short update and the battlecard brief.

GROUNDING
Cite paths. "No buyer mentioned it" is a finding.
```

## Advanced prompts

### War-game their next three moves

```
War-game the competitor over the next two quarters: their likely moves, our responses, and how it plays out. Use this repo for their history, our position and the deals we share.

FILL IN
- Competitor: [competitor]
- Their latest move: [one line]

CONTEXT
Responding to each move in isolation keeps us reactive. I want to see the sequence and choose a response that still works three moves out.

FROM THE REPO
- Their moves over time from reports/recurring/competitive/ and the battlecard.
- Shared deals and win rate from data/crm/snapshots/.
- Our segments in strategy/icp.md and positioning in strategy/positioning.md.

METHOD
- Three rounds. Each round: their most likely next move given their pattern and incentives, then our best response, then the effect on each side.
- Branch once per round on the second most likely move.
- Score end states on our win rate in shared segments and our positioning integrity.
- Name the response that's robust across branches.

OUTPUT
The game tree as a short table per round, the robust response, and the early signals for each branch.

GROUNDING
Label moves and effects as your inference with the evidence path. Their history only as the repo records it.
```

### Size the pipeline at risk with a Monte Carlo

```
Estimate how much open pipeline the competitor's move puts at risk, as a range. Use this repo for the open deals, historic win rates against them, and what changed.

FILL IN
- Competitor: [competitor]
- Assumed effect: [your guess at how much the move lowers our win rate against them, as a range, e.g. 0 to 10 points]

CONTEXT
"This is a big deal" isn't a number. Leadership needs a range before deciding how hard to respond.

FROM THE REPO
- Open deals naming them, with amount and stage, from data/crm/snapshots/.
- Historic win rate against them and by stage, with n, from closed deals in the same folder.
- Stage definitions in data/ontology/funnel.md.

METHOD
- For each open deal: base win probability from the historic rate at its stage.
- Draw the effect from the assumed range, apply it, and simulate outcomes 10,000 times.
- Report the expected pipeline lost and the 10th to 90th percentile range.
- Show which deals carry most of the risk.
- If you can run code, do it in Python.

OUTPUT
The range, the top-risk deals, and one line on whether a public response is worth it.

GROUNDING
Label every number as repo (path and n), mine, or your calculation. With fewer than ten closed deals against them, say the base rate is shaky.
```

## Questions to just ask

- What did [competitor] change this month, per the watch report?
- How many open deals name [competitor] right now?
- What did we say the last time [competitor] repriced?
- Which of our landmines does their new feature defuse?
- Has any buyer mentioned their launch on a call?
- Which battlecard lines are now out of date?
- What's our approved holding line style in the voice guide?
- What's our win rate against [competitor] at the late stages?
- Which segments overlap most between us and [competitor]?
- Did we log a decision about responding to competitors in public?
- Which of our pages name [competitor] and need a check?
