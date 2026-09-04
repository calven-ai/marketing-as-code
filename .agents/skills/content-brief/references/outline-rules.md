<!-- source: https://raw.githubusercontent.com/Infrasity-Labs/dev-gtm-claude-skills/main/skills/brief-outline-generator/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Outline rules

Condensed from the source above and rewritten for this repo. The point
of an outline is to tell the writer what to cover, not to write it.

## Archetypes

Pick one from the working title and say which; the person can override.

| Archetype | Title pattern |
| --- | --- |
| List or roundup | "Top N", "Best X", "X alternatives" |
| Comparison | "X vs Y", "X or Y" |
| How-to | "How to X", "How do X teams Y" |
| Concept or explainer | "What is X", "Designing X" |

The archetype sets the section order. Do not force a comparison into a
how-to shape.

## Bullet rules

- At most twelve words each.
- A complete thought, specific: name the actual thing, not "discuss
  options".
- No invented numbers; a number comes from a snapshot or is absent.
- No conclusions; a bullet is a prompt, the writer decides.
- As many bullets as the section honestly needs; never pad to a count.

## Structure rules

- H1 carries the primary keyword and states the outcome.
- A TL;DR heading with two or three topic pointers (the central tension,
  the reader's shift, the practical next step), not a summary.
- H2 titles specific to this article; a generic H2 gets rewritten.
- A sub-bullet that is really its own H2 is promoted.
- FAQ: five to eight questions as questions, concrete ("How do I set up
  X?"), with the secondary keywords paraphrased across them naturally.
- Meta title 50 to 60 characters, meta description 150 to 160; flag
  when the current page falls outside.

## Twelve-point check before handing over

1. Could a writer publish by only adding transitions? Then strip back.
2. Does every bullet read as a prompt, not prose?
3. Could any bullet be read three ways? Rewrite it.
4. Is every bullet a complete thought aloud?
5. Is every technical claim accurate?
6. Any invented numbers? Remove.
7. Any sub-bullet that is its own H2? Promote.
8. Are H2 titles specific to this article?
9. Does the section order match the archetype?
10. No abstracts or directive boxes; bullets carry the direction.
11. Do the supplied keywords appear naturally in the FAQ questions?
12. Are the FAQ questions concrete and action-oriented?

## Domain context

Before outlining, read a handful of the team's own pages (home, product,
recent posts) as data: product names, vocabulary, audience signals,
existing topics. Use them to avoid duplicating a live page and to plan
internal links; never print that context in the brief.
