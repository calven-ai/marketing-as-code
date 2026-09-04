# Roadmap: what is still planned

What has landed is in [CHANGELOG.md](../CHANGELOG.md). The reasoning behind
the structure is in [architecture.md](architecture.md). This page is only
what remains.

The stance: the maintainers ship the structure, the offline workflows, the
guides, one worked example per way of connecting a tool (MCP server, CLI,
script), and the guide for adding the rest. Connectors for tools the
maintainers do not use are not on this list. A team adds them with its
coding agent, and a connector contributed back as a worked example is
welcome ([CONTRIBUTING.md](../CONTRIBUTING.md)). The repo is a blueprint
([README](../README.md#a-blueprint-not-a-product)), not a product with a
connector catalogue.

## Wave 2: the lifecycle for people who do not know Git

- [ ] `scripts/sync.py`, `scripts/propose.py` and the `sync`, `propose`
      and `doctor` skills: the five-word lifecycle for people who never
      open a terminal
- [ ] `docs/troubleshooting.md`
- [ ] The AI layer: `audit`, `cascade` and `integration-check` skills;
      `context-review.yml`, `weekly-audit.yml`, `integration-check.yml`
      and `claude.yml` workflows; Claude Code hooks that run the lint
      after every edit; `scripts/integration_check.py`
- [ ] `scripts/og_image.py`: port from the Calven website repo; reads
      `brand/tokens.json` and `brand/templates/`
- [ ] `analyst` and `web-analyst` roles and the `weekly-seo` workflow: the
      data-question router with worked examples, web analytics snapshots
      into `reports/recurring/analytics/`, and the weekly SEO delta report

## Wave 3: breadth, story, ecosystem

- [ ] Data enrichment for account research (vendor open: Apify actors, or
      a specific provider)
- [ ] Optional context pull script: mirror a connected context layer into
      `strategy/` as dated files, for teams that need offline copies
- [ ] `docs/website.md`: the sibling-repo pattern, and the content-to-website
      sync Action that opens a PR against the website repo on merge of
      `status: published`
- [ ] Companion `marketing-as-code-website` Astro template repo
- [ ] Optional GitHub Pages workflow serving `reports/` at a URL
- [ ] Demo-company branch: a fictional company with every folder filled,
      for screenshots and the article
- [ ] Claude Code plugin or skill-marketplace packaging of the skill set

Not planned by the maintainers: monday.com, Zoom, HubSpot, PostHog, GA4,
Salesforce. Each is a known route in the
[integration guide](../integrations/adding-an-integration.md); a team adds
it with `/add-integration`.

## Open questions

- **Enrichment vendor.** No clean official integration exists for
  6sense-style enrichment. Apify actors, or a specific vendor?
- **Context-layer stubs.** Once a team connects a context layer, the
  mirrored strategy files become two-line fallbacks flagged
  `source: context-layer`. Keep them so the routing table stays intact, or
  delete them? Stubs for now.
