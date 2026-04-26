"""Repo settings enforcer — refusal-shaped UI affordances on GitHub.

The single-operator + full-automation-or-no-engagement axiom set makes
GitHub's default UI affordances structurally inappropriate. Every
first-party repo must carry the same Settings policy:

  has_wiki        = false   (except hapax-constitution: true for axiom registry)
  has_projects    = false   (kanban surface assumes multi-contributor sync)
  has_discussions = false   (single-operator: no community to discuss)
  has_issues      = true    (kept open as REDIRECT surface; see ISSUE_TEMPLATE/config.yml)

Per drop 3 §3 of the publication-bus refusal-shaped-affordance stance:
empty FUNDING.yml does NOT hide Sponsorships — the UI feature must be
disabled in repo Settings.

The shell mirror at hapax-council ``scripts/repo-presentation-enforce.sh``
is the operator-immediate surface; this module is the daemon-side
surface for SDLC pipeline / cron integration. Both apply the same
policy to the same repos.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass

from sdlc.render.repo_registry import RepoSpec, load_registry

# Repos that keep ``has_wiki = true`` (the wiki is repurposed, not retired).
# Only hapax-constitution, where the wiki carries the axiom registry.
WIKI_REPURPOSED: frozenset[str] = frozenset({"hapax-constitution"})


@dataclass(frozen=True)
class RepoSettings:
    """Subset of GitHub repo settings the policy governs."""

    has_wiki: bool
    has_projects: bool
    has_discussions: bool


def desired_settings(repo: RepoSpec) -> RepoSettings:
    """Policy-mandated settings for a repo, derived from its registry entry."""
    return RepoSettings(
        has_wiki=repo.name in WIKI_REPURPOSED,
        has_projects=False,
        has_discussions=False,
    )


def current_settings(owner: str, repo_name: str) -> RepoSettings:
    """Read live settings from GitHub via the ``gh`` CLI."""
    result = subprocess.run(
        ["gh", "api", f"repos/{owner}/{repo_name}"],
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )
    data = json.loads(result.stdout)
    return RepoSettings(
        has_wiki=bool(data.get("has_wiki")),
        has_projects=bool(data.get("has_projects")),
        has_discussions=bool(data.get("has_discussions")),
    )


def apply_settings(
    owner: str, repo_name: str, desired: RepoSettings, *, dry_run: bool = False
) -> None:
    """PATCH GitHub repo settings via ``gh api``. No-op when ``dry_run=True``."""
    if dry_run:
        return
    subprocess.run(
        [
            "gh",
            "api",
            "-X",
            "PATCH",
            f"repos/{owner}/{repo_name}",
            "-F",
            f"has_wiki={'true' if desired.has_wiki else 'false'}",
            "-F",
            f"has_projects={'true' if desired.has_projects else 'false'}",
            "-F",
            f"has_discussions={'true' if desired.has_discussions else 'false'}",
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )


def first_party_repos() -> list[RepoSpec]:
    """Repos this enforcer governs — first-party only, upstream forks excluded."""
    return [r for r in load_registry().values() if r.is_first_party]


@dataclass(frozen=True)
class DriftReport:
    """Per-repo drift between desired and observed settings."""

    repo_name: str
    desired: RepoSettings
    observed: RepoSettings

    @property
    def has_drift(self) -> bool:
        return self.desired != self.observed


def detect_drift(owner: str, repos: list[RepoSpec] | None = None) -> list[DriftReport]:
    """Compare desired vs observed for every first-party repo (or the supplied list)."""
    repos = repos if repos is not None else first_party_repos()
    return [
        DriftReport(
            repo_name=r.name,
            desired=desired_settings(r),
            observed=current_settings(owner, r.name),
        )
        for r in repos
    ]


__all__ = [
    "DriftReport",
    "RepoSettings",
    "WIKI_REPURPOSED",
    "apply_settings",
    "current_settings",
    "desired_settings",
    "detect_drift",
    "first_party_repos",
]
