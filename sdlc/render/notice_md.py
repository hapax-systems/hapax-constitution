"""NOTICE.md renderer.

Constitutional disclosure document that ships in every first-party repo
plus, gitignored via ``.git/info/exclude``, in the two upstream forks.
Body text uses the sticky-per-document non-formal operator referent;
legal name does NOT appear.
"""

from __future__ import annotations

from sdlc.render.operator_referent import OperatorReferentPicker
from sdlc.render.repo_registry import RepoSpec, SurfaceClass, github_repo_url


def render(repo: RepoSpec) -> str:
    """Return NOTICE.md body for ``repo``."""
    referent = OperatorReferentPicker.pick_for_artifact(repo.id)
    license_summary = _license_summary(repo.license_class.value)
    return (
        f"# NOTICE — {repo.name}\n"
        "\n"
        f"{_opening(repo)}\n"
        "\n"
        f"Authorship is indeterminate by design. This codebase is co-produced "
        f"by Hapax (the system itself), Claude Code, and the operator "
        f"({referent}). Per the Hapax Manifesto, unsettled contribution "
        f"is a feature of the work, not a concealment.\n"
        "\n"
        "## Constitutional position\n"
        "\n"
        f"- Single-operator system; no auth, no roles, no contributor "
        f"onboarding (axiom: `single_user`).\n"
        f"- {_issue_line(repo)}\n"
        f"- License: {license_summary}\n"
        f"- Citation: see CITATION.cff; archival DOI: see .zenodo.json\n"
        "\n"
        "## Linked artifacts\n"
        "\n"
        "- Manifesto: https://hapax.weblog.lol/hapax-manifesto-v0\n"
        "- Refusal Brief: https://hapax.weblog.lol/refusal-brief\n"
        "- Cohort Disparity Disclosure: "
        "https://hapax.weblog.lol/cohort-disparity-disclosure\n"
        f"- Constitution: {github_repo_url('hapax-constitution')}\n"
        "\n"
        "## Inter-repo position\n"
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
            "PolyForm Strict 1.0.0 — source-available, non-distribution, non-modification."
        ),
        "BUSL-1.1": (
            "Business Source License 1.1 — source-available; not Open Source until "
            "the change license/date applies."
        ),
        "CC-BY-NC-ND-4.0": (
            "CC BY-NC-ND 4.0 — non-commercial, no derivatives. Specification text, not code."
        ),
        "CC0-1.0": "CC0 1.0 — public-domain dedication for the declared data/artifact surface.",
        "MIT": "MIT — permissive (MCP ecosystem alignment).",
        "Apache-2.0": "Apache 2.0 — permissive with patent grant.",
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
            "read/preview claim ceiling."
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
            f"`{repo.name}` is an ecosystem bridge for Hapax Systems APIs and "
            "MCP clients. It is not a general-purpose MCP framework."
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
    return (
        f"`{repo.name}` is a constituent of the Hapax operating environment. "
        "It is research or boundary infrastructure published as an artifact, "
        "not a staffed product or community project."
    )


def _issue_line(repo: RepoSpec) -> str:
    if repo.surface_class is SurfaceClass.ADOPTION_COMMONS:
        return (
            "Issues are redirect-only, support is bounded, and pull requests "
            "are not the intake path for this single-operator project."
        )
    if repo.surface_class is SurfaceClass.PRODUCT_FRONT_DOOR:
        return (
            "Issues are redirect-only; support, commercial engagement, and "
            "roadmap commitments do not happen through GitHub."
        )
    return (
        "No issues, no discussions, no pull requests accepted; refusal is the "
        "artifact (see /CONTRIBUTING.md)."
    )
