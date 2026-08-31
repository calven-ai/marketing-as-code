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

This repository is that floor, pre-built. Clone it, fill in your own strategy
and voice, connect the agents you want, and run your marketing from here.

## What you get

- **The hierarchy.** A working folder structure for a marketing team's second
  brain: strategy, content, campaigns, data, memory, agents, playgrounds. Every
  folder explains itself and comes with templates instead of blank pages.
- **A default agent set** (bring your own keys). Starter agents for SEO
  analysis, brand-mention tracking, web analytics reporting, data enrichment,
  and meeting-transcript processing. Each one is a plain text file you can read
  and edit.
- **A memory that compounds.** A decision log and a living knowledge base, fed
  automatically: a meeting transcript lands, an agent processes it, updates the
  knowledge base, logs the decisions, and files the follow-ups as issues.
  Meetings stop evaporating.
- **A prototyping culture.** `playgrounds/` and a prototype-builder agent, so
  you come to meetings with prototypes, not decks: a landing page mock, a
  campaign concept page, an email sequence preview, built from one sentence and
  thrown away after the decision is logged.
- **Best practices.** Which tools you replace, which you demote to data rails
  your agents operate via API, and which you merely index. Plus the review
  workflow that keeps a human in charge of everything that ships.

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
   is what this repo is tuned for (see [CLAUDE.md](CLAUDE.md)), and any
   AGENTS.md-aware tool works (see [AGENTS.md](AGENTS.md)).
3. **Run the setup interview.** Ask the agent to set up the repo for your team.
   It interviews you, fills in the strategy and voice templates from your
   answers, and switches on only the agents you have keys for.
4. **Start with one workflow.** Publish one piece of content, process one
   meeting transcript, or run one report. Let the repo prove itself before you
   move everything in.

## How this repo is organized

| Folder | What lives there |
| --- | --- |
| `strategy/` | Positioning, messaging, ICP and personas, brand voice: the context every agent loads before doing marketing work |
| `content/` | Content backlog, briefs, drafts, and published pieces |
| `campaigns/` | Campaign briefs as files, tasks as GitHub Issues |
| `data/` | Keyword research, prospect lists, exports: the raw data your agents produce and consume |
| `memory/` | The decision log and the living knowledge base, fed from meeting transcripts |
| `agents/` | The agent workforce: each agent's instructions as a plain text file |
| `playgrounds/` | Disposable prototypes: come to meetings with the thing itself, not a deck about it |
| `docs/` | Guides, including the start-here path for people new to GitHub |

## Project status

Early and under active construction. The structure is stable; templates,
agents, and guides are landing now. Watch the repo to follow along.

## Who is behind this

Maintained by [Calven.ai](https://calven.ai). This repo is the runnable
companion to the article
[Marketing as Code: Not a Move to GitHub. A Move to Agents.](https://calven.ai/resources)
and distills how Calven runs its own marketing (and most of the company) from
repositories with AI agents.

## License

[MIT](LICENSE).
