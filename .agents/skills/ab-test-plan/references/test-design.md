<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/ab-testing/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Test design: hypothesis, sample size, stop rules, reading a result

Condensed from the A/B testing skill above; the significance arithmetic
at the end is standard.

## The hypothesis

"Because <observation or data>, we believe <change> will cause <expected
outcome> for <audience>. We will know this is true when <metric> moves by
<amount>."

One change per test. A change too small to detect at this traffic is
not a test, it is a guess with a timer.

## Metrics

- Primary: one metric, tied to the hypothesis, named as the ontology
  names it. It decides the test.
- Secondary: the metrics that explain why (CTA clicks, form starts, time
  to convert).
- Guardrails: what must not get worse (revenue, retention, refunds,
  support tickets, unsubscribes); a guardrail that degrades
  significantly stops the test.

## Sample size per variant (95% confidence, 80% power)

| Baseline rate | 10% relative lift | 20% relative lift | 50% relative lift |
| --- | --- | --- | --- |
| 1% | 150,000 | 39,000 | 6,000 |
| 3% | 47,000 | 12,000 | 2,000 |
| 5% | 27,000 | 7,000 | 1,200 |
| 10% | 12,000 | 3,000 | 550 |

Interpolate for other baselines, or use a standard calculator and record
the inputs. Duration = sample x variants / weekly eligible traffic,
rounded up to whole weeks so weekday and weekend mixes balance; run at
least one full business cycle.

## What to test first

ICE (impact + confidence + ease) / 3: impact high when a 15%+ lift is
plausible, confidence high when heatmaps, support or research point the
same way, ease high when it ships in one or two weeks. Headlines,
offers and form length usually beat button colours.

## Stop rules

- Reach the pre-computed sample before reading the result. Peeking and
  stopping early produces false winners.
- Stop at once if a guardrail worsens significantly.
- Never change a variant, the split or the traffic source mid-test; if
  you must, restart.
- Do not cherry-pick a segment after the fact; a segment that looks
  interesting is the next hypothesis.

## Reading the result

For conversion rates `p1` (control) and `p2` (variant) on samples `n1`
and `n2`: relative lift = (p2 - p1) / p1; standard error of the
difference = sqrt(p1(1 - p1)/n1 + p2(1 - p2)/n2); z = (p2 - p1) / SE;
two-sided p under 0.05 means |z| over 1.96; the 95% interval of the
difference is (p2 - p1) plus or minus 1.96 SE. Report the interval, not
only the p-value; an interval that includes zero is "no evidence of a
difference", never "no difference".

## What the record keeps

Hypothesis, variants (with screenshots or the copy), sample and split,
primary metric change with its interval and p-value, guardrail outcomes,
segment notes, the decision (ship, reject, iterate), and the reusable
pattern learned.
