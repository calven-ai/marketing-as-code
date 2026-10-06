# Email nurtures

**Reads:** `strategy/personas.md`, `strategy/messaging.md`,
`data/ontology/funnel.md` and `events.md`, `content/` (pieces with
`channel: email`), the lifecycle map in `memory/knowledge/` once `/lifecycle-map` has run,
`data/email/snapshots/` · **Skills:** `/nurture-sequence` designs a
sequence end to end and `/lifecycle-map` maps everything you already send;
these prompts review, fix and test what sits between them.

Someone downloaded the guide, or came to the webinar, and now they get
emails. Whether those emails move them a stage or train them to ignore you
depends on whether each one says something the persona cares about, at the
right moment, with proof. You walk away with a sequence that fits the
lifecycle you already run, emails checked against the story, and a test the
list is big enough to answer. For a brand-new sequence, start with
`/nurture-sequence`; to see what already sends, run `/lifecycle-map`.

## Prompts

### Review a sequence as the buyer

```
Using this repo, read the sequence below as the persona would and tell me where they stop reading.

FILL IN
- Persona: [persona]
- Sequence: [paste your draft, or name its folder in content/]

CONTEXT
The sequence is written. Before it goes live I want to know which emails earn the next open and which ones lose the reader.

READ FROM THE REPO
- The persona's goals, pains and objections in strategy/personas.md.
- The pillars and proof in strategy/messaging.md.
- brand/voice.md.

CHECK
- Per email: what the persona thinks on reading the subject and first line, whether the CTA fits their stage, and the one line that sounds like us talking about us.
- Claims: supported, unsupported, contradicted, with the source.
- Where the sequence answers an objection the persona doesn't have, or skips one they do.

OUTPUT
A table, one row per email, then rewritten subject lines for the weakest two.

GROUNDING
Every persona reaction cites the persona file. Don't invent a statistic or a customer result. If the persona file is a template, stop and say so.
```

### Find the stages nobody emails

```
Using this repo, find the funnel stages and moments our automated emails don't cover.

CONTEXT
We've added sequences one campaign at a time. I suspect some stages get nothing and others get three overlapping sequences.

READ FROM THE REPO
- The lifecycle map in memory/knowledge/lifecycle-emails.md, if it exists.
- The stages and their exit conditions in data/ontology/funnel.md.
- Every content/ draft with channel: email.

BUILD
- A grid: stage by persona, each cell naming the sequence that covers it, or empty.
- Collisions: contacts who could be in two sequences at once.
- For each empty cell, the content we already have that a sequence could link.

OUTPUT
The grid and a ranked list of the three gaps worth filling first.

GROUNDING
Cite the path behind each cell. If the lifecycle map doesn't exist, say so and suggest /lifecycle-map rather than guessing what the tool sends.
```

### Rewrite an underperforming email

```
Using this repo, rewrite the email below, which isn't performing, and tell me why the new version should do better.

FILL IN
- Email: [paste the email]
- Its numbers: [opens, clicks, replies, or "check the snapshot"]

CONTEXT
One email in the sequence drags the rest down. I want a rewrite grounded in what the persona cares about, not a fresh coat of adjectives.

READ FROM THE REPO
- The latest email performance snapshot in data/email/snapshots/ and its report in reports/recurring/email/.
- The persona in strategy/personas.md and brand/voice.md.
- What resonates in memory/knowledge/, if the team keeps a file on it.

BUILD
- A diagnosis: subject, opening, offer, CTA or timing, with the evidence.
- Two rewrites that each change one thing, so a test can tell them apart.

OUTPUT
The diagnosis in three lines, then the two variants.

GROUNDING
Use only numbers from the snapshot or the ones I pasted, with the path. If neither exists, say which export to drop in data/email/snapshots/.
```

## Advanced prompts

### Design an A/B test the list can actually power

```
Design an A/B test for this nurture that our list size can actually answer, or tell me it can't. Use this repo for the list and engagement numbers and what counts as a conversion.

FILL IN
- Sequence: [name its folder in content/]
- What I want to test: [subject line, offer, send time, length]

CONTEXT
We keep running tests on a few hundred contacts and calling winners on noise. I'd rather know upfront what's detectable.

FROM THE REPO
- Sends, opens, clicks and conversions for this sequence from data/email/snapshots/.
- The conversion event by exact name in data/ontology/events.md.
- How many contacts enter the sequence per month, from the same snapshots or data/crm/snapshots/.

METHOD
- Pick the primary metric and its baseline rate from the snapshot.
- Run a power calculation at 80% power and 5% significance: the minimum detectable effect for the monthly volume, and the sample needed for a lift worth having.
- Translate that into weeks of sends. If it's longer than a quarter, say so and suggest a bolder variant or a higher-volume metric.
- Write the stop rule before the test starts.
- If you can run code, show the calculation in Python.

OUTPUT
A one-page test plan: hypothesis, metric, baseline, MDE, sample, duration, stop rule. Or a clear "don't run this" with the reason.

GROUNDING
Label every number as repo (file path and n), mine, or your assumption. If there's no baseline in the snapshots, say which export is missing; don't assume an industry rate.
```

## Questions to just ask

- Which automated emails do we send to [persona], and at what stage?
- Which funnel stage has no nurture at all?
- What's the exit event for the trial nurture, by its exact name?
- Which nurture email had the lowest click rate last month?
- Do we have a case study we could link in the consideration emails?
- Which sequences could hit the same contact in the same week?
- Is the lifecycle map in memory/knowledge/ up to date with content/?
- Which objections does [persona] raise that no email answers?
- How many contacts entered the [campaign] nurture last month?
- Which emails in content/ are still drafts and never went live?
- What did our last email performance report recommend?
- Which claims in this sequence aren't backed by the messaging file?
