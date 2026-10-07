# References and reviews

**Reads:** `data/crm/snapshots/` (customers, open deals),
`data/reviews/snapshots/`, `reports/recurring/reviews/`,
`memory/knowledge/` (the reference roster when it exists), `projects/`
(the advocacy project) · **Skills:** `/advocacy-program` builds the ask
list, drafts and roster, and `/review-monitor` reports what review sites
say; these prompts match references to deals and decide where reviews
matter most.

A rep needs a reference by Thursday for a deal against a competitor you've
never beaten in that segment. Meanwhile your review rating hasn't moved in
a year. You walk away with the right reference for a live deal, briefed
both ways, and a review ask that goes to the customers most likely to say
something specific. To build the program from scratch, `/advocacy-program`
does it.

## Prompts

### Match a reference to a live deal

```
Using this repo, find the best reference customer for the deal below.

FILL IN
- Deal: [account]
- Competitor: [competitor]
- Persona: [the buyer who wants to talk to a reference]

CONTEXT
The reference has to look like the buyer: same segment, same persona, ideally switched from the same competitor.

READ FROM THE REPO
- The reference roster in memory/knowledge/, if there is one, and the advocacy project in projects/.
- The customer base in data/crm/snapshots/ with segment, tenure and owner.
- Won deals against the competitor in the closed-deals snapshot.

BUILD
- Three candidates ranked by match: segment, persona, competitor, tenure.
- For each: when they last gave a reference, so we don't burn them.
- What each can speak to, from calls in memory/transcripts/processed/ or their reviews.

OUTPUT
A short ranked list with one line on why each fits.

GROUNDING
Cite paths. Don't list a customer as a reference unless the roster or a logged decision says they agreed. If there's no roster, say so and suggest /advocacy-program.
```

### Brief the reference and the rep

```
Using this repo, write the two briefs for the reference call below: one for the customer, one for the rep.

FILL IN
- Reference: [account]
- Deal: [account]

CONTEXT
The customer is doing us a favour; they need two minutes of context. The rep needs to know what the reference can and can't speak to.

READ FROM THE REPO
- Both accounts in data/crm/snapshots/.
- What the reference said on calls in memory/transcripts/processed/ and in reviews in data/reviews/snapshots/.
- The prospect's likely objections from strategy/personas.md.

WRITE
- Customer brief: who the prospect is, what they're worried about, three topics that would help.
- Rep brief: what the reference has said on record, what to avoid asking, how to thank them.

OUTPUT
Two short briefs. Save as a content draft on a branch if I say save.

GROUNDING
Cite paths. Never script the customer's answers. Don't share the prospect's deal size or internal notes with the reference.
```

### Build this month's review ask list

```
Using this repo, build this month's list of customers to ask for a review, and what to ask each about.

CONTEXT
Generic review asks get generic reviews. I want customers who'll be specific about the strengths buyers compare us on.

READ FROM THE REPO
- The latest review report in reports/recurring/reviews/ and the reviews snapshot in data/reviews/snapshots/.
- The customer base with health, tenure and NPS in data/crm/snapshots/ and data/reviews/snapshots/.
- The pillars in strategy/messaging.md.

BUILD
- Which pillars reviews already mention and which they never do.
- Twenty customers to ask, excluding anyone asked in the last six months or with an open support issue.
- Per customer: the pillar they could speak to, with the evidence.

OUTPUT
A table of asks. The drafts come from /advocacy-program.

GROUNDING
Cite paths. Never pick a customer as happy without a score, a review or a call line. Don't offer anything in exchange for a positive review.
```

## Advanced prompts

### Simulate how many reviews it takes to move the rating

```
Work out how many new reviews it takes to move our rating, and whether that's realistic. Use this repo for the current reviews and how customers have rated us.

FILL IN
- Target rating: [e.g. 4.6]
- Platform: [the review site]

CONTEXT
Leadership wants the rating up by next quarter. I want to know whether that's twenty reviews or two hundred.

FROM THE REPO
- Every review with rating and date from data/reviews/snapshots/.
- The response rate of past review asks, from the advocacy project in projects/ or the email snapshots.

METHOD
- Model the rating distribution of new reviews from the last twelve months (not all time).
- Monte Carlo: for N new reviews from 10 to 200, simulate the resulting average 10,000 times.
- Find the N where the target is hit in 80% of runs.
- Divide by the ask response rate to get how many customers we'd have to ask.
- If you can run code, plot probability of hitting the target against N.

OUTPUT
The N, the asks it implies, and a verdict: realistic this quarter or not.

GROUNDING
Label every number as repo (file path and n), mine, or your assumption. If there's no response-rate data, say so and show the answer for a range of rates.
```

## Questions to just ask

- Who's on the reference roster, and who was used most last quarter?
- Which customers in [segment] switched from [competitor]?
- What's our average rating this year versus last?
- Which pillars do reviews never mention?
- Which customers left a review in the last 90 days?
- Who gave a reference this month and shouldn't be asked again yet?
- What do negative reviews complain about most?
- Which promoters have never been asked for anything?
- What did the last review report recommend?
- Which reviews mention [competitor]?
- Do we have a reference for [persona] in [segment]?
- Which review quotes are we allowed to reuse on the site?
