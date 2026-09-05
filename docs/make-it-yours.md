# Make it yours: what to change in your copy

The template ships with the maintainer's names in a few places, example
rows in the tables, and a fictional company in `examples/`. Nothing here is
hidden: `python3 scripts/doctor.py` lists what is left under "Make it
yours", and `/setup` does the first three items for you. In order:

1. **`examples/`.** Delete the folder. Beacon is a fictional company, there
   to show what filled templates look like; once yours are filled it only
   confuses the agents.
2. **`.github/CODEOWNERS`.** Replace every `@owner-placeholder` with the
   GitHub handle of whoever reviews that area. One handle is enough.
   `/setup` round 10 asks.
3. **`docs/schema.json`.** `repo.private` matches your repository (it
   should be private: transcripts and strategy live here). `review.self_merge`
   is `true` only if one person merges everything; the day a second person
   joins, set it to `false` and the gate waits for their approval.
4. **Repository settings.** An admin runs `sh scripts/github_setup.sh` once,
   or follows the click path in [github-settings.md](github-settings.md).
   Then `python3 scripts/doctor.py --github` should print nothing under
   "GitHub settings". A private repo needs GitHub Team or Pro for the rules
   to be enforced rather than suggested.
5. **`SECURITY.md` and `CODE_OF_CONDUCT.md`.** They point at the template's
   security inbox and contact address. Put your own in, or delete both.
6. **`CHANGELOG.md` and `docs/roadmap.md`.** They are the template's own
   history and plan. Delete both together (and the roadmap line in
   [README.md](../README.md)), or empty them and keep them for your own.
7. **`CONTRIBUTING.md`.** It is about contributing to the template. Delete
   it, or rewrite it for your team.
8. **The README.** Keep the sections you want. "Who is behind this" and the
   pictures are the template's; replace them or leave the attribution.
9. **`memory/decision-log.md`.** It should hold only your decisions. The
   first one is the entry `/setup` wrote.
10. **The tables.** `data/seo/keywords.csv`, `data/seo/prompts.csv` and
    `data/accounts/target-accounts.csv` ship with rows whose notes start
    with `example row:`. Replace them with yours; `/setup` seeds the first
    two from your positioning.
11. **`strategy/competitive/`.** One file per real competitor, from
    `_battlecard-template.md`. `/setup` round 4 starts them; the `battlecard`
    skill fills them.
12. **`.mcp.json` and `.cursor/mcp.json`.** Remove the servers you do not
    use with `python3 scripts/wire_integration.py --unwire <vendor>`, which
    edits both files together and the binding; then wire your own stack,
    one vendor per category, with `python3 scripts/wire_integration.py
    <vendor>` (`--list` shows the catalog).
13. **`integrations/wired.json`.** The bindings are now yours; the Wired
    table in `integrations/README.md` renders from them
    (`python3 scripts/lint.py --fix`).
14. **`.env`.** Copy `.env.example` to `.env` yourself and fill only what you
    use. The agent cannot read either file, by design
    ([secrets.md](secrets.md)).
15. **`brand/tokens.json` and `brand/logos/`.** Real colors, fonts and logo
    files. `/setup` round 6 asks.
16. **`.github/workflows/`.** Turn off what you will not run
    ([operating-model.md](operating-model.md#turning-a-workflow-off)).
17. **Docs you may delete.** [architecture.md](architecture.md),
    [is-this-for-you.md](is-this-for-you.md) and [stages.md](stages.md) are
    for evaluating the template. If you drop them, remove their lines from
    [README.md](README.md) so the check stays green.

## Later: taking improvements from the template

The template keeps improving. Your strategy, content and memory are yours
and never come back from it; the machinery can. Once, in a terminal:

```
git remote add template https://github.com/calven-ai/marketing-as-code.git
```

Then, on a branch, whenever you want the latest machinery:

```
git fetch template
git checkout template/main -- scripts .github/workflows docs/schema.json .agents/skills scripts/hooks
```

Say `/propose` and read the diff. Only those paths; never `strategy/`,
`content/`, `memory/`, `data/`. Expect to reconcile `docs/schema.json` by
hand where you changed a convention, and to rerun `python3
scripts/sync_skills.py` if a skill was added.
