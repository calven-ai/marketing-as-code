# Contributing to Marketing as Code

Contributions of every size are welcome: docs fixes, new agent definitions,
template improvements, catalog corrections, bug reports.

## Two ways to use this repo, one way to contribute

- **Running your own marketing:** use your own copy, made with "Use this
  template". Fork only to contribute back here; a fork of a public
  repository cannot be made private. Fill
  `strategy/`, `content/` and `memory/` with real material, add integrations
  for your stack, rewrite skills, reshape folders. None of that comes back
  here.
- **Contributing here:** pull requests carry structure, templates, agents
  and docs only. Never anyone's real strategy, customer data or credentials.
  Built an integration or a skill others could reuse? Contribute it as a
  worked example that follows
  [integrations/adding-an-integration.md](integrations/adding-an-integration.md),
  with its registry row and its `.env.example` lines.

## Before you propose

Run the same checks the repository runs on every proposal, from the root:

```
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/lint.py
```

Both must be clean. `python3 scripts/lint.py --fix` regenerates the tables
the check compares against (the roster, the scripts index, the catalog).

- **A skill:** one folder in `.agents/skills/`, written to the contract in
  [docs/skill-authoring.md](docs/skill-authoring.md). Then
  `python3 scripts/sync_skills.py` for the Claude Code link and
  `python3 scripts/lint.py --fix` for the roster row.
- **A catalog entry:** edit `integrations/catalog/<category>.json` in the
  shape of a neighbour, with `verified` and `checked` set to what you did
  and when, then `python3 scripts/lint.py --fix`.
- **A doc:** plain language, an example filled in, no unexplained jargon.
  Every backticked path must exist; the check refuses one that does not.

## How a contribution lands

Every pull request from outside the repository is needs-review: the gate
never merges it and never pushes fixes to it, and a maintainer reads the
diff and runs the review gate by hand when the automatic run cannot find
the proposal. Expect a reply within a few business days.

By opening a pull request you agree that your contribution is licensed
under the repository's [MIT license](LICENSE). There is no contributor
agreement to sign.

## Ground rules

- Keep every template useful to a non-technical marketer: plain language, an
  example filled in, no unexplained jargon.
- One change per pull request, with a sentence on who it helps.
- Be excellent to each other. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
