# Customer evidence packs

**Reads:** `memory/transcripts/processed/`, `memory/knowledge/`,
`data/reviews/snapshots/`, `data/crm/snapshots/`, `content/` (case
studies), `strategy/messaging.md` · **Skills:** `/voice-of-customer`
turns raw feedback into themes, `/case-study` writes one customer's story.
These prompts pull the evidence across customers for a specific asset.

You're building a page, a deck or an objection doc and you need proof: a
quote for the pricing slide, three outcomes for the security pillar, a
customer who switched from a competitor. It's somewhere in forty call
transcripts. You walk away with an evidence pack grouped by theme or
pillar, every line cited, each marked approved for public use or internal
only.

## Prompts

### Assemble an evidence pack on a theme

```
Using this repo, assemble the customer evidence on the theme below.

FILL IN
- Theme or pillar: [pillar, or a topic like onboarding or switching]
- Use: [the asset it's for, internal or public]

CONTEXT
I need the best quotes, outcomes and stories on one theme, ready to drop into an asset.

READ FROM THE REPO
- Call transcripts in memory/transcripts/processed/.
- Review exports in data/reviews/snapshots/.
- Case studies in content/ with channel case-study, and any customer language file in memory/knowledge/.

BUILD
- Ten quotes on the theme, verbatim, each with source path, role and segment where recorded.
- Outcomes with numbers, each with its source.
- Two short stories: situation, change, result.
- For each item: approved for public use (a signed-off case study or public review) or internal only.

OUTPUT
An evidence pack grouped by sub-theme.

GROUNDING
Quotes verbatim with the file path. Never trim a quote so it says more than the speaker did. Without approval on record, an item is internal only.
```

### Pull the proof from won deals

```
Using this repo, pull the evidence from deals we won in the window below.

FILL IN
- Window: [window]
- Segment: [segment, or "all"]

CONTEXT
I want to know why customers chose us, in their words, for a sales deck and the messaging proof column.

READ FROM THE REPO
- Won deals in the closed-deals snapshot and coded win/loss file in data/crm/snapshots/.
- Calls for those deals in memory/transcripts/processed/.

BUILD
- A table: deal, segment, primary win driver, the best line from the buyer, source path.
- The three drivers that appear most, each with its two strongest quotes.
- Won deals with no call on record.

OUTPUT
The table and the top-three summary.

GROUNDING
Cite paths. Company names stay internal. Drivers come from the coded file, not your reading.
```

### Map proof coverage against what costs deals

```
Using this repo, map where we have proof and where we don't, against what buyers object to.

CONTEXT
We have lots of quotes about ease of use and none about security. I want to find the holes before sales does.

READ FROM THE REPO
- Pillars and objections in strategy/messaging.md.
- Loss drivers in the coded win/loss file in data/crm/snapshots/.
- Evidence in memory/transcripts/processed/, data/reviews/snapshots/ and case studies in content/.

BUILD
- A grid: each pillar and each top objection, with count of public proof, internal proof and none.
- The three gaps tied to the most lost deals.
- For each gap: which customers might supply the proof, from the transcripts.

OUTPUT
The grid and a short ask list for customer marketing.

GROUNDING
Cite paths and counts. Don't name a customer as a likely source unless a transcript shows them speaking to that theme.
```

## Advanced prompts

### Rank quotes in a credibility tournament

```
Rank the candidate quotes for this asset by how credible a skeptical buyer would find them, using a pairwise tournament. Use this repo for the quotes and the personas who'll read them.

FILL IN
- Asset: [what it's for]
- Reader: [persona]

CONTEXT
I have twenty quotes and room for three. Gut feel picks the most enthusiastic, which buyers trust least.

FROM THE REPO
- Candidate quotes from memory/transcripts/processed/ and data/reviews/snapshots/.
- The reader persona in strategy/personas.md: role, skepticism, what proof they trust.

METHOD
- Compare quotes in pairs from the persona's point of view: which is more believable and relevant, and why.
- Judge on specificity, speaker seniority, a number, an admitted downside, match to the persona's pain.
- Fit a Bradley-Terry or Elo ranking from the pairwise results. If you can run code, do it in Python.
- Report the top five with the reason each won.

OUTPUT
The ranked list with scores, the winning three, and the pattern in what lost.

GROUNDING
Label judgements as simulated from the persona file. Quotes verbatim with paths.
```

### Audit the pack for selection bias

```
Audit this evidence pack for selection bias before it goes to leadership. Use this repo for the full set of customers and feedback it was drawn from.

FILL IN
- Pack: [paste the evidence pack]

CONTEXT
Packs get built from the happiest customers. If leadership reads it as "what customers think", we'll make bad calls.

FROM THE REPO
- Every transcript in memory/transcripts/processed/ and review export in data/reviews/snapshots/ in the window.
- The customer base snapshot in data/crm/snapshots/, for segment mix.

METHOD
- Compare the pack's mix (segment, size, tenure, sentiment) with the full base and the full feedback set.
- Count negative or mixed feedback on the same themes that the pack left out.
- Say which conclusions survive with the full set and which don't.

OUTPUT
A bias table (pack versus population), the left-out counter-evidence, and a corrected one-line takeaway.

GROUNDING
Label every number as repo (path and n), or your calculation. If there's no customer base snapshot, say which export to drop in data/crm/snapshots/.
```

## Questions to just ask

- What did customers say about onboarding on calls? Quote three.
- Which case studies are approved for public use?
- Do we have a quote from a [persona] about [pillar]?
- Which customers switched from [competitor], according to the transcripts?
- Which pillar has the least proof?
- What's the most-repeated phrase in our reviews?
- Which won deals in [segment] had a call recorded?
- What outcomes with numbers do we have on record?
- Which reviews mention price, and what do they say?
- Is there a customer language file in memory/knowledge/?
- Which objection in our messaging has no customer quote behind it?
- Which quotes appear in more than one published piece?
