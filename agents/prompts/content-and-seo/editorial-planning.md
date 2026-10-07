# Editorial planning

**Reads:** `strategy/messaging.md`, `strategy/personas.md`, `content/`
frontmatter, `data/seo/keywords.csv`, `data/seo/prompts.csv`, `projects/`
· **Skills:** `/content-strategy` ranks next quarter's gaps,
`/keyword-cluster` maps keywords to pages and `/content-calendar` dates
the result; these prompts feed them and argue with them.

It's the last week of the quarter and you need a plan you can defend: what
you'll write, for whom, and why that beats the alternatives. You walk away
with a slate where every slot names a persona, a stage, a pillar and the
evidence it rests on. The skills do the inventory and the ranking. The
prompts below find the gaps they can't see from keywords alone (the
objections that cost deals, the stages nobody writes for) and stress-test
the slate before it's dated.

## Prompts

### Find the buyer gaps in what you've published

```
Using this repo, find the questions and objections our content doesn't answer.

FILL IN
- Window: [window, for the calls to read]

CONTEXT
I'm planning next quarter. I want buyer-side gaps, not just keyword gaps.

READ FROM THE REPO
- Each persona's objections and pains in strategy/personas.md.
- Every published or in-flight piece in content/, by frontmatter and brief.
- Calls in memory/transcripts/processed/ from the window.

BUILD
- A grid of persona by buying stage (from strategy/messaging.md), each cell counting published pieces.
- Objections with no piece answering them, ranked by how often they come up on calls.
- For each gap: the format that would answer it and two verbatim lines to build it on.

OUTPUT
The grid and a ranked gap table, with paths.

GROUNDING
Count only pieces in content/. Quotes verbatim with paths. Don't add topics from your own knowledge of the category.
```

### Find losses content could head off

```
Using this repo, find what costs us deals that content could address earlier.

FILL IN
- Period: [quarter or two]

CONTEXT
The best editorial slot answers the reason we lose before sales hears it.

READ FROM THE REPO
- The latest win/loss report in reports/adhoc/ and the coded deals file in data/crm/snapshots/.
- Every battlecard in strategy/competitive/.
- What's published in content/ per competitor and per objection.

BUILD
- For each loss driver content can touch (proof, comparison, clarity on a capability): the piece that would pre-empt it, its stage, and the evidence to lead with.
- The drivers content can't fix, listed separately for product or sales.

OUTPUT
A table of content ideas, each tied to a loss driver and its deal count.

GROUNDING
Cite paths and n. If there's no win/loss report for the period, say so and suggest /win-loss first.
```

### Challenge the draft slate before it's dated

```
Using this repo, review the slate below before I hand it to /content-calendar.

FILL IN
- Slate: [paste the list, or the path to the content-strategy report]

CONTEXT
I want to cut the weakest third before anyone commits to dates.

READ FROM THE REPO
- strategy/messaging.md, for the pillars.
- projects/, for launches and events in the quarter.
- data/seo/keywords.csv and the latest ranking report in reports/recurring/seo/.

CHECK
- Each slot's persona, stage and pillar. Flag any with none.
- Pillars with no slot, and launches with no supporting piece.
- Two slots chasing the same keyword or question.
- Slots targeting keywords we already rank for in the top three.

OUTPUT
The slate as a table with a keep, merge or cut column and one reason each.

GROUNDING
Cite paths. Never estimate a volume or rank that isn't in keywords.csv or a snapshot.
```

## Advanced prompts

### Allocate the quarter like a portfolio

```
Pick the content slate that maximises expected pipeline contribution under our capacity, with the uncertainty shown. Use this repo for the candidate pieces, the gaps they close and what similar pieces did before.

FILL IN
- Candidates: [paste the list, or the content-strategy report path]
- Capacity: [pieces the team can ship this quarter, by format]

CONTEXT
We can't write everything. I want to choose the mix on evidence, not on who argued loudest.

FROM THE REPO
- Each candidate's persona, stage and keyword from the strategy report or keywords.csv (volume, difficulty, intent).
- What comparable published pieces did, from the latest snapshots in data/analytics/snapshots/ and data/seo/snapshots/.
- The pipeline definition in data/ontology/metrics.md.

METHOD
- For each candidate, estimate a range (low, likely, high) for traffic or influenced pipeline, anchored on its nearest published analogue. State the analogue.
- Run a Monte Carlo over the ranges, 10,000 draws, for every slate that fits capacity (or a greedy search if there are too many).
- Rank slates by expected value and by the 10th percentile, so I can choose between upside and safety.
- Show which single assumption moves the ranking most.
- If you can run code, do it in Python and give me the script with the ranges as inputs.

OUTPUT
The top three slates with expected value, P10 and P90, the pieces in each, and the assumption that matters most.

GROUNDING
Label every number as repo (path and n), mine, or your assumption. Where no analogue exists, say so and widen the range rather than invent one.
```

## Questions to just ask

- What did we publish last quarter, by channel and persona?
- Which pillar has had nothing published in 90 days?
- Which launches in projects/ this quarter have no content planned?
- How many pieces are stuck at draft or in-review right now?
- Which keywords in keywords.csv are commercial intent with no target page?
- Which buyer prompts at the decision stage have no piece answering them?
- What's the oldest evergreen piece we still rely on?
- Who owns the most in-flight pieces?
- Which competitors have a battlecard but no comparison page?
- What did the last content-strategy report recommend, and how much of it shipped?
- Which persona do we write for most, and which least?
- Which formats does our voice guide say we shouldn't do?
