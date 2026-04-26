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


class RepoNotBootstrapped(RuntimeError):
    """Raised when a registry-declared repo doesn't exist on GitHub yet.

    Some registry entries (e.g. ``hapax-assets`` pre-CDN-bootstrap) point
    at repos the operator hasn't created yet. The drift-checker should
    skip and warn, not fail.
    """


def current_settings(owner: str, repo_name: str) -> RepoSettings:
    """Read live settings from GitHub via the ``gh`` CLI.

    Raises :class:`RepoNotBootstrapped` on 404 so callers can skip-and-
    warn for registry-declared repos the operator hasn't created yet.
    """
    result = subprocess.run(
        ["gh", "api", f"repos/{owner}/{repo_name}"],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if result.returncode != 0:
        if "HTTP 404" in result.stderr or "Not Found" in result.stderr:
            raise RepoNotBootstrapped(f"{owner}/{repo_name} does not exist on GitHub")
        raise subprocess.CalledProcessError(
            result.returncode, result.args, output=result.stdout, stderr=result.stderr
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


def detect_drift(
    owner: str, repos: list[RepoSpec] | None = None
) -> tuple[list[DriftReport], list[str]]:
    """Compare desired vs observed for every first-party repo.

    Returns ``(reports, skipped)`` where ``skipped`` lists repo names
    that don't yet exist on GitHub (registry-declared but not
    bootstrapped). The drift-check workflow surfaces these as warnings.
    """
    repos = repos if repos is not None else first_party_repos()
    reports: list[DriftReport] = []
    skipped: list[str] = []
    for r in repos:
        try:
            observed = current_settings(owner, r.name)
        except RepoNotBootstrapped:
            skipped.append(r.name)
            continue
        reports.append(
            DriftReport(
                repo_name=r.name, desired=desired_settings(r), observed=observed
            )
        )
    return reports, skipped


def main(argv: list[str] | None = None) -> int:
    """CLI entry. ``--check`` reports drift (exit 1 on drift detected);
    ``--enforce`` applies the policy."""
    import argparse

    parser = argparse.ArgumentParser(prog="sdlc.render.repo_settings")
    parser.add_argument("--owner", default="ryanklee", help="GitHub owner")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Detect drift; exit 1 on drift")
    mode.add_argument("--enforce", action="store_true", help="Apply policy where drift exists")
    args = parser.parse_args(argv)

    reports, skipped = detect_drift(args.owner)
    drifted = [r for r in reports if r.has_drift]

    for r in reports:
        marker = "DRIFT" if r.has_drift else "ok   "
        print(
            f"{marker} {args.owner}/{r.repo_name:25s} "
            f"wiki={r.observed.has_wiki!s:5s} (want {r.desired.has_wiki!s}) "
            f"projects={r.observed.has_projects!s:5s} (want {r.desired.has_projects!s}) "
            f"discussions={r.observed.has_discussions!s:5s} (want {r.desired.has_discussions!s})"
        )
    for name in skipped:
        print(f"SKIP  {args.owner}/{name:25s} (not yet bootstrapped on GitHub)")

    if not drifted:
        return 0

    if args.check:
        print(f"\n{len(drifted)} repo(s) drifted; run with --enforce to correct", flush=True)
        return 1

    for r in drifted:
        apply_settings(args.owner, r.repo_name, r.desired)
        print(f"patched {args.owner}/{r.repo_name}")
    return 0


__all__ = [
    "DriftReport",
    "RepoNotBootstrapped",
    "RepoSettings",
    "WIKI_REPURPOSED",
    "apply_settings",
    "current_settings",
    "desired_settings",
    "detect_drift",
    "first_party_repos",
    "main",
]


if __name__ == "__main__":
    raise SystemExit(main())
