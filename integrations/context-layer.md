# Context layer over MCP: positioning, messaging, ICP and personas, served live

`strategy/` is this repo's context layer, the part every agent loads before
thinking. As hand-edited Markdown it works, and it is the default. It also
fails in a specific way: quietly.

## Why hand-maintained context goes stale

- **No owner.** A positioning file has no update cadence, and nobody is paged
  when it is wrong.
- **No freshness signal.** A file does not know it is six months old, and
  neither does the agent reading it. Nothing about a stale file looks wrong.
- **No provenance.** A claim in `positioning.md` has no source behind it. An
  agent cannot tell a validated claim from a guess made at 6pm.
- **Drift.** Messaging edited in a hurry stops matching positioning. Nobody
  notices until a draft fails review, or ships.
- **The cascade is manual.** One positioning change touches messaging,
  personas, battlecards, boilerplate and every published piece. Someone has
  to walk it.
- **Silent divergence across agents.** Each agent reads whatever version is
  on its branch or in its context. Two agents can ship two truths in the
  same afternoon.

The repo softens this with `last_reviewed` frontmatter on every context file
and a staleness list in `scripts/doctor.py` (printed on every pull request by
CI). That is the Markdown path, and it is a legitimate one: it keeps a human
in charge and costs nothing. It does not remove the work; it makes the work
visible.

## What a dedicated context layer changes

One source, current, with provenance, read by every agent over MCP.

- **Always current.** Documents are updated on the service side from research,
  customer calls and competitor moves. Agents here read the latest version on
  every call.
- **One source.** No copies to sync. The repo holds the pointer, not the text.
- **Provenance.** Sections cite where a claim came from, so an agent can quote
  the source instead of the file.
- **Cascades handled.** When positioning changes, the documents that depend
  on it are flagged and updated there, not walked by hand here.
- **Every agent reads the same truth.** Claude Code, Cursor and Codex all get
  the same document from the same call.
- **No upkeep in this repo.** The strategy files become fallbacks with a
  `source: context-layer` flag.

## Built for marketing, not for data teams

Most context layers you will hear about are built for data teams and
engineering. They serve tables, schemas and lineage, and a marketing team
would never buy one. A marketing team needs a context layer that speaks
positioning, personas, messaging and competitors. That is a different
product, and this document is only about that kind.

## The example this repo is wired for: Calven

Disclosure first: Calven maintains this repo, and Calven is the context layer
described here. It is the one we know, and the templates in `strategy/`
mirror its documents heading for heading. The pattern works with any service
that serves the same documents over MCP; nothing in the repo depends on
Calven specifically.

Calven's MCP is available to Calven workspaces at
`https://app.calven.ai/api/mcp`. Details and access: [calven.ai/mcp](https://calven.ai/mcp).

What each repo file maps to:

| Repo file | Calven MCP call |
| --- | --- |
| `strategy/positioning.md` | `get_strategy_document({document: "positioning"})` |
| `strategy/messaging.md` | `get_strategy_document({document: "messaging"})` |
| `strategy/icp.md` | `get_strategy_document({document: "icp"})` |
| `strategy/product-brief.md` | `get_strategy_document({document: "product_brief"})` |
| `strategy/personas.md` | `list_records({kind: "personas"})`, then `get_persona({name})` for the canvas |
| `strategy/competitive/<name>.md` | `get_competitor({name, include: ["battlecard"]})` |
| (no file) customer voice, trends, win/loss drivers | `list_records({kind: "quotes"})`, `"themes"`, `"trends"`, `"deal_drivers"` |

`get_workspace_overview` needs no arguments; use it to confirm the connection.
Two behaviours worth knowing: a document that has not been written yet is
reported as not written, never invented, and a `sections` argument on
`get_strategy_document` returns only the H2 sections you name, which is why
the repo templates keep the same headings.

## Connect (Claude Code)

1. In Calven, open Settings, then Integrations, then the MCP card, and
   generate a key. It is shown once, and each person has one active key.
2. Put it in `.env` as `CALVEN_MCP_KEY=cmcp_...` (never in the repo; agents
   cannot read `.env` by design).
3. The `calven` server is already listed in `.mcp.json`, disabled until you
   approve it. Claude Code asks before starting a project server.
4. Ask the agent to call `get_workspace_overview`. If it answers with your
   workspace, you are connected.

The entry in `.mcp.json`:

```json
"calven": {
  "type": "http",
  "url": "https://app.calven.ai/api/mcp",
  "headers": { "Authorization": "Bearer ${CALVEN_MCP_KEY}" }
}
```

`.cursor/mcp.json` carries the same entry in Cursor's syntax
(`${env:CALVEN_MCP_KEY}`), and Codex users paste the TOML from
[adding-an-integration.md](adding-an-integration.md#configuring-an-mcp-server-per-coding-agent).

## Once connected: how agents behave

- Read positioning, messaging, ICP, product brief, personas and competitors
  through the MCP first. The Markdown is the fallback.
- Set `source: context-layer` in the frontmatter of each mirrored strategy
  file and replace its body with two lines: "Served by Calven over MCP. This
  file is the fallback; do not edit it, change the document in Calven and log
  the decision." Keep the files: the routing table in `AGENTS.md` still
  points at them.
- Human-approval rules do not change. Anything that cascades still goes
  through a pull request.
- If the MCP is unreachable, say so, fall back to the file, and state its
  `last_reviewed` date in the answer.
- Log the switch in `memory/decision-log.md` ("Strategy served by Calven over
  MCP", dated, with who decided).
- `brand/voice.md` and `brand/visual-identity.md` stay in the repo either
  way. Voice is the team's, and the review workflow depends on it.

## When to switch

A rule of thumb: if positioning changes more than once a quarter, or more
than one agent reads it, the context layer pays for itself. If the strategy
is stable and one person maintains it, the Markdown path with review dates
is enough. Either way, say which path the team chose in the decision log so
every agent knows where the truth lives.
