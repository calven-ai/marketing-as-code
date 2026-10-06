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

Only a `branded` row names us; it measures whether engines describe us
correctly, not whether they choose us.

## Tier by shape

Decision and shortlist shapes are tier 1 (Buy); a problem question where
we want our method cited is tier 2; a craft question is tier 3. The tier
follows the question, not the track: an alternatives prompt with no
buying intent is tier 2.

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

Rows: tracks. Columns: tiers, split by stage. Cells: the count of active
prompts and the personas they serve. A track under five prompts or a
persona with no tier-1 prompt is the first gap; a cell with more than ten
is probably over-covered.
