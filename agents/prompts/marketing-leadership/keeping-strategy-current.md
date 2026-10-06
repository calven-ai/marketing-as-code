# Keeping strategy current

**Reads:** `strategy/`, `brand/`, `memory/decision-log.md`,
`memory/knowledge/`, `reports/recurring/context/` · **Skills:**
`/context-freshness` runs the monthly pass; `/positioning-refresh`,
`/messaging-house`, `/icp-refresh` and `/persona-builder` rewrite a file.
These prompts help you decide which one to run and when.

Every agent in this repo reads `strategy/` before it writes anything, so a
stale positioning file doesn't sit quietly in a drawer: it shows up in every
draft, brief and battlecard. You're the one who decides when the story
changes. You walk away knowing which files have drifted from what the team
has learned, which change would cascade furthest, and what to refresh first.

## Prompts

### Find where strategy and reality disagree

```
Using this repo, find where our strategy files disagree with what we've decided and learned since they were last reviewed.

CONTEXT
Lint tells me what's past 90 days. I want the harder part: what's wrong, not just old.

READ FROM THE REPO
- Every file in strategy/ and brand/voice.md, with last_reviewed.
- Decision-log entries dated after each file's last_reviewed, and the files in memory/knowledge/.
- The newest win/loss report in reports/adhoc/ and the newest competitor watch in reports/recurring/competitive/.

BUILD
- A table: strategy file, section, what it says, what the newer evidence says, evidence path.
- Contradictions between strategy files themselves, e.g. a persona the ICP doesn't target.
- Which refresh skill fixes each one.

OUTPUT
The table, sorted by how many other files inherit the section. Show it here.

GROUNDING
Cite both sides of every contradiction. Absence of evidence isn't a contradiction; mark it "no new evidence".
```

### Map the cascade before you change positioning

```
Using this repo, list everything that inherits from the change below before I approve it.

FILL IN
- Change: [paste the proposed positioning or messaging change, or the branch name]

CONTEXT
A positioning change touches messaging, personas, battlecards and published content. I want the whole list before it merges.

READ FROM THE REPO
- strategy/messaging.md, strategy/personas.md and every card in strategy/competitive/.
- Published and in-flight pieces in content/ (frontmatter status).
- Live campaigns in projects/.

BUILD
- Per inheriting file or piece: the line that would now be wrong, and whether it needs a rewrite or a word change.
- Published pieces that would contradict the new positioning, ranked by traffic if a web analytics snapshot exists in data/analytics/snapshots/.
- A suggested order of work.

OUTPUT
The cascade list, ready to paste into the proposal description.

GROUNDING
Cite file and line. Don't edit anything; list it. A piece with no traffic data is listed without a rank, not guessed.
```

## Advanced prompts

### War-game the story against the market

```
War-game our positioning against the competitors' likely next moves, and tell me which part of our story breaks first. Use this repo for our positioning, the battlecards and what competitors did recently.

FILL IN
- Horizon: [e.g. the next two quarters]

CONTEXT
Positioning is a bet on how the market will look. I want to know which assumption is most exposed before a competitor exposes it in a deal.

FROM THE REPO
- strategy/positioning.md: alternatives, unique attributes, value themes, best-fit customer.
- Every battlecard in strategy/competitive/ and the competitor watch reports in reports/recurring/competitive/.
- Win/loss drivers from the newest win/loss report in reports/adhoc/.

METHOD
- For each competitor, play their strategist: given their recent moves on record, what are their two most likely moves in the horizon (price, feature, segment, message)?
- Play each move against our positioning: which unique attribute or value theme does it neutralise?
- Play our response: what would we say, and does our proof hold?
- Score each of our positioning claims on exposure (how many plausible moves hit it) and proof strength.

OUTPUT
A matrix of competitor moves against our positioning claims, then the claim most exposed, the evidence we'd need to defend it, and whether to run /positioning-refresh now.

GROUNDING
Label every point as repo (file path), or your inference. Competitor moves must extend something on record; a move with no basis in their battlecard or watch reports is marked speculative.
```

## Questions to just ask

- Which files in strategy/ are past 90 days, and who owns them?
- What have we decided since positioning.md was last reviewed?
- Does any persona in personas.md fall outside the ICP?
- Which battlecards are older than our last loss to that competitor?
- Which proof points in messaging.md have no source?
- Is any strategy file still a template?
- What does the latest context-freshness report say we should refresh?
- Which published pieces still use a pillar messaging.md no longer has?
- Which knowledge files contradict the product brief?
- If I changed our best-fit customer, which files would I have to touch?
