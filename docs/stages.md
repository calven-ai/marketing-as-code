# Three stages to marketing as code

This repository is stage 3, the ultimate form of the pattern: every piece
of marketing knowledge as plain text in one place, agents reading and
writing it, a human merging. Most teams should not start here. Read
[is-this-for-you.md](is-this-for-you.md) first if you have not; it says who
this is for, who it is not for yet, and what it costs.

The two earlier stages are not consolation prizes. Each one is a complete,
useful place to stop, and each produces the raw material the next stage is
built from: context you have written down once, an agent you own and
understand, outputs that are files. A team that stops at stage 1 has still
stopped re-explaining its positioning to a chatbot every morning. A team
that stops at stage 2 has still replaced a subscription with an agent it
owns.

| Stage | In one sentence | You need | You get | Move on when |
| --- | --- | --- | --- | --- |
| 1. Use what you already pay for, fully | The team's AI assistant, set up deliberately and connected to the tools you already use | A paid team plan, one curator, an afternoon per connector | Shared instructions, connected data, less re-pasting | You keep re-pasting the same context, or want the same task to run the same way every week |
| 2. One activity, one agent | One recurring, data-heavy activity handed to a purpose-specific agent a human triggers | One person who can connect an MCP server and keep a key, a pay-as-you-go data account | One line item cheaper, outputs as files, the first agent you own | Two or three agents exist and need shared context, history, and review |
| 3. The repo (this template) | Strategy, content, projects, data, decisions, and the agents themselves as versioned plain text | An owner and a second person, a leader who reads diffs, a private repo, a coding-agent seat | Everything in the [README](../README.md#what-you-get) | There is no next stage; there is keeping it alive |

## Stage 1: use what you already pay for, fully

### What it is

The AI assistant the team already has a plan for, used deliberately instead
of one chat at a time. As of September 2026 that means products like
Claude's desktop app and Claude Cowork, or ChatGPT and its connectors; from
here on this page says "the assistant" and means whichever one you pay for.
Three moves:

1. **Shared projects or workspaces whose instructions are your context.**
   Positioning, voice, the persona list, and the words you never use go
   into the shared instructions once, so every chat starts from them. This
   is the first time most teams write their positioning down in a form a
   machine reads.
2. **Connectors to the tools you already use.** The assistant reads the
   task tool, the CRM, the shared drive, and the calendar through
   connectors, most of them built on MCP, the same protocol this repo's
   integrations use. MCP support and plan requirements vary by product and
   change often; check the product's own documentation rather than this
   page.
3. **Desktop agents that work on files.** Reading a folder of transcripts
   and drafting the summary, filling a spreadsheet from a report, rewriting
   a deck's notes in the house voice. Files in, files out, a person
   watching.

### What it is not

No repository, no Git, no coding agent, no keys beyond the ones the
product manages for you, and no "vibe coding". Nobody on the team needs a
terminal, and nobody should open one for this stage.

### What you need

A paid team plan so projects and connectors can be shared. One person who
curates the shared instructions and owns the connector list. An afternoon
per connector. IT's blessing for the connectors, which is a conversation
worth having now rather than at stage 2 when there are keys involved.

### What you get

The four kinds of files this repo is built from, in a crude form: context
as project instructions, agents as saved prompts, data read-only through
connectors, and no code at all. The cost is days, not weeks, and most of it
is writing the instructions well.

### Move on when

You keep re-pasting the same positioning into a chat because the shared
instructions are out of date and nobody owns them: that is the context
problem, and the pillar section below is about it. You want the same task
to run the same way every week and it does not, because a saved prompt is
not an agent. Or you want the outputs as files the team can keep, compare,
and review, not as chat history.

## Stage 2: one activity, one agent

### What it is

Pick one activity that recurs, runs on data, and is expensive to buy as a
suite. Replace the suite with two things: a data rail (an API or MCP server
that sells the data by the call) and a purpose-specific agent whose
instructions say what to do with it. A human still triggers the agent and
tells it what to do, every time. Nothing is automated end to end. That is
still a large step from a team that was not doing this, and it is a step
the team fully understands.

### Worked examples

**Search data.** An SEO subscription suite is replaced by pay-as-you-go
keyword and SERP data over the DataForSEO MCP, which this repo already
lists, plus an agent whose instructions are the
[seo-analyst](../.agents/skills/seo-analyst/SKILL.md) skill. That file is
plain Markdown; a stage-2 team can use it as the agent's prompt without
adopting the rest of the repo, and it will save every pull as a dated CSV.

**Account research.** An enrichment orchestration suite is replaced by a
cheaper data provider with an API or MCP server, plus an agent shaped like
[researcher](../.agents/skills/researcher/SKILL.md): a target list in, a
dated snapshot out, and a rule that it never contacts anyone.

**Reporting.** A reporting tool is replaced by CSV exports saved as
snapshots and the [make-dashboard](../.agents/skills/make-dashboard/SKILL.md)
skill, which turns them into a self-contained HTML file that opens from
Finder.

The trade, stated plainly: you own the instructions and the data bill, and
you understand every step. You lose the suite's interface, its alerting,
its support desk, and the comfort of a vendor to blame. For one activity,
run by a person who wanted to own it, that trade is usually good. For ten
activities at once, it is a migration, which is stage 3 and needs the
change management in [is-this-for-you.md](is-this-for-you.md#change-management-the-larger-half).

### What you need

One person who can connect an MCP server and keep a key safe
([secrets.md](secrets.md) is the whole procedure). A pay-as-you-go data
account. A place to keep the agent's instructions and its outputs. This is
where a single folder under version control starts to earn its place: not
the whole repo, one folder with the skill file and the snapshots, so that
the second person can see what changed.

### What it is not

No cron, no scheduled runs, no repo-wide migration, no rewriting the
strategy documents. (Scheduled runs are a stage-3 option, chosen per
workflow: [operating-model.md](operating-model.md).) If the agent needs positioning, paste it in from the
stage-1 instructions. Resist building the second agent until the first one
has run for a month.

### What you get

One line item cheaper, or gone. Outputs as files the team can diff and
keep. And the first agent the team owns, written in English, which changes
how people think about the next one. The first agent takes one to two
weeks, most of it learning; each one after that takes days.

### Move on when

Two or three agents exist. Their instructions need the same positioning,
their outputs need to sit next to each other, somebody wants to know what
changed last month, and two people are editing the instructions. At that
point the shared context, the history, and the review are the problem, and
the repo is the answer to exactly that problem.

## Stage 3: the repo (what this template is)

### What it is

Everything in one repository as plain text, organised as four kinds of
files ([README](../README.md#four-kinds-of-files)): context, agents, code,
and data. The setup interview ([setup](../.agents/skills/setup/SKILL.md))
fills the strategy, brand, and ontology templates from your answers. The
[roster](../agents/README.md) lists the agents and skills, each a Markdown
file you can read and change. The [review workflow](workflow.md) keeps a
human merging everything that ships. The [memory pipeline](../memory/README.md)
turns meeting transcripts into decisions, tasks, and knowledge. The
[integrations registry](../integrations/README.md) says what the agents may
reach, and `scripts/doctor.py` tells you which context files have gone
stale. It is a blueprint: the structure and the offline workflows are done,
the integrations are worked examples, and you are expected to change it
([README](../README.md#a-blueprint-not-a-product)).

### What it is not

Not a website deployment; the website is a sibling repo on purpose
([architecture.md](architecture.md#the-website-a-standalone-sibling-repo-deliberately-not-in-here)).
Not a data warehouse; `data/` holds dated CSV snapshots, not your event
stream. Not an engineering team; the only code is small scripts the agent
writes. Not a replacement for the task tool; tasks stay where the team
already tracks them ([integrations/tasks.md](../integrations/tasks.md)).

### What you need

An owner and a second person. Leadership that reads pull requests. A
private GitHub repository. A coding-agent seat for each person who will
work in it. Keys in a secrets manager. A willingness to let the coding
agent build the connectors for your stack
([integrations/adding-an-integration.md](../integrations/adding-an-integration.md)).
The effort by team size is in
[is-this-for-you.md](is-this-for-you.md#by-team-size); it ranges from a few
days for one person to a quarter for a group.

### What you get

The [README](../README.md#what-you-get) lists it. Read that section as a
description of the destination, not a promise about week one.

### How to enter

The README's [quick start](../README.md#quick-start), plus the three things
the change-management section insists on: one pilot workflow with a
pass/fail sentence, one sponsor who reads the first diffs, and a rollback
written before you start. Run the pilot by hand first; automating it in
GitHub Actions is a later, per-workflow choice
([operating-model.md](operating-model.md)).

## Buy, build, or wait: the four pillars

At every stage the same four questions come up, one per kind of file. For
each pillar you can wait, buy, or build; the table shows what each looks
like, with this repo's answer in the last column.

| Pillar | Wait (do nothing yet) | Buy | Build (this repo's answer) |
| --- | --- | --- | --- |
| Context | Keep positioning and voice in the drive or the wiki, with a review date at the top | A marketing context layer that serves positioning, personas, and competitors to every agent over MCP | Markdown in `strategy/` and `brand/`, with `last_reviewed` on every file and `scripts/doctor.py` flagging the old ones |
| Agents | Saved prompts and shared projects in the assistant you have | An all-in-one AI marketing suite with its agents built in | Skills in `.agents/skills/`, plain Markdown you edit, readable by every coding agent |
| Code | None | The automations inside the tools you already own | Small deterministic scripts the agent writes ([scripts/README.md](../scripts/README.md)) |
| Data | Exports by hand into a spreadsheet | SEO and enrichment suites with the data inside | Data rails over MCP, CLI, or API ([the ladder](../integrations/adding-an-integration.md)) plus dated CSV snapshots ([data/README.md](../data/README.md)) |

For agents, code, and data, stage 2 is the argument: buying the rail and
building the thin layer on top beats buying the suite, because the layer is
a page of English you own and the rail is billed by the call. Context is
the exception. There is no rail to buy for positioning. Either someone on
the team maintains it, with review dates and the discipline to honour them,
or a service maintains it and every agent reads the current version on
every call. Context is the one pillar where "buy" means a context layer,
and the choice is made once, so it is worth making on purpose.

Disclosure first: Calven maintains this repo and makes the marketing
context layer described in [integrations/context-layer.md](../integrations/context-layer.md).
It solves the context pillar and nothing else on this page; the repo works
without it, and the Markdown path is the default. The rule of thumb for
when a context layer pays for itself is in that document, under
[When to switch](../integrations/context-layer.md#when-to-switch).

## Picking your stage

One or two people who like tools: stage 3, today. A team of about five:
stage 2 with one pilot, then stage 3 within a quarter. A team of about
twenty: stage 1 for everyone, stage 2 for one function, stage 3 for that
function first. A team of about a hundred: stage 1 under IT's rules, stage
2 for one workflow, stage 3 for one lighthouse team.

Whichever you choose, write it in `memory/decision-log.md`, dated and
attributed, so that every agent and every newcomer knows which stage the
team is at and why.
