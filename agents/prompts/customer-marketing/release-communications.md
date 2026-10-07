# Release communications

**Reads:** `strategy/product-brief.md`, `strategy/personas.md`,
`strategy/messaging.md`, `brand/voice.md`, `content/` (past release posts
and newsletters), `memory/transcripts/processed/`,
`strategy/competitive/` · **Skills:** `/release-notes-to-marketing` turns a
changelog into email, post and blog drafts, and `/newsletter` assembles the
monthly issue; these prompts find who to tell, what the change makes wrong,
and how it lands against competitors.

The product team shipped something. The changelog says "added bulk
export", and that means nothing to the persona who's been asking for it for
a year. You walk away with release copy in that persona's words, a list of
customers who asked for it, and a sweep of every page and asset the change
just made out of date. For the drafts, run `/release-notes-to-marketing`.

## Prompts

### Tell the customers who asked for it

```
Using this repo, find the customers who asked for the change below and draft a note to each.

FILL IN
- Change: [paste the changelog entry]

CONTEXT
Telling someone "you asked, we built it" is the best release email there is. I need to know who asked.

READ FROM THE REPO
- Calls in memory/transcripts/processed/ that mention the need.
- Reviews and survey answers in data/reviews/snapshots/ and community digests in reports/recurring/community/.
- Account owners in data/crm/snapshots/.

BUILD
- A list: account, what they said, where, owner.
- A short note per account, opening with their words, ready for the owner to send.

OUTPUT
The table, then the notes. Save as a content draft on a branch if I say save.

GROUNDING
Cite the file behind each request. Quote verbatim. Don't send; owners do.
```

### Find what the change made wrong

```
Using this repo, find every page, asset and strategy line the change below makes out of date.

FILL IN
- Change: [paste the changelog entry]

CONTEXT
A release fixes one thing and quietly breaks ten claims: the comparison page, a battlecard weakness, a sales FAQ.

READ FROM THE REPO
- strategy/product-brief.md (capabilities, known weaknesses).
- Battlecards in strategy/competitive/ that list this as a gap.
- Published content in content/ that mentions the capability.

BUILD
- A list: file, the line, why it's now wrong, the fix.
- Which fixes are a cascade (positioning, messaging) that need review, and which are simple edits.

OUTPUT
The list, with the simple fixes proposed as one diff on a branch and the cascade listed for review.

GROUNDING
Cite paths and lines. Don't edit strategy files without listing what inherits them. If the changelog is vague about scope, ask before marking a claim wrong.
```

### Write the release in the persona's words

```
Using this repo, write the customer-facing release note for the change below, in the words of the persona who uses it.

FILL IN
- Change: [paste the changelog entry]
- Persona: [persona]

CONTEXT
Engineers wrote the changelog. The persona cares about what they can now do that they couldn't.

READ FROM THE REPO
- The persona's goals and language in strategy/personas.md.
- The pillar this change proves in strategy/messaging.md.
- brand/voice.md.

WRITE
- A headline about the outcome, not the feature.
- Three sentences: what changed, why it matters to them, what to do next.
- A line for the next newsletter.

OUTPUT
The note and the newsletter line.

GROUNDING
Cite paths. Describe the change only as the changelog and the product brief do. No invented benefits or metrics.
```

## Advanced prompts

### War-game the release against a competitor

```
War-game the release: how will the competitor respond, and what do we say then? Use this repo for the competitor's position and our story.

FILL IN
- Change: [paste the changelog entry]
- Competitor: [competitor]

CONTEXT
If this closes a gap they've been selling against, they'll reframe. I want our next move ready before theirs.

FROM THE REPO
- The competitor's battlecard in strategy/competitive/, including how they position against us.
- The latest competitor watch in reports/recurring/competitive/.
- Our positioning in strategy/positioning.md.

WAR-GAME
- Round 1: we announce. What the competitor's sales team says the next day, three likely lines.
- Round 2: our response to each, with proof.
- Round 3: their counter. Where do they still win?
- Score each exchange: we gain, neutral, they gain.

OUTPUT
A three-round table and the two lines sales should have ready, plus battlecard edits proposed on a branch.

GROUNDING
Label every point as repo (file path), mine, or your assumption. Competitor moves are hypotheses, not facts; never present one as something they said.
```

## Questions to just ask

- Which customers asked for [capability] on calls?
- Which battlecards list [capability] as our weakness?
- Which published pages mention [capability]?
- What did we ship this month, per project status?
- Which persona cares most about [capability]?
- Has the product brief been updated since the last release?
- What went into last month's customer newsletter?
- Which pillar does this release prove?
- Which comparison pages need an update after this release?
- Who owns the accounts that asked for [capability]?
- Is there an embargo or date decision logged for this release?
- Which release posts from last quarter got the most clicks?
