<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/prospecting/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Prospecting: building a verified candidate set

Condensed from the source above, rewritten for this repo. The list this
skill builds is company-level; the people fields in the source's lead sheet
belong to the `researcher` skill and to a private repo only.

## Five phases

1. **Define the ICP as pass/fail.** Firmographic fit (industry, size,
   revenue, geography, business model), technographic fit (tools in use,
   gaps), a buying signal (funding, hiring, expansion, a visible
   dissatisfaction), and explicit disqualifiers. Output: one paragraph plus
   a checklist. In this repo that paragraph is `strategy/icp.md`.
2. **Build the candidate set.** Source two to three times more candidates
   than the final target. Cross-check two or three sources for B2B; a
   smaller verified list beats a large junk list.
3. **Qualify each candidate** against the checklist with an evidence URL
   per claim. No assertion without a source.
4. **Score and prioritise.** A workable default mix is about 20 percent
   hot, 30 percent warm, the rest cold or skipped.
5. **Output.** A table under 25 rows, CSV above that. Always include the
   search parameters used and the open questions.

## Scoring rubric

| Score | Meaning |
| --- | --- |
| Hot | strong ICP fit, a clear and recent buying signal, an accessible decision maker |
| Warm | ICP fit, a softer or older signal |
| Cold | loose fit, or no signal |
| Skip | a disqualifier hit: out of ICP, closed, duplicate, competitor, low confidence |

Confidence: high when two independent sources or an official company page
agree; medium on one credible source; low when evidence is incomplete, and
say so. "Hot" needs a buying signal; ICP fit alone is warm at best.

## Signals worth capturing per company

Funding round, hiring in the buyer's function, a tech-stack change,
expansion into a new market, a leadership change, a public complaint about
the incumbent. Each with its source URL and date.

## Quality checklist before proposing rows

- Deduplicated by lowercased domain.
- Every hot account has at least one source URL and a dated signal.
- Confidence is honest: "high" means two or more sources.
- No bulk scraping of platforms that forbid it, no login walls, no
  CAPTCHA bypass; licensed vendors used within their terms.
- The final count matches the request, or the shortfall is explained.
- No sensitive traits inferred about anyone, ever.

## Common mistakes

Starting without an ICP; single-source verification; labelling hot without
a signal; missing source URLs (breaks the audit trail later); mixing the
scoring rules of different segments in one list.
