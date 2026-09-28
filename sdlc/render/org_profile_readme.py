"""Render the public organization profile from canonical repository metadata.

GitHub consumes ``hapax-systems/.github/profile/README.md``. Repository
descriptions stay in repos.yaml; license links point to each repository's
existing grant. Rendering does not publish or authorize publication.
"""

from __future__ import annotations

import re
from calendar import month_name
from datetime import date

from sdlc.render.repo_registry import DEFAULT_GITHUB_OWNER, LicenseClass, RepoSpec, RepoVisibility

ORG_PROFILE_PATH = "profile/README.md"

# Each entry binds reviewed registry metadata to an independently inspected grant
# summary, not a grant inferred from license_class. Pinned source excerpts and
# hashes live in tests/fixtures/org-profile-grant-evidence.json. Unexpected
# metadata changes require reconciliation before rendering; grant freshness is
# still a separate publication check. Keep the assets discrepancy and constitution
# split explicit until their respective authorities approve a change.
_LICENSE_LINKS = {
    "hapax-mcp": (LicenseClass.MIT, "MIT", "LICENSE"),
    "reins": (LicenseClass.BUSL_1_1, "Business Source License 1.1", "LICENSE"),
    "hapax-spine": (LicenseClass.BUSL_1_1, "Business Source License 1.1", "LICENSE"),
    "hapax-council": (LicenseClass.POLYFORM_STRICT_1_0_0, "PolyForm Strict 1.0.0", "LICENSE"),
    # Metadata names the specification bucket; tooling has a separate grant.
    "hapax-constitution": (
        LicenseClass.CC_BY_NC_ND_4_0,
        "Split by path: CC BY-NC-ND 4.0 / Apache-2.0",
        "LICENSE",
    ),
    "hapax-research-ledger": (
        LicenseClass.CC0_1_0,
        "CC0-1.0 for the declared data surface",
        "LICENSE",
    ),
    "hapax-officium": (LicenseClass.POLYFORM_STRICT_1_0_0, "PolyForm Strict 1.0.0", "LICENSE"),
    "hapax-phone": (LicenseClass.POLYFORM_STRICT_1_0_0, "PolyForm Strict 1.0.0", "LICENSE"),
    "hapax-watch": (LicenseClass.POLYFORM_STRICT_1_0_0, "PolyForm Strict 1.0.0", "LICENSE"),
    # Known metadata/grant discrepancy: registry SA; grant BY with exceptions.
    "hapax-assets": (
        LicenseClass.CC_BY_SA_4_0,
        "CC BY 4.0 default; per-asset notices take precedence",
        "LICENSE-SCOPE.md",
    ),
    "agentgov": (LicenseClass.MIT, "MIT", "LICENSE"),
}

_START_REPOS = (
    "hapax-mcp",
    "reins",
    "hapax-spine",
    "hapax-council",
    "hapax-constitution",
    "hapax-research-ledger",
)
_SUPPORTING_REPOS = ("hapax-officium", "hapax-phone", "hapax-watch", "hapax-assets")

# Reviewed public summaries, grounded in each linked repository README. These
# describe the artifact; they do not change the registry's other consumers.
_PROFILE_SUMMARIES = {
    "hapax-mcp": "MCP bridge that presents the council and officium HTTP APIs as bounded tools for compatible MCP clients",
    "reins": "Terminal cockpit for inspecting agent work and delivery state",
    "hapax-spine": "Runtime package for events, routing, receipts, quotas and projections",
    "hapax-council": "Source for the agent-work coordination and review environment",
    "hapax-constitution": "Governance specification and repository presentation tooling",
    "hapax-research-ledger": "Numeric observations with caveats and validation metadata",
    "hapax-officium": "Internal management decision support, published for inspection; not HR software and not offered as a service",
    "hapax-phone": "Android source documenting phone context signals and privacy boundaries; not a health claim",
    "hapax-watch": "Wear OS source documenting biometric and context signals and privacy boundaries; not a health claim",
    "hapax-assets": "Mirror of approved public assets with provenance and per-asset notices",
}

_PROFILE_USE = {
    "hapax-mcp": "Use under MIT; see its README for requirements",
    "reins": "Inspect; production use limited by BSL 1.1; see its README for requirements",
    "hapax-spine": "Inspect; production use limited by BSL 1.1; see its README for requirements",
    "hapax-council": "Inspect only under PolyForm Strict; see its README for requirements",
    "hapax-constitution": "Specification: CC BY-NC-ND; tooling: Apache-2.0",
    "hapax-research-ledger": "Data: CC0",
    "hapax-officium": "Inspect only under PolyForm Strict; see its README for requirements",
    "hapax-phone": "Inspect only under PolyForm Strict; see its README for requirements",
    "hapax-watch": "Inspect only under PolyForm Strict; see its README for requirements",
    "hapax-assets": "Use subject to the grant and each asset's notice",
}


_INTRO = """# Hapax Research Lab

Hapax Research Lab is an R&D laboratory whose research and engineering staff are AI agents. Its public code, specifications and records are published here, under the GitHub organization handle `hapax-systems`.

Byline: `hrl-han`. Legal entity (as filed): Hapax Research LLC, organized in Wyoming on 2026-05-10, filing ID 2026-001973400.

## Start here

"""

_BETWEEN_TABLES = """

For a concrete release artifact, inspect [hapax-spine v0.1.1](https://github.com/hapax-systems/hapax-spine/releases/tag/v0.1.1). The default branch may contain later changes; the release tag identifies that snapshot.

The license in each repository defines its terms. Source availability does not
establish support, general portability, or effectiveness in another setting.
No repository here is offered as a supported product or hosted service. For deployment requirements, see the READMEs for [reins](https://github.com/hapax-systems/reins), [hapax-spine](https://github.com/hapax-systems/hapax-spine), [hapax-council](https://github.com/hapax-systems/hapax-council), [hapax-phone](https://github.com/hapax-systems/hapax-phone) and [hapax-watch](https://github.com/hapax-systems/hapax-watch).

## Supporting repositories

"""

_AFTER_TABLES = """

[agentgov](https://github.com/hapax-systems/agentgov) was retired on 24 September 2026 at v0.3.1. Its MIT-licensed source and published release remain available. Its README explains the retirement and says it is not a current recommendation to deploy.

The tables list the main repositories; the [full list](https://github.com/orgs/hapax-systems/repositories) is on the organization page. Follow each repository's stated support and security boundaries.

## Provenance and corrections

This page is generated from the [profile source](https://github.com/hapax-systems/hapax-constitution/blob/main/sdlc/render/org_profile_readme.py) and [repository descriptions](https://github.com/hapax-systems/hapax-constitution/blob/main/sdlc/render/repos.yaml). [Earlier revisions](https://github.com/hapax-systems/hapax-constitution/commits/main/sdlc/render/org_profile_readme.py) remain inspectable. Corrections should identify the affected source revision and remain attached to its history. See the [published intake boundary](https://github.com/hapax-systems/hapax-constitution/blob/main/SUPPORT.md) before reporting a problem; it does not accept general pull requests or GitHub support requests.
"""


def provenance_line(*, source_commit: str, generated_on: str) -> str:
    """Format a caller-supplied source revision and generation date."""
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("source_commit must be 40 lowercase hexadecimal characters")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", generated_on):
        raise ValueError("generated_on must be an ISO calendar date (YYYY-MM-DD)")
    day = date.fromisoformat(generated_on)
    return (
        f"Generated on {month_name[day.month]} {day.day}, {day.year} "
        f"from hapax-constitution source commit {source_commit}."
    )


def render(registry: dict[str, RepoSpec], *, source_commit: str, generated_on: str) -> str:
    """Render only required entries with approved public first-party ownership."""
    provenance = provenance_line(source_commit=source_commit, generated_on=generated_on)
    # Validate the historical link as well as both tables before emitting copy.
    problems = []
    for repo_id in (*_START_REPOS, *_SUPPORTING_REPOS, "agentgov"):
        repo = registry.get(repo_id)
        if repo is None:
            problems.append(f"{repo_id}: missing")
        elif not repo.is_first_party:
            problems.append(f"{repo_id}: not first-party")
        elif repo.visibility is not RepoVisibility.PUBLIC:
            problems.append(f"{repo_id}: visibility={repo.visibility.value}")
        elif repo.github_owner != DEFAULT_GITHUB_OWNER:
            problems.append(
                f"{repo_id}: github_owner={repo.github_owner}; expected {DEFAULT_GITHUB_OWNER}"
            )
    if problems:
        raise ValueError(
            "Cannot render organization profile: " + "; ".join(problems) + ". "
            "Verify the approved public first-party inventory and reconcile "
            "sdlc/render/repos.yaml with the profile's required entries before rerendering; "
            "visibility or ownership changes require separate authority."
        )
    license_problems = []
    for repo_id, (expected, _label, _path) in _LICENSE_LINKS.items():
        actual = registry[repo_id].license_class
        if actual is not expected:
            license_problems.append(
                f"{repo_id}: license_class={actual.value}; reviewed metadata={expected.value}"
            )
    if license_problems:
        raise ValueError(
            "Cannot render organization profile: " + "; ".join(license_problems) + ". "
            "Inspect the repository grant and pinned grant evidence, then reconcile "
            "sdlc/render/repos.yaml and sdlc/render/org_profile_readme.py before rerendering. "
            "Registry metadata is not a legal grant; preserve known split-path and per-asset "
            "exceptions. Grant or legal metadata changes require separate authority."
        )
    public = {
        repo.id: repo
        for repo in registry.values()
        if repo.is_first_party and repo.visibility is RepoVisibility.PUBLIC
    }
    return (
        _INTRO
        + _table(public, _START_REPOS, "What to inspect")
        + _BETWEEN_TABLES
        + _table(public, _SUPPORTING_REPOS, "Role")
        + _AFTER_TABLES
        + "\n"
        + provenance
        + "\n"
    )


def _table(public: dict[str, RepoSpec], repo_ids: tuple[str, ...], role: str) -> str:
    rows = [f"| Repository | {role} | Use | License |", "|---|---|---|---|"]
    for repo_id in repo_ids:
        repo = public[repo_id]
        _expected_class, label, path = _LICENSE_LINKS[repo_id]
        rows.append(
            f"| [{repo.name}]({repo.github_url}) | {_compact(_PROFILE_SUMMARIES[repo_id])} | {_PROFILE_USE[repo_id]} | "
            f"[{label}]({repo.github_url}/blob/main/{path}) |"
        )
    return "\n".join(rows)


def _compact(value: str) -> str:
    """Keep registry descriptions within one Markdown table cell."""
    return " ".join(value.strip().replace("|", "/").split())


__all__ = ["ORG_PROFILE_PATH", "render"]
