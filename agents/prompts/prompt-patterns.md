# Prompt patterns

Most people start by typing a question and seeing what comes back. Good
instinct. That's the first of three ways to prompt an agent in this repo.
The second is a saved recipe for work that comes round every week. The
third is a piece of serious analysis where the repo supplies the facts that
keep the agent honest. This page covers all three, the templates behind
them and the placeholders the team pages use, so you can write your own.

## Three flavours

**Questions you just ask** are what you type mid-task. One line, plain
words, specific. You don't need to know which file answers it; the agent
reads [AGENTS.md](../../AGENTS.md) and knows where to look.

> Which objections in the [persona] section of our personas have no answer in our messaging?

**Workflow prompts** are recipes for work you do again and again. They spell
out the context, what to read, what to build, the format and the grounding
rule, so the result holds up whoever runs it and whichever agent they use.

**Advanced prompts** are serious analysis: a simulation, a backtest, a war
game, a pre-mortem. The job leads and the repo supplies the few facts that
stop the agent making things up.

## The workflow template

```
Using this repo, <what we are doing, in one line>.

FILL IN
- <Label>: [placeholder]
- <Label>: [paste ...]

CONTEXT
<who the output is for, what situation we are in, what I pasted>

READ FROM THE REPO
- <a file or folder, in plain words: "the competitor's battlecard in strategy/competitive/">
- <...>

BUILD   (or WRITE, CHECK, SCORE, COMPARE, ROLE-PLAY)
- <the steps or the structure of the output>

OUTPUT
<the artifact and where it goes: show it here, or save it under reports/adhoc/ on a branch>

GROUNDING
Cite the file path behind every point. Do not invent <the thing this prompt could invent>.
If something is missing, name the gap and the file or export that would fill it.
```

Rules:

- The first line starts with "Using this repo" so the agent loads context
  before it thinks, the way ground rule 1 asks.
- READ FROM THE REPO names folders and files in plain words. Name the two
  to four this work needs most. A list of eight dilutes the answer.
- Numbers come from `data/` and mean what `data/ontology/` says. A prompt
  that needs a number says which snapshot folder it lives in, so the agent
  can tell you which export to drop there when it's missing.
- One OUTPUT. Offer the alternative in one clause ("if I say deck, make
  slides"). Anything that changes a file in `strategy/`, `brand/` or
  `content/` is a proposal on a branch, never a direct edit to `main`.
- GROUNDING names this prompt's specific invention risk: numbers, product
  capabilities, quotes, persona reactions, competitor moves.
- Everything you supply, pasted text included, goes in FILL IN, one
  labelled line each. Nothing else has square brackets, so you edit one
  block and send. The rest refers back by label ("the persona", "the
  draft").
- A prompt with nothing to supply has no FILL IN block.
- When a skill already does the job end to end, the prompt says so and
  calls it (`/battlecard`, `/launch-plan`) instead of rebuilding it.

## The advanced template

```
<The job, in one line, in the imperative>. Use this repo for <the two or three inputs it supplies>.

FILL IN
- <Label>: [placeholder]
- <Label>: [paste or attach your data: an export, last year's results, the plan]

CONTEXT
<the decision at stake and why it matters now>

FROM THE REPO
- <two to four inputs, in plain words, with their folder>

METHOD   (or SIMULATE, MODEL, WAR-GAME, RED-TEAM, BACKTEST)
- <the method, step by step>
- <"If you can run code, ..." where code makes it better>

OUTPUT
<the decision-ready artifact: a scorecard, a distribution, a ranked list, a decision memo>

GROUNDING
Label every number as repo (with the file path and n), mine, or your assumption. <the specific invention risk>
```

Rules:

- The method is the point. Use what a strong analyst would: Monte Carlo
  and scenario ranges, sensitivity analysis, pre-mortems, red teams, war
  games, synthetic buying committees built from the personas, backtests
  against closed deals, expected-value decision trees, Van Westendorp price
  ladders, power calculations for a test.
- The repo supplies facts and approved views, never the method. The agent
  reasons and models; you supply anything the repo lacks in FILL IN.
- Every number is labelled by origin. An assumption is fine when it's
  stated, given a range and shown in the sensitivity.
- Same mechanics as workflow prompts: placeholders only in FILL IN, repo
  inputs in plain words, one OUTPUT, a grounding line naming the risk.

## Three modes

Where a use case has all three, there's a prompt for each:

1. **Create.** Build the thing from the repo plus what you supply.
2. **Review.** Paste what exists (a sequence, a deck, a page) and have it
   checked against the repo: on-message, factually right, how the persona
   reads it, what the competitor would say.
3. **Gap.** Find what's missing: content for a stage, objections with no
   answer, claims with no proof, accounts nobody worked.

## Placeholders

| Placeholder | Means |
| --- | --- |
| `[product]` | A product as `strategy/product-brief.md` names it; drop it if you sell one thing |
| `[persona]` | A persona as `strategy/personas.md` names it |
| `[competitor]` | A competitor with a file in `strategy/competitive/` |
| `[segment]` | An ICP segment or tier as `strategy/icp.md` names it |
| `[account]` | A company as your CRM exports name it |
| `[campaign]` | The campaign, launch or project, ideally its folder in `projects/` |
| `[piece]` | A piece of content, by its folder in `content/` or its URL |
| `[stage]` | A funnel stage as `data/ontology/funnel.md` names it |
| `[keyword]` | A keyword, ideally a row of `data/seo/keywords.csv` |
| `[pillar]` | A value pillar as `strategy/messaging.md` names it |
| `[channel]` | Email, LinkedIn, paid, web, event, and the rest of the content channels |
| `[window]` | A time window: last quarter, last 90 days, this year |
| `[quarter]` | A reporting period: Q3, last quarter, this fiscal year |
| `[paste your draft]` | You paste the text to be reviewed |
| `[paste the list]` | You paste a list or a CSV |

A page may add a local placeholder when the work needs one; it stays in
square brackets and gets explained once on that page.

## Asking for what the repo holds

Say the thing, not the path. These phrasings map cleanly:

| Say | The agent reads |
| --- | --- |
| "our positioning", "our messaging", "our ICP", "the product brief" | `strategy/` |
| "the [persona] persona", "[persona]'s objections" | `strategy/personas.md` |
| "the battlecard for X", "what changed at X" | `strategy/competitive/`, `reports/recurring/competitive/` |
| "our voice", "the brand rules" | `brand/voice.md`, `brand/visual-identity.md` |
| "what we've published on Y", "drafts in flight" | `content/` frontmatter |
| "what we decided about Y", "why we chose Z" | `memory/decision-log.md`, `memory/knowledge/` |
| "what the customer said on the call" | `memory/transcripts/processed/` |
| "pipeline", "closed-lost deals", "MQLs last month" | `data/crm/snapshots/` through `data/ontology/` |
| "our rankings", "what buyers ask AI tools" | `data/seo/keywords.csv`, `data/seo/prompts.csv` |
| "last month's report", "the QMR" | `reports/` |
| "how is the launch going" | `projects/<name>/status.md` |

## Never ask for

- A number with no snapshot behind it. The agent says which export is
  missing; it doesn't estimate one.
- A quote nobody said, a persona reaction the persona file doesn't
  support, a competitor move nobody recorded.
- Publishing, sending or deleting without your explicit go. Agents
  propose; you decide.
- Reading `.env` or pasting a key into chat.
