<!-- source: https://raw.githubusercontent.com/thatrebeccarae/claude-marketing/main/agents/ga4-monitor/README.md | license: MIT | fetched: 2026-09-04 -->

# Comparing live events against the taxonomy

The audit is a comparison of two lists: the events the taxonomy expects
(`data/ontology/events.md`) and the events the tool recorded (the events
snapshot). Three checks, then a verdict.

## Inputs

- The spec: per event, its name, category, expected properties, how it
  is implemented (tag, trigger, variables) and a priority so a gap can be
  ranked.
- The inventory: event name, count and users for the period, from
  `data/analytics/snapshots/YYYY-MM-DD-<vendor>-events.csv`.
- History for anomalies: daily counts for at least 14 days, or the
  previous period's totals when that is all there is.

## Checks

1. **Gaps**: spec events with no rows in the inventory. Rank by the
   spec's priority; a missing conversion event outranks a missing scroll
   event.
2. **Unexpected events**: inventory events absent from the spec, after
   removing the tool's automatic ones. For GA4 those are the automatic
   set (`page_view`, `session_start`, `first_visit`, `user_engagement`)
   and enhanced measurement (`scroll`, `click`, `view_search_results`,
   `video_start`, `video_progress`, `video_complete`, `file_download`,
   `form_start`, `form_submit`); PostHog's start with `$`. What remains is
   either an undocumented event to add to the taxonomy or noise to
   remove; the report says which.
3. **Volume anomalies**: with 14 or more days of history, an event is
   anomalous when it fails two of three baselines: a z-score over 3
   against the 7-day rolling mean, a drop over 25% against the same day
   last week, a drop over 25% against the same day four weeks ago. With
   only the previous period's totals, a drop over 25% period on period is
   the flag. Tune the thresholds and say what you used.

## Verdict

Three booleans, in this order: gaps found, anomalies found, all clear.
The report leads with the worst finding and lists every event under each
check with a proposed fix.

## Reading an anomaly

A drop on the day a page, a form or a consent banner changed is an
implementation break, not a marketing result; check the release date
against the drop. A rise with no campaign behind it is often a duplicate
tag. An event that vanished together with its siblings is a container or
SDK failure.
