<!-- source: https://raw.githubusercontent.com/NEON-Rutger/B2B-revops-skills/main/win-loss-program/SKILL.md | license: MIT | fetched: 2026-09-04 -->
# Driver rules and starter taxonomy

Open this file at step 2 (extraction), step 3 (labels) and step 5 (groups).

## What is a driver

**It moved the decision.** Would the deal plausibly have gone differently, or been harder to close, without it? A feature wish raised in passing, a minor process gripe, or a preference never weighted is not a driver. Counter-outcome drivers (a gap on a won deal, a strength on a lost one) are exempt from this test: by definition they did not decide the deal, and they still belong.

**It comes from what the buyer wrote or said.** Scores, dropdown picks and comparison-table cells are facts about the deal, not reasons. A 2 of 4 sales rating is not a driver. "More expensive" picked from a pricing question says what the price was, not that price cost the deal. Only the buyer's own sentences turn a fact into a reason.

**Short is not empty.** "Cheaper. Good support." gives two drivers. "Templates." names what they valued. Only placeholder answers ("n/a", "-", "none", "nothing really") carry nothing. A response with ratings and picks but no free text yields no drivers, and that is the correct answer.

**No target number.** A buyer who wrote three paragraphs supports more drivers than one who wrote a line. Never write a row to reach a count; never drop a real reason because you have several.

**Read the detail back.** If it only restates the question, or says something was mentioned without saying what mattered about it, drop it.

## How to write a label

- **An attribute of the user's company, with the judgement in it.** A rival doing something better is our gap; a rival doing something worse is our strength. "The rival's status page shows more history" becomes `Weak status page history`. "The rival had no post-incident report" becomes `Strong post-incident report`.
- **A judgement word carries the meaning**: Weak, Strong, Missing, Narrow, Slow, Expensive, Clear, Fast.
- **Never start with "Our" or "Rival's".** The first is a dead word down the column; the second splits one gap into a separate label per rival.
- **Never put a rival's name in the label.** `Broader functionality than Pagewise` becomes `Broader functionality`; the rival goes in the rivals column, so the same gap aggregates across deals.
- **Situation drivers name nobody.** When no attribute of ours is behind it: `Incumbent contract in place`, `Competing platform commitment`, `Budget moved to another project`.
- **No double negatives.** "Rival's lack of a tested advantage" says nothing; write what is true: `Head-to-head trial performance`.
- **Short noun phrase, reusable across deals:** no deal names, no people, no dates.

## Rivals on a driver

- List every rival the statement is true of: "the poorest of all three" names all three.
- Only rivals the buyer connected to this driver, not every vendor mentioned in the survey.
- A buyer building or keeping their own solution is the rival `In-house build`, always spelled exactly that way.
- Leave the list empty when the driver is about no rival (our onboarding, their budget, a reorg). Most drivers are like this.

## Gate: reasons to drop

Outcome side only: a pleasantry, a restatement of the outcome ("we lost"), a rating restated as a sentence, a feature wish in passing, a gripe that did not bear on the decision, a duplicate in the same deal and direction. Counter-outcome side: drop only if the buyer did not actually say it, or it duplicates another candidate. "Not decisive" is never a reason to drop a counter-outcome row.

## Tidy: merge test

Would a seller or product manager act on the two labels differently? Same fix closes both: merge. Different work: keep apart.

| Merge | Keep apart |
|---|---|
| `Missing CRM sync` + `No Salesforce write-back` | `Missing SSO` vs `Missing SCIM` |
| `Price too high` + `Pricing too expensive` | `Expensive per seat` vs `Pricing not in writing` |
| `Weak status page history` + `Shallow incident history` | Two different named integrations |

## Starter groups

Use these when the user has no taxonomy yet; rename or merge them to fit the business, then keep them stable. Aim for six to nine groups with at least three labels each.

| Group | Covers |
|---|---|
| Product capabilities | Something they needed that we do not do, or do worse, and what we do better |
| Integrations and fit | How the product fits their stack and workflow |
| Trust and proof | References, security, viability, believability of claims |
| Price and value | Value not believed at the price, packaging, licensing terms |
| Champion and stakeholders | Whether anyone inside carried it, who opposed, who held the budget |
| Competitive situation | The incumbent, a rival's offer or relationship, an in-house build |
| Timing and budget | Budget cut or moved, priorities shifted, no critical event |
| Sales experience | Our process: speed, expertise, demo, follow-through |

For a stable comparison across quarters, also allow each deal one primary and one secondary group, taken from its decisive and strongest contributing drivers. Single-cause coding hides most of what happened.
