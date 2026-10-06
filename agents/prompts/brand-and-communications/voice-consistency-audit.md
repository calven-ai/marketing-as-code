# Voice consistency audit

**Reads:** `brand/voice.md`, `strategy/messaging.md`, `content/`,
`data/social/snapshots/`, `data/email/snapshots/` · **Skills:** `/review`
checks one draft, `/web-copy-audit` checks the site, `/voice-refresh`
updates the voice guide itself. These prompts look across every channel
at once.

The blog sounds like one company, the emails like another and the ads like
a third. Nobody did anything wrong; five people wrote with five habits.
You walk away with a reference card anyone can write from, a channel by
channel read of where the voice drifts, a fix list by owner, and a
scorecard you can rerun next quarter. If the guide itself is the problem,
`/voice-refresh` proposes the change.

## Prompts

### Start with a reference card

```
Using this repo, turn our voice guide and messaging into a one-page reference card.

CONTEXT
The full guide is long and nobody reads it before writing a post. I want the card people actually keep open.

READ FROM THE REPO
- brand/voice.md: the three adjectives, how we write, tone by context, do and don't, the banned list.
- The one-liner and boilerplate in strategy/messaging.md.

BUILD
- The voice in three lines.
- Tone by channel in a small table.
- Five do and don't pairs, quoted from the guide.
- The banned list.
- The one-liner and boilerplate, word for word.

OUTPUT
One page. Show it here.

GROUNDING
Quote the guide; don't add rules it doesn't have. If brand/voice.md is still a template, stop and say /setup.
```

### Check channels against the voice

```
Using this repo, check a sample of recent copy from each channel against our voice.

FILL IN
- Window: [window]
- Channels: [e.g. blog, email, linkedin, ad, web]

CONTEXT
I want to see where each channel drifts, with real lines, not impressions.

READ FROM THE REPO
- brand/voice.md.
- Published pieces in content/ for each channel in the window, from their frontmatter.

CHECK
- Per channel: three to five pieces, scored on each voice adjective (on, drifting, off).
- The worst lines quoted, with what the guide says instead.
- Banned words found, with where.
- Patterns per channel ("emails go formal", "ads go hype").

OUTPUT
A channel by adjective table, then the quoted lines.

GROUNDING
Cite each piece's content/ path. Score against the guide only. Note channels with fewer than three pieces as thin.
```

### Compile the fix list by owner

```
Using this repo, turn the voice audit findings into a fix list by owner.

FILL IN
- Findings: [paste the channel check]

CONTEXT
Findings don't change anything until someone owns them.

READ FROM THE REPO
- The owner field in each piece's frontmatter in content/.
- integrations/tasks.md, for where tasks go.

BUILD
- Fixes grouped by owner: piece, line, the fix, priority.
- Which fixes are a rewrite and which are a guide gap.
- Guide gaps listed separately for /voice-refresh.

OUTPUT
The list, and draft tasks per integrations/tasks.md once I approve.

GROUNDING
Cite paths. Don't file anything until I say go.
```

## Advanced prompts

### Build a voice scorecard you can rerun

```
Build a voice scorecard with a fixed rubric and a test set, so next quarter's audit is comparable to this one. Use this repo for the voice guide and a sample of real copy.

FILL IN
- Window: [window]

CONTEXT
Audits that depend on who ran them can't show progress. I want a rubric and a set of graded examples the agent can apply the same way every time.

FROM THE REPO
- brand/voice.md, for the criteria.
- Published pieces in content/ across channels, for the test set.

METHOD
- Turn each voice rule into a criterion scored 0 to 2 with a one-line definition of each score.
- Pick twenty lines: ten clearly on-voice, ten clearly off, and grade them as anchors.
- Score the anchors twice in separate passes and report agreement; tighten any criterion that disagrees.
- Score this quarter's sample and report the channel averages as the baseline.

OUTPUT
The rubric, the anchor set, the agreement check and the baseline, saved as a knowledge file in memory/knowledge/ on a branch.

GROUNDING
Cite every anchor's path. Label baseline numbers as your scoring, with n per channel.
```

### Backtest whether on-voice pieces perform better

```
Test whether the pieces that follow our voice actually perform better than the ones that don't. Use this repo for the pieces and their performance data.

FILL IN
- Channel: [channel]
- Window: [window, the longer the better]

CONTEXT
If on-voice copy doesn't outperform, either the guide is wrong or the metric is. Either is worth knowing before we enforce it harder.

FROM THE REPO
- Published pieces for the channel in content/.
- Performance from data/social/snapshots/, data/email/snapshots/ or data/analytics/snapshots/.
- What the performance metric means in data/ontology/metrics.md.

METHOD
- Score each piece on the voice rubric (on, mixed, off).
- Match each piece to its performance; drop pieces with no match and count them.
- Compare the groups: median and spread, then a rank test (Mann-Whitney) for the difference.
- Control for the obvious confounders you can see: topic, format, publish month.
- If you can run code, do it in Python.

OUTPUT
A table by group with n, the test result in plain words, and what it means for the guide.

GROUNDING
Label every number as repo (path and n), or your calculation. With fewer than ten pieces per group, say it's inconclusive.
```

## Questions to just ask

- What are the three adjectives in our voice guide?
- When was brand/voice.md last reviewed?
- Which published pieces use a word on our banned list?
- How does our tone guide say email should differ from LinkedIn?
- Which channel strays furthest from the voice?
- Is the boilerplate the same everywhere it appears in content/?
- Who owns the most pieces flagged for voice?
- Which review findings come up again and again?
- Does our voice guide say anything about humour?
- Which pieces rated best on social, and do they follow the guide?
- Does the one-liner on the site match strategy/messaging.md?
