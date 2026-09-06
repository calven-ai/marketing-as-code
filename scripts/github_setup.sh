#!/usr/bin/env sh
# Apply the GitHub repository settings this repo's lifecycle assumes
# (docs/github-settings.md). Idempotent: run it again any time. Needs the gh
# CLI logged in as someone who administers the repository.
#
#   sh scripts/github_setup.sh            # apply to the repo this checkout tracks
#   sh scripts/github_setup.sh --dry-run  # print what it would do
#
# What it sets: proposals land as one squashed commit, their branches are
# deleted on merge, auto-merge is allowed (bookkeeping proposals use it), the
# three labels exist, the workflow token is read-only by default (a job that
# asks may open a proposal; the gate never counts a bot's approval), the bot
# keys have an environment only main may use, and a ruleset named "main"
# requires a pull request with the "doctor" and "review-gate" checks green
# before anything reaches the approved copy; an admin may bypass the checks,
# but only through a pull request, never with a direct push. The repository
# is private by rule (AGENTS.md); GitHub enforces the ruleset on a private
# repository under Pro or Team, and on Free it is created but not enforced.
# The script says which case it found.

set -eu

dry=""
[ "${1:-}" = "--dry-run" ] && dry="echo [dry-run]"

repo="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
echo "repository: $repo"

echo "1. merge settings: squash only, delete branch on merge, allow auto-merge, allow update branch"
$dry gh repo edit "$repo" \
  --enable-squash-merge \
  --enable-merge-commit=false \
  --enable-rebase-merge=false \
  --delete-branch-on-merge \
  --enable-auto-merge \
  --allow-update-branch

echo "2. labels"
for label in "bookkeeping:0E8A16:Only agent-maintained files; approves itself when the checks are green" \
             "needs-review:D93F0B:A person reads the diff and approves before it lands" \
             "stale:EDEDED:No activity for two weeks; closes in a week unless someone comments"; do
  name="${label%%:*}"; rest="${label#*:}"; color="${rest%%:*}"; desc="${rest#*:}"
  $dry gh label create "$name" --color "$color" --description "$desc" --force >/dev/null 2>&1 || true
  echo "   $name"
done

echo "3. workflow token: read-only by default; a job that asks may open a proposal (the gate counts no bot approval)"
# One GitHub toggle covers both creating and approving pull requests with the
# workflow token. housekeeping.yml, transcripts-cron.yml and the agent runs
# open their proposals with it, so it stays on; scripts/review_gate.py ignores
# approvals from any *[bot] login, so the approving half buys nothing.
$dry gh api -X PUT "repos/$repo/actions/permissions/workflow" \
  -f default_workflow_permissions=read -F can_approve_pull_request_reviews=true >/dev/null

echo "4. environment 'automation': the bot keys live here, and only main may use it"
$dry gh api -X PUT "repos/$repo/environments/automation" --input - <<EOF >/dev/null
{"deployment_branch_policy": {"protected_branches": false, "custom_branch_policies": true}}
EOF
if ! $dry gh api -X POST "repos/$repo/environments/automation/deployment-branch-policies" \
     -f name=main -f type=branch >/dev/null 2>&1; then
  echo "   (branch policy already present, or not available on this plan; docs/github-settings.md)"
fi

echo "5. ruleset 'main': pull request required, code-owner review, squash only, checks doctor + review-gate, no deletion, no force-push"
existing="$(gh api "repos/$repo/rulesets" -q '.[] | select(.name=="main") | .id' 2>/dev/null || true)"
body='{
  "name": "main",
  "target": "branch",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
  "bypass_actors": [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "pull_request"}],
  "rules": [
    {"type": "deletion"},
    {"type": "non_fast_forward"},
    {"type": "pull_request", "parameters": {
      "required_approving_review_count": 0,
      "dismiss_stale_reviews_on_push": false,
      "require_code_owner_review": true,
      "require_last_push_approval": false,
      "required_review_thread_resolution": false,
      "allowed_merge_methods": ["squash"]}},
    {"type": "required_status_checks", "parameters": {
      "strict_required_status_checks_policy": false,
      "required_status_checks": [{"context": "doctor"}, {"context": "review-gate"}]}}
  ]
}'
if [ -n "$existing" ]; then
  $dry gh api -X PUT "repos/$repo/rulesets/$existing" --input - <<EOF >/dev/null
$body
EOF
  echo "   updated ruleset $existing"
else
  $dry gh api -X POST "repos/$repo/rulesets" --input - <<EOF >/dev/null
$body
EOF
  echo "   created"
fi

echo
echo "Could not verify from here (check Settings -> Rules -> Rulesets in the browser):"
private="$(gh repo view "$repo" --json isPrivate -q .isPrivate)"
if [ "$private" = "true" ]; then
  echo "  - This repository is private. The ruleset is enforced on GitHub Pro (personal) or Team (organization);"
  echo "    on GitHub Free it shows 'not enforced' and nothing stops a direct push. Free is not supported;"
  echo "    python3 scripts/doctor.py --github says which plan this is. docs/github-settings.md."
else
  echo "  - This repository is PUBLIC. It must be private (AGENTS.md, rule 8): Settings -> General ->"
  echo "    Danger zone -> Change visibility. Add no transcripts or account lists until it is."
fi
echo "  - The bot keys for the optional automations (ANTHROPIC_API_KEY, GRANOLA_API_KEY, SLACK_BOT_TOKEN, and"
echo "    DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD for the monthly brand-monitor run) go in"
echo "    Settings -> Environments -> automation -> Environment secrets, never in repository secrets; docs/secrets.md."
echo "  - Secret scanning and push protection: Settings -> Advanced Security (the GitHub Secret Protection"
echo "    add-on on the Team plan); docs/github-settings.md."
echo "  - .github/CODEOWNERS names who is asked to review; replace the placeholder with real GitHub handles."
echo "  - Each clone turns on the pre-push hook once: git config core.hooksPath scripts/hooks"
echo "done; python3 scripts/doctor.py --github re-checks these settings any time."
