#!/usr/bin/env python3
"""Wire a catalog vendor into this repo: read integrations/catalog/, write the
MCP entry into .mcp.json and .cursor/mcp.json, add the missing variable names
to .env.example, deny the vendor's write tools in .claude/settings.json, record
the binding in integrations/wired.json, and print the Codex TOML plus the
docs/secrets.md row. --list shows every category with its wired vendor,
--category the routes of one, --unwire removes a vendor, --subset --stdout
prints a filtered .mcp.json for an unattended run. Standard library only.

    python3 scripts/wire_integration.py --list                  # categories, wired vendor, alternatives
    python3 scripts/wire_integration.py --category crm          # vendors and routes for one category
    python3 scripts/wire_integration.py hubspot                 # wire the default variant
    python3 scripts/wire_integration.py hubspot:token --dry-run # named variant, print only
    python3 scripts/wire_integration.py --unwire hubspot
    python3 scripts/wire_integration.py --subset dataforseo --stdout   # filtered .mcp.json for role-run.yml

Every edit is idempotent: a second identical run changes nothing and says so.
Refusals are one readable line and exit 1: an unknown vendor or variant, a
vendor marked `verified: unverified` (pass --force after reading its source),
a vendor without an MCP route (follow its cli, script or manual route by hand),
a server name already bound to another vendor, and an --unwire that would
strand a skill whose `needs` names the category. --allow-writes skips the
read-only switch and the deny rules; the human gate in AGENTS.md still
applies. Nothing here reads or writes .env: only variable names move, into
.env.example, and never a value.
"""

import argparse
import copy
import datetime as dt
import json
import re
import sys
from pathlib import Path

from _common import ROOT

DEFAULT_PLACEHOLDER = r"\$\{(?:env:)?([A-Z][A-Z0-9_]*)\}"
BARE_PLACEHOLDER = re.compile(r"\$\{(?!env:)([A-Z][A-Z0-9_]*)\}")
NEEDS_LIST = re.compile(r"^\s*needs:\s*\[(.*?)\]\s*$", re.M)
NEEDS_BARE = re.compile(r"^\s*needs:\s*([a-z0-9][a-z0-9-]*)\s*$", re.M)
VERIFIED_LEVELS = ("vendor", "listing", "unverified")


class Refusal(Exception):
    """One readable line; main() prints it and exits 1."""


# ------------------------------------------------------------------ files --

def load_json(path, default):
    path = Path(path)
    if not path.is_file():
        return copy.deepcopy(default)
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(obj):
    return json.dumps(obj, indent=2) + "\n"


class Repo:
    """One checkout: the catalog, the schema, and the five files a wire touches."""

    def __init__(self, root):
        self.root = Path(root).resolve()
        self.schema = load_json(self.root / "docs" / "schema.json", {})
        section = self.schema.get("catalog", {}) if isinstance(self.schema, dict) else {}
        self.placeholder = re.compile(self.schema.get("mcp", {}).get("placeholder", DEFAULT_PLACEHOLDER))
        self.catalog_dir = self.root / (section.get("dir") or "integrations/catalog")
        self.wired_path = self.root / (section.get("wired") or "integrations/wired.json")
        self.mcp_path = self.root / ".mcp.json"
        self.cursor_path = self.root / ".cursor" / "mcp.json"
        self.env_example = self.root / ".env.example"
        self.settings_path = self.root / ".claude" / "settings.json"
        self.skills_dir = self.root / ".agents" / "skills"
        self.catalog, self.broken = self._load_catalog()
        self.category_order = self._category_order(section.get("categories") or [])

    def _load_catalog(self):
        catalog, broken = {}, {}
        if not self.catalog_dir.is_dir():
            return catalog, broken
        for path in sorted(self.catalog_dir.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as err:
                broken[path.stem] = str(err).splitlines()[0]
                continue
            if not isinstance(data, dict):
                broken[path.stem] = "not a JSON object"
                continue
            data.setdefault("id", path.stem)
            data.setdefault("vendors", [])
            data["_file"] = path.relative_to(self.root).as_posix()
            catalog[data["id"]] = data
        return catalog, broken

    def _category_order(self, listed):
        ids = [c["id"] if isinstance(c, dict) else str(c) for c in listed]
        seen = set(ids)
        return ids + sorted(k for k in list(self.catalog) + list(self.broken) if k not in seen)

    # -- lookups --

    def find_vendor(self, vendor_id):
        """[(category, vendor)] for every category file that lists the vendor."""
        hits = []
        for cat_id in self.category_order:
            cat = self.catalog.get(cat_id)
            if not cat:
                continue
            for vendor in cat.get("vendors", []):
                if vendor.get("id") == vendor_id:
                    hits.append((cat, vendor))
        return hits

    def all_mcp_routes(self):
        for cat in self.catalog.values():
            for vendor in cat.get("vendors", []):
                for route in mcp_routes(vendor):
                    yield cat, vendor, route

    def wired(self):
        data = load_json(self.wired_path, {"wired": {}, "custom_servers": {}})
        data.setdefault("wired", {})
        data.setdefault("custom_servers", {})
        return data

    def server_owner(self, server, mcp_servers, wired):
        """The vendor id a server name in .mcp.json belongs to, or None when unknown."""
        for cat_id, entry in wired.get("wired", {}).items():
            vendor_id = entry.get("vendor")
            if not vendor_id:
                continue
            for cat, vendor in self.find_vendor(vendor_id):
                if cat["id"] != cat_id:
                    continue
                for route in mcp_routes(vendor):
                    if route.get("server") == server and entry.get("variant") in (None, route.get("id")):
                        return vendor_id
        existing = mcp_servers.get(server)
        if not existing:
            return None
        for _cat, vendor, route in self.all_mcp_routes():
            if route.get("server") != server:
                continue
            if route.get("url") and route.get("url") == existing.get("url"):
                return vendor.get("id")
            if route.get("command") and route.get("command") == existing.get("command") \
                    and list(route.get("args") or []) == list(existing.get("args") or []):
                return vendor.get("id")
        return None

    def skills_needing(self, category_id):
        """Skill names whose frontmatter `needs` list names the category."""
        names = []
        if not self.skills_dir.is_dir():
            return names
        for path in sorted(self.skills_dir.glob("*/SKILL.md")):
            head = path.read_text(encoding="utf-8", errors="replace").split("\n---", 2)[:2]
            text = "\n".join(head)
            needs = []
            for m in NEEDS_LIST.finditer(text):
                needs += [v.strip().strip("\"'") for v in m.group(1).split(",") if v.strip()]
            for m in NEEDS_BARE.finditer(text):
                needs.append(m.group(1))
            if category_id in needs:
                names.append(path.parent.name)
        return names


# ---------------------------------------------------------------- catalog --

def mcp_routes(vendor):
    routes = vendor.get("routes") or {}
    mcp = routes.get("mcp") or []
    return [r for r in mcp if isinstance(r, dict)]


def pick_variant(vendor, variant_id):
    routes = mcp_routes(vendor)
    if not routes:
        return None
    if variant_id:
        for r in routes:
            if r.get("id") == variant_id:
                return r
        raise Refusal(f"{vendor.get('id')} has no MCP variant {variant_id!r}; it has: "
                      + ", ".join(str(r.get("id")) for r in routes))
    for r in routes:
        if r.get("default"):
            return r
    return routes[0]


def route_kind(vendor):
    """The default route of a vendor, for the listings: mcp:http, mcp:stdio, cli, script, manual."""
    routes = vendor.get("routes") or {}
    mcp = mcp_routes(vendor)
    if mcp:
        route = next((r for r in mcp if r.get("default")), mcp[0])
        return "mcp:" + str(route.get("transport", "?"))
    if isinstance(routes.get("cli"), dict) and routes["cli"].get("tool"):
        return "cli"
    if isinstance(routes.get("script"), dict) and routes["script"].get("path"):
        return "script"
    return "manual"


def writes_status(vendor, allow_writes):
    if not vendor.get("writes"):
        return "n/a"
    return "allowed" if allow_writes else "denied"


def wired_routes(vendor):
    out = ["mcp"]
    script = (vendor.get("routes") or {}).get("script")
    if isinstance(script, dict) and script.get("path"):
        out.append("script")
    return out


# ---------------------------------------------------------------- entries --

def mcp_entry(vendor, route, allow_writes):
    """The .mcp.json entry for one route, with the read-only switch applied."""
    transport = route.get("transport")
    if transport not in ("http", "stdio"):
        raise Refusal(f"{vendor.get('id')}:{route.get('id')} has transport {transport!r}; only http and stdio are wired")
    entry = {"type": transport}
    if transport == "http":
        if not route.get("url"):
            raise Refusal(f"{vendor.get('id')}:{route.get('id')} is an http route without a url")
        entry["url"] = route["url"]
        if route.get("headers"):
            entry["headers"] = dict(route["headers"])
    else:
        if not route.get("command"):
            raise Refusal(f"{vendor.get('id')}:{route.get('id')} is a stdio route without a command")
        entry["command"] = route["command"]
        entry["args"] = list(route.get("args") or [])
        if route.get("env"):
            entry["env"] = dict(route["env"])
    if route.get("oauth_scopes"):
        entry["oauth"] = {"scopes": list(route["oauth_scopes"])}
    switch = vendor.get("read_only_switch")
    if switch and not allow_writes:
        apply_switch(entry, switch)
    return entry


def apply_switch(entry, switch):
    kind, name, value = switch.get("kind"), switch.get("name"), switch.get("value")
    if kind == "env":
        entry.setdefault("env", {})[name] = "" if value is None else str(value)
    elif kind == "arg":
        args = entry.setdefault("args", [])
        for piece in [name] + ([str(value)] if value not in (None, "") else []):
            if piece not in args:
                args.append(piece)
    elif kind == "url":
        url = entry.get("url", "")
        if name == "path":
            tail = "/" + str(value).lstrip("/")
            if not url.rstrip("/").endswith(tail.rstrip("/")):
                entry["url"] = url.rstrip("/") + tail
        else:
            param = f"{name}={value}"
            if param not in url:
                entry["url"] = url + ("&" if "?" in url else "?") + param
    elif kind == "header":
        entry.setdefault("headers", {})[name] = "" if value is None else str(value)
    else:
        raise Refusal(f"read_only_switch kind {kind!r} is not one of env, arg, url, header")


def cursor_entry(entry):
    """The .cursor/mcp.json form: no type key, ${VAR} as ${env:VAR}."""
    def rewrite(value):
        if isinstance(value, str):
            return BARE_PLACEHOLDER.sub(r"${env:\1}", value)
        if isinstance(value, list):
            return [rewrite(v) for v in value]
        if isinstance(value, dict):
            return {k: rewrite(v) for k, v in value.items()}
        return value
    return {k: rewrite(v) for k, v in entry.items() if k != "type"}


def placeholders_in(entry, pattern):
    found = []

    def walk(value):
        if isinstance(value, str):
            for m in pattern.finditer(value):
                if m.group(1) not in found:
                    found.append(m.group(1))
        elif isinstance(value, list):
            for v in value:
                walk(v)
        elif isinstance(value, dict):
            for v in value.values():
                walk(v)
    walk(entry)
    return found


def env_vars_for(route, entry, pattern):
    auth = route.get("auth") or {}
    names = [str(v) for v in (auth.get("env") or [])]
    for var in placeholders_in(entry, pattern):
        if var not in names:
            names.append(var)
    return names


def missing_env_vars(env_text, names):
    return [n for n in names if not re.search(r"^" + re.escape(n) + r"=", env_text, re.M)]


def env_block(vendor, cat, route, names):
    where = (route.get("auth") or {}).get("where") or "see integrations/catalog/"
    lines = [f"# {vendor.get('name') or vendor.get('id')} ({cat['id']}): {where}"]
    lines += [f"{n}=" for n in names]
    return "\n".join(lines) + "\n"


def deny_rules(vendor, route):
    server = route["server"]
    tools = [t for t in (vendor.get("write_tools") or []) if t]
    if tools:
        return [f"mcp__{server}__{t}" for t in tools], False
    if vendor.get("writes"):
        return [f"mcp__{server}"], True
    return [], False


# --------------------------------------------------------------- snippets --

def codex_toml(server, entry):
    lines = [f"[mcp_servers.{server}]"]
    if entry.get("type") == "http":
        lines.append(f"url = {json.dumps(entry['url'])}")
        plain, from_env = {}, {}
        for key, value in (entry.get("headers") or {}).items():
            bearer = re.fullmatch(r"Bearer \$\{(?:env:)?([A-Z][A-Z0-9_]*)\}", str(value))
            if key.lower() == "authorization" and bearer:
                lines.append(f"bearer_token_env_var = {json.dumps(bearer.group(1))}")
                continue
            whole = re.fullmatch(DEFAULT_PLACEHOLDER, str(value))
            if whole:
                from_env[key] = whole.group(1)
            else:
                plain[key] = value
        if plain:
            lines.append("http_headers = { " + ", ".join(f"{json.dumps(k)} = {json.dumps(v)}" for k, v in plain.items()) + " }")
        if from_env:
            lines.append("env_http_headers = { " + ", ".join(f"{json.dumps(k)} = {json.dumps(v)}" for k, v in from_env.items()) + " }")
    else:
        lines.append(f"command = {json.dumps(entry.get('command', ''))}")
        lines.append("args = [" + ", ".join(json.dumps(a) for a in entry.get("args") or []) + "]")
        env = entry.get("env") or {}
        if env:
            pairs = []
            for key, value in env.items():
                if re.fullmatch(DEFAULT_PLACEHOLDER, str(value)):
                    pairs.append(f'{key} = ""')
                else:
                    pairs.append(f"{key} = {json.dumps(value)}")
            lines.append("env = { " + ", ".join(pairs) + " }  # empty values: fill from your own .env, never commit")
    return "\n".join(lines)


def secrets_row(vendor, route, names):
    name = vendor.get("name") or vendor.get("id")
    auth = route.get("auth") or {}
    where = auth.get("where") or f"{name} settings"
    if auth.get("model") == "oauth" and not names:
        return (f"| {name} | per person, OAuth | each person | nowhere; the browser grant on first use "
                f"| {name}: revoke the grant | remove them from the {name} organization |")
    cred = ", ".join(f"`{n}`" for n in names) or name
    return (f"| {cred} | per person | each person | their own `.env`, their own 1Password item "
            f"| {where} | revoke their key in {name} |")


# ------------------------------------------------------------------ wire --

def wire(repo, spec, category=None, allow_writes=False, force=False, dry_run=False, out=None):
    out = out or sys.stdout
    vendor_id, _, variant_id = spec.partition(":")
    hits = repo.find_vendor(vendor_id)
    if not hits:
        known = sorted({v.get("id") for c in repo.catalog.values() for v in c.get("vendors", []) if v.get("id")})
        hint = "; the catalog is empty" if not known else ""
        if repo.broken:
            hint += "; unreadable catalog files: " + ", ".join(sorted(repo.broken))
        raise Refusal(f"unknown vendor {vendor_id!r}: not in any integrations/catalog/*.json{hint}. "
                      "Run --list to see what is there.")
    if category:
        hits = [(c, v) for c, v in hits if c["id"] == category]
        if not hits:
            raise Refusal(f"{vendor_id} is not listed under category {category!r}")

    plan = []
    for cat, vendor in hits:
        if vendor.get("verified") == "unverified" and not force:
            src = vendor.get("source_url") or "its source"
            raise Refusal(f"{vendor_id} is marked verified: unverified in {cat['_file']}: nobody on the team has "
                          f"read its source yet. Read {src}, set verified to listing or vendor in the catalog, "
                          "or pass --force to wire it anyway.")
        route = pick_variant(vendor, variant_id)
        if route is None:
            raise Refusal(f"{vendor_id} has no MCP route; follow the cli/script/manual route in the catalog "
                          f"({cat['_file']}) by hand.")
        if not route.get("server"):
            raise Refusal(f"{vendor_id}:{route.get('id')} has no server name in {cat['_file']}")
        plan.append((cat, vendor, route, mcp_entry(vendor, route, allow_writes)))

    mcp = load_json(repo.mcp_path, {"mcpServers": {}})
    cursor = load_json(repo.cursor_path, {"mcpServers": {}})
    settings = load_json(repo.settings_path, {"permissions": {"deny": []}})
    wired = repo.wired()
    env_text = repo.env_example.read_text(encoding="utf-8") if repo.env_example.is_file() else ""
    mcp.setdefault("mcpServers", {})
    cursor.setdefault("mcpServers", {})
    deny = settings.setdefault("permissions", {}).setdefault("deny", [])
    before = (dump_json(mcp), dump_json(cursor), dump_json(settings), dump_json(wired), env_text)
    today = dt.date.today().isoformat()
    changes, notes, snippets = [], [], []

    for cat, vendor, route, entry in plan:
        server = route["server"]
        owner = repo.server_owner(server, mcp["mcpServers"], wired)
        if owner and owner != vendor_id:
            raise Refusal(f"server {server!r} in .mcp.json is bound to {owner}; unwire that first or give "
                          f"{vendor_id}'s route another server name in {cat['_file']}.")
        label = f"{vendor_id}:{route.get('id')} for {cat['id']}"
        if mcp["mcpServers"].get(server) != entry:
            verb = "updated" if server in mcp["mcpServers"] else "added"
            mcp["mcpServers"][server] = entry
            changes.append(f".mcp.json: {verb} mcpServers.{server} ({label})")
        c_entry = cursor_entry(entry)
        if cursor["mcpServers"].get(server) != c_entry:
            verb = "updated" if server in cursor["mcpServers"] else "added"
            cursor["mcpServers"][server] = c_entry
            changes.append(f".cursor/mcp.json: {verb} mcpServers.{server}")

        names = env_vars_for(route, entry, repo.placeholder)
        missing = missing_env_vars(env_text, names)
        if missing:
            block = env_block(vendor, cat, route, missing)
            env_text = env_text + ("" if not env_text or env_text.endswith("\n") else "\n") + "\n" + block
            changes.append(".env.example: added " + ", ".join(missing))

        if not allow_writes:
            rules, whole = deny_rules(vendor, route)
            new = [r for r in rules if r not in deny]
            if new:
                deny.extend(new)
                changes.append(".claude/settings.json: denied " + ", ".join(new))
            if whole:
                notes.append(f"{vendor_id} can write but the catalog lists no write_tools, so the whole server "
                             f"(mcp__{server}) is denied until the tool names are recorded in {cat['_file']}.")
        elif vendor.get("writes"):
            notes.append(f"--allow-writes: {server} may change things at {vendor.get('name') or vendor_id}. "
                         "The human gate still applies (AGENTS.md rule 3): a person approves anything sent, "
                         "changed or deleted.")

        wanted = {"vendor": vendor_id, "variant": route.get("id"), "routes": wired_routes(vendor),
                  "writes": writes_status(vendor, allow_writes)}
        current = wired["wired"].get(cat["id"]) or {}
        if {k: current.get(k) for k in wanted} != wanted:
            wired["wired"][cat["id"]] = dict(wanted, since=today)
            changes.append(f"integrations/wired.json: {cat['id']} -> {vendor_id}:{route.get('id')} ({wanted['writes']})")

        snippets.append((server, entry, c_entry, vendor, route, names, cat))

    after = (dump_json(mcp), dump_json(cursor), dump_json(settings), dump_json(wired), env_text)
    if after == before:
        print(f"nothing to change: {spec} is already wired" + (f" for {category}" if category else "") + ".", file=out)
    elif dry_run:
        print("dry run: nothing written. The edits would be:", file=out)
        for line in changes:
            print("  " + line, file=out)
        shown = set()
        for server, entry, c_entry, vendor, route, names, cat in snippets:
            if server in shown:
                continue
            shown.add(server)
            print(f"\n.mcp.json mcpServers.{server}:", file=out)
            print(json.dumps(entry, indent=2), file=out)
            print(f"\n.cursor/mcp.json mcpServers.{server}:", file=out)
            print(json.dumps(c_entry, indent=2), file=out)
            missing = missing_env_vars(before[4], names)
            if missing:
                print("\n.env.example:", file=out)
                print(env_block(vendor, cat, route, missing), end="", file=out)
    else:
        if after[0] != before[0]:
            repo.mcp_path.write_text(after[0], encoding="utf-8")
        if after[1] != before[1]:
            repo.cursor_path.parent.mkdir(parents=True, exist_ok=True)
            repo.cursor_path.write_text(after[1], encoding="utf-8")
        if after[2] != before[2]:
            repo.settings_path.parent.mkdir(parents=True, exist_ok=True)
            repo.settings_path.write_text(after[2], encoding="utf-8")
        if after[3] != before[3]:
            repo.wired_path.parent.mkdir(parents=True, exist_ok=True)
            repo.wired_path.write_text(after[3], encoding="utf-8")
        if after[4] != before[4]:
            repo.env_example.write_text(after[4], encoding="utf-8")
        for line in changes:
            print(line, file=out)
    for note in notes:
        print("note: " + note, file=out)

    seen = set()
    for server, entry, _c, vendor, route, names, _cat in snippets:
        if server in seen:
            continue
        seen.add(server)
        print(f"\nCodex (~/.codex/config.toml), {vendor.get('name') or vendor_id}:", file=out)
        print(codex_toml(server, entry), file=out)
        print("\ndocs/secrets.md row (Credential | Kind | Who owns it | Where it lives | Rotate it at | When someone leaves):", file=out)
        print(secrets_row(vendor, route, names), file=out)
    print("\nrun: python3 scripts/lint.py --fix (regenerates integrations/README.md)", file=out)
    return 0


# ---------------------------------------------------------------- unwire --

def unwire(repo, vendor_id, category=None, force=False, dry_run=False, out=None):
    out = out or sys.stdout
    wired = repo.wired()
    targets = [(cat_id, entry) for cat_id, entry in wired["wired"].items()
               if entry.get("vendor") == vendor_id and (not category or cat_id == category)]
    mcp = load_json(repo.mcp_path, {"mcpServers": {}})
    cursor = load_json(repo.cursor_path, {"mcpServers": {}})
    mcp.setdefault("mcpServers", {})
    cursor.setdefault("mcpServers", {})

    servers = set()
    for cat_id, entry in targets:
        for cat, vendor in repo.find_vendor(vendor_id):
            if cat["id"] == cat_id:
                for route in mcp_routes(vendor):
                    if entry.get("variant") in (None, route.get("id")) and route.get("server"):
                        servers.add(route["server"])
    if not targets and vendor_id not in mcp["mcpServers"]:
        raise Refusal(f"{vendor_id} is not wired: no entry in integrations/wired.json and no server named "
                      f"{vendor_id!r} in .mcp.json.")
    if not servers and vendor_id in mcp["mcpServers"]:
        servers.add(vendor_id)

    stranded = []
    for cat_id, _entry in targets:
        for skill in repo.skills_needing(cat_id):
            stranded.append(f"{skill} (needs {cat_id})")
    if stranded and not force:
        raise Refusal(f"unwiring {vendor_id} leaves these skills without a vendor: " + ", ".join(stranded)
                      + ". Wire a replacement first, or pass --force.")

    remaining = {k: v for k, v in wired["wired"].items() if (k, v) not in targets}
    still_bound = set()
    for cat_id, entry in remaining.items():
        for cat, vendor in repo.find_vendor(entry.get("vendor") or ""):
            if cat["id"] == cat_id:
                for route in mcp_routes(vendor):
                    if entry.get("variant") in (None, route.get("id")) and route.get("server"):
                        still_bound.add(route["server"])
    servers = sorted(s for s in servers if s not in still_bound)

    changes = []
    for server in servers:
        if mcp["mcpServers"].pop(server, None) is not None:
            changes.append(f".mcp.json: removed mcpServers.{server}")
        if cursor["mcpServers"].pop(server, None) is not None:
            changes.append(f".cursor/mcp.json: removed mcpServers.{server}")
    for cat_id, _entry in targets:
        changes.append(f"integrations/wired.json: dropped {cat_id} ({vendor_id})")
    wired["wired"] = remaining

    if not changes:
        print(f"nothing to change: {vendor_id} is not wired.", file=out)
        return 0
    if dry_run:
        print("dry run: nothing written. The edits would be:", file=out)
        for line in changes:
            print("  " + line, file=out)
    else:
        repo.mcp_path.write_text(dump_json(mcp), encoding="utf-8")
        if repo.cursor_path.is_file() or cursor["mcpServers"]:
            repo.cursor_path.parent.mkdir(parents=True, exist_ok=True)
            repo.cursor_path.write_text(dump_json(cursor), encoding="utf-8")
        repo.wired_path.parent.mkdir(parents=True, exist_ok=True)
        repo.wired_path.write_text(dump_json(wired), encoding="utf-8")
        for line in changes:
            print(line, file=out)
    if stranded:
        print("note: these skills now have no vendor for what they need: " + ", ".join(stranded), file=out)
    print("left alone: .env.example and .claude/settings.json (remove the variable names and the "
          "mcp__ deny rules by hand if the vendor is gone for good).", file=out)
    print("run: python3 scripts/lint.py --fix (regenerates integrations/README.md)", file=out)
    return 0


# -------------------------------------------------------------- listings --

def wired_label(entry):
    if entry is None:
        return "none"
    vendor = entry.get("vendor")
    if not vendor:
        return "manual"
    label = vendor + (f":{entry['variant']}" if entry.get("variant") else "")
    routes = entry.get("routes") or []
    return label + (" (" + "+".join(routes) + ")" if routes else "")


def list_categories(repo, out=None):
    out = out or sys.stdout
    wired = repo.wired()["wired"]
    if not repo.catalog and not repo.broken:
        print(f"the catalog is empty: no {repo.catalog_dir.relative_to(repo.root).as_posix()}/*.json yet.", file=out)
    rows = []
    for cat_id in repo.category_order:
        cat = repo.catalog.get(cat_id)
        if cat is None:
            alt = "(unreadable: " + repo.broken[cat_id] + ")" if cat_id in repo.broken else "(no catalog file)"
        else:
            parts = []
            for v in cat.get("vendors", []):
                parts.append(f"{v.get('id')} ({route_kind(v)}, {v.get('verified', '?')})")
            alt = ", ".join(parts) or "(no vendors)"
        rows.append((cat_id, wired_label(wired.get(cat_id)), alt))
    for cat_id, entry in wired.items():
        if cat_id not in repo.category_order:
            rows.append((cat_id, wired_label(entry), "(not in the catalog)"))
    if not rows:
        return 0
    w0 = max(len(r[0]) for r in rows + [("category",)])
    w1 = max(len(r[1]) for r in rows + [("", "wired")])
    print(f"{'category':<{w0}}  {'wired':<{w1}}  catalog", file=out)
    for cat_id, wired_str, alt in rows:
        print(f"{cat_id:<{w0}}  {wired_str:<{w1}}  {alt}", file=out)
    return 0


def show_category(repo, cat_id, out=None):
    out = out or sys.stdout
    cat = repo.catalog.get(cat_id)
    if cat is None:
        if cat_id in repo.broken:
            raise Refusal(f"integrations/catalog/{cat_id}.json is unreadable: {repo.broken[cat_id]}")
        raise Refusal(f"unknown category {cat_id!r}; --list shows the catalog.")
    wired = repo.wired()["wired"].get(cat_id)
    print(f"{cat['id']}: {cat.get('title') or cat['id']}", file=out)
    if cat.get("for"):
        print(f"  for: {cat['for']}", file=out)
    print(f"  wired: {wired_label(wired)}", file=out)
    manual = cat.get("manual")
    if isinstance(manual, dict) and manual:
        print(f"  manual: {manual.get('export', '?')} -> {manual.get('drop', '?')}", file=out)
    if cat.get("bridges"):
        print("  bridges: " + ", ".join(cat["bridges"]), file=out)
    for vendor in cat.get("vendors", []):
        head = f"\n  {vendor.get('id')}  {vendor.get('name') or ''}".rstrip()
        print(f"{head}  [verified: {vendor.get('verified', '?')}, checked: {vendor.get('checked', '?')}, "
              f"writes: {'yes' if vendor.get('writes') else 'no'}]", file=out)
        if vendor.get("write_tools"):
            print("    write tools: " + ", ".join(vendor["write_tools"]), file=out)
        if vendor.get("read_only_switch"):
            s = vendor["read_only_switch"]
            print(f"    read-only switch: {s.get('kind')} {s.get('name')}={s.get('value')}", file=out)
        for route in mcp_routes(vendor):
            auth = route.get("auth") or {}
            env = ", ".join(auth.get("env") or []) or "none"
            flag = " (default)" if route.get("default") else ""
            print(f"    mcp {route.get('id')}{flag}: {route.get('transport')} -> {route.get('url') or route.get('command')}"
                  f"; auth {auth.get('model', '?')}; env {env}; headless {'yes' if route.get('headless') else 'no'}", file=out)
            if auth.get("where"):
                print(f"      where: {auth['where']}", file=out)
        routes = vendor.get("routes") or {}
        cli = routes.get("cli")
        if isinstance(cli, dict) and cli.get("tool"):
            print(f"    cli {cli['tool']}: {cli.get('install', '')} {cli.get('notes', '')}".rstrip(), file=out)
        script = routes.get("script")
        if isinstance(script, dict) and (script.get("path") or script.get("notes")):
            print(f"    script {script.get('path') or '(none yet)'}: {script.get('notes', '')}".rstrip(), file=out)
        if routes.get("manual"):
            print(f"    manual: {routes['manual']}", file=out)
        for caveat in vendor.get("caveats") or []:
            print(f"    caveat: {caveat}", file=out)
    return 0


def subset(repo, names, out=None):
    out = out or sys.stdout
    mcp = load_json(repo.mcp_path, {"mcpServers": {}}).get("mcpServers", {})
    wanted = [n.strip() for n in names.split(",") if n.strip()]
    missing = [n for n in wanted if n not in mcp]
    if missing:
        raise Refusal("not in .mcp.json: " + ", ".join(missing))
    print(dump_json({"mcpServers": {n: mcp[n] for n in wanted}}), end="", file=out)
    return 0


# ------------------------------------------------------------------ main --

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("vendor", nargs="?", metavar="VENDOR[:VARIANT]", help="catalog vendor to wire")
    ap.add_argument("--list", action="store_true", help="every category, its wired vendor, the alternatives")
    ap.add_argument("--category", metavar="ID", help="show one category; with a vendor, wire only this category")
    ap.add_argument("--unwire", metavar="VENDOR", help="remove a wired vendor")
    ap.add_argument("--subset", metavar="A,B", help="print .mcp.json filtered to these server names")
    ap.add_argument("--stdout", action="store_true", help="with --subset: print to stdout (the only output)")
    ap.add_argument("--dry-run", action="store_true", help="print the would-be edits, write nothing")
    ap.add_argument("--force", action="store_true", help="wire an unverified vendor; unwire past a stranded skill")
    ap.add_argument("--allow-writes", action="store_true",
                    help="skip the read-only switch and the deny rules (the human gate still applies)")
    ap.add_argument("--root", default=str(ROOT), help=argparse.SUPPRESS)
    args = ap.parse_args(argv)

    try:
        repo = Repo(args.root)
        if args.subset:
            return subset(repo, args.subset)
        if args.list:
            return list_categories(repo)
        if args.unwire:
            return unwire(repo, args.unwire, category=args.category, force=args.force, dry_run=args.dry_run)
        if args.vendor:
            return wire(repo, args.vendor, category=args.category, allow_writes=args.allow_writes,
                        force=args.force, dry_run=args.dry_run)
        if args.category:
            return show_category(repo, args.category)
    except Refusal as err:
        print(f"refused: {err}", file=sys.stderr)
        return 1
    except ValueError as err:
        print(f"error: a JSON file could not be parsed: {err}", file=sys.stderr)
        return 1
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
