# Battlecard template

Sections in this order. Every row, bullet and block ends with one or more source markers (`[^slug]`), defined once under Sources. Use `[^deep-dive]` for the competitor deep dive, `[^product]`, `[^icp]` and `[^positioning]` for your own documents, a file slug (`[^win-loss-q3]`) for deal notes, and a page slug (`[^pagewise-pricing]`) for anything you confirmed live.

```
# <Your company> vs <Competitor>

## At-a-glance
| Field | Value |
| --- | --- |
| Competitor | <name>[^deep-dive] |
| Threat level | High / Medium / Low, or Unknown[^deep-dive] |
| Our wedge | <2 or 3 words>[^deep-dive] |
| **Last updated** | YYYY-MM-DD |
| Card owner | <the person who asked> |

## TL;DR
- **We win when:** <one sentence>[^deep-dive][^product]
- **Do not attack:** <their genuine strengths>; attack on <X> and <Y> instead.[^deep-dive]

## Top strengths (concede) / Top weaknesses (attack)
| Top strengths (be honest) | Top weaknesses (our openings) |
| --- | --- |
| <strength>[^deep-dive] | <weakness>[^deep-dive] |
| <strength>[^deep-dive] | <weakness>[^deep-dive] |
| <strength>[^deep-dive] | <weakness>[^deep-dive] |

## How we win
- **<scenario>** → <the play, one line>[^deep-dive][^product]
- **<scenario>** → <the play>[^win-loss-q3]

## Landmines to set
- _"One thing worth asking <Competitor>: <question>"_ (exposes <the gap>)[^deep-dive]

## Top objections
| They say | You say |
| --- | --- |
| _"<objection, in the buyer's words>"_[^deep-dive] | <validate, then reframe, then proof>[^product] |

## Talk track
<two or three spoken sentences framing the category in your favour>[^deep-dive][^product]

## Proof points
- **<Customer> on <your product>: <outcome>.** <one line with the figure or the switch story>[^positioning]
- **<Review site or analyst>: <your standing, against theirs if the source compares>**[^positioning]

## Sources
[^deep-dive]: <Competitor> deep dive, <file or doc name>, last updated YYYY-MM-DD.
[^pagewise-pricing]: Pagewise: Pricing. https://... Read YYYY-MM-DD.
```

## Exact lines for empty sections

Write the line alone as the section body when its condition holds. Replace `<Competitor>` with the name.

- Strengths/weaknesses: `_Not enough data (no sourced strengths or weaknesses for <Competitor> yet; run competitor-deep-dive first)._`
- At-a-glance: `_Not enough data (no header facts for <Competitor> could be sourced)._`
- How we win (draft): open the section with `_Draft: no won deals against <Competitor> recorded yet; built from their weaknesses and our differentiators._`
- How we win and TL;DR (nothing to pair): `_Not enough data (no won deals against <Competitor>, and no weakness of theirs that a differentiator of ours answers)._`
- Landmines: `_Not enough data (no sourced weakness or contradicted claim to build a trap on)._`
- Objections: `_Not enough data (no recorded objections and no differentiators of ours to answer with)._`
- Talk track: `_Not enough data (no differentiators of ours to frame the category with)._`
- Proof points: `_Not enough data (no customer proof of ours against <Competitor> yet)._`

## Several products

If you sell more than one product and this competitor meets more than one, keep the portfolio-level lines first in How we win and Talk track, then one `###` subsection per contested product (`### How <Product> wins`, `### <Product> talk track`), each with its own two-to-three-line budget and no repeats of the portfolio lines. The TL;DR stays two lines; if the strongest scenario is product-specific, name the product in it.
