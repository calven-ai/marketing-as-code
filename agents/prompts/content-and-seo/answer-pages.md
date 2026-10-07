# Answer pages

**Reads:** `data/seo/prompts.csv`, `data/seo/snapshots/` (AI answer mentions),
`reports/recurring/mentions/`, `strategy/messaging.md`, `content/`
· **Skills:** `/prompt-set-builder` grows the buyer prompt set,
`/brand-monitor` checks who AI answer engines cite, and
`/aeo-page-optimize` makes one page citable; these prompts decide which
questions to own and write the pages between them.

A buyer asks an AI tool which [category] vendor to shortlist and your name
isn't in the answer. You walk away with a short list of questions worth
owning, a page for each that answers it in the first two sentences with
proof, and a way to tell whether it worked. The skills measure and polish.
The prompts pick the battles and write the answers.

## Prompts

### Pick the questions worth owning

```
Using this repo, pick the buyer questions where an answer page would move us most.

CONTEXT
I want to choose five questions to write for this quarter.

READ FROM THE REPO
- Every row in data/seo/prompts.csv, with persona and stage.
- The newest AEO results snapshot (the `*-aeo-results.csv` file) in data/seo/snapshots/ and the latest report in reports/recurring/mentions/.
- What we've published in content/ that answers each one.

BUILD
- A table: prompt, persona, stage, are we cited (yes, no, unknown), who is cited instead, our page that answers it (path or none).
- The five where we're not cited, the stage is consideration or decision, and we have something true to say.
- Prompts the set is missing for a persona, to hand to /prompt-set-builder.

OUTPUT
The table and the five picks with a reason each.

GROUNDING
Cite paths. Never claim a citation that isn't in a snapshot. If there's no mentions snapshot, say "unknown" and suggest /brand-monitor.
```

### Write an answer page

```
Using this repo, draft a page that answers one buyer question directly.

FILL IN
- Question: [a prompt from prompts.csv]
- Piece: [piece folder from /new-content]

CONTEXT
Answer engines quote passages that stand alone. The answer goes first, the proof right after.

READ FROM THE REPO
- strategy/messaging.md and strategy/product-brief.md, for what's true and approved.
- The persona for the question in strategy/personas.md.
- brand/voice.md.

WRITE
- A two-sentence direct answer under a heading phrased as the question.
- Three to five sections, each answering a follow-up question the persona would ask, each self-contained.
- One proof point per section, cited.
- A short "who this isn't for" section, if honest.

OUTPUT
The draft in the piece's draft.md on a branch, then run /aeo-page-optimize on it.

GROUNDING
Every factual line traces to a strategy file. Don't invent statistics, customers or capabilities to sound authoritative.
```

### Check a batch of existing pages for citability

```
Using this repo, check which of our pages could be quoted as an answer and which couldn't.

FILL IN
- Pages: [paste the list of piece folders or URLs]

CONTEXT
Some pages bury the answer under three paragraphs of setup. I want to know which.

READ FROM THE REPO
- Each page's draft in content/.
- The prompts each should answer in data/seo/prompts.csv.

SCORE
- Answer in the first two sentences: yes or no.
- Headings phrased as questions buyers ask.
- Claims that stand alone without the surrounding paragraph.
- Proof cited in the passage, not only at the end.

OUTPUT
A scorecard table, worst first, with the one fix that matters most per page.

GROUNDING
Quote the line each score rests on. Score only what's in the draft.
```

## Advanced prompts

### Simulate an answer engine choosing a source

```
Simulate how an AI answer engine would pick sources for our target question, and test whether our draft would make the cut. Use this repo for the question, our draft and who gets cited today.

FILL IN
- Question: [a prompt from prompts.csv]
- Draft: [piece]
- Competing pages: [paste the passages or URLs cited today, if you have them]

CONTEXT
I can't see inside the engines. I can approximate how retrieval and synthesis treat passages, and fix the obvious losers.

FROM THE REPO
- The question's row in data/seo/prompts.csv.
- Who is cited for it in the newest AEO results snapshot (the `*-aeo-results.csv` file) in data/seo/snapshots/.
- Our draft in content/.

METHOD
- Split our draft and the competing pages into passages of about 100 words.
- Score each passage for the question: does it answer directly, name entities, state a specific fact, stand alone without context.
- Rank all passages and pick the top three an engine would most likely quote. Explain each pick.
- Rewrite our weakest passage to beat the top competitor passage and re-score.
- Run it three times with the passages in a different order to check the ranking is stable.

OUTPUT
The ranked passages with scores, where ours land, and the rewritten passage.

GROUNDING
Label this as a simulation, not a measurement. Cite the snapshot for who is cited today. Only /brand-monitor's next run tells us if it worked.
```

## Questions to just ask

- Which buyer prompts are we cited for, and which not?
- Who gets cited most for decision-stage prompts?
- Which personas have no prompts in prompts.csv?
- What did the last mentions report say changed?
- Which of our pages answer [question] today?
- Which prompts mention a competitor by name?
- What's our share of citations this month versus last?
- Which prompts were retired in prompts.csv, and why?
- Does [piece] answer the question in its first two sentences?
- What proof do we have that an answer engine could quote for [pillar]?
- Which prompts have a page from us that still isn't cited?
