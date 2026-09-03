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

## 2026-09-03: Bot keys live in a GitHub environment only main can use; the gate runs from main; the agent in Actions gets no shell

- **Decided by:** David Kolinek (repository maintainer)
- **Source:** the "Security hardening" pull request and its review of keys, tokens, MCP servers and unattended runs
- **Context:** the repo will be run by marketers with no guaranteed developer, connected to several MCP servers and APIs. Three choices settled how keys and unattended runs work. Keys: each person makes their own vendor key and keeps it in their own `.env` and vault item; the three bot keys (Granola, the Slack bot, the Anthropic key) are made once by the integrations owner and live only in the GitHub environment `automation`, restricted to `main`, never in repository secrets (readable by any branch) and never on a laptop. Codespaces as a way to hand shared keys to local sessions was considered and rejected. Auto-merge of bookkeeping proposals is kept, but the gate that decides it now runs from `main` (`gate.yml`), the machinery paths are never bookkeeping, and `check.yml` runs a proposal's code read-only. The agent in Actions keeps working, with no shell, no network and no Slack token; Slack gets a pointer to the proposal, and a person posts the summary after review.
- **Follow-ups:** the integrations owner runs `sh scripts/github_setup.sh`, adds the three environment secrets, and replaces `@owner-placeholder` in `.github/CODEOWNERS` via `/setup`; turn on secret scanning and push protection (Team plan add-on for a private repo); every clone runs `git config core.hooksPath scripts/hooks` once; on the first `transcripts-process.yml` run, confirm the agent commits through the action's tool with bypass mode disabled.
