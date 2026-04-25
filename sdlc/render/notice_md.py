"""NOTICE.md renderer.

Constitutional disclosure document that ships in every first-party repo
plus, gitignored via ``.git/info/exclude``, in the two upstream forks.
Body text uses the sticky-per-document non-formal operator referent;
legal name does NOT appear.
"""

from __future__ import annotations

from sdlc.render.operator_referent import OperatorReferentPicker
from sdlc.render.repo_registry import RepoSpec


def render(repo: RepoSpec) -> str:
    """Return NOTICE.md body for ``repo``."""
    referent = OperatorReferentPicker.pick_for_artifact(repo.id)
    license_summary = _license_summary(repo.license_class.value)
    return (
        f"# NOTICE — {repo.name}\n"
        "\n"
        f"This repository is a constituent of the Hapax operating environment. "
        f"It is not a product, not a service, and not seeking contributors. "
        f"It is research infrastructure published as artifact.\n"
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
        f"- No issues, no discussions, no pull requests accepted; refusal "
        f"is the artifact (see /CONTRIBUTING.md).\n"
        f"- License: {license_summary}\n"
        f"- Citation: see CITATION.cff; archival DOI: see .zenodo.json\n"
        "\n"
        "## Linked artifacts\n"
        "\n"
        "- Manifesto: https://hapax.weblog.lol/hapax-manifesto-v0\n"
        "- Refusal Brief: https://hapax.weblog.lol/refusal-brief\n"
        "- Cohort Disparity Disclosure: "
        "https://hapax.weblog.lol/cohort-disparity-disclosure\n"
        "- Constitution: https://github.com/ryanklee/hapax-constitution\n"
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
        "CC-BY-NC-ND-4.0": (
            "CC BY-NC-ND 4.0 — non-commercial, no derivatives. Specification text, not code."
        ),
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
