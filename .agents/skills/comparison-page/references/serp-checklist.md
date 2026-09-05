<!-- source: https://raw.githubusercontent.com/seranking/seo-skills/main/skills/seo-competitor-pages/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# The search side of a comparison page

Condensed from the competitor pages skill in SE Ranking's seo-skills. The
source runs on SE Ranking's API; here the same steps run through
`seo-analyst` and whichever `seo-data` vendor is wired.

## Page types by query

Head-to-head ("X vs Y"), alternatives listicle ("alternatives to X",
"best X alternatives"), and use-case segmentation ("best X for solo
developers", "best X for enterprise"). Confirm the competitor is actually
a search rival before writing: if you share no ranking keywords, the page
may still serve sales, but not search.

## Steps that need data

1. Keyword mapping: the top organic keywords for each brand; which are
   exclusive, which overlap, which are gaps.
2. SERP check for the target keyword: the top ten, the people-also-ask
   questions, whether a featured snippet exists and what shape it has.
3. Teardown of the top three winners: their headings, table shape, FAQ,
   pricing mentions, number of calls to action, schema types.
4. Feature matrix: the dimensions the winners compare on (pricing, free
   tier, integrations, support tiers) plus the ones the battlecard adds.

Save each pull as a snapshot; the source keeps an evidence folder for the
same reason.

## What the draft carries

Hero and summary verdict; the feature table; one section per dimension;
a FAQ built from the people-also-ask questions (real queries, and what AI
answer engines cite); a recommendation block that says which product wins
for which use case; call-to-action placement. Optional: JSON-LD for
`Product` (each brand), `BreadcrumbList` and `FAQPage`, handed to the web
team as a separate block.

## Principles

- Balance converts: pages that admit the competitor's strengths outrank
  the partisan ones.
- Recommend our product only where it is genuinely better for that use
  case; the verdict is per use case, not global.
- No auto-publish: the draft goes to a person for fact-check and voice.

## Cost

The source budgets 15 to 25 API credits per page, plus a few for schema
benchmarking and one per URL scraped. State the equivalent for the wired
vendor in the report.
