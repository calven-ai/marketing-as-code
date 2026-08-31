# Security policy

## Reporting a vulnerability

Please report suspected vulnerabilities privately via
[GitHub Security Advisories](https://github.com/calven-ai/marketing-as-code/security/advisories/new)
("Report a vulnerability"). Do not open a public issue for security reports.

You can expect an acknowledgement within a few business days. Include
reproduction steps and the impact you believe the issue has.

## Scope notes

- Everything here runs locally in your own copy. Credentials live only in your
  untracked `.env` files; the shipped `.gitignore` excludes every `.env*`
  variant (the tracked `.env.example` template excepted).
- The agents act on external systems **you** configure with **your** keys.
  Reports about misuse of a user's own credentials or accounts are out of
  scope. In scope: templates or agent instructions that would cause an agent
  to leak credentials or act outside the destinations the user configured.
