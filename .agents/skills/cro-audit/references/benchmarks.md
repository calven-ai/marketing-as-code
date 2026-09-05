<!-- source: https://raw.githubusercontent.com/thatrebeccarae/claude-marketing/main/skills/cro-auditor/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Benchmarks, scoring and the hypothesis record

Condensed from the CRO auditor above. Benchmarks label a rate as
unusual; the page's own history and the campaign's target are the
comparison that matters.

## Conversion rate ranges by page type

| Page type | Good | Average | Poor |
| --- | --- | --- | --- |
| Landing page, paid traffic | over 5% | 2 to 5% | under 2% |
| Landing page, organic traffic | over 3% | 1 to 3% | under 1% |
| Signup form (start to complete) | over 25% | 10 to 25% | under 10% |
| Pricing page to signup | over 10% | 5 to 10% | under 5% |
| Free trial to paid | over 25% | 10 to 25% | under 10% |
| Email opt-in | over 5% | 2 to 5% | under 2% |
| Checkout | over 3% | 1.5 to 3% | under 1.5% |

Above the fold: the value proposition visible, the primary CTA
prominent, load under 2.5 s, navigation that does not distract.

## The LIFT lens

Six forces on a page: value proposition, relevance and clarity raise
conversion; urgency raises it when real; anxiety and distraction lower
it. Name which force each finding touches.

## Scoring a hypothesis

ICE = (impact + confidence + ease) / 3, each 1 to 10.

- Impact: 8 or more for a plausible 15%+ lift on the primary metric.
- Confidence: high when the funnel, a recording or research points at the
  same leak; low when it is a hunch.
- Ease: high when it ships in one or two weeks without engineering.

PIE (potential, importance, ease) is the alternative when traffic
differs a lot between pages: importance weights the page's traffic and
value.

## The record for each finding

Issue, location on the page, impact level, evidence (snapshot path and
number, or the heuristic), the specific fix, the hypothesis ("if we
<change>, <metric> will <improve> because <reason>"), and the ICE score.
This is what `ab-test-plan` takes as its input.
