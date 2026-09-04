<!-- source: https://raw.githubusercontent.com/manojbajaj95/claude-gtm-plugin/main/skills/pitch-deck-creation/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Pitch narrative: spine, timing, design discipline

Condensed from the pitch deck creation skill in the GTM plugin. The
source builds investor decks; the spine and the design rules carry over
to a sales pitch narrative with the audience tailoring below.

## The spine, one question per slide

| Slide | The question it answers | Time |
| --- | --- | --- |
| Title | Who are you, in six words | 15 s |
| Problem | Is this a real problem people pay to solve | 45 s |
| Solution | What do you do about it | 45 s |
| Demo | Show me | 60 s |
| Market | Is it big enough to matter | 30 s |
| Business model | How do you make money | 30 s |
| Traction | Is it working | 45 s |
| Competition | Why you and not them | 30 s |
| Team | Why you can do it | 30 s |
| Financials | Where is this going | 30 s |
| The ask | What do you want | 30 s |
| Contact | How to follow up | 15 s |

About six minutes total. Missing data gets a placeholder slide, never an
invented number.

## Tailoring by audience

- Seed and early: problem, solution, market, team, early traction.
- Growth: revenue and unit economics first; the moat.
- Sales and business development: drop the fundraising slides; lead with
  the customer's ROI, proof and implementation.
- Product launch: features and what is new; demo screenshots.

For a sales pitch narrative in this repo the order becomes: their
problem (in their words), the cost of it, what changed, our approach, a
demo moment, proof, the plan, the ask.

## Design discipline

- The 1-6-6 rule: one idea per slide, at most six words per bullet, at
  most six bullets.
- Titles at most six words; body large enough to read from the back.
- One background tone, one accent colour, three colours in total; no
  gradients on text.
- Left-aligned text, consistent margins, one visual per slide, slide
  numbers, the logo.
- Charts: lines for growth over time, bars for comparisons, a 2×2 for
  positioning, one big number for a key metric. No pie charts. Competition
  is a positioning map, never a feature matrix.

Use `brand/tokens.json` for the colours and fonts; `design-qa` checks the
result.

## Pitfalls the source lists

More than fifteen slides; walls of text; a number with no source; too
many team members; vanity metrics with no revenue context; forgetting the
ask; inconsistent styling.
