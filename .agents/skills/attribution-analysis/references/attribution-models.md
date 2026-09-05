<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/attribution/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Attribution models, blind spots, reconciliation

## The models and the story each tells

| Model | Credit | Good for | Bias |
| --- | --- | --- | --- |
| First touch | 100% to the first known touch | demand creation, awareness spend | ignores what closed; inflates top of funnel |
| Last touch | 100% to the last touch | direct response, short cycles | over-rewards branded search and bottom of funnel |
| Last non-direct | 100% to the last tracked non-direct source | the analytics default | still single touch; moves the blind spot |
| Linear | equal across all touches | long cycles where every step matters | a throwaway visit counts as much as a demo request; flatters frequent channels |
| Time decay | more to touches nearer the conversion | long cycles where recency signals intent | penalises early awareness |
| Position-based (U) | 40% first, 40% last, 20% spread over the middle | B2B, "created demand" and "closed" both matter | the split is a convention, middle touches get little |
| Data-driven | marginal contribution modelled from the data | high volume | a black box; needs volume (GA4 wants on the order of a thousand conversions a month); blind to touches it never saw |

Rules of use: for a cycle over a month, never report one model alone,
show first and last touch side by side and read the gap. Data-driven
without volume is noise; use position-based. A consistent, repeatable
model plus an out-of-model check (a survey field, a holdout) beats
chasing precision.

## Three ways to measure, beyond the model

- Multi-touch attribution: user-level touches stitched, a model applied.
  Answers which touches appear in converting journeys. Undercounts
  silently since cookies and cross-device loss.
- Marketing mix modelling: regression of spend against outcomes over
  months. Captures offline and brand; needs two to three years of data
  and real budget variation; slow to react.
- Incrementality tests: holdouts (geo, audience) comparing exposed to
  unexposed. The only method that answers "did this cause lift"; few
  tests at a time, volume needed.

Heuristic: small budget or short cycle, UTMs plus last non-direct plus a
survey field; mid-market, multi-touch daily plus periodic incrementality
tests; large portfolio with offline spend, mix modelling plus
incrementality.

## Self-reported attribution

"How did you first hear about us?", open text, asked at the conversion
moment (signup, demo request). Captures dark social, podcasts, word of
mouth, AI assistants. Recall credits the memorable touch, not the first,
so it is a triangulation input and the tiebreaker when platforms fight,
never the count.

## Blind spots

- Direct: bookmarks and typed URLs, but also stripped referrers, app to
  web, dark social. A large direct share is a measurement failure signal.
- Branded search: people who discovered the brand elsewhere and searched
  the name; segment branded from non-branded or the real top of funnel
  gets defunded.
- Dark social: DMs, Slack, podcasts, screenshots; only the survey sees
  it.
- AI assistants: influence, then send the buyer through branded search or
  direct; the AI touch is hidden (`brand-monitor` sees the mention side).

When direct and branded search dominate, the top of funnel is probably
working and the attribution is hiding it.

## Reconciling conflicting counts

Every source overclaims in its own way: ad platforms count the same sale
inside their own windows; web analytics defaults to last non-direct and
loses cross-device and blocked users; the CRM reflects what a form or a
person typed, with source overwrites; the survey has recall bias.

1. One source of truth for the count, usually the CRM or billing.
2. Never sum across platforms; de-duplicate against that total.
3. Read directional agreement, not absolute match.
4. Self-reported breaks ties.
5. Run an incrementality test when the stakes justify it.
6. Name the gap: "platforms claim X, we verify Y, the delta is
   overclaiming plus untracked touches".

## The readout

The decision it informs; the source of truth; a de-duplicated channel
table; first and last touch side by side for long cycles; confidence and
blind spots; a recommendation with the tests worth running.
