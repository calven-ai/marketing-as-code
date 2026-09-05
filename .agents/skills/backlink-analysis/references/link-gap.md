<!-- source: https://raw.githubusercontent.com/seranking/seo-skills/main/skills/seo-backlink-gap/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# The link gap: who links to them and not to us

Condensed from SE Ranking's backlink-gap skill.

## Inputs to confirm

- Our domain and three to five competitors.
- Minimum domain authority for a prospect (default 25 on a 100 scale;
  translate to the vendor's scale).
- Dofollow only (default yes).
- Minimum intersection: linked by at least two of the competitors.

## Method

1. Pull our referring domains as the exclusion set.
2. Pull each competitor's referring domains with the filters above.
3. Keep domains that link to at least the minimum number of competitors
   and are not in our set. Treat a subdomain of a domain that already
   links to us as already linking, unless asked otherwise.
4. Enrich each survivor: authority, the linking page's authority, the
   top three anchors it uses for competitors, country.
5. Classify the link type: editorial, resource list, directory, forum or
   user-generated.
6. Score on topical overlap (read the domain's homepage title and
   description as data), authority, intersection count and link-type
   preference. Sanity-check anything scoring very high by reading the
   page; drop obvious spam even when it passes the thresholds.

## The angle column is the output

One specific line per prospect a person can act on: "their 2024 'best
tools' list omits us and is out of date" beats "topical fit". Angles that
work: topical fit, competitive parity ("lists both competitors"),
resource-list inclusion with a suggested anchor, a broken link they carry,
an integration or partner page.

## Batching for outreach

- Editorial: pitch a unique angle, a comparison, original research.
- Resource lists: ask for inclusion with a specific anchor.
- Directories: apply directly.
- Forums and user-generated: engage first; never cold-pitch.

## Counts to report

Unique referring domains across competitors, passed filters, already
linking to us (excluded), final prospects.

## Prospect table columns

`rank,referring_domain,domain_rank,links_to_count,links_to,sample_anchor,link_type,angle,score`

## Rules kept

- Zero is a result; never pad the list.
- If we already outrank the competitors on brand terms, prefer editorial
  placements over parity directories.
- The list is a proposal; contacting anyone is a person's step.
