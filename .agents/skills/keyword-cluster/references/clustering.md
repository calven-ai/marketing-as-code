<!-- source: https://raw.githubusercontent.com/seranking/seo-skills/main/skills/seo-keyword-cluster/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Clustering by SERP overlap

Condensed from SE Ranking's keyword-cluster skill. The idea: group keywords
by how the search engine actually ranks them (shared top-10 URLs), not by
how similar the words look. Wording-based clustering manufactures
cannibalisation: two pages for one intent.

## Defaults to confirm with the team

- Seeds: 3 to 20.
- Candidates after expansion: at least 100 per seed, de-duplicated.
- Volume floor: 100 searches a month (lower for a niche B2B category;
  this repo's example rows sit at 90 to 480).
- Difficulty ceiling: 60.
- Strip branded terms the team does not own.

## The overlap method

1. Pre-group by intent first (informational, commercial, transactional,
   navigational). Pairs are only compared inside an intent group; that
   avoids comparing every pair.
2. Fetch the top 10 organic URLs once per candidate keyword and cache
   them for the session. Total SERP fetches equal the number of keywords,
   not the number of pairs.
3. Score each pair by shared URLs in the top 10:

   | Shared URLs | Meaning |
   | --- | --- |
   | 7 to 10 | Same page; merge the keywords |
   | 4 to 6 | Same cluster, may be separate sections of one page |
   | 2 to 3 | Separate pages that should link to each other |
   | 0 to 1 | Separate clusters, or exclude |

4. Clusters are the connected components of the 4-or-more graph. Aim for
   5 to 12 clusters. Each gets a name, a primary keyword, secondaries, a
   volume total and a volume-weighted difficulty.
5. A cluster is pillar-worthy when it is broad, informational or
   commercial, and its primary keyword could carry a long page; otherwise
   it is spoke-only.

## Pillar and spokes

- Each pillar nominates 3 to 7 spokes, one per sub-cluster or question.
- Each spoke gets an H1 and 3 to 5 H2s.
- Pillar links to every spoke; spokes link back to the pillar and
  cross-link where adjacent.

## Priority score

Applied after clustering, never to decide what clusters together:
volume 40 percent, inverse difficulty 30 percent, commercial intent 30
percent. It is a starting point; ask the team to review the top three
clusters before a quarter of content is committed to them.

## Quality gates (run against the finished map)

| Gate | Threshold | Fix |
| --- | --- | --- |
| Cannibalisation | No two clusters share 40 percent or more SERP overlap | Re-merge them |
| Orphan | Every spoke has an inbound link from its pillar | Add the link |
| Coverage | The pillar covers 70 percent of the cluster's high-volume keywords in its primary, secondaries or H2s | Widen the pillar or split the cluster |
| Anchor diversity | No anchor text is more than 40 percent of a cluster's internal links | Vary the anchors |

## Budget guard

Estimate SERP cost before fetching (one call per candidate). If the
candidate set is large, offer two paths: proceed, or raise the volume
floor and lower the difficulty ceiling and re-run the filter. Never run
the pass without saying the count.

## Tips

- "Best X" (commercial) and "what is X" (informational) never share a
  cluster, however similar the words.
- A pillar primary keyword should be broad enough to justify a long page;
  a narrow term makes a weak pillar.
