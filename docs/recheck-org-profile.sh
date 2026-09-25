#!/usr/bin/env bash
# Read-only observations; run from the hapax-constitution repository root.
set -euo pipefail

date -u '+Observed at: %Y-%m-%dT%H:%M:%SZ'
git rev-parse HEAD
git status --short
sha256sum sdlc/render/org_profile_readme.py sdlc/render/repos.yaml \
  tests/fixtures/org-profile-README.md
rg -o 'Repository and release status checked [^.]+\.' \
  tests/fixtures/org-profile-README.md

gh api --paginate 'orgs/hapax-systems/repos?type=public&per_page=100' \
  --jq '[.[] | {full_name, html_url, visibility, archived, default_branch}]'
gh api repos/hapax-systems/hapax-spine/releases/tags/v0.1.1 \
  --jq '{html_url, tag_name, target_commitish, draft, prerelease, published_at}'
gh api repos/hapax-systems/hapax-spine/releases/latest \
  --jq '{html_url, tag_name, target_commitish, draft, prerelease, published_at}'
gh api repos/hapax-systems/agentgov \
  --jq '{full_name, html_url, visibility, archived, default_branch, license}'
gh api repos/hapax-systems/agentgov/releases/latest \
  --jq '{html_url, tag_name, target_commitish, draft, prerelease, published_at}'

agentgov_head=$(gh api repos/hapax-systems/agentgov/commits/main --jq .sha)
printf 'agentgov source commit: %s\n' "$agentgov_head"
gh api "repos/hapax-systems/agentgov/license?ref=$agentgov_head" \
  --jq '{html_url, path, sha, license}'
gh api -H 'Accept: application/vnd.github.raw+json' \
  "repos/hapax-systems/agentgov/contents/LICENSE?ref=$agentgov_head"
