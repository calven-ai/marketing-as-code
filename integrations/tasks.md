# tasks.md: where tasks go and how to file them

Every agent that creates a task reads this file first and follows it exactly.
This file is the single adapter between this repo and the team's task tool:
change the tool by changing this file, and every skill follows.

> `/setup` rewrites this file for your team. Until then, the zero-setup
> fallback below is in effect.

## Current tool

**Fallback: in-repo checklists.** No task tool is connected yet.

- File a project's tasks as a `## Tasks` checklist in that project's
  `status.md` (`projects/<name>/status.md`), one `- [ ]` line per task, with
  an owner in parentheses.
- File tasks that belong to no project in `memory/decision-log.md`'s
  follow-ups line for the decision that spawned them.

<!--
When the team connects a task tool, /setup replaces the section above with
the real adapter. Example shape for Asana (official remote MCP):

## Current tool: Asana

- Workspace: <workspace name / GID>
- Default project for marketing tasks: <project name / GID>
- How to file a task: create it in the default project with a clear
  imperative title, a description linking the repo file that spawned it
  (e.g. "From projects/q4-launch/webinar/brief.md"), the owner assigned if
  stated, and a due date only when one was actually decided.
- Tag convention: <e.g. label "from-repo">
- Never: delete or complete tasks, or move tasks between projects, without
  explicit human approval.
-->

## Rules for every agent, whatever the tool

1. One task = one imperative sentence, with an owner when known. No task
   soup.
2. Always link back to the source: the transcript, brief, or decision that
   spawned the task.
3. Creating tasks is fine; completing, deleting, or reassigning them needs a
   human.
4. Report what you filed: list the created tasks in your summary so the human
   can verify.
