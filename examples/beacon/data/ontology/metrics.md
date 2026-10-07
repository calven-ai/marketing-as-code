# Metric definitions

One row per term the team uses in reports. The Definition column is
precise enough to compute from raw data.

| Term | Definition (exact) | Computed from |
| --- | --- | --- |
| Signup | Created a workspace and verified the email address | Product database, `workspaces.verified_at` |
| Activation | Published a first status page update, test or real, within 14 days of signup | Product events, `update_published` with `first = true` |
| MQL | A verified signup at a company with 50 or more employees, or any signup that requested a demo | HubSpot, contact property `lifecycle_stage = marketingqualifiedlead` |
| SQL | An MQL a salesperson accepted after a discovery call | HubSpot, `lifecycle_stage = salesqualifiedlead` |
| Pipeline ($) | Sum of open deal amounts in stages Discovery, Evaluation and Proposal | HubSpot deals, `amount` where `dealstage` in those three |
| Search location | United States | keyword and SERP pulls |
| Search language | en | keyword and SERP pulls |
| Session | A PostHog session on example.com, bots and answer-engine fetches excluded; never "visitors" | PostHog, `$session_id` on `$pageview` |
| Campaign-attributed MQL | An MQL whose first-touch session carries the campaign's `utm_campaign`, or whose first pageview is a page the campaign brief lists, inside the campaign window | HubSpot `first_touch_campaign`, PostHog first pageview |
| Cost per MQL | Platform spend for a campaign divided by its campaign-attributed MQLs | Ad platform spend, HubSpot |
| Pieces published | `content/` pieces whose `published` date falls in the quarter | `content/` frontmatter |
| Named in AI answers | Prompts in `data/seo/prompts.csv` where at least one tracked engine names the brand, out of the active prompts | `*-aeo-results.csv`, `mentioned = true` |
