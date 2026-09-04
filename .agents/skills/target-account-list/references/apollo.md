# Apollo.io: company search and firmographics

Wired through the Apollo MCP server (`integrations/catalog/enrichment.json`;
OAuth, browser grant on first use). Read tools only; if the tool list shows
any create, add or send tool, stop and tell the team the server needs
review before this skill uses it.

## Tools to look for

Check the server's tool list in the session. Expect a company (organisation)
search taking filters such as country, industry keywords, employee-count
range and technologies, and an organisation enrichment call taking a domain.
Use search to build the candidate set, enrichment to fill the survivors.

## Field mapping to the snapshot

| Snapshot column | Apollo field |
| --- | --- |
| `domain` | `primary_domain` |
| `company` | `name` |
| `industry` | `industry` |
| `headcount` | `estimated_num_employees` |
| `revenue_band` | `annual_revenue_printed` or a band you derive from `annual_revenue` (say which) |
| `country` | `country` |
| `tech_stack` | `technology_names`, joined with `;` |
| `funding_stage` | `latest_funding_stage` |
| `source` | `apollo` |
| `pulled_at` | today, ISO date |

Field names drift between versions; read the actual response keys once and
note any difference in the hand-over.

## Cost and limits

Search results page at 25 to 100 per call; enrichment spends credits per
domain. Run 10 domains first, report the credits, then scale on approval.
