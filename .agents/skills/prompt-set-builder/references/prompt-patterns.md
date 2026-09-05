# Prompt patterns by buying stage

What a buyer types into an answer engine at each stage, and which shapes
tend to produce answers that name vendors (the only prompts worth
tracking for citations). `persona` and `stage` in `data/seo/prompts.csv`
come from `strategy/personas.md` and `strategy/messaging.md`.

## Awareness (the problem, not the product)

- "How do [role]s keep [the thing that goes wrong] from happening?"
- "Why does [symptom] happen in [team type]?"
- "What is [category] and do we need it?"

Answers here often cite guides, not vendors. Keep one or two per persona
for the citation of our content, not of our brand.

## Consideration (the category and its shapes)

- "What are the best [category] tools for [team size or type]?"
- "Which [category] platforms work with [system they already use]?"
- "What should I look for in a [category] tool?"
- "[Approach A] or [approach B] for [job to be done]?"

These name vendors. Most of the set belongs here.

## Decision (the shortlist)

- "[Competitor] vs [competitor]: which is better for [use case]?"
- "What are the alternatives to [competitor]?"
- "Is [competitor] worth it for a [team size] team?"
- "How much does a [category] tool cost for [scope]?"

Never put our brand in the prompt; a prompt that names us only tests
whether the engine knows the name.

## Category tags used in `prompts.csv`

`category` (the category question), `use case`, `integration`,
`comparison`, `pricing`, `alternatives`, `how-to`. Add a new tag only with
a reason in `notes`.

## Phrasing rules

- A full question in the first person or the plural, as typed into a
  chat box; no keyword strings.
- One intent per prompt.
- Words the buyer uses (transcripts, reviews, community threads), not
  our messaging pillars.
- Stable for a year: no dates, no version numbers, no this-quarter
  features.
- Distinct from existing rows: the same question in different words is
  a duplicate, and it costs a model call per run.

## Coverage grid

Rows: personas. Columns: awareness, consideration, decision. Cells: the
count of prompts and their category tags. A persona with zero
consideration prompts is the first gap; a cell with more than five is
probably over-covered.
