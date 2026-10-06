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
