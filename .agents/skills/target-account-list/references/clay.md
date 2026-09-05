# Clay: waterfall enrichment through tables

Wired through the Clay MCP server (`integrations/catalog/enrichment.json`;
OAuth). Clay enriches by running columns over a table, and every column run
spends credits, so the server's write tools drive spend. Deny them until a
person has reviewed the tool list.

## How to use it from this skill

1. Check the server's tool list in the session for a search, an enrich and a
   table read.
2. Prefer reading a table the team already built (they chose the providers
   and the waterfall order); export it as the firmographics snapshot with
   `source` set to `clay`.
3. Only create or run a table when a person says so, with the row count
   and the columns stated first; Clay bills per provider per cell.

## Mapping

Clay columns are user-named. Map by meaning to
`domain,company,industry,headcount,revenue_band,country,tech_stack,funding_stage`
and list the mapping you used in the hand-over so the next run repeats it.
