"""CONTRIBUTING.md renderer (refuse-and-redirect mode).

Per the operational checklist, CONTRIBUTING.md is positively asserted
with constitutional refusal text rather than left absent (which would
let GitHub's default contribution prompts surface). Body text uses the
sticky-per-document operator referent.
"""

from __future__ import annotations

from sdlc.render.operator_referent import OperatorReferentPicker
from sdlc.render.repo_registry import RepoSpec, SurfaceClass


def render(repo: RepoSpec) -> str:
    referent = OperatorReferentPicker.pick_for_artifact(repo.id)
    return (
        "# Contributing\n"
        "\n"
        f"This repository does not accept contributions. {referent} is the "
        f"sole operator of the Hapax operating environment by constitutional "
        f"axiom (`single_user`, weight 100); the architecture forecloses "
        f"contributor onboarding at the structural level.\n"
        "\n"
        "## Why\n"
        "\n"
        f"{_why(repo)}\n"
        "\n"
        "## What this means in practice\n"
        "\n"
        "- Issues are redirect-only; `.github/ISSUE_TEMPLATE/config.yml` "
        "disables blank issues.\n"
        "- `.github/workflows/` auto-closes pull requests.\n"
        "- Repositories disable Discussions and Wiki except for the "
        "`hapax-constitution` Wiki, which mirrors the axiom registry.\n"
        "- Funding links, if present, are no-perk research support only.\n"
        "- This file is rendered from `hapax-constitution/sdlc/render/`; "
        "edits are overwritten on next render.\n"
        "\n"
        "## If you are reading this because you found a bug\n"
        "\n"
        f"{_bug_boundary(repo)}\n"
        "\n"
        "## Citation\n"
        "\n"
        "If your research engages with this codebase, cite via `CITATION.cff` "
        "(Citation File Format v1.2.0). Archival DOI lives in "
        "`.zenodo.json`. The constellation graph is queryable via DataCite "
        "Commons (GraphQL: https://api.datacite.org/graphql).\n"
    )


def _why(repo: RepoSpec) -> str:
    if repo.surface_class is SurfaceClass.ADOPTION_COMMONS:
        return (
            f"`{repo.name}` is the bounded adoption surface for the Hapax "
            "Systems portfolio. It is usable and auditable, but this "
            "repository is still operated through a single-operator release "
            "process rather than community maintenance."
        )
    if repo.surface_class is SurfaceClass.PRODUCT_FRONT_DOOR:
        return (
            f"`{repo.name}` is the Hapax Systems product front door. GitHub is "
            "an inspection and source-available evaluation surface, not the "
            "support, roadmap, or commercial intake channel."
        )
    if repo.surface_class is SurfaceClass.RUNTIME_MECHANISM:
        return (
            f"`{repo.name}` is a source-available runtime mechanism. It is "
            "published for inspection and evaluation without turning the "
            "mechanism into a community-maintained framework."
        )
    return (
        "Hapax is research infrastructure for one operator's externalised "
        "executive function. This repository is not a staffed product, "
        "service, or community library. The refusal is the artifact: see the "
        "Refusal Brief at https://hapax.weblog.lol/refusal-brief."
    )


def _bug_boundary(repo: RepoSpec) -> str:
    if repo.surface_class is SurfaceClass.ADOPTION_COMMONS:
        return (
            "Use the published documentation and examples to evaluate the "
            "adoption surface. GitHub Issues remain redirect-only, not a "
            "staffed support queue."
        )
    if repo.surface_class is SurfaceClass.PRODUCT_FRONT_DOOR:
        return (
            "Use the published demo/evaluation path to inspect current "
            "behavior. Operational support and commercial discussions do not "
            "happen through GitHub Issues."
        )
    if repo.surface_class is SurfaceClass.RUNTIME_MECHANISM:
        return (
            "Use the repository as a source-available inspection surface. "
            "Integration help and framework-style issue triage are out of "
            "scope for GitHub."
        )
    return (
        "Hapax is a research apparatus, not a staffed product. Bug reports "
        "are not actionable through this surface. The codebase is published "
        "for citation and reproducibility, not for general use."
    )
