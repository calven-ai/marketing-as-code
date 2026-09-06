---
name: log-decision
description: Record a decision in memory/decision-log.md. Use whenever a discussion, meeting or thread resolves something ("log this decision", "we decided X"), or when work surfaces a decision never logged.
license: MIT
metadata:
  kind: workflow
  area: core
  needs: []
  writes: repo
  runs: person
---

# Log a decision

## Procedure

1. **Extract the decision** as one clean sentence of *what was decided* (not
   the discussion). If multiple decisions are tangled together, log them as
   separate entries.
2. **Add the entry to `memory/decision-log.md`** directly below the `---`
   separator (newest on top), in the file's exact format: date, decided-by, source (transcript path, PR, or link),
   context (1 to 3 sentences: the problem and the options weighed), follow-ups.
3. **File the follow-ups** per `integrations/tasks.md` and list them in the
   entry.
4. **Cascade if obvious**: if the decision plainly invalidates something in
   `strategy/`, `brand/`, or `memory/knowledge/`, propose that edit as a
   diff for review; never apply it silently.

## Rules

- Append-only: never edit or delete an existing entry. A reversal is a new
  entry linking the old one.
- No attribution guessing: if you don't know who decided, ask or write
  "team".
