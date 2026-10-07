# Messaging audits

**Reads:** `strategy/messaging.md`, `strategy/positioning.md`,
`strategy/personas.md`, `content/`, `memory/transcripts/processed/` ·
**Skills:** `/review` checks one draft before it ships, `/web-copy-audit`
checks the live site. These prompts audit everything else: decks, sales
assets, campaigns and how the story holds across them.

You rewrote the messaging last quarter. Did anyone notice? The site says
one thing, the sales deck says another, and the nurture still uses last
year's pillars. You walk away with a list of what drifted, where, by how
much, and who owns the fix, plus the gaps in the framework itself. For a
single draft, `/review` is faster.

## Prompts

### Catch drift from the approved messaging

```
Using this repo, check the asset below against our approved messaging and list where it drifts.

FILL IN
- Asset: [paste your draft, or give a content/ folder]
- Audience: [persona]

CONTEXT
This asset is already in use. I want to know whether it tells our current story, not whether it reads well.

READ FROM THE REPO
- strategy/messaging.md: the core narrative, pillars, the persona's value proposition and the matrix row for their stage.
- strategy/positioning.md: category, alternatives and unique attributes.
- memory/decision-log.md, for messaging changes since the asset was written.

CHECK
- Which pillar each section advances, or none.
- Lines that use retired language or contradict the positioning.
- The persona's value proposition: present, weak or missing.
- Category and competitor framing that doesn't match.

OUTPUT
A table: line quoted, the problem, the approved wording it should follow, severity. Then a clean rewrite of the three worst lines.

GROUNDING
Cite the section of the strategy file behind every finding. Don't invent new messaging; if the framework has no answer, list it as a framework gap.
```

### Check the asset speaks like customers

```
Using this repo, compare the language in the asset below with how customers actually talk.

FILL IN
- Asset: [paste your draft]

CONTEXT
Our copy drifts into our own jargon. I want to see where the asset uses our words and where buyers use different ones.

READ FROM THE REPO
- Call transcripts in memory/transcripts/processed/.
- Any customer language file in memory/knowledge/.
- Review exports in data/reviews/snapshots/.

COMPARE
- Ten key phrases from the asset, each with how customers say the same thing, quoted and cited.
- Phrases customers never use.
- Customer phrases the asset should borrow.

OUTPUT
A two-column word swap table with sources.

GROUNDING
Customer phrases are verbatim with the file path. If there are fewer than five transcripts, say the sample is thin.
```

### Find the gaps in the messaging framework

```
Using this repo, find what our messaging framework doesn't cover.

CONTEXT
Before I audit assets, I want to know where the framework itself is thin, so I don't blame writers for gaps in the source.

READ FROM THE REPO
- strategy/messaging.md, every section.
- strategy/personas.md, for personas and their objections.
- Loss drivers in the coded win/loss file in data/crm/snapshots/ and objections in memory/transcripts/processed/.

BUILD
- Persona by stage cells in the matrix that are empty or generic.
- Objections buyers raise that the objection section doesn't answer, with how often.
- Pillars with no proof point.
- Personas with no value proposition.

OUTPUT
A gap list ranked by deals affected, ready to hand to /messaging-house.

GROUNDING
Cite paths and counts. Don't fill the gaps here; name them.
```

### Assemble the audit across assets

```
Using this repo, assemble a messaging audit across the assets below.

FILL IN
- Assets: [list content/ folders, URLs, or paste the findings already run]

CONTEXT
Leadership wants one view: how on-message are we, where, and who fixes what.

READ FROM THE REPO
- Each asset's frontmatter in content/ for owner and channel.
- strategy/messaging.md for the pillars to score against.
- integrations/tasks.md for where fixes go.

BUILD
- A scorecard: asset, channel, owner, pillar coverage, drift count, severity.
- The three patterns that repeat across assets.
- A fix list grouped by owner, filed as tasks per integrations/tasks.md once I approve.

OUTPUT
The audit as report.md in a new reports/adhoc/ folder, on a branch.

GROUNDING
Cite paths. Scores follow a rubric you state up front. Don't file tasks until I say go.
```

## Advanced prompts

### Run a recall test on a synthetic buying committee

```
Test whether buyers would remember our message after one read, using a synthetic buying committee built from our personas. Use this repo for the personas, the pillars and their own words.

FILL IN
- Asset: [paste your draft]

CONTEXT
A message nobody remembers is a message that failed. I can't afford a panel for every asset, so I want a disciplined proxy before we spend on distribution.

FROM THE REPO
- The personas in strategy/personas.md, as the committee members.
- The pillars and core narrative in strategy/messaging.md, as the answer key.
- Their language from memory/transcripts/processed/.

METHOD
- Build one reader per persona, constrained to their goals, pains and vocabulary from the file.
- Each reads the asset once, then answers cold: what does this company do, why is it different, what would you tell a colleague?
- Score recall against the answer key: pillar named, paraphrased or missing.
- Run each reader three times with varied framing and report the spread.
- Say where the committee agrees and where one persona misses everything.

OUTPUT
A recall table per persona and pillar, the spread, and the edit most likely to raise recall.

GROUNDING
Label results as simulated. Each reader's reasoning cites the persona section it draws on. This is a proxy, not evidence; say so in the output.
```

### Size an A/B test for the new message

```
Work out whether we can test the new message against the old one with the traffic we have. Use this repo for the baseline conversion rate and the traffic.

FILL IN
- Page or email: [the page URL or campaign]
- Smallest lift worth acting on: [e.g. 15% relative]

CONTEXT
Everyone wants to "just test it". On low traffic a test can run for months and prove nothing. I want the numbers before we start.

FROM THE REPO
- Baseline traffic and conversions from data/analytics/snapshots/ or data/email/snapshots/.
- What counts as a conversion in data/ontology/metrics.md.

METHOD
- Compute the sample size per arm for 80% power at 5% significance, two-sided.
- Convert it to weeks at current traffic.
- If it's too long, show what lift or what metric (a higher-volume step) makes it feasible.
- If you can run code, show the calculation.

OUTPUT
Sample size, weeks to answer, and a go, change or don't verdict. If go, hand it to /ab-test-plan.

GROUNDING
Label every number as repo (path), mine, or your calculation. With no baseline snapshot, say which export to drop and stop.
```

## Questions to just ask

- Which pillar does our homepage lead with?
- Which content pieces were published before the last messaging change?
- What does our messaging say to [persona] at the [stage] stage?
- Which objections in our messaging have no proof?
- Which words in our messaging do customers never use on calls?
- Which persona has no value proposition in the messaging?
- When was strategy/messaging.md last reviewed, and by whom?
- Does the boilerplate match the positioning statement?
- Which pieces in content/ mention a pillar we retired?
- Which campaign variations in our messaging are still in use?
- What did the decision log say when we changed the core narrative?
- Which sales assets in content/ have channel "sales" and are older than six months?
