# Product profile template

Open this when filling the seven sections (step 6). The headings are fixed: keep all of them, in this order, and do not add, rename or reorder any. Inside a section, use paragraphs, lists, tables and sub-headings freely.

## How to fill it

- **Keep the structure.** Every section and every table column stays. Put the gap marker in the individual cell you cannot support and fill the rest. Use a single gap line for a whole section only when nothing you read bears on any of it.
- **Rows are slots, not quotas.** Write one row per real item the evidence supports. Never numbered empty rows ("integration 1 ... 4"), never a row whose every cell is a gap.
- **Cite every fact** with `[n]`, pointing at the numbered Sources list. Do not add an "evidence" column; the citation is the evidence.
- **Label an inference once.** When a whole table or section is inferred from the same evidence, say so in one line under the heading. Label a single cell only when it differs from the rest.
- **Say each thing once.** No duplicate rows, no repeated caveat or testimonial across sections. A figure that proves two claims is cited in both places briefly, not restated in full.
- **Gap markers:** `_Not enough data: only your team can confirm this._` for what only the team knows; `_Not enough data from the sources read._` for what the sources simply did not cover.

## The template

```markdown
# Product profile: <Product>
Company: <Company> · Mode: <Create | Update> · Sources read: <n> · As of <YYYY-MM-DD>

## Product Overview
- **One-liner:** <the product's own one-line description, quoted> [n]
- **What it is:** <form factor and where it sits in the buyer's stack> [n]
- **Target users:** <roles, company size, industries, as stated; or a labelled inference> [n]
- **Core value:** <the promise the source makes, in its words> [n]

## Capabilities & Features
| Module | Capability | Feature | What it does | Source |
| --- | --- | --- | --- | --- |

One row per feature, with a one-sentence description of what it does for the user. Use the module column only when the source groups features into named modules. Add the date a feature shipped when the source states it.

## Use Cases
- **<The situation, in the buyer's words>:** <what the product does in it, and the outcome the source claims> [n]

Primary customer workflows the source markets. Read them off solution pages and customer stories.

## Integrations
| Integration | Type | What it does | Source |
| --- | --- | --- | --- |

Third-party tools, APIs and supported platforms the source names. Group by type (monitoring, CRM, messaging, data). "Hundreds of integrations" without names is a claim, not a list: quote it once.

## Technical Architecture
- **Deployment:** <cloud, self-hosted, hybrid; regions> [n]
- **Architecture:** <what the source states about how it is built> [n]
- **Security and compliance:** <certifications with their period if stated, SSO, SCIM, audit logs, data residency> [n]

Most of this is inferred from security and docs pages. Label it.

## Pricing & Packaging
| Element | Detail | Source |
| --- | --- | --- |

One row per tier, metric, add-on, trial and billing term. Record the unit exactly ("per seat per month, billed annually"). A "contact sales" tier is recorded as that, never as an estimate. Pricing shown only for a bundle is recorded as bundle pricing.

## Differentiators & Known Weaknesses (Internal)
**Differentiators**
- <what the source claims sets it apart, with the proof that backs it> [n]

**Known weaknesses**
- <only from the user's own material, cited; or a conspicuous silence labelled as an unconfirmed observation; otherwise the gap marker>

Internal only: candid weaknesses here never appear in external copy.

## Open questions for the team
- <each gap, as a question the team can answer in one line>

## Sources
1. <URL or file name>, <read YYYY-MM-DD, or dated YYYY-MM-DD>
```

## Portfolio overview (multi-product companies)

When writing the company-level overview instead of a single product's profile, use these six sections in place of the seven above:

```markdown
## Portfolio Overview
## Products & How They Fit Together
| Product | What it does | Who buys it | Link to the rest (data, workflow, platform) | Source |
## Expansion & Cross-Sell Paths
## Shared Platform & Architecture
## Cross-Product Pricing & Bundling
## Portfolio Differentiators
```

The rules for each are in `references/product-or-not.md`.
