# Content briefs

**Reads:** `strategy/messaging.md`, `strategy/personas.md`,
`data/seo/keywords.csv`, `content/` frontmatter, `memory/transcripts/processed/`
· **Skills:** `/new-content` scaffolds the folder and `/content-brief` fills
the brief; these prompts pick the angle before it and pressure-test the
brief after.

A writer, or an agency, is starting Monday and needs a brief they can run
with without a call. You walk away with a brief that names one persona, one
pillar, one keyword, the argument and the proof, and that doesn't repeat
something you published last year. The skill fills the template. The work
around it is deciding whether the piece deserves to exist, finding the
buyer's words, and checking the brief would survive a sceptical reader.

## Prompts

### Decide whether the piece should exist

```
Using this repo, tell me whether this piece is worth briefing and what its job is.

FILL IN
- Idea: [one sentence on the piece]
- Keyword: [keyword, or "none"]

CONTEXT
I don't want to brief a piece with no job, or one we've already written.

READ FROM THE REPO
- The pillars and buying stages in strategy/messaging.md.
- Every piece in content/ by frontmatter: channel, status, title, and the brief's keyword.
- The keyword's row in data/seo/keywords.csv, if it has one.

BUILD
- The pillar and persona it serves, or "none" if it serves neither.
- Pieces that already cover it, with status and path, and whether to refresh one of those instead.
- If the keyword has no row in keywords.csv: the row to propose, with intent.

OUTPUT
A go, refresh-instead, or drop verdict with the reasons, then the next step (run /new-content and /content-brief, or the refresh brief for the existing path).

GROUNDING
Cite paths. Never estimate a volume or a rank; if keywords.csv has none, say so.
```

### Find the buyer's words for the brief

```
Using this repo, collect the language the brief should be written in.

FILL IN
- Persona: [persona]
- Topic: [the problem the piece addresses]

CONTEXT
Briefs written in our words get pieces buyers skim past. I want theirs.

READ FROM THE REPO
- The persona's section in strategy/personas.md: pains, objections, the words they use.
- Calls in memory/transcripts/processed/ where the topic comes up.
- The buyer questions for this persona in data/seo/prompts.csv.

BUILD
- Ten verbatim phrases the persona uses for the problem, each with its transcript path.
- The three questions they ask before they'd act, in their phrasing.
- Words our messaging uses that they never do.

OUTPUT
A short language sheet to paste into the brief's sources section.

GROUNDING
Quotes verbatim with paths. If no call covers the topic, say so and don't paraphrase the persona file into fake quotes.
```

### Review a finished brief before it goes to the writer

```
Using this repo, review this brief the way a demanding editor would.

FILL IN
- Brief: [piece folder in content/, or paste the brief]

CONTEXT
The writer should be able to work from this without asking anything.

READ FROM THE REPO
- strategy/messaging.md and strategy/personas.md.
- brand/voice.md.
- data/seo/keywords.csv for the target keyword.

CHECK
- One persona, one pillar, one thing the reader should think or do after.
- The argument is a claim someone could disagree with, not a topic.
- Every proof point named has a source in the repo.
- The outline answers the persona's top objection somewhere.
- The keyword is a row in keywords.csv and the intent matches the format.

OUTPUT
Findings as a numbered list, blocking first. No rewrite unless I ask.

GROUNDING
Cite the file behind each finding. Don't invent proof to fill a gap; name what's missing.
```

## Advanced prompts

### Run the brief past a synthetic reader panel

```
Test the brief's argument on a panel of simulated readers before anyone writes a word. Use this repo for who the readers are and what they believe.

FILL IN
- Brief: [piece folder in content/]
- Panel size: [e.g. 5]

CONTEXT
A weak angle costs a writer a week and earns nothing. I'd rather find out now.

FROM THE REPO
- The target persona and one adjacent persona from strategy/personas.md: role, pains, objections, what they distrust.
- The ICP segments in strategy/icp.md, to vary company size and context across the panel.
- The competitor the reader most likely knows, from strategy/competitive/.

METHOD
- Build the panel: each reader a persona plus a segment plus one stated prior belief, all traced to the persona file.
- Show each reader the title, the argument and the outline. Each says whether they'd click, where they'd stop, and the objection they'd raise, in their voice.
- Tally: click intent, the most common stopping point, objections the outline doesn't answer.
- Rewrite the argument once to answer the top objection and re-run the panel on the new version.

OUTPUT
A table per reader (click, stop point, objection), the before and after argument, and the outline changes.

GROUNDING
Label every reader trait as repo (with path) or your assumption. This is a simulation, not research: never report it as what buyers said.
```

## Questions to just ask

- Have we already written about [keyword]? Show the paths and statuses.
- Which pillar in our messaging has the fewest published pieces?
- What does [persona] worry about most, according to our personas?
- Which buyer prompts in prompts.csv have no piece answering them?
- Is [keyword] in keywords.csv, and what page targets it?
- Which briefs in content/ are still at status brief after a month?
- What proof do we have for [pillar] that a writer can cite?
- Which keywords in keywords.csv have no target_url yet?
- What did customers say about [topic] on calls this quarter?
- Which personas have nothing at the decision stage?
- What's the target keyword and persona in the brief for [piece]?
- Does this title match our voice? [paste the title]
