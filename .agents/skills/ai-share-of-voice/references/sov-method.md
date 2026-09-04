<!-- source: https://raw.githubusercontent.com/seranking/seo-skills/main/skills/seo-ai-search-share-of-voice/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Share of voice in AI answers: method and report shape

Condensed from SE Ranking's ai-search-share-of-voice skill.

## Inputs

Our domain and brand name; competitor domains and brand names; country;
the engines to compare (AI Overviews, ChatGPT, Perplexity, Gemini, AI
Mode, whichever the vendor covers).

## Method

1. Leaderboard: mention counts and share per engine per domain for the
   category and country.
2. Heatmap: rows are domains (ours plus competitors), columns are
   engines, cells are share of voice; mark the leader and the weakest
   per engine.
3. Prompt sampling per domain: ten prompts where the domain appears as a
   linked source, ten where the brand is named without a link. Keep the
   query text and the exact sources so a person can validate.
4. Topic clustering: group prompts by theme (pricing, feature comparison,
   tutorials, alternatives, reviews, integrations). In this repo the
   `category` column of `data/seo/prompts.csv` is the cluster; use it.
5. Gaps: three to five clusters where we underperform despite relevant
   content; for each, a specific action (a new angle, structured data, a
   comparison page, a real FAQ, presence on a frequently cited source).

## Share formula

Share of voice for a brand on an engine equals that brand's mentions
divided by the sum of mentions across all tracked brands on that engine,
for the period. Report the denominator; a share with no denominator is
not comparable next month.

## Report shape

- Summary: our share across engines, the leader and its share, our rank
  of N.
- Heatmap table.
- Who owns what: per brand, strong in and absent from.
- Cluster ownership table: cluster, leader, share, our position, gap.
- Top five actions to close gaps.

## Rules kept

- Never invent a citation count; zero prompts returned is zero, reported
  as such.
- Validate brand-name matches in the prompt text; a brand word can be a
  common word or a person's name; flag the ambiguous ones.
- Base-domain scope by default; subdomain scope only when asked.
- Re-run monthly and diff; momentum is the signal, one run is a sample.
