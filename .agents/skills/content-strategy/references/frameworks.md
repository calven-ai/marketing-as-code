<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/content-strategy/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# Content strategy frameworks

Condensed from the source above and rewritten for this repo. Use them as
lenses; the team's messaging and personas outrank any of them.

## Searchable or shareable

Every topic is one or both. Searchable content captures demand that
already exists (a keyword in `data/seo/keywords.csv`); shareable content
creates demand (an insight, original data, an opinion). Search first,
because it compounds.

Calendar split to aim for: 60% searchable (use cases, hub and spoke,
how-tos), 30% shareable (thought leadership, original data, opinion), 10%
experimental (a new format or channel).

## Pillars and clusters

- Three to five pillars. A good pillar aligns with the product, matches
  what the audience cares about, has search volume or social interest,
  and is broad enough for many subtopics.
- Under each pillar, clusters of related topics; a hub piece links to its
  spokes, spokes link back and to each other.
- Trace each pillar to a pillar in `strategy/messaging.md` and to a
  persona; a pillar with no persona is a hobby.

## Buying-stage modifiers

| Stage | Query modifiers |
| --- | --- |
| Awareness | what is, how to, guide to, introduction to |
| Consideration | best, top, vs, alternatives, comparison |
| Decision | pricing, reviews, demo, trial |
| Implementation | templates, examples, tutorial, how to use, setup |

The stages here are buying stages (the axis in `strategy/messaging.md`),
not the funnel stages in `data/ontology/funnel.md`.

## Format taxonomy

Searchable: use-case pages (persona plus use case, long tail), hub and
spoke guides, template libraries. Shareable: thought leadership that names
an unnamed concept, data pieces (product data, public data, original
research), expert roundups, case studies (challenge, solution, results,
learnings), behind-the-scenes.

Link-earning ratio the source reports (backlinks per share): statistics
roundups 4.25, glossaries 1.47, interactive tools 1.38, how-tos 1.36,
original research 0.80, ultimate guides 0.77, thought leadership 0.74,
templates 0.68. Curated statistics earn roughly five times the links of
original research; cite this as the source's number, not ours.

## Prioritisation score

Rate each topic 1 to 10 on four factors, weight, sum, rank:

| Factor | Weight | Evidence |
| --- | --- | --- |
| Customer impact | 40% | how often it appears in transcripts, reviews, support; who it affects |
| Content-market fit | 30% | product alignment, a real customer story, a natural next step |
| Search potential | 20% | volume and difficulty from a snapshot, trend |
| Cost | 10% | expertise on hand, research needed, assets needed |

## Where topics come from

Keyword data (clusters, stage, quick wins), call transcripts
(`memory/transcripts/processed/`: questions, objections, competitor
names, the customer's own words), surveys and reviews (themes that reach
about 30% of responses), forums, competitor blogs (what they repeat, what
they miss, what is dated), sales and support (repeated questions, ticket
patterns, feature requests).

## Failure modes

Spray and pray (posting everywhere with no flagship), platform dependency
(building only on rented reach), and spending most of the effort on
channels the team does not own while the owned ones that convert starve.
