# Funnel and lifecycle stages

## Stages, in order

| Stage | Entry condition (exact) | Exit → next stage when | Lives in |
| --- | --- | --- | --- |
| Visitor | A session on the website | Creates a workspace | PostHog |
| Signup | Verified email on a workspace | Publishes a first update | Product database |
| Activated | First update published within 14 days | Company size or demo request qualifies | Product events |
| MQL | 50 or more employees, or a demo request | Sales accepts after a discovery call | HubSpot |
| SQL | Accepted by sales | Deal closed won | HubSpot |
| Customer | A paid plan | Never, unless churned | HubSpot |

## Rules of interpretation

- A record can skip Activated (a demo request from a large company goes
  straight to MQL). It never moves backwards; a lost SQL stays an SQL with
  a closed-lost deal.
- HubSpot is authoritative from MQL onwards; the product database before
  that. When they disagree, the product database wins for counts of
  signups and activations.
- Attribution is first touch, from the PostHog `initial_referrer` on the
  workspace creator.
