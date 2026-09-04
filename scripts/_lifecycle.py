"""Shared pieces of the marketer's lifecycle (scripts/sync.py and scripts/propose.py):
where a checkout stands, its proposals on GitHub in plain words, and the outcome a
proposal will have. Standard library only; git and gh through scripts/_common.py.

    from _lifecycle import Checkout, describe, outcome
    co = Checkout(root)               # co.branch(), co.base, co.repo, co.dirty()
    describe(pr, self_merge=True)     # "ready for you to merge"
    outcome("bookkeeping", True, [], url)

Every string these functions return is read by a person who never opens a
terminal: a proposal, the approved copy, the check, the gate. Never a git word.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint  # noqa: E402
import review_gate  # noqa: E402
from _common import default_branch, gh, gh_ready, git, origin_repo, run  # noqa: E402

NOT_CONNECTED = ("This folder is not connected to GitHub yet. Create your copy from the template "
                 "and clone it with GitHub Desktop (docs/new-to-github.md).")
OFFLINE = "Could not reach GitHub. Check your connection and try again."
NO_GH = "Install the GitHub CLI to see your proposals here (docs/troubleshooting.md)."
PR_FIELDS = "number,title,url,labels,statusCheckRollup,reviewDecision,headRefName,isDraft"


class Checkout:
    """One clone: the folder, its branch, the approved copy's name, its repository on GitHub."""

    def __init__(self, root=None):
        self.root = Path(root or lint.ROOT).resolve()

    def git(self, *args, check=True):
        return git(*args, cwd=self.root, check=check)

    def run(self, *args):
        return run(["git", *args], cwd=self.root, check=False)

    @property
    def connected(self):
        return (self.root / ".git").exists() and bool(self.repo)

    @property
    def repo(self):
        return origin_repo(self.root) if (self.root / ".git").exists() else None

    @property
    def base(self):
        return default_branch(self.root)

    def branch(self):
        """The current branch name, or "" when between branches."""
        return self.run("branch", "--show-current").stdout.strip()

    def dirty(self, paths=()):
        """Paths with unsaved edits (modified, added, deleted, untracked)."""
        proc = self.run("status", "--porcelain", "--untracked-files=all", "--", *paths)
        return [line[3:].split(" -> ")[-1] for line in proc.stdout.splitlines() if line.strip()]

    def has_ref(self, ref):
        return self.run("rev-parse", "--verify", "-q", ref).returncode == 0

    def count(self, spec):
        """Commits in SPEC (for example origin/main..HEAD); 0 when a side is missing."""
        proc = self.run("rev-list", "--count", spec)
        return int(proc.stdout.strip() or 0) if proc.returncode == 0 else 0

    def merging(self):
        return (self.root / ".git" / "MERGE_HEAD").exists()

    def conflicted(self):
        return [p for p in self.run("diff", "--name-only", "--diff-filter=U").stdout.splitlines() if p]

    def identity(self):
        name = self.run("config", "user.name").stdout.strip()
        email = self.run("config", "user.email").stdout.strip()
        return name, email

    def schema(self):
        path = self.root / "docs" / "schema.json"
        if not path.is_file():
            path = lint.SCHEMA_PATH
        return json.loads(path.read_text(encoding="utf-8"))

    def ctx(self):
        return lint.Ctx(root=self.root, schema=self.schema())


# ------------------------------------------------------------ proposals --

def proposals(co, *args, fields=PR_FIELDS):
    """Open proposals from GitHub, or None when gh is missing or logged out."""
    if not co.repo or not gh_ready(co.root):
        return None
    out = gh("pr", "list", "-R", co.repo, "--state", "open", "--json", fields, *args, cwd=co.root, check=False)
    try:
        return json.loads(out or "[]")
    except json.JSONDecodeError:
        return []


def proposal_for(co, branch, state="open"):
    """The proposal for BRANCH in STATE (open, merged, closed), or None."""
    if not branch or not co.repo or not gh_ready(co.root):
        return None
    out = gh("pr", "list", "-R", co.repo, "--head", branch, "--state", state, "--json", PR_FIELDS,
             cwd=co.root, check=False)
    try:
        found = json.loads(out or "[]")
    except json.JSONDecodeError:
        found = []
    return found[0] if found else None


def _conclusion(check):
    return str(check.get("conclusion") or check.get("state") or "").upper()


def _name(check):
    return str(check.get("name") or check.get("context") or "")


def describe(pr, self_merge):
    """One phrase for where a proposal stands: checking, problems, merges itself, ready, waiting."""
    checks = pr.get("statusCheckRollup") or []
    failed = [c for c in checks if _conclusion(c) in ("FAILURE", "ERROR", "TIMED_OUT", "CANCELLED", "STARTUP_FAILURE")
              and _name(c) != review_gate.CHECK]
    pending = [c for c in checks if _conclusion(c) in ("", "PENDING", "IN_PROGRESS", "QUEUED", "EXPECTED", "WAITING")]
    gate = next((c for c in checks if _name(c) == review_gate.CHECK), None)
    labels = [str(lab.get("name", lab)) for lab in pr.get("labels") or []]
    if failed:
        return "problems: see the health check comment on the proposal"
    if pending:
        return "checking"
    if "bookkeeping" in labels:
        return "bookkeeping, merges itself once the check is green"
    approved = str(pr.get("reviewDecision") or "").upper() == "APPROVED"
    if approved or self_merge or (gate and _conclusion(gate) == "SUCCESS"):
        return "ready for you to merge"
    if gate and _conclusion(gate) == "ACTION_REQUIRED":
        return "waiting for a teammate to read it"
    return "waiting"


def outcome(kind, self_merge, owners, url):
    """What happens to a proposal next, in one sentence."""
    if kind == "bookkeeping":
        return "This is bookkeeping: once the check is green it merges itself."
    if self_merge:
        return f"This needs review. You are the reviewer: read the diff at {url}, then click Merge."
    who = ", ".join(owners) if owners else "a teammate"
    return f"This needs review from {who}. Link: {url}."
