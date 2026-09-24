"""Render the public organization profile from canonical repository metadata.

GitHub consumes ``hapax-systems/.github/profile/README.md``. Repository
descriptions stay in repos.yaml; license links point to each repository's
existing grant. Rendering does not publish or authorize publication.
"""

from __future__ import annotations

from sdlc.render.repo_registry import RepoSpec, RepoVisibility

ORG_PROFILE_PATH = "profile/README.md"

_LICENSE_LINKS = {
    "hapax-mcp": ("MIT", "LICENSE"),
    "reins": ("Business Source License 1.1", "LICENSE"),
    "hapax-spine": ("Business Source License 1.1", "LICENSE"),
    "hapax-council": ("PolyForm Strict 1.0.0", "LICENSE"),
    "hapax-constitution": ("Split by path: CC BY-NC-ND 4.0 / Apache-2.0", "LICENSE"),
    "hapax-research-ledger": ("CC0-1.0 for the declared data surface", "LICENSE"),
    "hapax-officium": ("PolyForm Strict 1.0.0", "LICENSE"),
    "hapax-phone": ("PolyForm Strict 1.0.0", "LICENSE"),
    "hapax-watch": ("PolyForm Strict 1.0.0", "LICENSE"),
    "hapax-assets": ("CC BY 4.0 default; per-asset notices take precedence", "LICENSE-SCOPE.md"),
}


_INTRO = """# Hapax Systems

Hapax Research Labs is the public research program of Hapax Systems, an
agent-staffed R&D laboratory. Our position on AI progress is a commitment to
**finding out, in public, with instruments.**

## Start here

"""

_BETWEEN_TABLES = """

For a concrete release artifact, inspect [hapax-spine v0.1.1](https://github.com/hapax-systems/hapax-spine/releases/tag/v0.1.1). The default branch may contain later changes; the release tag identifies that snapshot.

The license in each repository defines its terms. Source availability does not
establish support, general portability, or effectiveness in another setting.
The runtime and device repositories have their own deployment requirements.

## Supporting repositories

"""

_AFTER_TABLES = """

[agentgov](https://github.com/hapax-systems/agentgov) is an **archived historical
repository**. Its MIT-licensed source and published release remain available.
Its README records the successor research directions and their limits; it is
not the current adoption entry point.

See the [full public repository list](https://github.com/orgs/hapax-systems/repositories)
for current repository metadata. Follow each repository's stated support and
security boundaries.

## Research protocol

Position, test, score, implication: that loop is the work. The protocol commits
us to:

- State prospective empirical claims with a proposition, threshold, deadline
  and resolution method fixed before testing.
- Check sources and run experiments while preserving each result's setting
  and limits. Label retrospective source checks as retrospective.
- Publish outcomes under the registered rules, including misses, unresolved
  cases and corrections with the same prominence as hits.
- Record what each result changes about the next claim and the next action.

Every claim card should state its evidence and method; its scope; what was
checked, by whom and when; and how its conclusion relates to the evidence.
These are separate dimensions. A source check does not reproduce an experiment,
and a forecast probability is not an evidence grade.

This is a protocol, not a claim of an established prospective scoring record.
The numeric research ledger is not a prediction register. A public prospective
register and its scores are in preparation; they will be linked here when
published and verified. Original predictions and timestamped amendments should
remain inspectable, and late or omitted outcomes should be recorded and corrected.

Our public claims must remain within the evidence readers can inspect.

## Provenance and corrections

Repository and release status checked September 24, 2026. This page is generated from the [profile source](https://github.com/hapax-systems/hapax-constitution/blob/main/sdlc/render/org_profile_readme.py) and [repository descriptions](https://github.com/hapax-systems/hapax-constitution/blob/main/sdlc/render/repos.yaml). [Earlier revisions](https://github.com/hapax-systems/hapax-constitution/commits/main/sdlc/render/org_profile_readme.py) remain inspectable. Corrections should identify the affected source revision and remain attached to its history. See the [published intake boundary](https://github.com/hapax-systems/hapax-constitution/blob/main/SUPPORT.md) before reporting a problem; it does not accept general pull requests or GitHub support requests.
"""


def render(registry: dict[str, RepoSpec]) -> str:
    """Render the profile; missing or nonpublic required entries fail closed."""
    public = {
        repo.id: repo
        for repo in registry.values()
        if repo.is_first_party and repo.visibility is RepoVisibility.PUBLIC
    }
    public["agentgov"]  # The historical link also requires public first-party status.
    return (
        _INTRO
        + _table(
            public,
            (
                "hapax-mcp",
                "reins",
                "hapax-spine",
                "hapax-council",
                "hapax-constitution",
                "hapax-research-ledger",
            ),
            "What to inspect",
        )
        + _BETWEEN_TABLES
        + _table(public, ("hapax-officium", "hapax-phone", "hapax-watch", "hapax-assets"), "Role")
        + _AFTER_TABLES
    )


def _table(public: dict[str, RepoSpec], repo_ids: tuple[str, ...], role: str) -> str:
    rows = [f"| Repository | {role} | License |", "|---|---|---|"]
    for repo_id in repo_ids:
        repo = public[repo_id]
        label, path = _LICENSE_LINKS[repo_id]
        rows.append(
            f"| [{repo.name}]({repo.github_url}) | {_compact(repo.reader_promise)} | "
            f"[{label}]({repo.github_url}/blob/main/{path}) |"
        )
    return "\n".join(rows)


def _compact(value: str) -> str:
    """Keep registry descriptions within one Markdown table cell."""
    return " ".join(value.strip().replace("|", "/").split())


__all__ = ["ORG_PROFILE_PATH", "render"]
