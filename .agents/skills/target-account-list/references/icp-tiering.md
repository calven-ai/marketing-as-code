<!-- source: https://raw.githubusercontent.com/NEON-Rutger/B2B-revops-skills/main/icp-builder/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# ICP tiering: from definition to a 0 to 100 fit score

Condensed from the source above. Use it to turn the tier definitions in
`strategy/icp.md` into something that scores a company from enrichment data
alone, and to notice when the ICP itself is not ready to build a list from.

## Is the ICP real yet?

| Sales motion | Customers needed for a real ICP |
| --- | --- |
| Product-led, no touch | about 160 |
| Low touch | about 80 |
| Medium touch | about 40 |
| High touch, field sales | about 27 |
| Named accounts | about 20 |

Below the threshold the team has an early customer profile, not an ICP.
Label it as such in the hand-over and expect it to move quarterly.

## Seven checks on the ICP file

Specificity (named firmographics, not "everyone"); pain in customer
language, not vendor language; buying signals that separate in-market from
the whole TAM; an evidence base of real customers; segments with different
motions kept apart; criteria a CRM can filter on; a review cadence. A
missing check is a question for the team, not something to fill in.

## Fit score and tiers

Five to eight weighted attributes across firmographic, technographic and
signal pillars, one weight set per segment, summing to 100.

| Tier | Score | What it means |
| --- | --- | --- |
| Tier 1 | 80 to 100 | every ICP criterion met; the list to work first |
| Tier 2 | 50 to 79 | most criteria met |
| Tier 3 | below 50 | opportunistic; do not chase |

Tier 1 should be a narrow list (hundreds out of a universe of tens of
thousands), not 40 percent of the market. A rep should be able to say yes
or no to a company in 30 seconds from the score and the notes.

## Sanity checks on the segment

| Check | Threshold |
| --- | --- |
| Deal cycle | 2 to 4 months; longer suggests the ICP is too large for the stage |
| Reference customers in the segment | at least 5 |
| Cost to serve | under 30 percent of ACV |
| Addressable companies | at least 100, or the segment is too small to list |

## Analysis dimensions when deriving tiers from closed-won data

Industry, company size, tech stack, revenue model, product usage,
enrichment signals, pipeline behaviour (cycle length and win rate by
attribute). Tier 1 should beat tier 2 on every cycle time; if it does not,
the weights are wrong.

## Refresh loop

Re-enrich, re-score, add new companies and purge dead ones quarterly. Log
each weight change through `log-decision` so the tiers stay explainable.
