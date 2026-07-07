"""GOVERNANCE.md renderer.

Redirects to the hapax-constitution axiom registry per the operational
checklist. The asymmetry is the argument: governance is centralised at
hapax-constitution; non-anchor repos point at it rather than re-stating
their own governance.
"""

from __future__ import annotations

from sdlc.render.operator_referent import OperatorReferentPicker
from sdlc.render.repo_registry import RepoSpec, github_repo_url


def render(repo: RepoSpec) -> str:
    referent = OperatorReferentPicker.pick_for_artifact(repo.id)
    if repo.id == "hapax-constitution":
        return _render_anchor(referent)
    return _render_redirect(repo, referent)


def _render_anchor(referent: str) -> str:
    return (
        "# Governance\n"
        "\n"
        f"This repository holds the canonical axiom registry for the Hapax "
        f"operating environment. The whole constellation uses this registry.\n"
        "\n"
        "## Authority\n"
        "\n"
        f"Single operator: {referent}. There is no multi-stakeholder "
        f"governance body. The single-operator axiom (weight 100) forecloses "
        f"shared-decision structures.\n"
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
        "Changes to `axioms/registry.yaml` always carry L-complexity. "
        "Pre-commit and CI hooks enforce the axiom gate. T0 violations block "
        "at commit. There is no review committee. The operator reviews "
        "changes against the constitutional canons: textualist, purposivist, "
        "absurdity, and omitted-case.\n"
        "\n"
        "## Downstream\n"
        "\n"
        "Other constellation repos consume this registry via the "
        "published `hapax-sdlc` package. Their `GOVERNANCE.md` redirects "
        "back here.\n"
    )


def _render_redirect(repo: RepoSpec, referent: str) -> str:
    constitution_url = github_repo_url("hapax-constitution")
    return (
        "# Governance\n"
        "\n"
        f"`hapax-constitution` governs this repository. This repo has no "
        f"separate governance body. The single-operator axiom (weight 100) "
        f"keeps decisions with one operator.\n"
        "\n"
        "## Authoritative sources\n"
        "\n"
        f"- [Axiom registry]({constitution_url}/blob/main/axioms/registry.yaml)\n"
        f"- [Implications]({constitution_url}/tree/main/axioms/implications/)\n"
        f"- [Precedents]({constitution_url}/tree/main/axioms/precedents/)\n"
        f"- [Axiom registry as Wiki]({constitution_url}/wiki)\n"
        "\n"
        "## Operator\n"
        "\n"
        f"{referent}. Single operator, single workstation. The same rules "
        f"apply across the constellation.\n"
        "\n"
        "## Inter-repo position\n"
        "\n"
        f"This repository follows the portfolio role recorded in NOTICE.md "
        f"and the constitution registry.\n"
        "\n"
        "---\n"
        "\n"
        "This file is rendered from `hapax-constitution/sdlc/render/`. "
        "Edits are overwritten on next render.\n"
    )
