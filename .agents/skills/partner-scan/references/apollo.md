# Apollo.io: firmographics for partner candidates

Wired through the Apollo MCP server (`integrations/catalog/enrichment.json`;
OAuth). Read tools only; if the tool list shows any create, add or send
tool, stop and tell the team the server needs review.

## Use

Organisation enrichment by domain for each candidate: headcount, industry,
funding stage, technologies, country. One batch of up to 50 domains per
call; state the count and the credits before scaling.

## Mapping

Same snapshot and columns as the `target-account-list` skill:
`data/accounts/snapshots/YYYY-MM-DD-apollo-firmographics.csv` with
`domain,company,industry,headcount,revenue_band,country,tech_stack,
funding_stage,source,pulled_at`. Read the actual response keys once
(`primary_domain`, `estimated_num_employees`, `technology_names`,
`latest_funding_stage`) and note any difference.

## What it does not give

Audience size, newsletter reach or event attendance; those are the
candidate's own published claims, dated in `notes`. Shared customers come
from both companies' customer pages, not from enrichment.
