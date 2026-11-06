"""README constitutional preamble renderer.

The README is rendered as a *section-replacement* operation rather than
a full overwrite, so per-repo README body content (technical docs,
architecture notes, etc.) is preserved between renders while any
duplicate leading ``# <repo.name>`` H1 immediately following the
preamble is stripped so every README carries exactly one H1.
"""

from __future__ import annotations

import re

from sdlc.render.repo_registry import RepoSpec, SurfaceClass, github_repo_url

PREAMBLE_BEGIN = "<!-- hapax-sdlc:preamble:begin -->"
PREAMBLE_END = "<!-- hapax-sdlc:preamble:end -->"

LEGAL_ENTITY_FILING = (
    "Legal entity (as filed): Hapax Research LLC, organized in Wyoming on "
    "2026-05-10, filing ID 2026-001973400"
)


def public_surface_marker_pair(repo_name: str) -> tuple[str, str]:
    """Claim-bearing generated-section markers.

    Co-emitted INSIDE the ``hapax-sdlc`` anchors: the outer family remains the
    section-replacement anchor, while this inner family marks the generated,
    claim-bearing region that public-surface claim checks recognize.
    """
    surface_id = f"github.repo.{repo_name}.readme.preamble"
    return (
        f"<!-- hapax-public:surface={surface_id}:begin -->",
        f"<!-- hapax-public:surface={surface_id}:end -->",
    )


def render(repo: RepoSpec) -> str:
    """Return the preamble block (between BEGIN/END markers, inclusive)."""
    license_summary = _license_one_liner(repo.license_class.value)
    opening = _opening(repo)
    issue_line = _issue_line(repo)
    authority_surfaces = _authority_surfaces(repo)
    public_begin, public_end = public_surface_marker_pair(repo.name)
    return (
        f"{PREAMBLE_BEGIN}\n"
        f"{public_begin}\n"
        f"\n"
        f"# {repo.name}\n"
        f"\n"
        f"{opening}\n"
        f"\n"
        f"## Reader promise\n"
        f"\n"
        f"{repo.reader_promise.strip()}\n"
        f"\n"
        f"## Reader value\n"
        f"\n"
        f"{repo.reader_value.strip()}\n"
        f"\n"
        f"## Claim ceiling\n"
        f"\n"
        f"{repo.claim_ceiling.strip()}\n"
        f"\n"
        f"## License and rights\n"
        f"\n"
        f"{repo.license_posture.strip()}\n"
        f"\n"
        f"Rendered summary: {license_summary}. See {authority_surfaces} for "
        f"the authority surfaces.\n"
        f"\n"
        f"## Public boundary\n"
        f"\n"
        f"- {issue_line}\n"
        f"- Published by **Hapax Research Lab** (`hrl-han`, "
        f"[hapaxresearch.com](https://hapaxresearch.com)). {LEGAL_ENTITY_FILING}.\n"
        f"- Security disclosures and factual correction proposals: "
        f"`hrl-han@hapaxresearch.com` (see `SECURITY.md` and "
        f"[hapaxresearch.com/about/#contact](https://hapaxresearch.com/about/#contact)). "
        f"The network commits to receipt, retention and published correction. "
        f"It promises no response time.\n"
        f"- Public copy uses `hapax-systems` organization links for "
        f"first-party repositories; README text is orientation rather than a "
        f"live runtime receipt.\n"
        f"- Governance reference: {github_repo_url('hapax-constitution')}\n"
        f"\n"
        f"## Portfolio position\n"
        f"\n"
        f"{repo.role_in_constellation.strip()}\n"
        f"\n"
        f"{public_end}\n"
        f"{PREAMBLE_END}"
    )


def _strip_duplicate_leading_h1(body: str, preamble: str) -> str:
    """Strip a duplicate leading ``# <repo.name>...`` H1 from ``body``."""
    stripped = body.lstrip()
    if not stripped:
        return ""
    match = re.search(r"^# (\S+)\s*$", preamble, re.MULTILINE)
    if match:
        repo_name = match.group(1)
        h1_re = re.compile(rf"^#\s+{re.escape(repo_name)}(?:\b[^\n]*)?\n*", re.IGNORECASE)
        stripped = h1_re.sub("", stripped, count=1).lstrip()
    return stripped


def replace_section(existing_readme: str, preamble: str) -> str:
    """Replace the BEGIN..END preamble block in ``existing_readme``.

    If markers are absent, the preamble is prepended. Any duplicate leading
    ``# <repo.name>`` heading at the top of the remaining body is removed so
    rendered README files never emit two H1 headings.
    """
    begin_idx = existing_readme.find(PREAMBLE_BEGIN)
    end_idx = existing_readme.find(PREAMBLE_END)
    if begin_idx == -1 or end_idx == -1 or end_idx < begin_idx:
        cleaned_body = _strip_duplicate_leading_h1(existing_readme, preamble)
        if not cleaned_body:
            return preamble + "\n"
        return preamble + "\n\n" + cleaned_body
    prefix = existing_readme[:begin_idx]
    rest = existing_readme[end_idx + len(PREAMBLE_END) :]
    cleaned_body = _strip_duplicate_leading_h1(rest, preamble)
    if not cleaned_body:
        return prefix + preamble + "\n"
    return prefix + preamble + "\n\n" + cleaned_body


def _authority_surfaces(repo: RepoSpec) -> str:
    preferred = [
        "LICENSE",
        "LICENSE-SCOPE.md",
        "NOTICE.md",
        "_NOTICES.md",
        "_manifest.yaml",
        "CITATION.cff",
        ".zenodo.json",
    ]
    surfaces = [f"`{name}`" for name in preferred if name in repo.public_files]
    if not surfaces:
        return "the files declared in `sdlc/render/repos.yaml`"
    if len(surfaces) == 1:
        return surfaces[0]
    if len(surfaces) == 2:
        return f"{surfaces[0]} and {surfaces[1]}"
    return f"{', '.join(surfaces[:-1])}, and {surfaces[-1]}"


def _license_one_liner(license_class: str) -> str:
    return {
        "PolyForm-Strict-1.0.0": (
            "PolyForm Strict 1.0.0 (source-available, non-distribution, non-modification)"
        ),
        "BUSL-1.1": (
            "Business Source License 1.1 (source-available; not Open Source until the "
            "Change Date converts the work to Apache-2.0)"
        ),
        "CC-BY-NC-ND-4.0": (
            "CC BY-NC-ND 4.0 (specification text, no derivatives; runnable hapax-sdlc "
            "tooling under Apache-2.0)"
        ),
        "CC-BY-4.0": (
            "CC BY 4.0 for original documentation and metadata (trademarks reserved; "
            "mirrored third-party assets retain declared upstream licenses)"
        ),
        "CC0-1.0": "CC0 1.0 (public-domain dedication for the declared data/artifact surface)",
        "MIT": "MIT",
        "Apache-2.0": "Apache 2.0",
        "CC-BY-SA-4.0": (
            "CC BY-SA 4.0 (existing aesthetic-library blend with "
            "BSD-3-Clause for BitchX components)"
        ),
        "upstream": "Upstream license preserved (fork)",
    }.get(license_class, license_class)


def _opening(repo: RepoSpec) -> str:
    if repo.archived or repo.surface_class is SurfaceClass.HISTORICAL_ARCHIVE:
        return (
            f"**[Archived Prototype — Superseded by [hapax-systems/reins]"
            f"({github_repo_url('reins')})]** `{repo.name}` is an archived early "
            "standalone governance-hook prototype in the **Hapax Research Lab** "
            "portfolio ([hapaxresearch.com](https://hapaxresearch.com)). It is "
            "retained for historical inspection and citation; evaluate "
            f"[reins]({github_repo_url('reins')}) for active governed "
            "agent-delivery observation and command preview."
        )
    if repo.surface_class is SurfaceClass.ADOPTION_COMMONS:
        return (
            f"`{repo.name}` is a bounded adoption-commons repository in the "
            "**Hapax Research Lab** portfolio. It is published so adopters can "
            "inspect and pilot the governance-hook surface without inheriting "
            "the broader Hapax runtime estate."
        )
    if repo.surface_class is SurfaceClass.PRODUCT_FRONT_DOOR:
        return (
            f"`{repo.name}` is the product front door for the **Hapax Research Lab** "
            "portfolio ([hapaxresearch.com](https://hapaxresearch.com)). Its "
            "current public ceiling is observation and governed command preview, "
            "not autonomous write authority."
        )
    if repo.surface_class is SurfaceClass.RUNTIME_MECHANISM:
        return (
            f"`{repo.name}` is a source-available runtime mechanism in the "
            "**Hapax Research Lab** portfolio ([hapaxresearch.com](https://hapaxresearch.com)). "
            "It exposes dispatch, receipt, quota, and projection machinery "
            "without claiming to be the whole Hapax estate."
        )
    if repo.surface_class is SurfaceClass.GOVERNANCE_SPEC:
        return (
            f"`{repo.name}` anchors governance and public metadata for "
            "**Hapax Research Lab** repositories ([hapaxresearch.com](https://hapaxresearch.com))."
        )
    if repo.surface_class is SurfaceClass.ECOSYSTEM_BRIDGE:
        return (
            f"`{repo.name}` is an integration bridge in the **Hapax Research Lab** "
            "portfolio ([hapaxresearch.com](https://hapaxresearch.com)). It is "
            "maintained for MCP integration and inspection, not as a "
            "general-purpose framework."
        )
    if repo.surface_class is SurfaceClass.ASSET_MIRROR:
        return (
            f"`{repo.name}` is a public asset mirror for the **Hapax Research Lab** "
            "portfolio ([hapaxresearch.com](https://hapaxresearch.com)). Source "
            "of truth and approval remain outside this mirror."
        )
    if repo.surface_class is SurfaceClass.EVIDENCE_ARTIFACT:
        return (
            f"`{repo.name}` is an evidence-artifact repository in the **Hapax Research Lab** "
            "portfolio ([hapaxresearch.com](https://hapaxresearch.com)). It publishes "
            "bounded observations and witness records, not runtime authority."
        )
    if repo.surface_class is SurfaceClass.INTERNAL_APPARATUS:
        return (
            f"`{repo.name}` is internal apparatus in the **Hapax Research Lab** "
            "portfolio. It is visible only where a separate visibility "
            "decision permits inspection."
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
            "for active governed agent-delivery inspection"
        )
    if repo.surface_class is SurfaceClass.ADOPTION_COMMONS:
        return (
            "Issues are redirect-only and support is bounded; pull requests "
            "are not the intake path for this repository"
        )
    if repo.surface_class is SurfaceClass.PRODUCT_FRONT_DOOR:
        return (
            "Issues are redirect-only; support, commercial engagement, and "
            "roadmap commitments do not happen through GitHub"
        )
    return (
        "Issues are redirect-only; no discussions, no pull requests accepted; "
        "see `CONTRIBUTING.md` and `SUPPORT.md`"
    )
