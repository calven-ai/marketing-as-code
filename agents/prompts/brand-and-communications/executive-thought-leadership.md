# Executive thought leadership

**Reads:** `strategy/positioning.md` (trends, point of view),
`brand/voice.md`, `memory/transcripts/processed/`, `memory/knowledge/`,
`content/` (channel linkedin and social), `data/social/snapshots/` ·
**Skills:** `/social-post` writes one post in an exec's voice, `/repurpose`
cuts a published piece into variants. These prompts plan the agenda and
pull the ideas out of the executive.

Your CEO wants to post more. They have opinions in every meeting and no
time to write. You walk away with a quarter's topic agenda tied to the
company's point of view, questions to get the ideas out of them in a
thirty-minute session, and a batch of drafts reviewed before they see
them. The executive still decides what goes out under their name.

## Prompts

### Build the executive's quarterly topic agenda

```
Using this repo, build a quarterly topic agenda for the executive below.

FILL IN
- Executive: [name and role]
- Their stated interests: [two or three topics, or "none yet"]

CONTEXT
I want topics the executive can credibly own that also move the company's story, not generic leadership posts.

READ FROM THE REPO
- Trends and category in strategy/positioning.md.
- Persona pains in strategy/personas.md.
- What already performed in data/social/snapshots/ and memory/knowledge/ (a what-resonates file if one exists).

BUILD
- Six to eight topics, each with: the point of view in one line, the trend it ties to, the persona who cares, why this exec.
- One contrarian take the positioning supports.
- Topics to avoid and why.

OUTPUT
A one-page agenda for the executive to react to.

GROUNDING
Cite paths. Points of view come from the positioning, not from you. If there's no performance data, say the ranking is untested.
```

### Write this month's session questions

```
Using this repo, write the questions for a thirty-minute interview session with the executive.

FILL IN
- Executive: [name and role]
- Topics: [two or three from the agenda]

CONTEXT
I'll record the session and turn it into posts. The questions have to pull stories and opinions, not talking points.

READ FROM THE REPO
- The topics' trend and point of view in strategy/positioning.md.
- Customer moments on those topics in memory/transcripts/processed/.

BUILD
- Per topic: three open questions, one "what do most people get wrong", one "tell me about a time".
- A customer moment from the transcripts to react to, per topic.

OUTPUT
A session guide I can read from.

GROUNDING
Customer moments cite their transcript path and stay anonymous.
```

### Draft posts from the session transcript

```
Using this repo, draft posts from the executive's session transcript.

FILL IN
- Executive: [name and role]
- Transcript: [give its memory/transcripts/processed/ path]

CONTEXT
I want posts that sound like them on a good day, built from what they actually said.

READ FROM THE REPO
- The transcript.
- brand/voice.md, and any notes on this exec's voice in memory/knowledge/.
- Their past posts in content/ with channel linkedin.

WRITE
- Four posts, each from one idea in the transcript: hook, body, close.
- Under each: the transcript lines it came from.
- Flag any claim about the company or product that needs a check.

OUTPUT
Drafts for review, each scaffolded with /new-content on a branch once I pick.

GROUNDING
Every idea traces to a line they said. Don't add opinions they didn't voice. Product claims match strategy/product-brief.md or get flagged.
```

## Advanced prompts

### Put calibrated odds on the executive's prediction

```
Before the executive posts a prediction, put calibrated odds on it like a forecaster would. Use this repo for the trends, the market evidence and what we've seen in deals.

FILL IN
- Prediction: [the claim, e.g. "half of mid-market teams will do X by next year"]

CONTEXT
Bold predictions get engagement and get remembered when they're wrong. I want the exec to post a version they'll be glad to have said in a year.

FROM THE REPO
- Trends in strategy/positioning.md and their sources.
- What buyers say about the trend in memory/transcripts/processed/.
- Any relevant data in data/ snapshots.

METHOD
- Restate the prediction so it's checkable: what, by when, measured how.
- Start from a base rate for similar shifts, stated as an assumption.
- Adjust with the evidence for and against, each cited.
- Give a probability and an 80% range on timing.
- Rewrite the prediction at a confidence the exec can own.

OUTPUT
The probability, the evidence for and against, and two rewrites: bold and safe.

GROUNDING
Label every input as repo (path), or your assumption. Base rates are assumptions unless the repo holds them.
```

### Map the topics the executive can own

```
Map which topics the executive could own against how crowded each one is. Use this repo for our point of view, buyer interest and what we've already published.

FILL IN
- Executive: [name and role]
- Candidate topics: [paste five to ten]

CONTEXT
Some topics everyone talks about; some nobody does because buyers don't care. I want the white space where our view is distinctive and buyers are listening.

FROM THE REPO
- Point of view and differentiation in strategy/positioning.md.
- Buyer questions in data/seo/prompts.csv and volumes in data/seo/keywords.csv.
- What competitors say, from strategy/competitive/.

METHOD
- Score each topic on buyer interest, distinctiveness of our view, and the exec's credibility, 1 to 5, with the evidence.
- Plot interest against crowdedness in a 2x2.
- Pick the two topics in the high-interest, low-crowd corner.

OUTPUT
The scored table, the 2x2 as a list by quadrant, and the two picks with a first post idea each.

GROUNDING
Label scores as your judgement with the evidence path. Without keyword or prompt data, say interest is a guess.
```

## Questions to just ask

- Which trends in our positioning could the CEO credibly comment on?
- What did our exec posts about last quarter, according to content/?
- Which of their posts performed best in the social snapshots?
- What's the company's contrarian point of view, if we have one?
- Which customer stories could the exec retell without naming the customer?
- What does our voice guide say about tone on LinkedIn?
- Which buyer questions in prompts.csv could become a post?
- Has the exec said anything in transcripts that contradicts our positioning?
- What topics do our competitors' execs post about, per the battlecards?
- Which exec drafts are still sitting at status draft?
- What resonates on LinkedIn, according to memory/knowledge/?
