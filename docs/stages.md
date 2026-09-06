# Three stages to marketing as code

This repository is stage 3, the final form of the pattern. Most teams
should not start here. The two earlier stages are not consolation prizes.
Each is a complete place to stop, and each produces what the next stage is
built from: context written down once, an agent you own, outputs that are
files. A team that stops at stage 1 has still stopped re-explaining its
positioning to a chatbot every morning. A team that stops at stage 2 has
still replaced a subscription with an agent it owns. Read
[is-this-for-you.md](is-this-for-you.md) first if you have not.

| Stage | In one sentence | You need | You get | Move on when |
| --- | --- | --- | --- | --- |
| 1. Use what you already pay for, fully | The team's AI assistant, set up deliberately and connected to the tools you already use | A paid team plan, one curator, an afternoon per connector | Shared instructions, connected data, less re-pasting | You keep re-pasting the same context, or want the same task to run the same way every week |
| 2. One activity, one agent | One recurring, data-heavy activity handed to a purpose-specific agent a human triggers | One person who can connect an MCP server and keep a key, a pay-as-you-go data account | One line item cheaper, outputs as files, the first agent you own | Two or three agents exist and need shared context, history, and review |
| 3. The repo (this template) | Strategy, content, projects, data, decisions, and the agents themselves as versioned plain text | An owner and a second person, a leader who reads diffs, a private repo on GitHub Team or Pro, a coding-agent seat | Everything in the [README](../README.md#what-you-get) | There is no next stage; there is keeping it alive |

## Stage 1: use what you already pay for, fully

The AI assistant the team already has a plan for, used deliberately instead
of one chat at a time. Three moves:

1. **Shared projects whose instructions are your context.** Positioning,
   voice, personas, and the words you never use go into the shared
   instructions once. For most teams this is the first time the positioning
   exists in a form a machine reads.
2. **Connectors to the tools you already use.** The task tool, the CRM, the
   drive, the calendar, most of them over MCP, the same protocol this repo's
   integrations use. Support varies by product and changes often; check the
   product's own documentation.
3. **Desktop agents that work on files.** A folder of transcripts in, a
   summary out. A person watching.

No repository, no Git, no coding agent, no keys beyond the ones the product
manages. Nobody opens a terminal. You need a paid team plan, one person who
curates the instructions and owns the connector list, and IT's blessing
for the connectors. Get that conversation done now, before there are keys
involved.

**Move on when** you keep re-pasting the same positioning because the
shared instructions are out of date and nobody owns them. Or when you want
the same task to run the same way every week and it doesn't, because a
saved prompt is not an agent. Or when you want outputs as files, not chat
history.

## Stage 2: one activity, one agent

Pick one activity that recurs, runs on data, and is expensive to buy as a
suite. Replace the suite with a data rail (an API or MCP server that sells
the data by the call) and a purpose-specific agent whose instructions say
what to do with it. A human triggers the agent every time. Nothing runs end
to end on its own, and the team understands every step.

Three worked examples, each a skill in this repo you can use as the
agent's prompt without adopting anything else:

- **Search data.** An SEO suite becomes pay-as-you-go keyword and SERP data
  over the DataForSEO MCP plus the
  [seo-analyst](../.agents/skills/seo-analyst/SKILL.md) skill, which saves
  every pull as a dated CSV.
- **Account research.** An enrichment suite becomes a cheaper data provider
  plus an agent shaped like
  [researcher](../.agents/skills/researcher/SKILL.md): a target list in, a
  dated snapshot out, and a rule that it never contacts anyone.
- **Reporting.** A reporting tool becomes CSV exports plus the
  [make-dashboard](../.agents/skills/make-dashboard/SKILL.md) skill, which
  turns them into a self-contained HTML file.

The trade: you own the instructions and the data bill, and you understand
every step. You lose the suite's interface, its alerting, its support desk,
and a vendor to blame. For one activity, run by a person who wanted to own
it, that trade is good. For ten activities at once it is a migration, which
is stage 3 and needs the change management in
[is-this-for-you.md](is-this-for-you.md#change-management-the-larger-half).

You need one person who can connect an MCP server and keep a key safe
([secrets.md](secrets.md)), a pay-as-you-go data account, and one folder
under version control for the skill file and the snapshots. No cron, no
scheduled runs, no rewriting the strategy documents. Resist building the
second agent until the first has run for a month. The first agent takes
one to two weeks, mostly learning. Each one after that takes days.

**Move on when** two or three agents exist, their instructions need the
same positioning, their outputs need to sit next to each other, and two
people are editing the instructions. Shared context, history and review
are now the problem. The repo is the answer to exactly that problem.

## Stage 3: the repo (what this template is)

Everything in one repository as plain text, organised as
[four kinds of files](../README.md#four-kinds-of-files). The setup
interview ([setup](../.agents/skills/setup/SKILL.md)) fills the strategy,
brand and ontology templates from your answers. The
[roster](../agents/README.md) lists the agents, each a Markdown file you
can change. The [review workflow](workflow.md) keeps a human merging
everything that ships. The [memory pipeline](../memory/README.md) turns
transcripts into decisions, tasks and knowledge. It is a blueprint you are
expected to change ([README](../README.md#a-blueprint-not-a-product)).

What it is not: a website deployment (the website is a sibling repo,
[architecture.md](architecture.md#the-website-a-standalone-sibling-repo-deliberately-not-in-here)),
a data warehouse (`data/` holds dated snapshots, not your event stream), or
a replacement for the task tool
([integrations/tasks.md](../integrations/tasks.md)).

You need an owner and a second person, leadership that reads pull
requests, a private repository on GitHub Team or Pro, a coding-agent seat
per person, and keys in a secrets manager. Effort by team size is in
[is-this-for-you.md](is-this-for-you.md#by-team-size). Enter through the
README's [quick start](../README.md#quick-start), plus the three things the
change-management section insists on: one pilot workflow with a pass/fail
sentence, one sponsor who reads the first diffs, and a rollback written
before you start. Run the pilot by hand first. Automating it in GitHub
Actions is a later, per-workflow choice
([operating-model.md](operating-model.md)).

## Buy, build, or wait: the four pillars

At every stage the same four questions come up, one per kind of file.

| Pillar | Wait (do nothing yet) | Buy | Build (this repo's answer) |
| --- | --- | --- | --- |
| Context | Keep positioning and voice in the drive or the wiki, with a review date at the top | A marketing context layer that serves positioning, personas, and competitors to every agent over MCP | Markdown in `strategy/` and `brand/`, with `last_reviewed` on every file and `scripts/doctor.py` flagging the old ones |
| Agents | Saved prompts and shared projects in the assistant you have | An all-in-one AI marketing suite with its agents built in | Skills in `.agents/skills/`, plain Markdown you edit, readable by every coding agent |
| Code | None | The automations inside the tools you already own | Small deterministic scripts the agent writes ([scripts/README.md](../scripts/README.md)) |
| Data | Exports by hand into a spreadsheet | SEO and enrichment suites with the data inside | Data rails over MCP, CLI, or API ([the ladder](../integrations/adding-an-integration.md)) plus dated CSV snapshots ([data/README.md](../data/README.md)) |

For agents, code and data, buying the rail and building the thin layer on
top beats buying the suite. The layer is a page of English you own; the
rail is billed by the call. Context is the exception. There is no rail to
buy for positioning. Either someone maintains it, with review dates
honoured, or a context layer maintains it and every agent reads the current
version on every call. That choice is made once, so make it on purpose.
Calven maintains this repo and makes such a context layer; the repo works
without it, and
[integrations/context-layer.md](../integrations/context-layer.md#when-to-switch)
says when switching pays off.

Whichever stage you choose, write it in `memory/decision-log.md`, dated and
attributed, so every agent and every newcomer knows where the team is and
why.
