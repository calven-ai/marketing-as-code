# docs/

**Kind:** context, what the team knows.

Guides for running your marketing from this repo.

- [is-this-for-you.md](is-this-for-you.md): the honest fit check: who this
  is for, who it is not for yet, team-size profiles, and the change
  management it takes.
- [stages.md](stages.md): the three-stage path to marketing as code, with a
  complete place to stop at every stage.
- [new-to-github.md](new-to-github.md): the start-here path if you have never
  used GitHub. Written for marketers, no terminal required.
- [workflow.md](workflow.md): the review ritual: how agent-proposed work
  gets human-approved and shipped, no terminal required.
- [operating-model.md](operating-model.md): where things run (a person at a
  coding agent, GitHub Actions, never a server), the two ways to run any
  recurring workflow and their trade-off, and what never runs unattended.
- [secrets.md](secrets.md): who holds which key and where it lives: your
  keys on your machine, the bot keys in a GitHub environment only `main`
  can use, what the agent can and cannot read, rotation and leaving.
- [github-settings.md](github-settings.md): the repository settings the
  lifecycle assumes (the read-only check, the gate that runs from `main`,
  the `automation` environment, pinned actions, secret scanning), the
  script that applies them, and which GitHub plan enforces them.
- [schema.json](schema.json): what "valid" means here, in one machine- and
  human-readable file: frontmatter per folder, naming rules, CSV headers,
  which files count as bookkeeping. `scripts/lint.py` enforces it.
- [../integrations/adding-an-integration.md](../integrations/adding-an-integration.md):
  how your agent connects a tool this template does not ship: MCP server
  first, vendor CLI second, a script last, and what a finished integration
  contains.
- [architecture.md](architecture.md): the target structure and the reasoning
  behind every design decision.
- [roadmap.md](roadmap.md): everything this repo will contain (agents,
  skills, templates, scripts, integrations), phased into three waves.
