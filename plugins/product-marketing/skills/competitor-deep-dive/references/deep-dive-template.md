# Deep-dive template

Copy this structure in this order. Keep every heading; a section with nothing sourced holds only the not-enough-data line. Every paragraph, bullet and table row ends with one or more source markers (`[^slug]`), placed in the cell they support. You may add `###` subsections and tables inside a section, never new `##` headings.

Slugs are lowercase and hyphenated, named for the source: `pagewise-pricing`, `pagewise-about`, `analyst-report-2026` (a year only when the source itself carries one), `win-loss-notes-q3` for a file. Define each slug once in Sources and reuse it.

```
# <Competitor>: deep dive

## At-a-glance
| Field | Value |
| --- | --- |
| Website | <url>[^slug] |
| Threat level | High / Medium / Low, or Unknown[^slug] |
| HQ / Founded | <city, country> / <year>[^slug] |
| Size | <employees> · <revenue or total funding>[^slug] |
| Ownership | Private / Public / PE-backed / Acquired by <company> (<date>)[^slug] |

## Company snapshot
Who they sell to: segments, industries, company sizes, named reference customers. Only what changes how you sell.

## Positioning and messaging
Category claim, tagline, core value propositions, stated audience, any competitor they name or compare against, in their own words (short verbatim quotes from their homepage and product pages).

## Product
**Deployment:** SaaS / on-premises / hybrid, regions, runtime requirements.[^slug]
**Notable integrations:** <named systems>[^slug]

### <Module or product name>
| Capability | What it does | Notes (maturity, gaps) |
| --- | --- | --- |

### Recent product motion
- <YYYY-MM-DD> <launch, GA, beta, deprecation, roadmap item>[^slug]

## Pricing and packaging
| Element | Detail |
| --- | --- |
| Packaging / editions | |
| Pricing model and unit | |
| Published prices | |
| Free tier / trial | |
| Billing terms | |
| Add-ons | |
| Discounting / contract tactics | |
| Cost traps | |
If pricing is not published, say so and cite the page you checked.

## Trust and security
| Item | Status | Detail (period, scope, date) |
| --- | --- | --- |
Certifications and attestations, data regions, security capabilities (SSO, SCIM, audit logs, customer-managed keys), subprocessors of note (especially AI vendors), pen test or bug bounty.

## Legal terms
Data categories processed, processing purposes (model training in particular), contracting entities and governing law, transfer mechanisms, retention, liability and SLA terms, AI or automated-decision clauses. Quote the operative sentence.

## Company moves (last 12 months)
| Date | Move | Type | Source |
| --- | --- | --- | --- |
Type: funding, acquisition, launch, partnership, executive change, customer, financial, certification, expansion, recognition, pricing, layoffs. Date by the original announcement.

## Market activity
Named customers and case studies, named integrations, comparison or migration pages, first-party numbers (customers, ARR, usage, growth).

## Analyst and market standing
Analyst evaluations and software review sites: their placement and rating, and yours relative to theirs when a source compares both.

## Strengths (be honest)
3 to 6 bullets: genuine advantages buyers like, each sourced.

## Weaknesses and vulnerabilities
3 to 6 bullets: concrete gaps and repeated complaints from reviews, analysts and win/loss. Buyer-side evidence only.

## Claims vs their own docs
| Surface | Claim | Reality (per their docs) | Source |
| --- | --- | --- | --- |
Surface is where the claim lives (homepage hero, review-site tagline, their sales deck). Source is the docs page that contradicts it.

## Feature comparison
| Capability | <Your product> | <Competitor> |
| --- | --- | --- |
Yes / Partial / No. A backup reference: lead with outcomes, not this grid.

## Win/loss evidence
| Direction | Weight | Reason | Evidence |
| --- | --- | --- | --- |
Direction: for you / against you. Weight: decisive / contributing. Evidence: a verbatim quote attributed to a role, and the file or call it came from.

## Sources and freshness
- **Last updated:** YYYY-MM-DD
- **Review cadence:** every two weeks and on any material change (Tier 1), quarterly (others).
- **Rerun the claims check** after their next major launch or a site or docs refresh: that is when claims and manual drift apart.

[^slug]: <Publisher>: <page or document title>. <URL or file name>. Published <date the source states, or "undated">. Read <YYYY-MM-DD>.
```

## What goes where, in short

- At-a-glance: facts a rep reads in five seconds. "Unknown" beats a guess.
- Positioning comes from their homepage and product copy, so it can be recognised and reframed.
- Product is the deepest section: one subsection per module.
- Pricing is the most volatile section; record the unit and billing basis, not only the number.
- Weaknesses come from the outside world and your own deals, never their website.
- Claims vs their own docs is the highest-trust trap material: their words against their own manual. A claim you cannot contradict from their docs does not belong here.
- Feature comparison and Win/loss need your side; without it, the not-enough-data line says so.
- Their case studies, customers, metrics and awards belong in Strengths or Market activity. They are never your proof.
