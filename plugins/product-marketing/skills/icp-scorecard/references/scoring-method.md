# Scoring method

## One account

1. Apply the gates. An account in a blacklisted vertical or region, or failing an absolute disqualifier, is marked `Excluded: <gate>` and not scored.
2. For each dimension, find the account's value. If the value is unknown, the dimension is skipped for this account.
3. Level for a known value: the level in the table, or 0 if the value is not in the table. For an *any of* dimension, take the best level among the account's values.
4. Score = round(100 × Σ(weight × level) ÷ Σ(weight of dimensions with a known value)).
5. Confidence = Σ(weight of dimensions with a known value), out of the total weight of 100.
6. Tier from the thresholds (default: 80 or more Tier 1, 50 to 79 Tier 2, under 50 Tier 3).
7. If no dimension has a known value, score and tier stay blank.

Example: weights Industry 30, Employee band 25, Tech stack 20, Triggers 15, Region 10. An account is a developer tool (1.0), 201-500 employees (1.0), runs Datadog (0.6), triggers unknown, region NA (1.0).
Known weight = 30 + 25 + 20 + 10 = 85. Earned = 30 + 25 + 12 + 10 = 77. Score = round(100 × 77 ÷ 85) = 91, Tier 1. Confidence = 85.

Why missing data is excluded rather than zeroed: zeroing punishes accounts nobody has researched yet, so the list sorts by how much you know instead of how well they fit. Report confidence beside every score, and treat any score under 50 confidence as "needs enrichment".

## Reporting a scored list

- Sort by tier, then score, then confidence.
- For each account, list the dimensions that earned full credit ("Top matches") and the dimensions with no data ("Missing data").
- Give the distribution: accounts per tier, excluded accounts per gate, accounts below 50 confidence.
- Never edit the original columns; append Score, Tier, Confidence, Top matches, Missing data.

## Several products

- One company equation: the dimension set, the weights and the tier thresholds are the same for every product. That is what makes "fits product A at 82, product B at 64" a meaningful comparison.
- Per product, write only levels, and only for dimensions where the product's ICP differs from the company view (a vertical that is secondary for the company but core for this product). An omitted dimension uses the company's levels.
- Never restate weights or thresholds per product.
- Score each account once per product and report its best-fit product beside the company score.

## Calibration

Score the best customers and the lost deals the user supplied. Report a small table: `| Account | Expected | Score | Tier | Fits? |`. If best customers fall below Tier 1, raise the levels of the values they share before touching weights. If losses score Tier 1, look for the attribute they share that the ICP's disqualifiers name, and make it a gate or a 0 level. State every change and the account that prompted it.
