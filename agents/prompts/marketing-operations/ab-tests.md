# A/B tests

**Reads:** `data/ontology/metrics.md`, `data/ontology/events.md`,
`data/analytics/snapshots/` (traffic and funnel), `projects/` (test records)
· **Skills:** `/ab-test-plan` designs a test and records its result; these
prompts pick which test is worth running, read a result someone else
reported, and size what you can test at all.

Someone wants to test a new headline next week. You walk away knowing
whether you have the traffic to tell, what result would count, and what
you'll do either way. The skill writes the test record. The prompts below
decide which idea earns the traffic and read results without fooling
anyone, including yourself.

## Prompts

### Rank the test backlog

```
Using this repo, rank our test ideas by what they're worth and whether we can run them.

FILL IN
- Ideas: [paste the list]

CONTEXT
We have traffic for maybe two tests a month. I want to spend it well.

READ FROM THE REPO
- Traffic and baseline conversion per page from the newest funnel or conversions snapshot in data/analytics/snapshots/.
- Past test records in projects/, under each project's experiments folder.
- The primary metrics in data/ontology/metrics.md.

BUILD
- Per idea: page, primary metric, baseline, weekly traffic, the smallest lift we could detect in four weeks.
- Ideas we've already tested, with the result.
- A ranked list: likely impact times feasibility, with the reason.

OUTPUT
A ranked table. For the top one, the next step is /ab-test-plan.

GROUNDING
Cite paths. Never estimate a baseline or traffic; name the export to drop in data/analytics/snapshots/.
```

### Read a result honestly

```
Using this repo, read this test result and tell me what it actually shows.

FILL IN
- Test: [path to the test record in projects/, or paste the result]

CONTEXT
Someone posted "variant B won by 18%". I want to know if that holds.

READ FROM THE REPO
- The test record: hypothesis, primary metric, planned sample and stop rule.
- The metric's definition in data/ontology/metrics.md.

CHECK
- Did it reach the planned sample, or was it stopped early on a good day?
- Is the reported metric the planned primary metric?
- The interval on the difference, not just the point estimate.
- Segments or secondary metrics that tell a different story.

OUTPUT
A verdict (ship, don't ship, inconclusive) with three lines of reasoning, then the result appended to the test record on a branch.

GROUNDING
Cite paths. A test stopped early or judged on a metric it didn't plan for is "inconclusive", whatever the number says.
```

### Find tests nobody closed

```
Using this repo, list tests that started and never got a result recorded.

CONTEXT
Open tests pollute traffic and teach us nothing.

READ FROM THE REPO
- Every test record in projects/.
- memory/decision-log.md, for decisions that cite a test.

BUILD
- Tests with no result, how long past their planned end, and the owner.
- Decisions that cite a test with no recorded result.

OUTPUT
A short table.

GROUNDING
Cite paths. Don't infer a result from a decision.
```

## Advanced prompts

### Size what you can test with a power calculation

```
Work out the smallest effect each candidate test could reliably detect with our traffic, and which tests aren't worth running. Use this repo for baselines and traffic.

FILL IN
- Candidates: [paste the list with page and metric]
- Max duration: [e.g. 4 weeks]

CONTEXT
A test without enough power wastes a month and returns noise we'll be tempted to read as signal.

FROM THE REPO
- Weekly traffic and baseline conversion per page from the newest snapshots in data/analytics/snapshots/.
- Week-to-week variation in those numbers over the last few snapshots.
- The metric definitions in data/ontology/metrics.md.

METHOD
- For each candidate: compute the minimum detectable effect at 80% power and 5% significance, two-sided, for the max duration.
- Show the duration needed to detect a 5%, 10% and 20% relative lift.
- Flag tests where the minimum detectable effect is bigger than any plausible lift.
- Suggest a fix for those: a higher-traffic page, a metric earlier in the funnel, or a bolder variant.
- If you can run code, do it in Python and give me the function so I can rerun it.

OUTPUT
A table per candidate: baseline, traffic, MDE, weeks for each lift, verdict (run, fix, drop).

GROUNDING
Label every number as repo (path and n), mine, or your calculation. Never assume a baseline that isn't in a snapshot.
```

## Questions to just ask

- Which tests are running right now, and when do they end?
- What did we learn from the last three tests?
- What's the baseline conversion on [page]?
- How much weekly traffic does [page] get?
- Have we tested [idea] before?
- Is a 10% lift on [page] detectable in four weeks?
- Which tests were stopped early?
- What's the primary metric for signup tests, per our ontology?
- Which decisions in the log came from a test result?
- Which test records have no owner?
