# Writing the question set

Open this in procedure step 2. Six questions in three families.

## A. Self-portrait (names the company)

> Define <Company> (<domain>). Name the category it belongs to, its main competitive strengths, and its weaknesses. Be specific and concise.

The domain stays in: company names collide, and it is how the assistant and you tell this company
from a namesake.

## B. Category (names the claimed label)

> What is the "<claimed label>" category, and who are the leading vendors in it? Briefly define the space and name the main players.

Use the label exactly as the positioning claims it. Families A and B follow the current
positioning; only the four buying questions are frozen.

## C. Four buying questions (never name the company)

These measure whether assistants name the company unprompted. Write them the way a person types,
not the way a form is filled. No output instructions: no "list five", no "in a table", no
formats. A question that tells the assistant how to answer measures instruction-following, not
what the assistant believes.

**The market is authoritative.** Write every question inside the market recorded in step 1. Never
infer the market from the company's name, and never correct it from what you believe about a
company by that name: names collide, and the one you are thinking of is often a different business.
One question written for the wrong market measures, from then on, a market the company does not
compete in, and fills the results with vendors it never meets.

1. **Category head.** The market at shopping granularity: a noun someone would search on a review site ("status page software"). Never scope it to a team or role ("best tools for support teams" returns a whole stack across unrelated categories). Never invent an umbrella no buyer searches; it returns dozens of unrelated vendors. Name at most one technology.
2. **Buy-shaped job.** The core job, phrased so that buying one product is the natural answer. Test: could an assistant answer it well without naming any product? If yes, rewrite. "How do support teams communicate during outages?" fails (it invites a process essay). "Is there a tool that sends our outage updates to the status page, the app and email at once?" passes.
3. **Constrained buyer.** A real buying constraint (company size, team size, budget, stack) that forces a ranked recommendation rather than a tour. Scale the constraint to who actually buys this product: describing a small team with a small budget to an enterprise vendor's market measures the segment you invented, not the vendor's visibility. Read the best-fit customer and pitch the scenario at the buyer who would genuinely shortlist this company. Do not reuse question 1's noun.
4. **Alternatives.** Alternatives to the market's best-known incumbent, named. Choose it from the known competitors; never invent one. It must not be the company itself, and must not be a technology or standard the company is built on or known for implementing: asking for alternatives to that asks assistants to replace the company, not recommend it.

The four must not re-sample each other: if two would return substantially the same vendor list,
rewrite one.

## Freezing

Record the set with its date. Rerun the same four buying questions at every audit so the share of
voice compares over time. Changing any buying question starts a new series; say so in the report
rather than comparing across it.
