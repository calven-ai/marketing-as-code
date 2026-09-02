# Decision log

Append-only, newest on top: a new entry goes directly below the `---`
separator, above the previous newest entry. Every entry follows this format:

```markdown
## YYYY-MM-DD: [decision in one imperative-free sentence]

- **Decided by:** [who]
- **Source:** [meeting/transcript path, PR, or discussion link]
- **Context:** [the problem and the options weighed, 1–3 sentences]
- **Follow-ups:** [tasks filed per integrations/tasks.md, or "none"]
```

An agent may append entries (the `log-decision` and `chief-of-staff` skills
do); nothing here is ever edited or deleted — a reversed decision gets a new
entry that references the old one.

---
