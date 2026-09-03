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
# three labels exist, the workflow token is read-only by default, the bot keys
# have an environment only main may use, and a ruleset named "main" requires a pull request with
# the "doctor" and "review-gate" checks green before anything reaches the
# approved copy. Rulesets are enforced on public repositories and on private
# ones under GitHub Pro or Team; on GitHub Free private repositories they are
# created but not enforced, and the script says so.

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

echo "3. workflow token: read-only by default, and Actions may not approve pull requests"
$dry gh api -X PUT "repos/$repo/actions/permissions/workflow" \
  -f default_workflow_permissions=read -F can_approve_pull_request_reviews=false >/dev/null

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
  "bypass_actors": [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}],
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
  echo "  - This repository is private. The ruleset is enforced only on GitHub Pro (personal) or Team (organization)."
  echo "    On GitHub Free it shows 'not enforced': the scripts and hooks still guard the local path, CI still"
  echo "    reports, but nothing stops a direct push. docs/github-settings.md lays out the trade-off."
else
  echo "  - Public repository: rulesets are enforced on every plan."
fi
echo "  - The bot keys for the optional automations (ANTHROPIC_API_KEY, GRANOLA_API_KEY, SLACK_BOT_TOKEN) go in"
echo "    Settings -> Environments -> automation -> Environment secrets, never in repository secrets; docs/secrets.md."
echo "  - Secret scanning and push protection: Settings -> Advanced Security (free on public repositories;"
echo "    private ones need the GitHub Secret Protection add-on on the Team plan); docs/github-settings.md."
echo "  - .github/CODEOWNERS names who is asked to review; replace the placeholder with real GitHub handles."
echo "  - Each clone turns on the pre-push hook once: git config core.hooksPath scripts/hooks"
echo "done; python3 scripts/doctor.py --github re-checks these settings any time."
