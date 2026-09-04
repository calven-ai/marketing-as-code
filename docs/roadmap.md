# Roadmap: what is still planned

What has landed is in [CHANGELOG.md](../CHANGELOG.md). The reasoning behind
the structure is in [architecture.md](architecture.md). This page is only
what remains.

The stance: the maintainers ship the structure, the skills for every
marketing function, the guides, one worked example per way of connecting a
tool (MCP server, CLI, script), the catalog of vendor routes per
integration category, and the guide for adding what the catalog lacks.
The catalog is a list of routes with a verification date, not a set of
connectors the maintainers run: a team wires the vendor it uses with
`scripts/wire_integration.py`, verifies the entry on the day, and a
corrected entry contributed back is welcome
([CONTRIBUTING.md](../CONTRIBUTING.md)). The repo is a blueprint
([README](../README.md#a-blueprint-not-a-product)), not a product.

## Next

- [ ] Re-verify the catalog every six months (the check warns per entry
      after 180 days); promote `listing` entries to `vendor` as the
      vendors' own pages confirm them
- [ ] A `role-<skill>.yml` caller for each role once a team wires its
      categories to key-based servers; a dispatch run of `role-run.yml`
      against a real key to confirm `--mcp-config` alongside the action's
      own server, and `secrets: inherit` into the `automation` environment
- [ ] `scripts/doctor.py`: warn when a wired server's variable is not set
      in the person's environment, without printing values
- [ ] `scripts/og_image.py`: port from the Calven website repo; reads
      `brand/tokens.json` and `brand/templates/`
- [ ] Optional context pull script: mirror a connected context layer into
      `strategy/` as dated files, for teams that need offline copies
- [ ] `docs/website.md`: the sibling-repo pattern, and the content-to-website
      sync Action that opens a PR against the website repo on merge of
      `status: published`
- [ ] Companion `marketing-as-code-website` Astro template repo
- [ ] Optional GitHub Pages workflow serving `reports/` at a URL
- [ ] Claude Code plugin or skill-marketplace packaging of the skill set

## Open questions

- **Context-layer stubs.** Once a team connects a context layer, the
  mirrored strategy files become two-line fallbacks flagged
  `source: context-layer`. Keep them so the routing table stays intact, or
  delete them? Stubs for now.
- **Thin categories.** `intent` has one optional user and `billing` two.
  Kept because the vendors are distinct; fold into `enrichment` and `crm`
  if no team wires them within a year.
