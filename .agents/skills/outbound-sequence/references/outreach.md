# Outreach: staging an inactive sequence

Wired through the Outreach MCP server (`integrations/catalog/outbound.json`;
OAuth, needs the Amplify add-on and an admin to enable it). The server can
read, create and delete, never update, and there is no read-only mode: the
admin toggles create (on by default) and delete (off by default). Check the
server's tool list in the session before the first write.

## What this skill may do

1. Read existing sequences and their step counts to avoid a duplicate name.
2. Create one sequence, named after the content slug per
   `data/ontology/naming.md`, with its steps, in the disabled state, with
   zero prospects enrolled. Ask before the call; report the sequence id.
3. Stop. Enabling the sequence, enrolling prospects and sending are a
   person's acts in the Outreach UI.

## What it never does

Enrol a prospect, enable a sequence, create or edit prospects, delete
anything, or run unattended. Because the server cannot update, a fix to a
step means a person edits it in the UI, or asks for a second sequence and
deletes the first themselves.

## Reading outcomes

Reply, open and meeting counts per sequence are a `snapshot-pull` into
`data/email/snapshots/YYYY-MM-DD-outreach-<what>.csv`, columns
`sequence,step,sent,opened,replied,positive,meetings,bounced,pulled_at`.
Other vendors in the category (Salesloft, lemlist, Instantly, Smartlead,
Apollo) follow the same rule: inactive object only, ids reported, a person
activates.
