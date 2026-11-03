# ICP template

The twelve H2 sections, in this order. Keep every section and every column. Italic text is a slot: replace it with a cited fact, a labelled inference, or a gap marker. Never add an "evidence" column; citations go inline.

```markdown
# Ideal Customer Profile

## ICP Summary

> Our best-fit customer is a **_company size or segment_** in **_the industries where the value is sharpest_**, with **_the org structure or buying signal that means a budget owner and a champion exist_**, running **_the technology or operating model that makes the product relevant_**, facing **_the trigger or pain that forces them to act now_**.

## Firmographic Attributes

| Attribute | Ideal range | Why it matters |
| --- | --- | --- |
| Company size | _best-fit employee band_ | Complexity and budget to justify the purchase |
| Annual revenue | _revenue floor that supports the price_ | Account scale justifies the investment |
| Industry | _verticals where the value is sharpest_ | Where the problem is most acute |
| Geography | _target regions_ | Coverage, language, regulation, reach |
| Org structure | _the team or role that owns the problem_ | A buyer and a champion already exist |
| Operational footprint | _the scale or complexity that creates the need_ | The problem is big enough to pay to solve |

## Technographic Attributes

| Attribute | Ideal signal | Why it matters |
| --- | --- | --- |
| Core systems in use | _tools the product integrates or co-sells with_ | Integration and co-sell motion |
| Adoption or migration state | _the change in motion that opens a window_ | A transition forces a buying decision |
| Existing program maturity | _the initiative that means they are ready_ | Mature enough to value the product |
| Incumbent tooling | _tools the product displaces or consolidates_ | Displacement opportunity |
| Deployment needs | _the deployment model the product fits_ | Where it beats narrower alternatives |

## Behavioral Attributes

| Attribute | Ideal signal | Why it matters |
| --- | --- | --- |
| Decision culture | _data-driven, committee-led or champion-led_ | Who to mobilise and how the deal runs |
| Buying process | _trial-led, RFP, top-down mandate_ | How to sell and how long it takes |
| Build or buy posture | _willingness to buy rather than build_ | A build bias disqualifies; a buy bias accelerates |
| Engagement signals | _events, communities, content they consume_ | Observable intent and reachability |
| Prior tool adoption | _track record with adjacent tools_ | Predicts adoption and expansion |
| Domain maturity | _how advanced their practice is_ | Too early means long education; too late means an entrenched incumbent |

## Use Cases & Pain Points

- **_Use-case theme_:** _the problem that makes a best-fit account buy, and the pain behind it._

## Buying Triggers / Signals

| Trigger | Signal | Urgency |
| --- | --- | --- |
| _trigger type, such as a new leader or a migration_ | _the observable event to watch for_ | _High, Medium or Low_ |

## Segment Tiers

| Tier | Definition | Fit criteria |
| --- | --- | --- |
| Tier 1: Core | _the sweet spot_ | _the firmographic, technographic and trigger combination of an ideal account_ |
| Tier 2: Expansion | _strong fit, lighter on one axis_ | _meets most criteria, missing one_ |
| Tier 3: Opportunistic | _plausible fit, weaker signals_ | _interest or partial fit, no urgent trigger_ |

## Priority Verticals

| Vertical | Sizing proxy | Lead angle | Why we win here |
| --- | --- | --- | --- |
| _short vertical name_ | _relative size or deal value signal_ | _the message that lands here_ | _why the product fits best_ |

## Secondary Verticals

| Vertical | Why it is secondary | Angle if a deal comes |
| --- | --- | --- |
| _plausible-fit vertical_ | _smaller, less proven, harder to reach_ | _the angle to use_ |

## Disqualifiers / Anti-Profile

- **_Pattern_:** _why it kills the deal._

## Blacklisted Verticals & Regions

| Vertical or region | Reason |
| --- | --- |
| _hard exclusion, or "None"_ | _regulation, sanctions, no support coverage, strategy_ |

## ICP Fit Scorecard

Scores FIT only; keep buying intent (site visits, content downloads) out of it.

| Criterion | Weight | Scoring guide |
| --- | :---: | --- |
| Industry or vertical fit | 25 | _core 25, adjacent 12, other 0_ |
| Company size or revenue | 20 | _ideal 20, acceptable 12, below 0_ |
| Buyer and sponsor present | 20 | _both 20, one 10, neither 0_ |
| Tech stack or operational fit | 15 | _in use 15, planned 8, none 0_ |
| Active trigger | 15 | _strong 15, soft 7, none 0_ |
| Complexity or scale of need | 5 | _high 5, moderate 3, low 0_ |
| **Total** | **100** | **80 or more: Tier 1. 50 to 79: Tier 2. Under 50: Tier 3 or disqualify** |
```

The weights and thresholds above are sound defaults. When the sources give no better basis, keep them and label the table `_Template default: calibrate with your team._` What needs the company's input is the scoring guide per criterion.

A Vertical cell holds only the vertical's short name (60 characters at most). Qualifiers and inference labels go in the row's other cells.

## Several products

When the company sells more than one product, write one portfolio ICP plus one ICP per product.

**Portfolio ICP** (nine sections): ICP Summary, Firmographic Attributes, Segment Tiers, Priority Verticals, Secondary Verticals, Disqualifiers / Anti-Profile, Blacklisted Verticals & Regions, ICP Fit Scorecard, Product Coverage Matrix.

- Firmographics are the qualification floor an account must clear for **any** product: the intersection across products, never the union. Where two products disagree on a band, the portfolio value is the one both clear.
- One company-wide scorecard, so every product's scores compare.
- Product Coverage Matrix: `| Product | Best-fit segments | Priority verticals | Coverage notes |`, one row per product. A product with no ICP yet gets a row saying so.
- Write the summary last, from the finished document.

**Product ICP** (eight sections): Product ICP Summary, Firmographic Overrides, Technographic Attributes, Behavioral Attributes, Use Cases & Pain Points, Buying Triggers / Signals, Best-Fit Segments, Product-Specific Disqualifiers.

- It records only where this product's buyer deviates from the portfolio floor. Restating the floor hides the deltas that are the point of the document.
- Firmographic Overrides: `| Attribute | Override for this product | Why it differs |`. If nothing differs, one line saying the product inherits the portfolio firmographics.
- Best-Fit Segments: `| Segment | Definition | Fit criteria |`, the sweet spot first, then the expansion segment.
- Sources describe the whole company. Use only what pertains to this product; a page that never mentions it is not evidence about it. Research the product fully all the same: its pages, the customer stories that name it, its integrations.
