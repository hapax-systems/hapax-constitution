"""NOTICE.md renderer.

Constitutional disclosure document that ships in every first-party repo
plus, gitignored via ``.git/info/exclude``, in the two upstream forks.
Body text is registry-driven and must not carry personal-owner, manifesto,
or stale launch-copy assumptions.
"""

from __future__ import annotations

from sdlc.render.repo_registry import RepoSpec, SurfaceClass, github_repo_url


def render(repo: RepoSpec) -> str:
    """Return NOTICE.md body for ``repo``."""
    license_summary = _license_summary(repo.license_class.value)
    return (
        f"# NOTICE - {repo.name}\n"
        "\n"
        f"{_opening(repo)}\n"
        "\n"
        "This repository is part of the Hapax Systems portfolio. Public "
        "metadata, issue affordances, and support boundaries follow the "
        "registry in `hapax-constitution`.\n"
        "\n"
        "## Reader promise\n"
        "\n"
        f"{repo.reader_promise.strip()}\n"
        "\n"
        "## Reader value\n"
        "\n"
        f"{repo.reader_value.strip()}\n"
        "\n"
        "## Claim ceiling\n"
        "\n"
        f"{repo.claim_ceiling.strip()}\n"
        "\n"
        "## License and rights\n"
        "\n"
        f"{repo.license_posture.strip()}\n"
        "\n"
        f"Rendered summary: {license_summary}\n"
        "\n"
        "## Public boundary\n"
        "\n"
        f"- {_issue_line(repo)}\n"
        "- First-party public links must use the `hapax-systems` GitHub "
        "organization.\n"
        "- Public fanout must route through the governed publication bus or a "
        "documented guarded legacy surface.\n"
        f"- Governance reference: {github_repo_url('hapax-constitution')}\n"
        "\n"
        "## Portfolio position\n"
        "\n"
        f"{repo.role_in_constellation.strip()}\n"
        "\n"
        "---\n"
        "\n"
        f"This file is rendered from `hapax-constitution/sdlc/render/`. "
        f"Do not edit by hand; edits will be overwritten on next render. "
        f"To change content, edit `sdlc/render/repos.yaml` or the renderer "
        f"templates in `hapax-constitution`.\n"
    )


def _license_summary(license_class: str) -> str:
    return {
        "PolyForm-Strict-1.0.0": (
            "PolyForm Strict 1.0.0 - source-available, non-distribution, non-modification."
        ),
        "BUSL-1.1": (
            "Business Source License 1.1 - source-available; not Open Source until "
            "the change license/date applies."
        ),
        "CC-BY-NC-ND-4.0": (
            "CC BY-NC-ND 4.0 - non-commercial, no derivatives. Specification text, not code."
        ),
        "CC0-1.0": "CC0 1.0 - public-domain dedication for the declared data/artifact surface.",
        "MIT": "MIT - permissive.",
        "Apache-2.0": "Apache 2.0 - permissive with patent grant.",
        "CC-BY-SA-4.0": (
            "CC BY-SA 4.0 (existing aesthetic-library asset blend; "
            "BSD-3-Clause for BitchX components preserved)."
        ),
        "upstream": (
            "Upstream license preserved (this is a fork). NOTICE.md is "
            "gitignored via `.git/info/exclude`."
        ),
    }.get(license_class, license_class)


def _opening(repo: RepoSpec) -> str:
    if repo.surface_class is SurfaceClass.ADOPTION_COMMONS:
        return (
            f"`{repo.name}` is the bounded adoption-commons repository in the "
            "Hapax Systems portfolio. It is published for inspection and "
            "pilot use without granting rights to the broader Hapax runtime "
            "estate."
        )
    if repo.surface_class is SurfaceClass.PRODUCT_FRONT_DOOR:
        return (
            f"`{repo.name}` is the product front door for the Hapax Systems "
            "portfolio. Public materials must stay within the shipped "
            "read and command-preview claim ceiling."
        )
    if repo.surface_class is SurfaceClass.RUNTIME_MECHANISM:
        return (
            f"`{repo.name}` is a source-available runtime mechanism in the "
            "Hapax Systems portfolio. It is not the full Hapax estate."
        )
    if repo.surface_class is SurfaceClass.GOVERNANCE_SPEC:
        return (
            f"`{repo.name}` is the governance-specification and publication "
            "metadata anchor for the Hapax Systems repository constellation."
        )
    if repo.surface_class is SurfaceClass.ECOSYSTEM_BRIDGE:
        return (
            f"`{repo.name}` is an integration bridge for Hapax Systems APIs and "
            "MCP clients. It is maintained for integration and inspection, "
            "not as a general-purpose MCP framework."
        )
    if repo.surface_class is SurfaceClass.ASSET_MIRROR:
        return (
            f"`{repo.name}` is a public asset mirror for the Hapax Systems "
            "portfolio. Per-asset notices and upstream licenses remain "
            "controlling."
        )
    if repo.surface_class is SurfaceClass.EVIDENCE_ARTIFACT:
        return (
            f"`{repo.name}` is an evidence-artifact repository in the Hapax "
            "Systems portfolio. It publishes bounded observations or "
            "metadata, not runtime code authority."
        )
    if repo.surface_class is SurfaceClass.INTERNAL_APPARATUS:
        return (
            f"`{repo.name}` is internal apparatus in the Hapax Systems "
            "portfolio. It is not a public product, hosted service, or "
            "community project unless a separate product boundary is ratified."
        )
    return (
        f"`{repo.name}` is a constituent of the Hapax operating environment. "
        "It is research or boundary infrastructure published as an artifact, "
        "not a staffed product or community project."
    )


def _issue_line(repo: RepoSpec) -> str:
    if repo.surface_class is SurfaceClass.ADOPTION_COMMONS:
        return (
            "Issues are redirect-only, support is bounded, and pull requests "
            "are not the intake path for this repository."
        )
    if repo.surface_class is SurfaceClass.PRODUCT_FRONT_DOOR:
        return (
            "Issues are redirect-only; support, commercial engagement, and "
            "roadmap commitments do not happen through GitHub."
        )
    return (
        "Issues are redirect-only; no discussions and no pull requests are accepted through GitHub."
    )
