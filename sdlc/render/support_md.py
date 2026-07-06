"""SUPPORT.md renderer.

The public support surface is a boundary file, not a service promise. It keeps
GitHub's reader-facing affordances coherent with the registry-defined repo
posture: issues may exist as a redirect surface, but support is not staffed.
"""

from __future__ import annotations

from sdlc.render.repo_registry import RepoSpec, SurfaceClass, github_repo_url


def render(repo: RepoSpec) -> str:
    """Return the support-boundary document for ``repo``."""
    return (
        "# Support\n"
        "\n"
        f"{_opening(repo)}\n"
        "\n"
        "## GitHub issues\n"
        "\n"
        "GitHub Issues are kept available only as a redirect surface. Blank "
        "issues are disabled; the issue chooser points readers to the "
        "appropriate published files instead of opening a support queue.\n"
        "\n"
        "## What is in scope\n"
        "\n"
        "- Reading the repository and its rendered metadata.\n"
        "- Citing the repository through `CITATION.cff` and `.zenodo.json`.\n"
        "- Reporting a concrete security disclosure through `SECURITY.md`.\n"
        "- Following the governance boundary through `GOVERNANCE.md` and "
        f"{github_repo_url('hapax-constitution')}.\n"
        "\n"
        "## What is out of scope\n"
        "\n"
        "- Troubleshooting, integration help, feature requests, roadmap requests, "
        "or consulting through GitHub Issues.\n"
        "- Pull requests, community maintenance, or contributor onboarding.\n"
        "- Claims that a funding link, citation, fork, or public issue creates "
        "support, feature priority, commercial rights, or license expansion.\n"
        "\n"
        "## Funding\n"
        "\n"
        "Funding links, if present, are no-perk research support only. Payment "
        "does not create an SLA, support entitlement, product commitment, "
        "license grant, or consulting relationship.\n"
        "\n"
        "---\n"
        "\n"
        "This file is rendered from `hapax-constitution/sdlc/render/`. "
        "Edits are overwritten on next render.\n"
    )


def _opening(repo: RepoSpec) -> str:
    if repo.surface_class is SurfaceClass.ADOPTION_COMMONS:
        return (
            f"`{repo.name}` is the bounded adoption surface for Hapax Systems. "
            "It is published to make the adopter-facing governance primitives "
            "inspectable and usable without turning the repository into a "
            "staffed support channel."
        )
    if repo.surface_class is SurfaceClass.PRODUCT_FRONT_DOOR:
        return (
            f"`{repo.name}` is a product-front-door repository. Public metadata "
            "can orient readers, but operational support and commercial "
            "engagement do not happen through GitHub Issues."
        )
    if repo.surface_class is SurfaceClass.RUNTIME_MECHANISM:
        return (
            f"`{repo.name}` describes a runtime mechanism in the Hapax Systems "
            "portfolio. Public repository affordances are for inspection and "
            "citation, not support intake."
        )
    if repo.surface_class is SurfaceClass.GOVERNANCE_SPEC:
        return (
            f"`{repo.name}` is the governance-specification anchor for the "
            "Hapax Systems repository constellation. Support is limited to "
            "the published specification, rendered metadata, and security "
            "disclosure path."
        )
    return (
        f"`{repo.name}` is published as a Hapax Systems research or boundary "
        "artifact. The repository is available for inspection, citation, and "
        "governance review, not as a staffed support surface."
    )
