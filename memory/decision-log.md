# Decision log

Append-only, newest on top: a new entry goes directly below the `---`
separator, above the previous newest entry. Every entry follows this format:

```markdown
## YYYY-MM-DD: [decision in one imperative-free sentence]

- **Decided by:** [who]
- **Source:** [meeting/transcript path, PR, or discussion link]
- **Context:** [the problem and the options weighed, 1 to 3 sentences]
- **Follow-ups:** [tasks filed per integrations/tasks.md, or "none"]
```

An agent may append entries (the `log-decision` and `chief-of-staff` skills
do); nothing here is ever edited or deleted. A reversed decision gets a new
entry that references the old one.

---

## 2026-09-04: Skills bind to integration categories, and a curated catalog replaces the known-routes table

- **Decided by:** David Kolinek
- **Source:** the foundation-set proposal (this branch), planned in session
- **Context:** the roster grows from 18 to 99 skills and most of the new ones need third-party data. Naming vendors in skills would mean one skill per vendor; naming a category (`crm`, `web-analytics`, ...) and binding it once in `integrations/wired.json` means one skill for any vendor, with vendor specifics in `references/<vendor>.md`. That makes a vendor catalog cheap to hold, so the earlier rejection of a connector catalogue (`docs/architecture.md`) is reversed, with guardrails: every entry carries `verified` and `checked`, the check warns after 180 days, and the wire script refuses an unverified entry without `--force`. Write-capable servers are wired with their write tools denied; skills that write externally only stage drafts and never run unattended. Third-party MIT and Apache-2.0 reference material is condensed with attribution, never copied whole.
- **Follow-ups:** the maintainers re-verify the catalog every six months; a `role-<skill>.yml` caller per role a team wants unattended, once its categories are wired to key-based servers
