"""README constitutional preamble renderer.

The README is rendered as a *section-replacement* operation rather than
a full overwrite, so per-repo README body content (technical docs,
architecture notes, etc.) is preserved between renders.

The preamble lives between two HTML comment markers; the renderer
replaces only that delimited region. If the markers are absent, the
preamble is prepended.
"""

from __future__ import annotations

from sdlc.render.repo_registry import RepoSpec, SurfaceClass, github_repo_url

PREAMBLE_BEGIN = "<!-- hapax-sdlc:preamble:begin -->"
PREAMBLE_END = "<!-- hapax-sdlc:preamble:end -->"


def render(repo: RepoSpec) -> str:
    """Return the preamble block (between BEGIN/END markers, inclusive)."""
    license_summary = _license_one_liner(repo.license_class.value)
    opening = _opening(repo)
    issue_line = _issue_line(repo)
    authority_surfaces = _authority_surfaces(repo)
    return (
        f"{PREAMBLE_BEGIN}\n"
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
        f"- Public copy must use `hapax-systems` organization links for "
        f"first-party Hapax repositories.\n"
        f"- README text is orientation, not a freshness witness; current "
        f"public claims require surface-specific release, reconcile, or "
        f"publication receipts.\n"
        f"- Publication, weblog, RSS, social, DOI/archive, and other public "
        f"fanout paths must route through the governed publication bus or a "
        f"documented guarded legacy surface.\n"
        f"- Governance reference: {github_repo_url('hapax-constitution')}\n"
        f"\n"
        f"## Portfolio position\n"
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


def _authority_surfaces(repo: RepoSpec) -> str:
    preferred = [
        "LICENSE",
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
            "change license/date applies)"
        ),
        "CC-BY-NC-ND-4.0": "CC BY-NC-ND 4.0 (specification text, no derivatives)",
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
    if repo.surface_class is SurfaceClass.ADOPTION_COMMONS:
        return (
            f"`{repo.name}` is the bounded adoption-commons repository in the "
            "Hapax Systems portfolio. It is published so adopters can inspect "
            "and pilot the governance-hook surface without inheriting the "
            "Hapax runtime estate."
        )
    if repo.surface_class is SurfaceClass.PRODUCT_FRONT_DOOR:
        return (
            f"`{repo.name}` is the product front door for the Hapax Systems "
            "portfolio. Its current public ceiling is observation and "
            "governed command preview, not autonomous write authority."
        )
    if repo.surface_class is SurfaceClass.RUNTIME_MECHANISM:
        return (
            f"`{repo.name}` is a source-available runtime mechanism in the "
            "Hapax Systems portfolio. It exposes dispatch, receipt, quota, "
            "and projection machinery without claiming to be the whole "
            "Hapax estate."
        )
    if repo.surface_class is SurfaceClass.GOVERNANCE_SPEC:
        return (
            f"`{repo.name}` anchors governance and public metadata for Hapax Systems repositories."
        )
    if repo.surface_class is SurfaceClass.ECOSYSTEM_BRIDGE:
        return (
            f"`{repo.name}` is an integration bridge for the Hapax Systems "
            "portfolio. It is maintained for MCP integration and inspection, "
            "not as a general-purpose framework."
        )
    if repo.surface_class is SurfaceClass.ASSET_MIRROR:
        return (
            f"`{repo.name}` is a public asset mirror for the Hapax Systems "
            "portfolio. Source of truth and approval remain outside this "
            "mirror."
        )
    if repo.surface_class is SurfaceClass.EVIDENCE_ARTIFACT:
        return (
            f"`{repo.name}` is an evidence-artifact repository in the Hapax "
            "Systems portfolio. It publishes bounded observations or "
            "metadata, not runtime authority."
        )
    if repo.surface_class is SurfaceClass.INTERNAL_APPARATUS:
        return (
            f"`{repo.name}` is internal apparatus in the Hapax Systems "
            "portfolio. It is visible only where a separate visibility "
            "decision permits inspection."
        )
    return (
        f"`{repo.name}` is a constituent of the Hapax operating environment. "
        "It is research or boundary infrastructure published as an artifact, "
        "not a staffed product or community project."
    )


def _issue_line(repo: RepoSpec) -> str:
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
