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

Ask a marketing team where their marketing lives and you get a list. Campaign
plans in a project tool. Briefs in a shared drive. Website copy behind a CMS
login. Dashboards nobody opens. Slack, where answers go to die. Seven logins,
and one marketer in the middle acting as the human API between them. AI
can't help either, because the context it needs is scattered behind those
logins.

The fix is not moving marketing to GitHub. A repository is storage with
version history and no intelligence inside. The fix is moving the work to
code: strategy, messaging, briefs, decisions and knowledge as plain text, in
one place, where agents read all of it and write into it. The repo is the
floor. The agents are the point.

This repository is that floor, pre-built. Fourteen agents and skills. Five
integrations wired. No server. Start from it, make it yours, and run your
marketing from here.

## What you get

- **The hierarchy.** A folder structure for a marketing team's second brain:
  strategy, brand, content, projects, data, reports, memory, agents,
  playgrounds. Every folder explains itself and ships templates instead of
  blank pages. The reasoning is in [docs/architecture.md](docs/architecture.md).
- **A default agent set.** Fourteen agents and skills for onboarding, content,
  project scaffolding, review, meeting transcripts, the quarterly marketing
  review, keyword and ranking analysis, AI answer-engine tracking, account
  research and campaign discovery. Each is a plain text file you can read
  and edit, in a format Claude Code, Cursor and Codex all understand.
- **A memory that compounds.** A meeting transcript lands, an agent processes
  it, updates the knowledge base, logs the decisions and files the follow-ups
  in your task tool. Meetings stop evaporating.
- **A prototyping culture.** Come to meetings with a landing page mock or an
  email sequence preview built from one sentence. Not a deck about it.
  `playgrounds/` holds prototypes until the decision is logged, then they go.
- **Best practices.** Which tools you replace, which you demote to data rails
  your agents operate through an API, and which you merely index. Plus the
  review workflow that keeps a human in charge of everything that ships.

## Is this for your team?

Not necessarily. Marketing as code is a change project before it is a tool
project. Team size, the appetite for semi-technical work (a repository, pull
requests, API keys, a coding agent) and a leader who will read a diff decide
whether it fits. [docs/is-this-for-you.md](docs/is-this-for-you.md) is the
fit check, with profiles for teams of about 5, 20 and 100.
[docs/stages.md](docs/stages.md) is the path for everyone not there yet: use
the AI tools you already pay for, then hand one activity to one agent, then
this repo.

## Never used GitHub?

You are who this repo was built for. You don't need to be a developer or
live in a terminal. [docs/new-to-github.md](docs/new-to-github.md) explains
what a repository is in plain language and walks the no-terminal path: the
GitHub website, GitHub Desktop, and a coding agent that does the technical
parts for you.

## Quick start

1. **Get the repo.** Click "Use this template" (or fork it) so you have your
   own private copy.
2. **Open it with a coding agent.** [Claude Code](https://claude.com/claude-code)
   is what this repo is tuned for ([CLAUDE.md](CLAUDE.md)), in the terminal
   or the desktop app. Cursor, Codex and any AGENTS.md-aware tool work too
   ([AGENTS.md](AGENTS.md)).
3. **Run the setup interview.** Ask the agent to set up the repo for your
   team. It interviews you, fills the strategy and voice templates from your
   answers, and connects only the integrations you use.
4. **Start with one workflow.** Publish one piece of content, process one
   meeting transcript, or run one report. Let the repo prove itself before
   you move everything in.
5. **Add your first integration.** Tell the agent which tool your team uses
   for that workflow. It wires the connection by the rules in
   [integrations/adding-an-integration.md](integrations/adding-an-integration.md).

## A blueprint, not a product

This repo is a starting point. Expect to change it.

What works with no keys and nothing connected: the setup interview, content
briefs and drafts, project folders, the pre-publish review, the decision log,
processing a transcript you drop in the inbox, and a quarterly review built
from exported CSVs. Try that part first.

What you make yours: the **integrations** (your CRM, task tool, meeting
recorder, analytics), the **structure** where it doesn't match your team,
and the **agents**, which are Markdown files you edit. Five integrations ship
wired as worked examples. The rest of your stack is a job for your coding
agent, not for this repo's maintainers. Tell it "We use Zoom for meetings.
Automate reading the transcripts into the inbox." and it builds the
connector by [the guide](integrations/adding-an-integration.md): the vendor's
MCP server first, its CLI second, a small script last.

Nothing here needs a server. Work runs where a person is typing to a coding
agent, or on a schedule in GitHub Actions.
[docs/operating-model.md](docs/operating-model.md) lays out the trade-off.

## Four kinds of files

<p align="center">
  <img src="docs/assets/four-kinds-8bit.svg" alt="The four kinds of files as pixel-art panels: Context holds strategy, brand, content, projects, memory and docs plus AGENTS.md and CLAUDE.md; Agents holds agents, .agents/skills and integrations; Data holds data and reports; Code holds scripts, playgrounds and .github/workflows" width="640">
</p>

- **Context**, what the team knows: `strategy/`, `brand/`, `content/`,
  `projects/`, `memory/`, `docs/`, plus `AGENTS.md` and `CLAUDE.md`. Every
  strategy file is dated, and the health check flags stale ones.
- **Agents**, the workforce as instructions in English: `agents/`,
  `.agents/skills/`, `integrations/`.
- **Code**, small deterministic scripts and throwaway prototypes the agent
  writes: `scripts/`, `playgrounds/`, `.github/workflows/`.
- **Data**, tables, dated snapshots and the reports built from them:
  `data/`, `reports/`.

The full model, and how context can be served live by a marketing context
layer over MCP, is in [AGENTS.md](AGENTS.md) and
[integrations/context-layer.md](integrations/context-layer.md).

## How this repo is organized

| Kind | Folder | What lives there |
| --- | --- | --- |
| Context | `strategy/` | Positioning, messaging, ICP, personas, battlecards |
| Context | `brand/` | Voice, visual identity, logos, design tokens |
| Context | `content/` | Every piece of content, at every stage |
| Context | `projects/` | Briefs and status; campaigns as projects that contain projects |
| Context | `memory/` | The decision log and the knowledge base, fed from transcripts |
| Context | `docs/` | Guides: fit check, stages, workflow, secrets, architecture |
| Agents | `agents/` | The roster; definitions live in `.agents/skills/` |
| Agents | `integrations/` | How the repo talks to your stack, and the rules agents follow |
| Code | `playgrounds/` | Disposable prototypes |
| Code | `scripts/` | Deterministic helpers with no AI inside |
| Data | `data/` | Keyword tables, snapshots, target accounts, the metrics ontology |
| Data | `reports/` | Analyses, the quarterly review, HTML dashboards |

## Project status

The structure, templates, offline workflows and guides are in place. The
integrations are worked examples plus a guide for adding yours. What is
still planned is in [docs/roadmap.md](docs/roadmap.md). Take it, change it,
and send back what others could reuse
([CONTRIBUTING.md](CONTRIBUTING.md)).

## Who is behind this

Maintained by [Calven](https://calven.ai). This repo is the runnable
companion to the article
[Marketing as Code: Not a Move to GitHub. A Move to Agents.](https://calven.ai/resources)
and distills how Calven runs its own marketing from repositories with
agents. Calven also makes the marketing context layer described in
[integrations/context-layer.md](integrations/context-layer.md). The repo
works without it.

## License

[MIT](LICENSE).
