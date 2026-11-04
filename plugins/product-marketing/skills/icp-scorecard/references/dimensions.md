# Standard dimensions

Use these when the team has no CRM picklists of its own. When it does, use its values verbatim and keep the same dimension logic.

| Dimension | Match | Values | Where the value comes from |
| --- | --- | --- | --- |
| Employee band | exact | 1-50, 51-200, 201-500, 501-2000, 2001-5000, 5000+ | Headcount |
| Size | exact | SMB (under 200), Mid-market (200 to 2000), Enterprise (2000+) | Headcount; use instead of employee band, never both |
| Revenue band | exact | <$10M, $10-50M, $50-250M, $250M-1B, >$1B | Annual revenue |
| Region | exact | NA (the Americas), EMEA (Europe, Middle East, Africa), APAC (Asia-Pacific incl. Australia) | Headquarters location |
| Funding stage | exact | Bootstrapped, Seed, Series A, Series B, Series C, Series D+, Public, PE-owned | Latest round or ownership |
| Industry | exact | The team's own vertical names, as the ICP's Priority and Secondary Verticals spell them | The account's vertical |
| Tech stack | any of | The tools the ICP's technographics name (integrations, incumbents, co-sell partners) | Observable tooling |
| Triggers | any of | Recent funding, Exec hire, M&A, Tech migration, Expansion, Restructuring, plus any trigger the ICP names | Dated events on the account |
| Buyer present | exact | both (economic buyer and champion known), one | Contacts on open or past deals |
| Complexity | any of | Low, Medium, High | Scale of need recorded on deals |

Rules:

- Size and employee band measure the same thing. Pick one; scoring both double counts.
- Industry is often free text in a CRM. Normalise to the ICP's vertical names before scoring and list the mapping you used.
- Buyer present and complexity come from deal records, so a list of cold accounts will usually lack them. That is expected: they drop out of the score and lower confidence.
- A dimension with only one possible value in the list (every account is in NA) cannot separate accounts; give it no weight for that list and say so.
