# Press releases

**Reads:** `strategy/positioning.md`, `strategy/messaging.md` (boilerplate),
`strategy/product-brief.md`, `brand/voice.md`, `content/` (past releases),
`data/pr/snapshots/` · **Skills:** `/press-release` drafts the release or
a holding statement, `/media-outreach` builds the media list and pitches.
These prompts frame the news first and check it after.

You have news, or someone thinks you do. Before anyone writes "pleased to
announce", you need to know what the story is, why a journalist would
care, which facts you can stand behind and who approved the quotes. You
walk away with the angle, a fact sheet, a checked draft and the questions
press will ask. `/press-release` writes the draft itself.

## Prompts

### Frame the news and build the fact sheet

```
Using this repo, frame the announcement below and build its fact sheet before anyone drafts.

FILL IN
- The news: [what's happening, in two sentences]
- Date: [planned announce date, or "not set"]

CONTEXT
I need to know if this is news to anyone outside the company, what the angle is, and which facts are confirmed.

READ FROM THE REPO
- strategy/positioning.md: category, trends and proof points.
- strategy/product-brief.md, for what the product actually does.
- Past releases in content/ with channel pr, and coverage in data/pr/snapshots/.

BUILD
- The story in one sentence a reporter could use as a headline.
- Why now: the trend from the positioning it ties to.
- Who outside the company cares, and why.
- A fact sheet: every fact with its source, and the facts still missing.
- What we said in past releases that this builds on or contradicts.

OUTPUT
A one-page frame and fact sheet. Then hand it to /press-release.

GROUNDING
Cite paths. A fact with no source goes on the missing list, not the sheet. If this isn't news, say so.
```

### Check every claim in the release

```
Using this repo, check every claim in the press release below.

FILL IN
- Draft: [paste your draft, or give its content/ folder]

CONTEXT
Once it's on the wire it can't be corrected quietly. Every number, superlative and quote must hold up.

READ FROM THE REPO
- strategy/product-brief.md and strategy/positioning.md for product and proof claims.
- The boilerplate in strategy/messaging.md.
- memory/decision-log.md, for approvals and anything embargoed.

CHECK
- Every claim, quoted, with its source or "unsupported".
- Superlatives ("first", "only", "leading") and what backs them.
- Quotes: marked approved or pending, and whose.
- Boilerplate: matches the approved one word for word.

OUTPUT
A table of findings, then the lines to change before it goes out.

GROUNDING
Cite paths. Never supply a number or a quote. A quote with no approval on record is pending.
```

### Write the pitch angles and the press FAQ

```
Using this repo, write the pitch angles and the likely press questions for the announcement.

FILL IN
- Release: [paste the approved draft]
- Spokesperson: [name and title]

CONTEXT
Different outlets want different stories. The spokesperson needs tough questions answered before the interview, not during.

READ FROM THE REPO
- Trends in strategy/positioning.md, for angles beyond the product.
- The battlecards in strategy/competitive/, for the competitor questions.
- The media list in data/pr/snapshots/ if one exists.

BUILD
- Three angles: trade, business, and the trend story, each with a one-line pitch.
- Ten likely questions, including the hard ones (competitors, numbers we won't share, what's missing), with a short answer each.
- What not to say.

OUTPUT
An angles and FAQ document for the spokesperson. If I say pitches, hand the angles to /media-outreach.

GROUNDING
Cite paths. Answers stay within the release and the strategy files. "We don't share that" is an answer; a made-up number isn't.
```

## Advanced prompts

### Cross-examine the release as a skeptical reporter

```
Interview our spokesperson as a skeptical trade reporter who's covered the category for ten years, then tell me where the story breaks. Use this repo for our claims, our competitors and our known weak spots.

FILL IN
- Release: [paste the draft]

CONTEXT
A friendly read always passes. I want the release tested the way the toughest reporter on the list would test it.

FROM THE REPO
- strategy/positioning.md and strategy/product-brief.md, including known weaknesses.
- The battlecards in strategy/competitive/.
- Past coverage in data/pr/snapshots/, for how we've been written about.

METHOD
- As the reporter: read the release and write the ten questions they'd ask, hardest first.
- Answer each as the spokesperson could, using only the repo.
- Mark each answer strong, weak or no answer.
- Write the skeptical paragraph the reporter would publish if the weak answers stand.

OUTPUT
The Q&A with ratings, the paragraph, and the three fixes that close the gaps.

GROUNDING
Answers cite their source path. Questions may use only public facts or what the repo records; no invented scandals.
```

### Run a headline tournament with a reader panel

```
Pick the headline by running a pairwise tournament with a synthetic panel of the readers we want. Use this repo for who those readers are and what they care about.

FILL IN
- Release: [paste the draft]
- Headline options: [paste five to ten]

CONTEXT
The headline decides whether anyone reads the second paragraph. I want the pick made by the readers, not the room.

FROM THE REPO
- The personas in strategy/personas.md.
- The trend and category language in strategy/positioning.md.
- brand/voice.md, for words we don't use.

METHOD
- Build a panel: two personas plus a trade editor.
- Each panelist compares headlines in pairs: which would make them read on, and why.
- Fit a simple Elo ranking per panelist and overall. If you can run code, do it.
- Disqualify any headline that breaks the voice guide or makes an unsupported claim.

OUTPUT
The ranked headlines, the winner, and what the winners have in common.

GROUNDING
Label results as simulated. Each judgement cites the persona or voice section it rests on.
```

## Questions to just ask

- What did our last three press releases announce?
- What's our approved boilerplate?
- Which trend in our positioning is the best hook for this news?
- Which outlets covered us last quarter?
- Is there anything embargoed in the decision log?
- Which proof points can we use publicly?
- Does this release use any word on our voice banned list?
- Which quotes in the draft are still pending approval?
- What did [competitor] announce recently, according to the watch reports?
- Who's the named spokesperson for product news?
- Have we called ourselves "the first" anywhere before?
