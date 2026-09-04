# Security policy

> In your own copy of this template, point this at your own repository's
> advisories page, or delete the file (docs/make-it-yours.md).

## Reporting a vulnerability

Report suspected vulnerabilities privately through
[GitHub Security Advisories](https://github.com/calven-ai/marketing-as-code/security/advisories/new)
("Report a vulnerability"). Do not open a public issue. Include reproduction
steps and the impact you believe the issue has. Expect an acknowledgement
within a few business days.

## Scope

Everything here runs in your own copy, on your machine or in your own
GitHub Actions. Your keys live in untracked `.env` files; bot keys live in a
GitHub environment only `main` can use ([docs/secrets.md](docs/secrets.md)).

**Out of scope:** misuse of a user's own credentials or accounts. The agents
act on systems you configure with your keys.

**In scope:** templates, workflows or agent instructions that would make an
agent leak credentials, act outside the destinations the user configured, or
land a change on `main` without the review gate
(`.github/workflows/gate.yml`) allowing it. Also any way for content an agent
reads (transcripts, scraped pages, vendor output) to make it do either.
