# Metric definitions

> **Template: unfilled.** Type over the brackets, or say `/setup` and answer a
> few questions. Agents: an unfilled definition means "ask the team", never
> "use the industry default".

One row per term the team uses in reports. The Definition column must be
precise enough to compute from raw data.

| Term | Definition (exact) | Computed from |
| --- | --- | --- |
| *Example: Signup* | *created an account and verified the email address* | *product database, `users.verified_at`* |
| Signup | [e.g. "created an account, verified email"] | [system + event/field] |
| Activation | [the specific action that counts] | |
| MQL | [the exact criteria: score? action? list membership?] | |
| SQL | [who flips the bit, based on what] | |
| Opportunity | | |
| Win | | |
| Pipeline ($) | [which stages count, at what probability] | |
| Search location | [the one market search pulls measure, e.g. United States] | `scripts/seo_rank_track.py`, `scripts/seo_snapshot.py` |
| Search language | [its language code, e.g. en] | the same pulls |
| [add your own] | | |

## Web sessions

The default definitions for web reports (`web-analyst`); edit them here,
never in a report.

| Term | Definition (exact) | Computed from |
| --- | --- | --- |
| Session | one visit, attributed to its entry (`naming.md`, Channels and sources); reports say "sessions", never "visitors": cookieless and consent-limited tracking cannot count people | the analytics tool's session id |
| Human session | a session that is neither an engine fetch nor another bot; the denominator of every web rate | the class rule below |
| Engine fetch | an answer engine's link fetcher reading a page to answer a prompt: tagged by an engine, no referrer, under 5 s, no scroll, at most one pageview. The AEO leading indicator, counted per page, never in a rate | session class `engine_fetch` |
| Other bot | the same shape without an engine tag | session class `other_bot` |
| Engaged session | a human session lasting 30 s or more, or with two or more pageviews, or scrolled past half the page | session duration, pageviews, scroll depth |
| Content type | what a page is for: home, pricing, product, comparison, guide, template, legal, other; a property the site stamps on every event, else a rule on the URL path | `content_type` property or path |
