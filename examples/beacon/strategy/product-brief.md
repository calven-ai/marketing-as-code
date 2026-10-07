---
document: product_brief
source: repo
last_reviewed: 2026-10-01
owner: Ana Ruiz
---

# Product

## Product Overview

- **One-liner:** Beacon is the incident communication platform for SaaS
  support teams: voice templates, audience segments and a customer-facing
  post-incident report, sent to the status page, the product and the inbox
  from one update.
- **What it is:** a hosted web app the support team runs during an
  incident. It sits beside the monitoring tool, not inside it: monitoring
  opens the incident, Beacon tells the customers.
- **Core promise:** the first update goes out in under a minute, reaches
  only the customers who were affected, and ends with a report the
  customer can forward the next morning.

## Capabilities & Features

| Module | Capability | Feature | What it does |
| --- | --- | --- | --- |
| Composer | Write the update | Voice templates | Updates start from wording the team approved once, so nobody faces a blank page mid-incident |
| Composer | Write the update | Incident timeline | Each update adds to one timeline that the status page, the in-app banner and the report all read from |
| Composer | Send everywhere at once | Channel toggles | One update goes to the status page, an in-app banner, email and Slack Connect channels; switch each one on or off per update |
| Audiences | Reach the right people | Audience segments | Target an update by region, plan or feature, so unaffected customers are not alarmed (shipped 2026-08-25) |
| Audiences | Reach the right people | Account sync | Keeps plan, region and owner per account in step with the support tool and the CRM |
| Status page | Show the state | Hosted status page | A branded public page on the customer's own domain, with component status and history |
| Reports | Close the loop | Post-incident report | A plain-language summary built from the timeline, ready for customer success to send without editing |
| Reports | Close the loop | Report analytics | Opens and forwards per report, so support can see who read it |

## Use Cases

- **The incident with a ticket spike:** a regional outage hits one plan
  tier; the update reaches those accounts in under a minute, and the rest
  of the customer base never hears about it.
- **The escalation from a large account:** the account's success manager
  sends the post-incident report the next morning instead of writing one.
- **Replacing the hand-written outage email:** teams that kept the bundled
  status page and wrote emails by hand move the email, the banner and the
  report into one place.
- **Scheduled maintenance:** the same templates and segments announce
  planned work to the customers it touches.

## Integrations

| Integration | Type | Notes |
| --- | --- | --- |
| PagerDuty, Opsgenie, Datadog | Monitoring and alerting | Opens a draft incident in Beacon when an alert fires |
| Zendesk, Intercom, Freshdesk | Support tools | Account sync for segments; tags incident tickets so ticket volume can be measured |
| HubSpot, Salesforce | CRM | Plan, region and owner per account for segments and report sends |
| Slack | Messaging | Internal incident channel, and Slack Connect channels with large customers |
| Any web app | In-product | A script tag shows the in-app incident banner |

## Technical Architecture

- One timeline per incident; every channel and the report render from it,
  so they never disagree.
- Hosted on AWS in the EU and the US; the customer picks the region at
  signup and data stays there.
- The status page runs on separate infrastructure from the app, so it
  stays up when Beacon has its own bad day.
- SOC 2 Type II report available on request; single sign-on on every plan.

## Pricing & Packaging

| Element | Detail |
| --- | --- |
| Per seat | 79 USD per seat per month, billed annually; every feature included |
| Per workspace (from 2026-10-01) | 990 USD per month, billed annually, unlimited seats; for support teams over ten seats |
| Trial | 14 days, no card |
| Deployment | Hosted only, EU or US region |
| Marketplaces | None yet |

## Differentiators & Known Weaknesses

**Differentiators**

- Built for the person who talks to customers, not the person who fixes
  the server: templates, segments and the report are the product, not
  add-ons to a page.
- Audience segments by region, plan and feature; neither Northstar nor
  Pagewise sends a different message to the customers who were affected.
- The customer-facing report: 64 percent open rate across workspaces.
- Proof from the product itself: 48 seconds median time to first update.

**Known weaknesses**

- More expensive than a standalone status page, and the bundled one feels
  free.
- Segments are only as good as the account data; teams with a messy CRM
  spend the first week cleaning it.
- No on-premises option, which rules out a few regulated buyers.
- No SMS channel yet.
