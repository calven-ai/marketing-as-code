# Claim checks

**Reads:** `strategy/product-brief.md`, `strategy/positioning.md` (proof
points), `strategy/competitive/`, `data/` snapshots, `content/` ·
**Skill:** `/review` checks a draft against strategy and voice; these
prompts go claim by claim on facts.

A page is about to go live with "cuts reporting time in half" and a
comparison table. Is any of it true? Who said so? You walk away with every
product, pricing, competitive and outcome claim listed, each marked
supported, weak or unsupported, with the file behind it and a safer
rewrite where needed. Use it before a launch, a comparison page or
anything legal might read.

## Prompts

### Fact-check product and pricing claims

```
Using this repo, fact-check every product and pricing claim in the draft below.

FILL IN
- Draft: [paste your draft, or give a content/ folder]

CONTEXT
This ships soon. Every statement about what the product does, what it integrates with and what it costs must match what's written down.

READ FROM THE REPO
- strategy/product-brief.md: capabilities, integrations, pricing and packaging, known weaknesses.
- memory/decision-log.md, for pricing or packaging changes since the brief was reviewed.

CHECK
- List every product or pricing claim, quoted.
- Mark each supported, partly supported or unsupported, with the section it rests on.
- Flag claims that touch a known weakness.

OUTPUT
A claims table, then a rewrite for every claim not fully supported.

GROUNDING
Cite the file and section for every verdict. If the product brief is older than 90 days, say so at the top. Never mark a claim supported from general knowledge.
```

### Check the competitive claims

```
Using this repo, check every claim about competitors in the draft below.

FILL IN
- Draft: [paste your draft]

CONTEXT
Competitive claims get screenshotted and sent back to us. Each must be fair, current and sourced.

READ FROM THE REPO
- The battlecards in strategy/competitive/, with their last_reviewed dates.
- The latest competitor watch report in reports/recurring/competitive/.
- strategy/positioning.md, for our side of the comparison.

CHECK
- Each claim about a competitor, quoted.
- Whether the card or a watch report supports it, and how recent that source is.
- Claims that were true once and may not be now.
- Tone: anything a fair reader would call a cheap shot.

OUTPUT
A table: claim, competitor, source and date, verdict, safer wording.

GROUNDING
Cite paths and dates. Their pricing, features and customers only as recorded. Anything older than 90 days is "verify before publishing".
```

### Check the proof and outcome claims

```
Using this repo, check every outcome, number and customer claim in the draft below.

FILL IN
- Draft: [paste your draft]

CONTEXT
"Customers see 3x ROI" needs a customer and a source. I want every number and every named customer traced.

READ FROM THE REPO
- Proof points in strategy/positioning.md.
- Published case studies in content/ (channel case-study) and their approval status.
- Snapshots in data/ that the numbers might come from.

CHECK
- Every number, percentage, customer name and quote, listed.
- Its source, or "no source found".
- Whether a named customer approved use of the quote.

OUTPUT
A table of claims with source and verdict, then the list of claims to cut or soften.

GROUNDING
Cite paths. A number with no source is unsupported, however plausible. Never suggest a replacement number.
```

## Advanced prompts

### Score every claim in a risk register

```
Turn the claims in this asset into a risk register, scored on likelihood of challenge and impact if challenged. Use this repo for the evidence behind each claim.

FILL IN
- Asset: [paste your draft]

CONTEXT
Not every unsupported claim matters equally. A vague benefit line is low risk; a named-competitor price comparison is high. I want to spend review time where the exposure is.

FROM THE REPO
- strategy/product-brief.md and strategy/positioning.md for support.
- strategy/competitive/ for competitive claims.
- memory/decision-log.md for any past claim we had to withdraw.

METHOD
- Classify each claim: product, pricing, competitive, outcome, customer.
- Score evidence strength 1 to 5 from the repo source.
- Score likelihood of challenge 1 to 5 (named competitor, number, superlative score higher) and impact 1 to 5.
- Risk = (6 minus evidence) times likelihood times impact. Rank.
- For the top five: keep, soften or cut, with the rewrite.

OUTPUT
The register as a table sorted by risk, and the five decisions.

GROUNDING
Label each score as your judgement with the evidence path. Scoring rules stated before the table.
```

### Grade the evidence behind outcome claims

```
Grade the strength of evidence behind each outcome claim on an evidence ladder. Use this repo for the case studies, proof points and data behind them.

FILL IN
- Claims: [paste the outcome claims, or a draft]

CONTEXT
"One customer said" and "measured across 40 accounts" both end up as "customers see X". I want each claim graded so we say exactly what we can stand behind.

FROM THE REPO
- Proof points in strategy/positioning.md.
- Case studies in content/ and the transcripts behind them in memory/transcripts/processed/.
- Any measured data in data/ snapshots.

METHOD
- Ladder: 1 anecdote, 2 single customer with a number, 3 several customers, 4 measured across a defined set with n, 5 measured with a comparison group.
- Place each claim on the ladder with its source.
- Write the strongest wording each level honestly supports ("one customer cut..." versus "customers cut...").

OUTPUT
A table: claim, ladder level, source, the honest wording.

GROUNDING
Cite paths. Never promote a claim up the ladder by assumption. Unknown n is level 1 or 2.
```

## Questions to just ask

- Does the product brief say we integrate with [tool]?
- Which proof points in our positioning have a source?
- Is the pricing on this draft the same as in the product brief?
- Which case studies have approved quotes?
- What known weaknesses does the product brief list?
- When was the [competitor] battlecard last checked against their pricing page?
- Which claims on our comparison pages cite a battlecard older than 90 days?
- Has the decision log ever recorded a withdrawn claim?
- Which numbers in this draft have no snapshot behind them?
- Which published pieces say "the only" or "the first"?
- Does our boilerplate make any claim the product brief doesn't support?
