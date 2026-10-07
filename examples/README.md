# examples/

Beacon is a fictional B2B company: an incident communication platform for
SaaS support teams, four people in marketing, frozen on 2026-10-07. `beacon/`
is this repo after a team has run it for a quarter. Every path mirrors the
real one, so the template and the example open side by side.

## A tour in the order things happened

1. **Context.** [Positioning](beacon/strategy/positioning.md) came out of a
   workshop, now an [archived project](beacon/projects/_archive/positioning-workshop/brief.md)
   with its [decision](beacon/memory/decision-log.md). Around it:
   [messaging](beacon/strategy/messaging.md), [ICP](beacon/strategy/icp.md),
   two [personas](beacon/strategy/personas.md), the
   [product brief](beacon/strategy/product-brief.md) and battlecards for
   [Northstar](beacon/strategy/competitive/northstar.md) and
   [Pagewise](beacon/strategy/competitive/pagewise.md).
2. **Brand.** The [brand library](beacon/brand/library/index.html) (download
   the repo and open it in a browser) shows it page by page:
   [voice](beacon/brand/voice.md),
   [visual identity](beacon/brand/visual-identity.md) and its
   [tokens](beacon/brand/tokens.json), [logos](beacon/brand/logos/),
   [screenshots](beacon/brand/screenshots/) and the
   [image rules](beacon/brand/image-rules.md).
3. **Definitions.** The [ontology](beacon/data/ontology/): funnel, metrics,
   events, naming. [Keywords](beacon/data/seo/keywords.csv),
   [AI-answer prompts](beacon/data/seo/prompts.csv) and
   [tracked brands](beacon/data/seo/brands.csv).
4. **A campaign.** [The Q3 launch](beacon/projects/q3-launch/campaign.md) has
   three child projects (launch content, comparison page, paid social). Each
   brief links its pieces in [content/](beacon/content/): a
   [blog post](beacon/content/2026-08-what-customers-want-during-an-outage/draft.md),
   an [email](beacon/content/2026-09-audience-segments-announcement/draft.md),
   a [LinkedIn post](beacon/content/2026-09-launch-linkedin-post/draft.md)
   with its [image kit](beacon/content/2026-09-launch-linkedin-post/kit.json),
   and the [comparison page](beacon/content/2026-09-beacon-vs-northstar/draft.md),
   first mocked as a [playground](beacon/playgrounds/2026-09-10-comparison-page-mock/).
5. **Meetings become memory.** A [status meeting transcript](beacon/memory/transcripts/processed/2026-08-20-q3-launch-status.md)
   paused paid social; the [decision log](beacon/memory/decision-log.md)
   records it and the [paid-social status](beacon/projects/q3-launch/paid-social/status.md)
   shows the restart. One transcript still waits in the
   [inbox](beacon/memory/transcripts/inbox/).
6. **Evidence.** Dated snapshots under [data/](beacon/data/), the
   [Q2](beacon/reports/qmr/2026-q2/report.md) and
   [Q3](beacon/reports/qmr/2026-q3/report.md) reviews with dashboards, the
   [launch retro](beacon/reports/adhoc/2026-10-03-q3-launch-retro/report.md),
   and [recurring reports](beacon/reports/recurring/): weekly, pipeline,
   SEO, competitive, context freshness. What the team learned lives in
   [knowledge/](beacon/memory/knowledge/).
7. **Next quarter.** The [Q4 campaign](beacon/projects/q4-pipeline/campaign.md)
   (a webinar and Tier 1 ABM against [target accounts](beacon/data/accounts/target-accounts.csv))
   and the standalone [customer-stories](beacon/projects/customer-stories/brief.md)
   project, whose case study is a draft with quotes awaiting approval.

Render Beacon's images in its brand:
`python3 scripts/brand_render.py --brand examples/beacon/brand batch examples/beacon/content/2026-09-launch-linkedin-post/kit.json`
(output in the gitignored `examples/beacon/brand/renders/`).

## Rules

It is not your data. Delete this folder when you adopt the repo
(`docs/make-it-yours.md`, step 1); `python3 scripts/doctor.py` reminds you
once your own templates are filled. The check's tests overlay `beacon/` onto
a fixture repository so it passes every rule, and reconcile the Q2 and Q3
reviews against their snapshots.
