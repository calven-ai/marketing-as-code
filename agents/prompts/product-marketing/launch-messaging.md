# Launch messaging

**Reads:** `strategy/product-brief.md`, `strategy/messaging.md`,
`strategy/personas.md`, `memory/transcripts/processed/`, the launch folder
in `projects/` · **Skills:** `/launch-plan` builds the project folder and
asset stubs, `/release-notes-to-marketing` turns the changelog into copy,
`/messaging-house` changes the framework itself. These prompts do the
thinking in between.

Something ships in three weeks and everyone wants the story by Friday.
Sales wants a talk track, the web team wants a headline, and nobody has
written down which persona this is really for. You walk away with launch
positioning that sits inside the approved story, claims you can prove,
a read on how each persona hears it, and a field brief. Run `/launch-plan`
once the story holds; it turns this into the project and the stubs.

## Prompts

### Gather the evidence buyers asked for this

```
Using this repo, collect the evidence that buyers wanted what we're about to launch.

FILL IN
- What ships: [one or two sentences on the feature or product]

CONTEXT
Before I write launch messaging I want to know who asked for this, in what words, and how often. The launch story should start from the buyer's problem, not our feature list.

READ FROM THE REPO
- Call transcripts in memory/transcripts/processed/ that mention the problem this solves.
- The closed-deals snapshot and coded win/loss file in data/crm/snapshots/, for deals lost on this gap.
- The personas in strategy/personas.md and their stated pains.

BUILD
- The problem in the buyer's words: five verbatim lines, each with the transcript path.
- Which personas raised it, and how often, with n.
- Deals lost where this gap was a driver, with amount where the snapshot has it.
- What buyers said they used instead.

OUTPUT
One page of evidence I can build the story on.

GROUNDING
Cite the file path behind every quote and count. Quotes are verbatim. If no transcript mentions the problem, say so plainly; don't backfill from the feature description.
```

### Draft the launch positioning and messaging

```
Using this repo, draft the launch positioning and messaging for what ships below.

FILL IN
- What ships: [one or two sentences]
- Evidence: [paste the evidence page, or "none"]

CONTEXT
This is launch messaging, not a new positioning. It has to sit inside the approved story and prove one of our existing pillars.

READ FROM THE REPO
- strategy/positioning.md and strategy/messaging.md, for the story and pillars it must fit.
- strategy/product-brief.md, for how the product actually works and its known weaknesses.
- strategy/personas.md, for who cares about this change.

BUILD
- The launch one-liner and a 50-word description.
- Which pillar it proves, and why that one.
- Per persona: the problem, the change, the outcome, in their words where the evidence has them.
- Three claims, each with its proof or marked "needs proof".
- What we will not say, and why.

OUTPUT
A launch messaging document, then a list of anything it implies should change in strategy/messaging.md as a separate proposal.

GROUNDING
Cite paths. Don't invent a capability the product brief doesn't describe. If the launch contradicts the positioning, say so instead of bending it.
```

### See how each persona reads the messaging

```
Using this repo, read the launch messaging as each of our personas would.

FILL IN
- Messaging: [paste your draft]

CONTEXT
I want to hear how each buyer reacts before the copy goes to web, email and sales.

READ FROM THE REPO
- Each persona in strategy/personas.md: goals, pains, objections, the words they use.
- The objection handling section of strategy/messaging.md.
- Their own words in memory/transcripts/processed/ where we have them.

ROLE-PLAY
- For each persona: what lands, what they'd question, what's missing, the first objection they'd raise.
- Whether the draft uses their words or ours.
- One line per persona: would they forward it?

OUTPUT
A table, persona by reaction, then the three edits that would help most.

GROUNDING
Every reaction cites the persona section or transcript it rests on. Mark any reaction the persona file doesn't support as "my guess".
```

### Brief the field before launch

```
Using this repo, write the internal launch brief for sales and customer-facing teams.

FILL IN
- Launch project: [campaign]
- Messaging: [paste the approved launch messaging]

CONTEXT
Reps get five minutes with this before the first customer asks. They need what it is, who to raise it with, what to say and what not to promise.

READ FROM THE REPO
- The launch folder in projects/ for dates, tier and audience.
- strategy/product-brief.md for limits and availability.
- The battlecards in strategy/competitive/ for how competitors cover this.

BUILD
- What ships, for whom, when, in five lines.
- The talk track: opener, the problem, the change, the proof.
- Five likely questions with answers, including "does [competitor] have this?"
- Don't-say list: promises the product brief doesn't support.

OUTPUT
A one-page brief. If I say enablement kit, hand it to /sales-enablement-kit.

GROUNDING
Cite paths. Availability and pricing only as written in the repo. Anything unknown is "ask product", not a guess.
```

## Advanced prompts

### Pick the launch tier with an expected-value tree

```
Decide which launch tier this release deserves with an expected-value decision tree. Use this repo for the evidence of demand, the deals at stake and the cost of past launches.

FILL IN
- What ships: [one or two sentences]
- Tier costs: [rough cost and team time for tier 1, 2 and 3, or "use your assumptions"]

CONTEXT
Every team wants tier 1. If we spend a tier-1 budget on a tier-3 feature, the next real launch gets less. I want the call made on numbers.

FROM THE REPO
- Deals lost on this gap and their amounts from data/crm/snapshots/.
- How often buyers raised the problem in memory/transcripts/processed/.
- Past launch retros in reports/adhoc/ and launch projects in projects/, for what each tier delivered.

METHOD
- Build a tree: tier choice, then outcome branches (strong, expected, weak pickup), each with a probability and pipeline value.
- Set probabilities from the evidence and past retros; state each one with a range.
- Compute expected value net of cost per tier, then a sensitivity: which assumption flips the answer?
- If you can run code, run it as a small simulation over the ranges.

OUTPUT
The recommended tier, the tree as a table, and the one assumption that would change my mind.

GROUNDING
Label every number as repo (file path and n), mine, or your assumption. With no past retros, say the probabilities are assumptions and widen the ranges.
```

### Pre-mortem the launch

```
Run a pre-mortem on this launch: it's three months later and it flopped. Tell me why. Use this repo for the launch plan, the personas and what went wrong last time.

FILL IN
- Launch project: [campaign]

CONTEXT
Launch plans are optimistic by design. I want the failure modes named while there's still time to fix them.

FROM THE REPO
- The launch folder in projects/: brief, campaign, status.
- Past retros in reports/adhoc/ and decisions in memory/decision-log.md.
- strategy/personas.md and the battlecards in strategy/competitive/.

METHOD
- Write five short failure stories, each from a different cause: wrong audience, weak proof, sales didn't use it, a competitor answered first, the product wasn't ready.
- For each, the early warning sign we'd see in the first two weeks and where in the repo or data it would show.
- Score each on likelihood and impact (1 to 5) with a one-line reason.
- Propose one change to the plan for each of the top three.

OUTPUT
A ranked risk table and the three plan changes, ready to add to the project's status.md as a proposal.

GROUNDING
Label every score as your judgement with the evidence path behind it. A failure that repeats a past retro cites that retro.
```

## Questions to just ask

- Which persona cares most about [product], according to our personas?
- Which pillar in our messaging does this launch prove best?
- What did buyers call this problem on calls? Quote them.
- Which lost deals named this gap, and what were they worth?
- Is there content already announcing this feature in content/?
- Does the product brief list anything this launch contradicts?
- What did the last launch retro say we should do differently?
- Which competitor battlecard mentions this capability?
- What's the ship date in the decision log, and who decided it?
- Which claims in the draft have no proof point in positioning?
- What launch tier did we give the last comparable release?
- Which objections in our messaging does this launch help answer?
