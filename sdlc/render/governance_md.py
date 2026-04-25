"""GOVERNANCE.md renderer.

Redirects to the hapax-constitution axiom registry per the operational
checklist. The asymmetry is the argument: governance is centralised at
hapax-constitution; non-anchor repos point at it rather than re-stating
their own governance.
"""

from __future__ import annotations

from sdlc.render.operator_referent import OperatorReferentPicker
from sdlc.render.repo_registry import RepoSpec


def render(repo: RepoSpec) -> str:
    referent = OperatorReferentPicker.pick_for_artifact(repo.id)
    if repo.id == "hapax-constitution":
        return _render_anchor(referent)
    return _render_redirect(repo, referent)


def _render_anchor(referent: str) -> str:
    return (
        "# Governance\n"
        "\n"
        f"This repository is the canonical axiom registry for the Hapax "
        f"operating environment. Governance for the entire constellation "
        f"is centralised here.\n"
        "\n"
        "## Authority\n"
        "\n"
        f"Single operator: {referent}. No multi-stakeholder governance "
        f"body. The single-operator axiom (weight 100) forecloses any "
        f"shared-decision structure.\n"
        "\n"
        "## Mechanism\n"
        "\n"
        "- Axioms in `axioms/registry.yaml` (CODEOWNERS-protected).\n"
        "- Implications graduated across enforcement tiers (T0 block, "
        "T1 review, T2 warn, T3 lint).\n"
        "- Precedents in `axioms/precedents/`, append-only with "
        "supersession tracking.\n"
        "- Wiki mirrors registry as one-axiom-per-page (the Wiki is "
        "enabled here exclusively for this purpose).\n"
        "\n"
        "## Change process\n"
        "\n"
        "Changes to `axioms/registry.yaml` are always classified as "
        "L-complexity. Pre-commit + CI hooks enforce the axiom gate; "
        "T0 violations block at commit. There is no review committee — "
        "the operator self-reviews against the constitutional canons "
        "(textualist, purposivist, absurdity, omitted-case).\n"
        "\n"
        "## Downstream\n"
        "\n"
        "Other constellation repos consume this registry via the "
        "published `hapax-sdlc` package. Their `GOVERNANCE.md` redirects "
        "back here.\n"
    )


def _render_redirect(repo: RepoSpec, referent: str) -> str:
    return (
        "# Governance\n"
        "\n"
        f"Governance for this repository is centralised at "
        f"`hapax-constitution`. There is no per-repo governance body; "
        f"the single-operator axiom (weight 100) forecloses one.\n"
        "\n"
        "## Authoritative sources\n"
        "\n"
        "- Axiom registry: "
        "https://github.com/ryanklee/hapax-constitution/blob/main/axioms/registry.yaml\n"
        "- Implications: "
        "https://github.com/ryanklee/hapax-constitution/tree/main/axioms/implications/\n"
        "- Precedents: "
        "https://github.com/ryanklee/hapax-constitution/tree/main/axioms/precedents/\n"
        "- Axiom registry as Wiki: "
        "https://github.com/ryanklee/hapax-constitution/wiki\n"
        "\n"
        "## Operator\n"
        "\n"
        f"{referent}. Single operator, single workstation; governance "
        f"applies uniformly across the constellation.\n"
        "\n"
        "## Inter-repo position\n"
        "\n"
        f"{repo.role_in_constellation.strip()}\n"
        "\n"
        "---\n"
        "\n"
        "This file is rendered from `hapax-constitution/sdlc/render/`. "
        "Edits are overwritten on next render.\n"
    )
