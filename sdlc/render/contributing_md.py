"""CONTRIBUTING.md renderer (refuse-and-redirect mode).

Per the operational checklist, CONTRIBUTING.md is positively asserted
with constitutional refusal text rather than left absent (which would
let GitHub's default contribution prompts surface). Body text uses the
sticky-per-document operator referent.
"""

from __future__ import annotations

from sdlc.render.operator_referent import OperatorReferentPicker
from sdlc.render.repo_registry import RepoSpec


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
        f"Hapax is research infrastructure for one operator's externalised "
        f"executive function. It is not a product, not a service, and not a "
        f"library to extend. The refusal is the artifact: see the Refusal "
        f"Brief at https://hapax.weblog.lol/refusal-brief.\n"
        "\n"
        "## What this means in practice\n"
        "\n"
        "- Issues are disabled; do not open them on a fork.\n"
        "- Pull requests are auto-closed by `.github/workflows/`.\n"
        "- Discussions and Wiki are disabled (except `hapax-constitution` "
        "Wiki, which mirrors the axiom registry).\n"
        "- Sponsorships are disabled.\n"
        "- This file is rendered from `hapax-constitution/sdlc/render/`; "
        "edits are overwritten on next render.\n"
        "\n"
        "## If you are reading this because you found a bug\n"
        "\n"
        f"Hapax is a research apparatus, not a product. Bug reports are not "
        f"actionable through this surface. The codebase is published for "
        f"citation and reproducibility, not for use.\n"
        "\n"
        "## Citation\n"
        "\n"
        "If your research engages with this codebase, cite via `CITATION.cff` "
        "(Citation File Format v1.2.0). Archival DOI lives in "
        "`.zenodo.json`. The constellation graph is queryable via DataCite "
        "Commons (GraphQL: https://api.datacite.org/graphql).\n"
    )
