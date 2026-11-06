"""NOTICE.md renderer.

Constitutional disclosure document that ships in every first-party repository
plus, gitignored via ``.git/info/exclude``, in the two upstream forks.
Body text is registry-driven and carries institutional attribution (Hapax
Research Lab / hrl-han), qualified legal-entity filing facts, contact
commitments, and HACA-C v0.3.15 outside provenance.
"""

from __future__ import annotations

from sdlc.render.repo_registry import RepoSpec, SurfaceClass, github_repo_url

LEGAL_ENTITY_FILING = (
    "Legal entity (as filed): Hapax Research LLC, organized in Wyoming on "
    "2026-05-10, filing ID 2026-001973400"
)

HACA_C_OUTSIDE_FOOTER = (
    "*HACA-C v0.3.15, the lab's draft rule for labelling machine-made text, "
    "not an external certification. No request to a natural person to approve "
    "the final wording, and no such approval, was found in hrl-han's sending, "
    "review and coordination records when the text was released. hrl-han "
    "releases a text once its checking is complete, under a standing rule that "
    "hrl-han's principal, who is not named in this text, adopted before the "
    "text was drafted. Review record: https://hapaxresearch.com/review-record/ "
    "(open to anyone). This label records how the text was made; it does not "
    "certify that the text is true. An unaltered record can contain false "
    "claims or miss relevant events.*"
)


def render(repo: RepoSpec) -> str:
    """Return NOTICE.md body for ``repo``."""
    license_summary = _license_summary(repo.license_class.value)
    return (
        f"# NOTICE - {repo.name}\n"
        "\n"
        f"{_opening(repo)}\n"
        "\n"
        "This repository is published by **Hapax Research Lab** (`hrl-han`, "
        "https://hapaxresearch.com). Public metadata, issue affordances, and "
        "support boundaries follow the registry in `hapax-constitution`.\n"
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
        f"- {LEGAL_ENTITY_FILING}.\n"
        "- Contact: `hrl-han@hapaxresearch.com` (see `SECURITY.md` and "
        "https://hapaxresearch.com/about/#contact). The network commits to "
        "receipt, retention and published correction. It promises no response "
        "time.\n"
        f"- Governance reference: {github_repo_url('hapax-constitution')}\n"
        "\n"
        "## Portfolio position\n"
        "\n"
        f"{repo.role_in_constellation.strip()}\n"
        "\n"
        "---\n"
        "\n"
        f"{HACA_C_OUTSIDE_FOOTER}\n"
        "\n"
        "This file is rendered from `hapax-constitution/sdlc/render/`. "
        "Do not edit by hand; edits will be overwritten on next render. "
        "To change content, edit `sdlc/render/repos.yaml` or the renderer "
        "templates in `hapax-constitution`.\n"
    )


def _license_summary(license_class: str) -> str:
    return {
        "PolyForm-Strict-1.0.0": (
            "PolyForm Strict 1.0.0 - source-available, non-distribution, non-modification."
        ),
        "BUSL-1.1": (
            "Business Source License 1.1 - source-available; not Open Source until "
            "the Change Date converts the work to Apache-2.0."
        ),
        "CC-BY-NC-ND-4.0": (
            "CC BY-NC-ND 4.0 - non-commercial, no derivatives for specification text; "
            "runnable hapax-sdlc tooling uses Apache-2.0."
        ),
        "CC-BY-4.0": (
            "CC BY 4.0 for original documentation and metadata (trademarks expressly "
            "reserved); mirrored third-party assets retain their declared upstream licenses."
        ),
        "CC0-1.0": "CC0 1.0 - public-domain dedication for the declared data/artifact surface.",
        "MIT": "MIT - permissive.",
        "Apache-2.0": "Apache 2.0 - permissive with patent grant.",
        "CC-BY-SA-4.0": (
            "CC BY-SA 4.0 (aesthetic-library asset blend; "
            "BSD-3-Clause for BitchX components preserved)."
        ),
        "upstream": (
            "Upstream license preserved (this is a fork). NOTICE.md is "
            "gitignored via `.git/info/exclude`."
        ),
    }.get(license_class, license_class)


def _opening(repo: RepoSpec) -> str:
    if repo.archived or repo.surface_class is SurfaceClass.HISTORICAL_ARCHIVE:
        return (
            f"**[Archived Prototype — Superseded by [hapax-systems/reins]"
            f"({github_repo_url('reins')})]** `{repo.name}` is an archived early "
            "prototype in the Hapax Research Lab portfolio retained for "
            "historical inspection and citation."
        )
    if repo.surface_class is SurfaceClass.ADOPTION_COMMONS:
        return (
            f"`{repo.name}` is a bounded adoption-commons repository in the "
            "Hapax Research Lab portfolio. It is published for inspection and "
            "pilot use without granting rights to the broader Hapax runtime "
            "estate."
        )
    if repo.surface_class is SurfaceClass.PRODUCT_FRONT_DOOR:
        return (
            f"`{repo.name}` is the product front door for the Hapax Research Lab "
            "portfolio. Public materials stay within the shipped "
            "read and command-preview claim ceiling."
        )
    if repo.surface_class is SurfaceClass.RUNTIME_MECHANISM:
        return (
            f"`{repo.name}` is a source-available runtime mechanism in the "
            "Hapax Research Lab portfolio. It is not the full Hapax estate."
        )
    if repo.surface_class is SurfaceClass.GOVERNANCE_SPEC:
        return (
            f"`{repo.name}` is the governance-specification and publication "
            "metadata anchor for the Hapax Research Lab repository constellation."
        )
    if repo.surface_class is SurfaceClass.ECOSYSTEM_BRIDGE:
        return (
            f"`{repo.name}` is an integration bridge for Hapax Research Lab APIs and "
            "MCP clients. It is maintained for integration and inspection, "
            "not as a general-purpose MCP framework."
        )
    if repo.surface_class is SurfaceClass.ASSET_MIRROR:
        return (
            f"`{repo.name}` is a public asset mirror for the Hapax Research Lab "
            "portfolio. Per-asset notices and upstream licenses remain "
            "controlling."
        )
    if repo.surface_class is SurfaceClass.EVIDENCE_ARTIFACT:
        return (
            f"`{repo.name}` is an evidence-artifact repository in the Hapax Research Lab "
            "portfolio. It publishes bounded observations and witness records, "
            "not runtime code authority."
        )
    if repo.surface_class is SurfaceClass.INTERNAL_APPARATUS:
        return (
            f"`{repo.name}` is internal apparatus in the Hapax Research Lab "
            "portfolio. It is not a public product, hosted service, or "
            "community project unless a separate product boundary is ratified."
        )
    return (
        f"`{repo.name}` is a constituent repository of **Hapax Research Lab**. "
        "It is research or boundary infrastructure published as an artifact, "
        "not a staffed product or community project."
    )


def _issue_line(repo: RepoSpec) -> str:
    if repo.archived or repo.surface_class is SurfaceClass.HISTORICAL_ARCHIVE:
        return (
            f"Repository is archived and read-only; evaluate {github_repo_url('reins')} "
            "for active governed agent-delivery inspection."
        )
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
