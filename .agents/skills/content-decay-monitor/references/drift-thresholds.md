<!-- source: https://raw.githubusercontent.com/seranking/seo-skills/main/skills/seo-drift/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Drift thresholds: when a change is yellow or red

Condensed from SE Ranking's seo-drift skill (baseline, compare, history).
Its framing: capture a snapshot, diff the next one against it, list red
findings first. This repo's dated snapshots in `data/seo/snapshots/` are
the baselines; the monthly decay report is the compare.

## Site level

| Metric | Yellow | Red |
| --- | --- | --- |
| Domain authority | plus or minus 5 | plus or minus 10 |
| Estimated organic traffic | 20 percent | 50 percent |
| Organic keyword count | 10 percent | 30 percent |
| Top-3 keyword count | 15 percent | 40 percent |
| Top-100 churn | | any high-volume keyword dropped out |
| Net referring domains | minus 5 to minus 20 | below minus 20 |

## Page level (compare the page's own fingerprint)

| Change | Level |
| --- | --- |
| canonical, robots meta, language, H1 | red |
| title or meta description | yellow |
| schema types added or removed | yellow |
| Open Graph or Twitter card fields | yellow |

Fields that were not captured in one of the two snapshots are "not
comparable", never a green pass.

## Field data, when Search Console or CrUX is wired

| Change | Level |
| --- | --- |
| LCP or INP p75 up 20 percent or more | red |
| CLS p75 up 0.05 or more | yellow |
| FCP or TTFB p75 up 30 percent or more | yellow |
| indexation status left INDEXED | red |
| Google's chosen canonical changed | yellow |
| last crawl older than 60 days | yellow |

## Report order

Red findings first, then yellow, then positive deltas, then "what to
investigate first" as a numbered list. Include the history table when
more than two snapshots exist: date, authority, traffic, keywords, top-3
count.

## Cadence and caveats

Monthly is the natural rhythm; backlink data is too noisy weekly. A
flat-zero authority history means insufficient history, not a regression.
The skill diagnoses; nothing is fixed, disavowed or edited from a drift
finding.
