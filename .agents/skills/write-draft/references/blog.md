<!-- source: https://raw.githubusercontent.com/manojbajaj95/claude-gtm-plugin/main/skills/blog-writing-specialist/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Blog post shapes

Condensed from the source above and rewritten for this repo. Written
for technical and product blogs; drop the code rules for a general post.

## Universal shape

Title with the primary keyword and the outcome; a TL;DR of two or three
sentences; "why this matters" made specific; the core content in steps
with explanation, code or example and the result of each; results with
numbers; trade-offs and limitations, honestly; a conclusion that ties
back to the opening and says what to do next; three to five further
links.

## Shapes by type

- Tutorial: what we are building (show the end first), prerequisites,
  steps, complete code, next steps.
- Explainer: what and why care, simple mental model, detailed mechanics,
  a real example, when not to use it, further reading.
- Postmortem: summary with impact and duration, timeline, root cause,
  fix, prevention, lessons.
- Benchmark: what and why, method (reproducible), results with tables,
  what the numbers mean, recommendation with caveats, raw data.
- Architecture: the problem, constraints, options considered, the
  choice with a diagram, trade-offs accepted, results.

## Length

Quick tip 500 to 800 words; tutorial 1,500 to 3,000; deep dive 2,000 to
4,000; architecture 2,000 to 3,500; benchmark 1,500 to 2,500. A brief
with a SERP-based target overrides these.

## Openings and closings

Open on a real position or event, set a tension or a question, state
who the post assumes the reader is, and reach substance within two or
three paragraphs. Close by returning to the opening, offering a forward
view and one concrete action.

## Formatting

Headers of two to four words that tell the story when read in sequence;
varied paragraph length; inline code where it is code; no emoji. Code
blocks runnable as written, with a language tag, expected output,
realistic names, error handling in production examples, and pinned
versions ("works with React 18.2").

## Voice do and don't

Do: be direct ("use connection pooling"), admit trade-offs, use "we" for
team decisions, give specific numbers ("p99 from 800 ms to 90 ms"), cite
sources, acknowledge alternatives.

Don't: "In today's fast-paced world", "as we all know", "simply",
"it's easy to", "obviously", marketing language in a technical post,
burying the point under context.

## Checklist before review

Every claim verified; no overselling; beta status and limits disclosed;
TL;DR present; code tested; versions pinned; trade-offs section present;
a diagram where a system is described; further reading present; no
broken links; frontmatter complete; active voice.
