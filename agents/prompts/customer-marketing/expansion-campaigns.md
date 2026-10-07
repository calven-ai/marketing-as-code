# Expansion campaigns

**Reads:** `data/crm/snapshots/` (customers, subscriptions, deals),
`data/analytics/snapshots/` (usage), `strategy/product-brief.md`,
`strategy/personas.md`, the latest expansion report in `reports/adhoc/`,
`reports/recurring/customer/` · **Skills:** `/expansion-play` ranks the
accounts ready to buy more and `/churn-signals` lists the ones at risk;
these prompts build the campaign around the list and decide what to offer.

Your best pipeline is often the customers you already have, but an upsell
email to an account that's quietly unhappy does more harm than good. You
walk away with a campaign aimed at accounts that are actually ready, a
message tied to what they already use, and an offer chosen on expected
value rather than gut. Run `/expansion-play` for the ranked list first.

## Prompts

### Find accounts that already asked for it

```
Using this repo, find customers who've already asked for the product or tier below.

FILL IN
- Product: [product or tier we'd expand them into]

CONTEXT
The warmest expansion lead is a customer who asked. Those requests are scattered across calls, reviews and community threads.

READ FROM THE REPO
- Calls in memory/transcripts/processed/ that mention the product or the need it solves.
- Reviews and survey answers in data/reviews/snapshots/.
- Community digests in reports/recurring/community/.

BUILD
- A list: account, what they said, where, when.
- Cross-check against data/crm/snapshots/: do they already own it, and who's the owner?
- Remove anyone on the latest churn list in reports/recurring/customer/.

OUTPUT
A table of accounts with the verbatim and the owner.

GROUNDING
Cite the file behind every request. Quotes verbatim. Don't infer a request from a vague complaint.
```

### Write the expansion email

```
Using this repo, write the expansion email for accounts on the list below.

FILL IN
- Product: [product or tier]
- Persona: [persona]
- Accounts: [paste the list, or name the expansion report]

CONTEXT
These customers know us. The email should start from what they already use, not from a pitch.

READ FROM THE REPO
- What the product does and how it connects to what they own, in strategy/product-brief.md.
- The persona's goals in strategy/personas.md.
- A case study or quote from a customer who expanded, in content/ or memory/knowledge/.

WRITE
- Subject, opener tied to their current use, the one outcome the expansion adds, proof, a soft ask.
- A personalisation slot per account (what they use today) and where to fill it from.

OUTPUT
One email and its slots, as a content draft on a branch if I say save.

GROUNDING
Cite paths. No invented usage numbers or discounts. Don't send anything.
```

### Fact-check the campaign assets

```
Using this repo, check the expansion campaign assets below before they go out.

FILL IN
- Assets: [paste them, or name their folders in content/]

CONTEXT
Customers notice when we describe our own product wrong.

READ FROM THE REPO
- strategy/product-brief.md: tiers, modules, what's included where.
- strategy/messaging.md and brand/voice.md.
- Pricing decisions in memory/decision-log.md.

CHECK
- Every product and packaging claim against the product brief.
- Any price or discount against logged decisions.
- Voice and message.

OUTPUT
A findings table and corrected copy.

GROUNDING
Cite paths. A price that isn't in the product brief or the decision log is removed and flagged.
```

## Advanced prompts

### Pick the offer with an expected-value tree

```
Pick the expansion offer with an expected-value decision tree, not a hunch. Use this repo for how many accounts qualify, how they've converted before and what's at stake.

FILL IN
- Offers: [two to four, e.g. discounted upgrade, free trial of the add-on, an onboarding session]
- Cost of each offer: [per account]

CONTEXT
Each offer costs something and pulls a different share of accounts. I want the one with the best expected return, and to know how sure we are.

FROM THE REPO
- The qualifying accounts and their current spend from the latest expansion report in reports/adhoc/ and data/crm/snapshots/.
- Past expansion deals and their win rate from the closed-deals snapshot.
- Accounts at risk from reports/recurring/customer/, since an offer to them carries churn risk.

METHOD
- Draw the tree per offer: accept or not, then expand or not, then retained or churned.
- Fill probabilities from past deals where they exist; elsewhere state an assumption with a range.
- Compute expected net revenue per account per offer.
- Sensitivity: which probability flips the choice, and by how much it has to move.

OUTPUT
The tree as a table, expected value per offer with a range, the pick, and the one number to watch.

GROUNDING
Label every number as repo (file path and n), mine, or your assumption. Never invent a past conversion rate; if there are no past expansion deals, say so.
```

## Questions to just ask

- Which customers are on the latest expansion list?
- Which accounts own only the entry tier after a year?
- Which expansion candidates are also on the churn list?
- Who owns [account], and when is their renewal?
- Which customers asked for [product] on calls?
- How many expansion deals did we close last quarter?
- What does the product brief say the upgrade path is?
- Which persona usually signs off on an expansion?
- Do we have a case study of a customer who expanded?
- Which accounts' usage grew most in the last 90 days?
- What did we decide about expansion discounts?
- Which accounts haven't heard from us in six months?
