# docs/

**Kind:** context, what the team knows.

Guides for running your marketing from this repo, grouped by who needs
them.

## Start here

- [new-to-github.md](new-to-github.md): what a repository is, in plain words, and the path with one command, once.
- [workflow.md](workflow.md): Sync, Work, Propose, Review, Merge. How agent-proposed work gets reviewed and merged.
- [troubleshooting.md](troubleshooting.md): every message the lifecycle commands print, and the one thing to do.

## Deciding whether to do this at all

- [is-this-for-you.md](is-this-for-you.md): the fit check. Who this is for, who it is not for yet, and what changes for teams of 5, 20 and 100.
- [stages.md](stages.md): the three-stage path to marketing as code, with a place to stop at each stage.

## Running it

- [operating-model.md](operating-model.md): where things run, the two ways to run any recurring workflow, and what never runs unattended.
- [secrets.md](secrets.md): who holds which key, where it lives, and what the agent can read.
- [github-settings.md](github-settings.md): the repository settings the workflow assumes, the script that applies them, and which GitHub plan enforces them.

## Under the hood, for your agent and whoever maintains the machinery

- [architecture.md](architecture.md): the structure and the reasoning behind it.
- [schema.json](schema.json): what "valid" means here, enforced by `scripts/lint.py`.
- [../integrations/adding-an-integration.md](../integrations/adding-an-integration.md): how your agent connects a tool this template does not ship.
- [roadmap.md](roadmap.md): what is still planned.
