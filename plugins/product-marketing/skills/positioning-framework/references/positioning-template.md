# Positioning document template

Eight sections, always in this order, with these headings and table columns. Replace every
`_italic guidance_` with evidence, a labelled inference, or the gap marker. Never leave guidance
in place, never cite it, and never add an "evidence" column: sourcing is the inline citation.
Each section ends with one `Why:` line (procedure step 7).

For a company-level document of a multi-product company, use six sections instead: Company
Positioning Statement, Market Category & Frame of Reference, Competitive Alternatives, Portfolio
Value Themes (columns `Theme | Value (benefit) | Who cares most`, naming the products each theme
rests on), Relevant Market Trends, Proof Points (company-level proof only).

```markdown
# Positioning: <Product>

## Positioning Statement

> **For** _the best-fit customer, in the segment where the value is sharpest_ **who** _the unmet need or problem that forces them to act_, **_product name_** is **_the market category it claims_** **that** _the single most important benefit_. **Unlike** _the primary alternative the buyer would otherwise use_, **_product name_** _the core differentiation the alternative cannot match_.

| Component | Value |
| --- | --- |
| Target customer | _the role and segment it sells to best_ |
| Need / opportunity | _the unmet need or outcome they are chasing_ |
| Product name | _product name_ |
| Market category | _the category it competes in_ |
| Key benefit | _one benefit, not a list_ |
| Primary alternative | _what the buyer uses if the product does not exist: incumbent, status quo or point tools_ |
| Differentiation | _the core differentiation the alternative cannot match_ |

Why: _evidence for the statement; the framing not chosen._

## Market Category & Frame of Reference

- **Category we claim:** _the category, and whether it is an established one or a deliberate reframe of the buyer's mental model._
- **Analyst frame of reference:** _standing in an analyst evaluation, if any; otherwise where analysts currently file this kind of product._
- **Why this frame:** _why this category beats the obvious alternative framing; what a narrower frame would undersell._

## Competitive Alternatives

What the buyer would use if the product did not exist: the real reference set the positioning must beat.

| Alternative | What it is | Why a buyer considers it |
| --- | --- | --- |
| _status quo, point tool, suite incumbent or native option_ | _one line_ | _the specific reason a buyer would pick it over this product_ |

## Unique Attributes

Capabilities the alternatives largely lack. Table-stakes features do not belong here.

- **_Attribute_:** _the capability, in one line._

## Value Themes

| Attribute | Value (benefit) | Who cares most |
| --- | --- | --- |
| _an attribute listed above_ | _the benefit the customer actually gets_ | _the role or segment, using the ICP and persona names when they exist_ |

## Best-Fit Customer Characteristics

The traits that make the value land hardest (consistent with the ideal customer profile, if one exists).

- _verticals or segments where the value is sharpest_
- _company size or org signal that means a buyer and a budget exist_
- _technology or operating model that makes the product relevant_
- _trigger or stalled initiative that forces them to act now_
- _operational complexity (scale, fragmentation, mergers) that creates the need_

## Relevant Market Trends (why now)

Use sparingly, and only trends a cited source supports.

- **_Trend:_** _the shift that makes the value urgent now._

## Proof Points

| Claim | Proof |
| --- | --- |
| _the claim that needs backing_ | _benchmark, ROI study, analyst standing, named customer or outcome metric, attributed and cited_ |

## Sources

1. _title, URL or file name, date read_
```

Gap markers, exactly:

- Inferred: `_Inferred from <evidence>; confirm with the team._`
- No evidence: `_Not enough data._`
- Only the team or market can answer: `_Not enough data: only your team or the market can confirm this._`
- The user said they do not know yet: `_Not tracked yet (per <role>, <date>)._` Do not ask about it again in the next round.
