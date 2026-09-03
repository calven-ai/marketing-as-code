<p align="center">
  <img src="docs/assets/hero.svg" alt="A pixel-art marketer at a terminal: they ask an SEO agent to find keywords they can rank for, it calls DataForSEO and checks SERP ranks, reports 12 gaps, and queues three content briefs" width="720">
</p>

<h1 align="center">Marketing as Code</h1>

<p align="center">
  <b>The starter repo for a marketing team that runs on code.<br>
  Plain text your AI agents can read and write.</b>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT license"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs welcome"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="docs/is-this-for-you.md">Is this for you?</a> ·
  <a href="#a-blueprint-not-a-product">Make it yours</a> ·
  <a href="#how-this-repo-is-organized">Structure</a> ·
  <a href="docs/new-to-github.md">New to GitHub?</a> ·
  <a href="#project-status">Status</a>
</p>

---

Ask a marketing team where their marketing actually lives and you get a list:
campaign plans in a project tool, briefs and decks in a shared drive, website
copy behind a CMS login, dashboards nobody opens, and Slack, where questions
get asked and answers die. Seven logins, each tool holding its own version of
the truth, and one marketer in the middle acting as the human API between all
of them. AI can't help much either, because the context it would need is
scattered behind those logins.

There is a lot of talk about fixing this by "moving the marketing team to
GitHub." GitHub is the right tool, and this repo lives on it. But a repository
creates no value on its own. It is storage and version history, with no
intelligence inside. The real shift is moving the work **to code**: strategy,
messaging, briefs, decisions, and knowledge as plain text, versioned, in one
place, where AI agents can read all of it and write into it. The repo is the
floor you build on. The agents are the point.

This repository is that floor, pre-built. Start from it, make it yours, and
run your marketing from here.

## What you get

- **The hierarchy.** A working folder structure for a marketing team's second
  brain: strategy, brand, content, projects, data, reports, memory, agents,
  playgrounds. Every folder explains itself and comes with templates instead
  of blank pages. The reasoning is written down in
  [docs/architecture.md](docs/architecture.md).
- **A default agent set** (bring your own stack). Starter agents and skills
  for onboarding, content, project scaffolding, review, meeting-transcript
  processing, the quarterly marketing review, keyword and ranking analysis,
  AI answer-engine mention tracking, account research, and campaign
  discovery, with analytics reporting landing next. Each one is
  a plain text file you can read and edit, in a format Claude Code, Cursor,
  and Codex all understand. Five integrations ship wired as worked examples;
  [the guide](integrations/adding-an-integration.md) shows your agent how to
  add the rest of your stack.
- **A memory that compounds.** A decision log and a living knowledge base, fed
  automatically: a meeting transcript lands, an agent processes it, updates the
  knowledge base, logs the decisions, and files the follow-ups into your task
  tool. Meetings stop evaporating.
- **A prototyping culture.** `playgrounds/` and a prototype-builder agent, so
  you come to meetings with prototypes, not decks: a landing page mock, a
  campaign concept page, an email sequence preview, built from one sentence and
  thrown away after the decision is logged.
- **Best practices.** Which tools you replace, which you demote to data rails
  your agents operate via API, and which you merely index. Plus the review
  workflow that keeps a human in charge of everything that ships.

## Is this for your team?

Not necessarily. Marketing as code is designed for specific teams, and it
is a change project before it is a tool project: team size, the appetite
for semi-technical work (a repository, pull requests, MCP servers, API
keys, a coding agent), and a leader who will read a diff decide whether it
fits. [docs/is-this-for-you.md](docs/is-this-for-you.md) is the honest fit
check, with profiles for teams of about 5, 20, and 100 and the change
management each one needs. [docs/stages.md](docs/stages.md) is the path for
everyone who is not there yet: use the AI tools you already pay for, then
hand one activity to one agent, then this repo.

## A blueprint, not a product

This repo is a starting point, not a finished system. Expect to change it.

What works as it is, with no keys and nothing connected: the setup
interview, content briefs and drafts, project folders, the pre-publish
review, the decision log, processing a meeting transcript you drag into the
inbox, and a quarterly review built from exported CSVs. That part is done,
and it is the part to try first.

What you are expected to make yours: the **integrations** (your CRM, your
task tool, your meeting recorder, your analytics), the **structure** where
it does not match how your team works, and the **agents**, which are
Markdown files you edit and extend. Five integrations ship wired, as worked
examples of the three ways to connect a tool. The rest of your stack is a
job for your coding agent, not for this repo's maintainers: tell it what you
use ("We use Zoom for meetings. Automate reading the transcripts into the
inbox.") and it builds the connector by the rules in
[integrations/adding-an-integration.md](integrations/adding-an-integration.md):
the vendor's official MCP server first, its CLI second, a small script
last. The `/add-integration` skill walks it through.

Nothing here needs a server. Work runs where a person is typing to a coding
agent, or on a schedule in GitHub Actions; each recurring workflow can be
run either way, and [docs/operating-model.md](docs/operating-model.md)
lays out the trade-off so your team can choose.

## Never used GitHub?

You are the audience this repo was built for. You do not need to be a
developer, and you do not need to live in a terminal. Start with
[docs/new-to-github.md](docs/new-to-github.md): it explains what a repository
is in plain language and walks you through the no-terminal path using the
GitHub website, GitHub Desktop, and an AI coding agent that does the technical
parts for you.

## Quick start

1. **Get the repo.** Click "Use this template" (or fork/clone it) so you have
   your own private copy.
2. **Open it with a coding agent.** [Claude Code](https://claude.com/claude-code)
   is what this repo is tuned for (see [CLAUDE.md](CLAUDE.md)), in the
   terminal or in the Claude desktop app, and any AGENTS.md-aware tool such
   as Cursor or Codex works too (see [AGENTS.md](AGENTS.md)). Where things
   run, and what may run unattended, is in
   [docs/operating-model.md](docs/operating-model.md).
3. **Run the setup interview.** Ask the agent to set up the repo for your team.
   It interviews you, fills in the strategy and voice templates from your
   answers, and connects only the integrations your team actually uses.
4. **Start with one workflow.** Publish one piece of content, process one
   meeting transcript, or run one report. Let the repo prove itself before you
   move everything in. [docs/stages.md](docs/stages.md) explains why one
   workflow, and what to do if even that is too much.
5. **Add your first integration.** Tell the agent which tool your team uses
   for that workflow and let it wire the connection per
   [integrations/adding-an-integration.md](integrations/adding-an-integration.md).

## Four kinds of files

Everything in this repo is one of four kinds of files:

- **Context**, what the team knows: positioning, messaging, personas, brand,
  briefs and status, the decision log and knowledge base, published content,
  and the guides on how the team works here (`strategy/`, `brand/`,
  `content/`, `projects/`, `memory/`, `docs/`, plus `AGENTS.md` and
  `CLAUDE.md` at the root). Context goes stale by default, so every strategy
  file is dated and the health check flags old ones; the same files are
  shaped to be served live by a marketing context layer over MCP instead
  (see [integrations/context-layer.md](integrations/context-layer.md)).
- **Agents**, the workforce, as instructions in English: every agent or skill
  is a Markdown file a person can read and change, plus the registry of what
  agents are allowed to reach (`agents/` for the roster, `.agents/skills/`
  for the definitions, `integrations/` for the registry, the task adapter,
  the Slack app, and `.mcp.json`).
- **Code**, small deterministic scripts and throwaway prototypes, written by
  the agent, not by the team (`scripts/`, `playgrounds/`, plus
  `.github/workflows/`).
- **Data**, the numbers as tables, dated snapshots, and the reports built
  from them (`data/`, `reports/`).

Three judgment calls, stated once so nobody has to guess. Content is an
output that becomes context once published, because agents read it the way
they read positioning. Playgrounds are code because prototypes are HTML the
agent writes and the team throws away. Integrations sit with agents because
they define what the agents may reach.

## How this repo is organized

| Kind | Folder | What lives there |
| --- | --- | --- |
| Context | `strategy/` | Positioning, messaging, ICP and personas, competitive battlecards: what every agent loads before doing marketing thinking |
| Context | `brand/` | Voice, visual identity, logos, design tokens: what every agent loads before making anything an outsider sees |
| Context | `content/` | Every piece of content, at every stage: the single source of truth projects link into |
| Context | `projects/` | How the work is organized: briefs and status, with campaigns as projects that contain projects |
| Context | `memory/` | The decision log and the living knowledge base, fed from meeting transcripts |
| Context | `docs/` | Guides: the review workflow, secrets, architecture, roadmap, and the start-here path for people new to GitHub |
| Agents | `agents/` | The workforce roster; the definitions live in `.agents/skills/`, readable by any coding agent |
| Agents | `integrations/` | How the repo talks to your stack: task tool, CRM, analytics, SEO, plus the conventions agents follow |
| Code | `playgrounds/` | Disposable prototypes: come to meetings with the thing itself, not a deck about it |
| Code | `scripts/` | Deterministic helpers with no AI inside: the transcript pull, the keyword snapshot, Slack posting, the health check, the skill-link sync |
| Data | `data/` | The machine-readable truth: keyword tables, analytics and CRM snapshots, target accounts, plus the ontology defining what your metrics mean |
| Data | `reports/` | What the data becomes: analyses, the quarterly marketing review, self-contained HTML dashboards |

## Project status

The structure, the templates, the offline workflows, and the guides are in
place; the integrations are worked examples plus a guide for adding yours.
The reasoning is in [docs/architecture.md](docs/architecture.md) and what is
still planned in [docs/roadmap.md](docs/roadmap.md). Take it, change it,
and send back what others could reuse (see
[CONTRIBUTING.md](CONTRIBUTING.md)).

## Who is behind this

Maintained by [Calven](https://calven.ai). This repo is the runnable
companion to the article
[Marketing as Code: Not a Move to GitHub. A Move to Agents.](https://calven.ai/resources)
and distills how Calven runs its own marketing (and most of the company) from
repositories with AI agents. Calven also makes the marketing context layer
that [integrations/context-layer.md](integrations/context-layer.md)
describes. The repo works without it.

## License

[MIT](LICENSE).
