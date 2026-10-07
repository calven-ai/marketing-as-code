# The web analyst's method

How a weekly run turns snapshots into one decision. The definitions are
`data/ontology/`; the queries are the vendor reference.

## Small numbers

- Under n = 100, every rate is written `k of n`. A rate without its n is
  not reported.
- Compare sources, pages or content types only when each has at least 10
  human sessions; below that, name the pages and sources instead.
- No trend from fewer than 4 weekly points. Rates are rolling 4-week with
  Wilson intervals; overlapping intervals are "no change detected". Counts
  are weekly.
- Bots are never in a rate. Human sessions are the denominator; engine
  fetches and other bots are their own counts. Pageviews are the one exact
  number when tracking is cookieless.
- What survives small n: a stage that drops to zero while its 4-week
  median is above zero, a page an engine reads for the first time, a new
  source, a named page moving.
- Never name a person or an id. Pages, sources and content types are the
  unit.

## Rank

Score each move as the change in sessions times its stage weight:
conversion 3, CTA 2, engaged 1, engine fetch 1, pageview 0.5. A zeroed
stage, a bot-share jump, a first engine read and anything with a
conversion behind it outrank the rest. Keep the top five. Under 5
sessions, or within normal variation (less than two interval widths from
the 4-week median), it is an observation, not a finding. A changed
definition (the snapshot's queries or the ontology changed) is said
before any move across it.

## Expectation before "so what"

Before judging a number, say what the page, source or content type is
for, citing `strategy/` where it says so. Defaults when it does not:

| Content type | Its job | So a bad week looks like |
| --- | --- | --- |
| comparison, alternatives | be read and cited by answer engines first, then convert the people they send | engine fetches flat, or AI-assistant humans bouncing |
| guide, blog | feed organic search and the corpus engines learn from; engaged reading and a next click | high bounce, no next page |
| template | deliver value on the page; a CTA is a bonus | low engagement, not low conversion |
| home, pricing, product | where the decision is made | a bounce here is a message or pricing problem, not a traffic problem |

Then judge the number against what it led to next: engine fetch, human
AI-assistant session, engaged, decision page, CTA, conversion. A number
is good or bad only relative to that chain.

## The cause ladder

Per finding: what (the number, `k of n`, the delta, the interval), where
(page, content type, channel, source), then why. Work down and stop at
the first rung with evidence:

1. **Instrumentation.** A site release in the window, page-leave or
   scroll coverage down, CTA attribution mismatches above 0. A drop that
   coincides with a release is a data question first.
2. **Volume.** n too small this week: say so and stop.
3. **Who is this traffic.** The class split on the page or source. An
   all-bot spike is not a win; an engine fetch is a leading indicator,
   not a visit; zero-second search sessions may be the search engine's
   own fetcher.
4. **Source quality.** Engaged share, pageviews per session, median
   duration by source. A source that sends many and keeps none is
   irrelevant traffic or a page that breaks the source's promise.
5. **Landing fit.** Bounce and scroll on the page that source lands on:
   does it answer the question the source implied, and offer the next
   step the strategy wants?
6. **CTA friction.** The drop from decision page to CTA, which location
   gets the clicks, decision-page sessions that scroll to the end and
   leave. Up to three human replays, described, not identified.
7. **Conversion handoff.** CTA clicks against conversions with matching
   forwarded source and landing page. Clicks with no matching conversion
   belong to whoever owns the conversion flow (hand over); conversions
   with no attribution after the handoff shipped are a handoff bug.

Classify the cause (instrumentation, bots, source, content, CTA, handoff,
too small) and its evidence level: **observed** (the data shows it) or
**inferred** (it fits, nothing links it). An inferred cause names the one
alternative not ruled out and what would tell them apart. "Unknown, needs
a look at the page" beats a guess.

Every now-what names content type, topic and source: "add a pricing
comparison table to the alternatives pages AI assistants send people to",
not "improve AI traffic".

## Verify last actions

For each open `web-finding:` task whose check date has arrived, re-read
its target metric and write moved, not moved, or not due (with the date),
against its decision rule. Two checks without movement make it the one
thing. Score the Watch items in memory the same way.

## The one thing

One action this week: the finding whose action is most reversible and
moves the highest-weight stage. Three lines: what, so what, now what, and
the strategy bet it moves.

## Make it stay caught

For each finding and caveat, ask what let it hide and change the first
layer that fits, climbing only as far as needed:

1. **The snapshot query** (`scripts/web_snapshot.py` or the vendor
   reference): a class rule, a threshold, a missing column. Proposed in
   its own branch, never in the report's; the next snapshot names the
   definition change.
2. **A saved insight** named `analyst/<what it shows>`, following the
   dashboard rules in the vendor reference.
3. **An alert** on that insight when the finding is a threshold (bot
   share, a stage at zero, coverage below a floor).
4. **A tracking fix** filed as a task: the property or event that would
   have answered the question, through `tracking-spec`.
5. **The model**: a channel arm, referrer or class rule in
   `data/ontology/` that is wrong, proposed as a cascade diff.

List every change under Measurement changes in the report.

## Forecast and memory

End with 80% integer ranges for next week's human sessions, engine
fetches, CTA sessions and conversions, with a one-line why; next week's
run scores them first (`k of 4` inside the range). Then rewrite the
memory file: add, score or drop Watch items (each with a check date and
what would confirm or refute it), add a pattern you had to work out,
record Events (a release, a launch, a campaign) that explain later
moves, prune to about 150 lines. A known pattern is not a finding next
week: name it and move on.

## Filing once

The owner is where the fix lives: how engines read or cite a page is
`aeo-page-optimize` and `brand-monitor`'s; whether search engines index
and rank it is `seo-analyst`'s; everything after the landing (page fit,
CTA, tracking, attribution) is yours. A finding you do not own goes under
Hand-offs with its numbers. Before filing, search open tasks for
`aeo-finding:`, `seo-finding:`, `web-finding:` and the page path; a match
gets this week's number as a comment. At most three new tasks a run, per
`integrations/tasks.md`, each with: evidence (numbers with n, page,
source), expectation, cause and evidence level, proposed action (content
type, topic, source), target metric and its current value, a check date
(1 week for instrumentation, CTA and handoff; 4 weeks for content, SEO and
AEO), a decision rule (done when, drop when), and the lines
`web-finding: <slug>`, `Page: <path>`, `Source: reports/recurring/analytics/YYYY-MM-DD.md`.

Hand-offs: fetched pages no tracked prompt targets, and cited pages, go
to the AEO role; an organic drop that is a rank or index question goes to
the SEO role.
