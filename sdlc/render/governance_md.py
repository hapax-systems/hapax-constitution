"""GOVERNANCE.md renderer.

Redirects to the hapax-constitution axiom registry per the operational
checklist. Governance is centralized at hapax-constitution; non-anchor
repositories point back to it rather than maintaining separate governance
bodies.
"""

from __future__ import annotations

from sdlc.render.repo_registry import RepoSpec, github_repo_url

LEGAL_ENTITY_LINE = (
    "Legal entity (as filed): Hapax Research LLC, organized in Wyoming on "
    "2026-05-10, filing ID 2026-001973400; in law, the answerable entity is "
    "Hapax Research LLC."
)


def render(repo: RepoSpec) -> str:
    if repo.id == "hapax-constitution":
        return _render_anchor()
    return _render_redirect(repo)


def _render_anchor() -> str:
    return (
        "# Governance\n"
        "\n"
        "This repository holds the canonical axiom registry for **Hapax Research Lab** "
        "(`hrl-han`, https://hapaxresearch.com). First-party repositories across the "
        "`hapax-systems` organization consume this registry.\n"
        "\n"
        "## Authority\n"
        "\n"
        "`hrl-han`, the research network of **Hapax Research Lab**, has human and AI "
        "agent members. Research and engineering staff are AI agents; one human "
        "member, the lab's principal, holds constitutional authority inside `hrl-han`, "
        "constituted the network, and adopted the standing rule under which public "
        "editions and releases are checked and published. There is no external "
        "multi-stakeholder governance body or community maintainer committee.\n"
        "\n"
        f"{LEGAL_ENTITY_LINE}\n"
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
        "There is no review committee. Constitutional changes to `axioms/registry.yaml` "
        "require explicit principal ratification and evaluation against the "
        "interpretive canons: textualist, purposivist, absurdity, and omitted-case.\n"
        "\n"
        "## Contact and corrections\n"
        "\n"
        "Contact: `hrl-han@hapaxresearch.com` (see `SECURITY.md` and "
        "https://hapaxresearch.com/about/#contact). The network commits to receipt, "
        "retention and published correction. It promises no response time.\n"
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
        f"`hapax-constitution` governs this repository. `{repo.name}` is published by "
        "**Hapax Research Lab** (`hrl-han`, https://hapaxresearch.com) and governed "
        "as a single trust domain under `hapax-constitution`. Research and engineering "
        "staff are AI agents; one human, the lab's principal, holds constitutional "
        "authority inside `hrl-han`. Public repositories are published for inspection, "
        "citation, and use within their stated license, not for external contributor "
        "onboarding or community governance.\n"
        "\n"
        "## Authoritative sources\n"
        "\n"
        f"- [Axiom registry]({constitution_url}/blob/main/axioms/registry.yaml)\n"
        f"- [Implications]({constitution_url}/tree/main/axioms/implications/)\n"
        f"- [Precedents]({constitution_url}/tree/main/axioms/precedents/)\n"
        "\n"
        "## Legal entity and contact\n"
        "\n"
        f"{LEGAL_ENTITY_LINE}\n"
        "\n"
        "Contact: `hrl-han@hapaxresearch.com` (see `SECURITY.md` and "
        "https://hapaxresearch.com/about/#contact). The network commits to receipt, "
        "retention and published correction. It promises no response time.\n"
        "\n"
        "## Inter-repo position\n"
        "\n"
        "This repository follows the portfolio role recorded in `NOTICE.md` "
        "and the constitution registry.\n"
        "\n"
        "---\n"
        "\n"
        "This file is rendered from `hapax-constitution/sdlc/render/`. "
        "Edits are overwritten on next render.\n"
    )
