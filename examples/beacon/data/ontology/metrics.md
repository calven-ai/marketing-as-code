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
