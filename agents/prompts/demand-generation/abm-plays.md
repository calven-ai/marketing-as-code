# ABM plays

**Reads:** `strategy/icp.md`, `strategy/personas.md`,
`data/accounts/target-accounts.csv`, `data/accounts/snapshots/`,
`data/crm/snapshots/`, `reports/recurring/accounts/` · **Skills:**
`/target-account-list` builds the tiered list, `/account-signals` reports
weekly heat and `/researcher` researches named accounts; these prompts
turn that into plays and test the list itself.

You have a list of accounts sales cares about and a quarter to warm them
up. A list is not a play: you need to know who in each account matters,
what they'd respond to, and which accounts are worth the effort at all.
You walk away with account briefs, a message per persona in the buying
group, and a list you've checked against who actually bought last year.
Run `/target-account-list` if the list doesn't exist yet.

## Prompts

### Write the account brief

```
Using this repo, write a one-page brief on the account below for the ABM play.

FILL IN
- Account: [account]

CONTEXT
Sales and marketing both work this account. The brief is what they agree on before anyone sends anything.

READ FROM THE REPO
- The account's row in data/accounts/target-accounts.csv and any research in data/accounts/snapshots/.
- Its contacts, deals and engagement in data/crm/snapshots/.
- strategy/icp.md for why it's a fit, and the personas who'd sit in the deal.

BUILD
- Why this account, why now: tier, fit reasons, the latest signal.
- The buying group: which personas we've reached and which we haven't.
- History: past deals, losses and why, competitors in play.
- The opening angle, tied to one pillar in strategy/messaging.md.

OUTPUT
A one-page brief. Show it here.

GROUNDING
Cite the path behind every fact. Don't invent a contact, a role or a trigger event. If there's no research snapshot, say /researcher would fill it.
```

### Write persona messages for the play

```
Using this repo, write the first message for each persona in the buying group at the account below.

FILL IN
- Account: [account]
- Angle: [the angle from the account brief]

CONTEXT
Each person in the group cares about something different. One message for all of them reads like a mass email.

READ FROM THE REPO
- Every persona in strategy/personas.md who sits in deals for this account's segment.
- The pillars and proof in strategy/messaging.md.
- brand/voice.md.

WRITE
- Per persona: the pain to lead with, a two-sentence opener, the proof, the ask.
- Which persona to reach first and why.

OUTPUT
A table by persona, then the drafts. Save them under content/ on a branch if I say save.

GROUNDING
Every pain cites the persona file. No invented numbers or customer names. Don't send anything.
```

### Re-rank the engaged accounts

```
Using this repo, re-rank our target accounts by fit and heat and tell me which to hand to sales this week.

CONTEXT
The list was tiered once. Some tier-3 accounts are suddenly busy; some tier-1 accounts have gone quiet for months.

READ FROM THE REPO
- data/accounts/target-accounts.csv.
- The latest account signals report in reports/recurring/accounts/ and its engagement snapshot in data/accounts/snapshots/.
- Open deals in data/crm/snapshots/.

BUILD
- A two-by-two: fit (tier) by heat (engagement this month).
- The five accounts to hand to sales, each with the signal and the persona engaged.
- The tier-1 accounts with no engagement and no owner.

OUTPUT
The two-by-two as a table and the hand-off list.

GROUNDING
Cite paths. If the signals report is older than two weeks, say so and suggest /account-signals before acting.
```

## Advanced prompts

### Backtest the target list on last year's deals

```
Backtest our ICP tiers on last year's closed deals: would the list have picked the accounts that actually bought? Use this repo for the tiers and the outcomes.

FILL IN
- Window: [the last four quarters]

CONTEXT
We're about to spend a quarter on tier-1 accounts. If the tiers don't predict wins, we're aiming at the wrong companies.

FROM THE REPO
- The tier rules in strategy/icp.md.
- Closed deals with company, segment, amount and outcome from data/crm/snapshots/.
- data/accounts/target-accounts.csv with each account's tier.

METHOD
- Tier every closed-deal account using the current rules, blind to outcome.
- Compare win rate, deal size and sales cycle by tier, with n.
- Compute lift: tier-1 win rate over the base rate, with an interval.
- List the won accounts the rules would have left out, and what they had in common.
- If you can run code, do it in Python and show the table.

OUTPUT
A table by tier, the lift with its interval, and the one rule change the misses suggest.

GROUNDING
Label every number as repo (file path and n), mine, or your calculation. Say when a tier has too few deals to judge. This is a backtest, not proof the rule causes wins.
```

### Split the ABM budget by expected value

```
Split next quarter's ABM budget across tiers by expected pipeline, not by habit. Use this repo for win rates, deal sizes and account counts.

FILL IN
- Budget: [amount]
- Cost per account per play: [by tier, or "assume and show"]

CONTEXT
Leadership wants the split justified. I want one I can defend when they ask "why not all on tier 1?"

FROM THE REPO
- Account counts per tier in data/accounts/target-accounts.csv.
- Win rate, deal size and engaged-to-opportunity rate by tier from data/crm/snapshots/.

METHOD
- Expected value per account per tier = P(opportunity) x P(win) x deal size.
- Expected value per dollar per tier, with a range from the uncertainty in each rate.
- Allocate with diminishing returns: the first accounts in a tier are the best ones.
- Show the allocation that maximizes expected pipeline and how much it changes if each rate moves by its interval.

OUTPUT
A table: tier, accounts, cost, expected pipeline, expected value per dollar, recommended spend. Then a one-line rationale.

GROUNDING
Label every number as repo (file path and n), mine, or your assumption. Don't use a rate from fewer than ten deals without flagging it.
```

## Questions to just ask

- How many tier-1 accounts have no owner?
- Which target accounts are already customers or closed-lost?
- Which accounts warmed up most this week?
- Which personas have we reached at [account]?
- Why did we lose [account] last time, according to the closed-deals snapshot?
- Which tier converts to opportunity fastest?
- Is there research on [account] in data/accounts/snapshots/?
- What does our ICP say disqualifies an account?
- Which tier-1 accounts have an open deal right now?
- Which competitors show up most in deals at tier-1 accounts?
- When was the target account list last changed?
- Which accounts did sales reject from the last hand-off, and why?
