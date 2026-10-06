# Campaign briefs

**Reads:** `strategy/` (positioning, messaging, ICP, personas, `competitive/`),
`projects/<campaign>/campaign.md`, the discovery report in `reports/adhoc/`,
`content/` frontmatter · **Skills:** `/campaign-discovery` researches the
idea and `/campaign-plan` writes the campaign folder; these prompts sharpen
the angle and test the brief before money goes behind it.

You've got a campaign idea and a budget conversation next week. Everyone
who touches it, the writer, the designer, the agency, will work from the
brief, so a vague brief turns into five different campaigns. You walk away
with one angle you can defend, a competitive frame, and a brief that's
been checked against the approved story and pressure-tested as the buyer.
If there's no discovery report yet, run `/campaign-discovery` first; if you
want the full folder with calendar and UTMs, `/campaign-plan` does that.

## Prompts

### Find the strongest campaign angle

```
Using this repo, give me three candidate angles for the campaign below and pick the strongest.

FILL IN
- Campaign: [campaign]
- Persona: [persona]
- Goal: [the one number and date the campaign answers to]

CONTEXT
I need one angle before I brief anyone. It has to be true, provable, and something the persona already cares about.

READ FROM THE REPO
- The persona's pains, triggers and objections in strategy/personas.md.
- The pillars and proof points in strategy/messaging.md.
- The discovery report for this campaign in reports/adhoc/, if there is one.

BUILD
- Three angles, each one sentence, each tied to one pillar and one persona pain.
- For each: the proof we hold, the objection it invites, and whether we have content that already backs it.
- A pick, with the reason, and what would make you change your mind.

OUTPUT
A short table, then the pick in three lines. Show it here.

GROUNDING
Cite the file path behind every pain, pillar and proof point. Do not invent proof. If the persona or messaging file is still a template, stop and tell me to run /setup.
```

### Set the competitive frame

```
Using this repo, set the competitive frame for the campaign below.

FILL IN
- Campaign: [campaign]
- Competitor: [competitor]

CONTEXT
The persona will compare us to someone. I want the brief to say who, on what, and where we don't pick a fight.

READ FROM THE REPO
- The competitor's battlecard in strategy/competitive/.
- Our positioning in strategy/positioning.md.
- The latest competitor watch in reports/recurring/competitive/, if any.

BUILD
- The alternative the persona weighs us against, in their words.
- Where we win, with proof, and where they're stronger.
- Two claims the campaign can make safely and one it must avoid.

OUTPUT
A frame section I can paste into the brief.

GROUNDING
Cite paths. Never invent a competitor's price, feature or customer. If the battlecard is older than 90 days, say so before using it.
```

### Check an agency brief against the story

```
Using this repo, check the brief below against our approved story before it goes to the agency.

FILL IN
- Brief: [paste your draft]

CONTEXT
An agency will take this literally. Anything off-message or unprovable in the brief ends up in the ads.

READ FROM THE REPO
- strategy/positioning.md and strategy/messaging.md.
- The target persona in strategy/personas.md and the tier in strategy/icp.md.
- brand/voice.md.

CHECK
- Every claim: supported, unsupported, or contradicted, with the source.
- Persona and tier: do they match how the repo defines them?
- KPIs: is each one a term defined in data/ontology/metrics.md?
- Voice: lines that break brand/voice.md.

OUTPUT
An annotated list of findings, then a corrected brief. Propose it on a branch if I say save.

GROUNDING
Cite the path for every finding. Don't soften a contradiction. A KPI the ontology doesn't define is an open question, not a number you pick.
```

## Advanced prompts

### Run a pre-mortem on the campaign

```
Run a pre-mortem: it's three months from now and this campaign failed. Tell me why, before I fund it. Use this repo for the persona, the competitive picture and what past campaigns taught us.

FILL IN
- Campaign: [campaign]
- Budget and timeline: [the plan, or paste campaign.md]

CONTEXT
Plans get approved on optimism. I want the most likely failure modes named while they're still cheap to fix.

FROM THE REPO
- The campaign's brief in projects/.
- Past retros in reports/adhoc/ and the playbooks in memory/knowledge/.
- The persona and the competitor's battlecard in strategy/.

METHOD
- Write five failure stories, each a different cause: wrong audience, weak offer, competitor response, channel didn't reach them, sales didn't follow up.
- For each: the early warning sign in week two, its likelihood (low, medium, high) and the cheapest prevention.
- Check each against past retros: has this failed here before?
- Rank by likelihood times cost.

OUTPUT
A ranked table of failure modes with warning sign and prevention, then the three changes to make to the brief now.

GROUNDING
Label every point as repo (with file path), mine, or your assumption. Don't cite a past failure that isn't in a retro or the decision log.
```

### Put the brief in front of a synthetic buying committee

```
Put the campaign brief in front of a synthetic buying committee and tell me who it loses. Use this repo for the personas and the objections on record.

FILL IN
- Brief: [paste the brief or name its folder in projects/]
- Segment: [segment]

CONTEXT
A campaign that wins the user and loses the budget holder generates leads that never close.

FROM THE REPO
- Every persona in strategy/personas.md who sits in a deal for this segment, with their goals and objections.
- How the segment buys in strategy/icp.md.
- Objections heard on calls in memory/transcripts/processed/, if any.

METHOD
- Build one committee member per persona, using only what the persona file says.
- Each reads the brief's message and offer and answers: would I click, would I forward it, what would stop me.
- Then run the room: who blocks, who champions, what the champion needs to win the argument.
- Score each member: engaged, neutral, blocks.

OUTPUT
A table per member with their reaction and the line that caused it, then two edits that move a blocker to neutral.

GROUNDING
Every reaction cites the persona line it rests on. Where the persona file is silent, say "the file doesn't say" instead of inventing a reaction.
```

## Questions to just ask

- Which persona is this campaign for, and does the messaging have a pillar for them?
- What proof points can we use for [pillar] without asking anyone?
- Which content do we already have that this campaign could link to?
- What did the last campaign aimed at [persona] get wrong, per its retro?
- Which competitor shows up most in the battlecards for [segment]?
- Is there a discovery report for [campaign] yet?
- Which KPIs in this brief aren't defined in the ontology?
- What did we decide about [campaign] in the decision log?
- Which claims in our messaging have no proof point attached?
- Which objections does [persona] raise that no campaign has addressed?
- What's the UTM slug pattern for a new campaign?
- Who owns [campaign], and what's its latest status entry?
