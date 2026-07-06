"""README constitutional preamble renderer.

The README is rendered as a *section-replacement* operation rather than
a full overwrite, so per-repo README body content (technical docs,
architecture notes, etc.) is preserved between renders.

The preamble lives between two HTML comment markers; the renderer
replaces only that delimited region. If the markers are absent, the
preamble is prepended.
"""

from __future__ import annotations

from sdlc.render.operator_referent import OperatorReferentPicker
from sdlc.render.repo_registry import RepoSpec, github_repo_url

PREAMBLE_BEGIN = "<!-- hapax-sdlc:preamble:begin -->"
PREAMBLE_END = "<!-- hapax-sdlc:preamble:end -->"


def render(repo: RepoSpec) -> str:
    """Return the preamble block (between BEGIN/END markers, inclusive)."""
    referent = OperatorReferentPicker.pick_for_artifact(repo.id)
    license_summary = _license_one_liner(repo.license_class.value)
    return (
        f"{PREAMBLE_BEGIN}\n"
        f"\n"
        f"# {repo.name}\n"
        f"\n"
        f"This repository is a constituent of the Hapax operating environment. "
        f"It is not a product, not a service, and not seeking contributors. "
        f"It is research infrastructure published as artifact.\n"
        f"\n"
        f"Authorship is indeterminate by design: this codebase is co-produced "
        f"by Hapax (the system itself), Claude Code, and the operator "
        f"({referent}). Per the Hapax Manifesto, unsettled contribution is a "
        f"feature of the work, not a concealment.\n"
        f"\n"
        f"## What this is, not what it does\n"
        f"\n"
        f"{repo.description.strip()}\n"
        f"\n"
        f"## Constitutional position\n"
        f"\n"
        f"- Single-operator system; no auth, no roles, no contributor "
        f"onboarding (axiom: `single_user`)\n"
        f"- Issues are redirect-only; no discussions, no PRs accepted; "
        f"refusal is the artifact (see `CONTRIBUTING.md` and `SUPPORT.md`)\n"
        f"- License: {license_summary}\n"
        f"- Citation: see `CITATION.cff`; archival DOI: see `.zenodo.json`\n"
        f"\n"
        f"## Linked artifacts\n"
        f"\n"
        f"- Manifesto: https://hapax.weblog.lol/hapax-manifesto-v0\n"
        f"- Refusal Brief: https://hapax.weblog.lol/refusal-brief\n"
        f"- Cohort Disparity Disclosure: "
        f"https://hapax.weblog.lol/cohort-disparity-disclosure\n"
        f"- Constitution: {github_repo_url('hapax-constitution')}\n"
        f"\n"
        f"## Inter-repo position\n"
        f"\n"
        f"{repo.role_in_constellation.strip()}\n"
        f"\n"
        f"{PREAMBLE_END}"
    )


def replace_section(existing_readme: str, preamble: str) -> str:
    """Replace the BEGIN..END preamble block in ``existing_readme``.

    If markers are absent, the preamble is prepended (with a blank line
    between preamble and existing body).
    """
    begin_idx = existing_readme.find(PREAMBLE_BEGIN)
    end_idx = existing_readme.find(PREAMBLE_END)
    if begin_idx == -1 or end_idx == -1 or end_idx < begin_idx:
        return preamble + "\n\n" + existing_readme.lstrip()
    end_idx += len(PREAMBLE_END)
    return existing_readme[:begin_idx] + preamble + existing_readme[end_idx:]


def _license_one_liner(license_class: str) -> str:
    return {
        "PolyForm-Strict-1.0.0": (
            "PolyForm Strict 1.0.0 (source-available, non-distribution, non-modification)"
        ),
        "BUSL-1.1": (
            "Business Source License 1.1 (source-available; not Open Source until the "
            "change license/date applies)"
        ),
        "CC-BY-NC-ND-4.0": "CC BY-NC-ND 4.0 (specification text, no derivatives)",
        "CC0-1.0": "CC0 1.0 (public-domain dedication for the declared data/artifact surface)",
        "MIT": "MIT (MCP ecosystem alignment)",
        "Apache-2.0": "Apache 2.0",
        "CC-BY-SA-4.0": (
            "CC BY-SA 4.0 (existing aesthetic-library blend with "
            "BSD-3-Clause for BitchX components)"
        ),
        "upstream": "Upstream license preserved (fork)",
    }.get(license_class, license_class)
