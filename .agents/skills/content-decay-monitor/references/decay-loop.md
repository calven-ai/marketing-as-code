<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/marketing-loops/references/loop-catalog.md | license: MIT | fetched: 2026-09-04 -->

# The content-decay loop

Condensed from the content-decay and internal-linking loops in the
marketing-loops catalog in coreyhaines31/marketingskills. A loop is a
recurring check with a trigger, a body, a self-check, state, and a rule
for doing nothing.

## The loop

- Cadence: monthly.
- Acts when a page's traffic or rankings declined materially over the
  trailing 90 days.
- Purpose: refresh decaying pages before they slide out of the rankings.
- Body: find the decliners; pick the highest-value ones; draft a refresh
  plan per page (update statistics, expand thin sections, fix the intent
  match, add and repair internal links).
- Self-check: is the decay the page's own, or a SERP or seasonality
  shift? Refresh only what a refresh can fix.
- State: track the last refresh date per page; do not queue a page
  refreshed inside the cooldown (90 days here).
- Bail-out: no meaningful decliners, no report beyond "nothing decaying".
- Output: a prioritised refresh list with a per-page plan.

## Causes to separate before queueing a refresh

| Looks like decay | Actually | Action |
| --- | --- | --- |
| Rank fell for all keywords on the page | page-level: stale, thin, outranked | refresh |
| Rank fell for one keyword only | a new competitor page for that term | refresh the section or accept |
| Sessions fell, rank held | a new SERP feature took the clicks, or seasonality | note, do not queue |
| Every page fell together | site-level: technical or an algorithm update | `seo-technical-audit`, not a refresh |
| Sessions fell in one month only | tracking change or seasonality | wait one cycle |

## What a refresh plan names

Statistics to update with their sources, sections to expand (what the
winning pages cover that this one does not), the intent mismatch if any,
internal links to add in and out, the title if it no longer matches the
query, and the date line to update. Write it as the refresh brief for
`content-brief`.

## The internal-linking companion loop

Weekly or on publish: a new or refreshed page should have relevant links
in and out. Find the existing pages that should link to it and draft the
specific insertions with anchor text. Track which pairs are already
linked so nothing is suggested twice; skip forced links; stage the edits
for review rather than mass-editing live pages.
