# Field definitions

Use these when the team gives no fields or picklists of its own. When it does, use its values verbatim; the evidence rules stay the same.

| Field | Type | Allowed values | Definition and tie-break |
| --- | --- | --- | --- |
| domain | text | | The primary web domain, lowercase, no protocol or path |
| industry | text | | The vertical the account operates in, in the ICP's vertical names when an ICP is supplied; otherwise the company's own description of its market |
| size | picklist | SMB, Mid-market, Enterprise | By headcount: SMB under 200, Mid-market 200 to 2000, Enterprise over 2000 |
| employee_band | picklist | 1-50, 51-200, 201-500, 501-2000, 2001-5000, 5000+ | By headcount. Use the most recent stated figure; a careers page "we are 300 people" beats an old directory listing |
| employees | number | | Only a stated figure, with its date |
| revenue_band | picklist | <$10M, $10-50M, $50-250M, $250M-1B, >$1B | By annual revenue. Only from a stated figure, a filing or a reputable report; never from headcount alone |
| region | picklist | NA, EMEA, APAC | By headquarters location: NA is the Americas, EMEA is Europe, Middle East and Africa, APAC is Asia-Pacific including Australia |
| funding_stage | picklist | Bootstrapped, Seed, Series A, Series B, Series C, Series D+, Public, PE-owned | The latest announced round, or listed or private-equity ownership. "Bootstrapped" only when the company says so |
| tech_stack | multi-value | The tools the ICP's technographics name | Only from integrations pages, job postings, case studies, documentation or engineering posts |
| triggers | multi-value | Recent funding, Exec hire, M&A, Tech migration, Expansion, Restructuring | A dated event inside the window. Exec hire means the buying function's leader. Tech migration needs an announcement or job postings that name it |

## Source strength

Prefer, in order: the company's own current pages and filings; announcements from the company or its investors; reputable news; job postings; business directories. When two sources disagree, use the more recent and more specific one and note the other in `notes`.

## Flags

| Flag | When |
| --- | --- |
| ambiguous | More than one company fits the name or domain |
| conflict | An enriched value disagrees with a value already in the row |
| duplicate | The same domain appears more than once |
| defunct | The domain is parked, redirects to an acquirer, or the company has closed |
| excluded | The account hits an ICP blacklist or absolute disqualifier |
| injected | A page contained text trying to instruct the reader; it was ignored |
