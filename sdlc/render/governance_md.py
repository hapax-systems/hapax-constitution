"""GOVERNANCE.md renderer.

Redirects to the hapax-constitution axiom registry per the operational
checklist. The asymmetry is the argument: governance is centralised at
hapax-constitution; non-anchor repos point at it rather than re-stating
their own governance.
"""

from __future__ import annotations

from sdlc.render.repo_registry import RepoSpec, github_repo_url


def render(repo: RepoSpec) -> str:
    if repo.id == "hapax-constitution":
        return _render_anchor()
    return _render_redirect(repo)


def _render_anchor() -> str:
    return (
        "# Governance\n"
        "\n"
        "This repository holds the canonical axiom registry for the Hapax "
        "operating environment. The whole constellation uses this registry.\n"
        "\n"
        "## Authority\n"
        "\n"
        "Single operator. There is no multi-stakeholder "
        "governance body. The single-operator axiom (weight 100) forecloses "
        "shared-decision structures.\n"
        "\n"
        "## Mechanism\n"
        "\n"
        "- Axioms in `axioms/registry.yaml`.\n"
        "- Implications graduated across enforcement tiers (T0 block, "
        "T1 review, T2 warn, T3 lint).\n"
        "- Precedents in `axioms/precedents/`, append-only with "
        "supersession tracking.\n"
        "\n"
        "## Change process\n"
        "\n"
        "Changes to `axioms/registry.yaml` always carry L-complexity. "
        "There is no review committee. The operator reviews "
        "changes against the constitutional canons: textualist, purposivist, "
        "absurdity, and omitted-case.\n"
        "\n"
        "## Downstream\n"
        "\n"
        "Other constellation repos consume this registry. Their "
        "`GOVERNANCE.md` redirects back here.\n"
    )


def _render_redirect(repo: RepoSpec) -> str:
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
        "\n"
        "## Operator\n"
        "\n"
        "Single operator, single workstation. The same rules "
        "apply across the constellation.\n"
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
