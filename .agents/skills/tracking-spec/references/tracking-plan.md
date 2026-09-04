<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/analytics/SKILL.md | license: MIT | fetched: 2026-09-04 -->

# A tracking plan, and how to audit one

## The plan

One row per event, and every event answers "which decision does this
inform". An event nobody would act on is noise that costs quota and
attention: leave it out.

| Column | Holds |
| --- | --- |
| event | object-action, lowercase, underscores: `signup_completed`, `demo_requested`, `pricing_viewed` |
| means | one sentence, the exact condition |
| emitted by | the system that fires it (site, product, tag manager, CRM) |
| properties | name, type, allowed values; the campaign properties (`source`, `medium`, `campaign`, `content`) come from the URL, not typed by hand |
| trigger | what the code or the tag checks before firing |
| decision | what the team does differently because of the number |

Properties that recur: page (`page_title`, `page_path`), user (`user_id`,
`plan`), campaign (the UTM set), product (`product_id`, `price`,
`category`). `data/ontology/events.md` is the plan in this repo; the
columns above map onto its table.

## What to track per funnel stage

- Marketing site: primary CTA clicks, form submissions, signups, demo
  requests, pricing views, content downloads.
- Product: onboarding steps completed, the activation action
  (`data/ontology/metrics.md` says which), key feature use, upgrade,
  subscription started, cancelled.

The conversion events are the subset `funnel.md` uses to move a record
between stages; mark exactly those as key events in the tool.

## Audit checklist

- Events fire on the right trigger, once: verify in the tool's debug view
  (GA4 DebugView, PostHog live events) and the tag manager's preview.
- Property values populate, with the allowed values and nothing else.
- No duplicate events across containers or SDKs (a site with both a
  tag-manager tag and a direct SDK call fires twice).
- Works across browsers and on mobile.
- No PII in any property or in a URL parameter (email, name, ids that
  identify a person).
- Conversions marked in the tool's admin match the ontology's list.
- UTMs lowercase and only on external links.

## Implementation notes

- GA4: `gtag('event', '<event>', {<properties>})` or a data-layer push
  the tag manager turns into a GA4 event tag; custom properties need a
  custom dimension registered before they appear in reports.
- Tag manager: one data-layer structure the site pushes, triggers on the
  data-layer event, tags per destination. The site owns the push; the
  tag manager only routes it.
- Product analytics (PostHog and similar): the SDK call in the product
  code, the same event names as the taxonomy, `identify` on login so
  events join to the person.

## The questions to ask before writing a plan

Which tools; which decisions the data informs; what is tracked today;
the stack and any consent or compliance constraints; who implements
(engineering or the tag manager owner).
