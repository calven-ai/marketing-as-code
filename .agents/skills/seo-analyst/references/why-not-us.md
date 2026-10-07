# Why not us: the gap ladder

Work the gaps in tier order: every tier-1 keyword outside the top 10 (best
volume and fit first), then tier 2, then tier 3 only where a page we own
dropped, plus every `loss` finding. For each, walk the classes in order and
stop at the first one with evidence. Read the keyword's rows in the
`-serp-results.csv` snapshot (grep its id) before naming a class.

| # | Class | Evidence | Fix (what the task asks for) |
| --- | --- | --- | --- |
| 1 | Measurement | the SERP call failed, or Google reads the keyword with another meaning (a brand that is also a common word) | fix the keyword row at the next review; no task |
| 2 | Indexing | the target page's `index_verdict` is not `PASS` in `-gsc-pages.csv`; `index_coverage` says why ("Discovered, currently not indexed": crawl budget or internal links; "URL is unknown to Google": discovery) | sitemap, internal links, canonical, a stray noindex; a technical task |
| 3 | No page | `target_url` empty, or the page does not exist | a page of a named type on the keyword's intent (comparison, alternatives, pricing answer, template, guide): name the format the top 10 rewards; a new-piece task |
| 4 | Wrong page | `wrong_page`: Google ranks another of our pages | consolidate, retarget title and H1, internal links with the keyword as anchor; a technical task |
| 5 | Page fitness | indexed, ranks below 10; or `ctr_gap` (20+ impressions, no click) | compare with the top 3: intent match (listicle vs guide vs tool), title and H1 wording, meta description, freshness, comparison table, depth (`on-page-optimize` holds the checklist); a refresh candidate, not a task |
| 6 | Authority | the top 3 are high-authority domains or listicles on third-party sites | get onto those pages (name the URLs) or the link targets `backlink-analysis` found for the topic; a link-target task |
| 7 | SERP shape | an AI Overview, forum or video block answers above the organic results | the click lives in the answer: hand it to the AEO roles (`aeo-page-optimize`), never filed here |

## Evidence levels

- **observed**: the snapshot shows it (the SERP order, the index verdict,
  the impressions with no click).
- **inferred**: a reading of what the snapshot shows (the top 3 are
  stronger because they are listicles). Say what would confirm it.

One SERP re-pull or volume check per doubtful gap is allowed inside the
ten-call budget; a re-pull is evidence for the report, never a new snapshot.

## Striking distance and refresh candidates

A striking-distance query sits at Search Console position 8 to 20 with 20
or more impressions on one page (`seo_diff.py`, `striking_distance`); an
untracked one is also a keyword candidate. A refresh candidate is a class-5
gap. Both are listed with the page, the keywords or queries, the current
rank or position and what the top 3 do better. The wait rule: a page
published or changed in the last 60 days is listed as waiting, never as a
candidate, unless it is not indexed.

New pieces have checkpoints after publishing: day 14, indexed with
impressions (not indexed is a class-2 task); day 28, impressions and a
position for the brief's primary keyword (no rank yet is normal); day 56,
a decision: leave, refresh candidate, or consolidate.
