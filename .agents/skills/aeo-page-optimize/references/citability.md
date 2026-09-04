<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/ai-seo/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Citability: structure, authority, presence

Condensed from coreyhaines31/marketingskills `ai-seo`. Three pillars:
make content extractable, make it citable, be where the engines look.

## Step 1: check the prompts

For the page's prompts, record per engine: an AI answer appears (yes or
no), we are cited, who is cited. In this repo that table is
`brand-monitor`'s snapshot; do not rebuild it by hand.

## Step 2: read why competitors are cited and we are not

Structure (more extractable), authority (citations, statistics, expert
quotes), freshness (updated recently), schema, third-party presence
(cited through review sites, forums, an encyclopedia entry).

## Step 3: the extractability checklist (per page)

- A clear definition or direct answer in the first paragraph.
- Self-contained answer blocks that work without the surrounding text.
- Statistics with their sources.
- A comparison table for "X vs Y" prompts.
- An FAQ section with natural-language questions (only when the
  questions are real).
- Schema: Article, FAQ, HowTo or Product as fits.
- A named author with credentials.
- Updated within six months, with the date shown.
- Headings that match how the prompt is phrased.
- AI crawlers allowed in `robots.txt`.

## Step 4: bot access

`GPTBot` and `ChatGPT-User` (OpenAI), `PerplexityBot`, `ClaudeBot`
(Anthropic), `Google-Extended` (Gemini and AI Overviews), `Bingbot`
(Copilot). A blocked bot cannot cite. Blocking a training-only crawler
(`CCBot`) while allowing these is a middle path; it is the team's
decision, report the state.

## Pillar 1: structure

Block patterns: definition blocks for "what is", step blocks for "how
to", comparison tables for "vs", pros and cons for evaluations, FAQ
blocks, statistic blocks with sources. Lead every section with the
answer; keep the key passage to 40 to 60 words; H2 and H3 phrased as
the query; tables beat prose for comparisons, numbered lists beat
paragraphs for processes; one idea per paragraph.

## Pillar 2: authority (what moved visibility in the Princeton GEO study)

| Method | Effect on visibility |
| --- | --- |
| Cite sources | about plus 40 percent |
| Add statistics | about plus 37 percent |
| Add expert quotations | about plus 30 percent |
| Authoritative tone, clarity, technical terms, fluency | plus 15 to 30 percent each |
| Keyword stuffing | minus 10 percent |

Statistics with dates and original sources; named authors and quoted
experts with titles; "last updated" shown; first-hand experience and
transparent method.

## Pillar 3: presence

Engines cite where a brand appears, not only its site: encyclopedia
entries, forums, industry publications, review sites (G2, Capterra,
TrustRadius for B2B), video with a good text layer, podcasts (transcripts
get crawled). Participate authentically; fabricated mentions are a
policy violation and a brand risk.

## Content types cited most

Comparison articles (about a third of citations), definitive guides,
original research, best-of lists, product pages with specifics, how-tos,
expert analysis. Underperformers: unstructured posts, thin marketing
pages, gated content, undated or unattributed pages, PDF-only.

Citation is not recommendation: being consulted differs from being on
the shortlist, which web-wide consensus (reviews, forums, analysts)
decides. Self-promotional "best in category" lists from an emerging brand
often earn citations in answers that recommend competitors.

## What not to do

Separate "for AI" content; chunking pages into fragments; generating
thin variants at scale; inauthentic mentions; blocking the bots you want
citations from; main content behind JavaScript that does not render;
skipping author, experience and sourcing.

## Search Console

No AI-specific report exists; Google's AI features use core ranking, so
the standard reports still apply. Cross-engine citation needs the
`ai-visibility` integration.
