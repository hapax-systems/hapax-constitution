"""GitHub organization profile README renderer.

GitHub renders the public organization profile from the public
``hapax-systems/.github`` repository at ``profile/README.md``. This renderer
keeps that page tied to the same repo registry as the per-repo frontmatter.
"""

from __future__ import annotations

from collections.abc import Iterable

from sdlc.render.repo_registry import RepoSpec, RepoVisibility, SurfaceClass


ORG_PROFILE_PATH = "profile/README.md"


def render(registry: dict[str, RepoSpec]) -> str:
    """Render the public Hapax Systems organization profile README."""
    repos = list(_public_first_party_repos(registry.values()))
    by_id = {repo.id: repo for repo in repos}
    return "\n".join(
        (
            "# Hapax Systems",
            "",
            "Hapax Systems publishes evidence-bound software for governing AI-agent work: "
            "authority before action, receipts before claims, and visible limits instead "
            "of unsupported automation claims. The practical value is legibility: "
            "operators, reviewers, researchers, and adopters can see what is shipped, "
            "what is reserved, and what evidence would have to exist before a stronger "
            "claim is allowed.",
            "",
            "The public portfolio is intentionally split by value surface. Some parts are "
            "open adoption commons, some are source-available commercial core, and some "
            "are source-visible research apparatus. The license on each repository is the "
            "authority for that repository; do not infer broader rights from the portfolio.",
            "",
            "## Public Entry Points",
            "",
            _entry_table(by_id),
            "",
            "## Supporting Public Surfaces",
            "",
            _supporting_table(by_id),
            "",
            "## Operating Frame",
            "",
            "- Reins is the product front door: read and command-preview for governed "
            "agentic delivery. It remains a read/preview surface until receipt-backed "
            "writes ship and are released.",
            "- agentgov is the adoption commons: portable governance hooks for AI coding "
            "agents under MIT.",
            "- hapax-spine is the source-available runtime mechanism behind Reins; it is "
            "not a general-purpose lifecycle kernel.",
            "- hapax-council is the research/runtime apparatus. It is published for "
            "inspection and citation, not as a supported framework.",
            "- Hapax Logos MCP Bridge, Mobile Context Source, and Wrist Biometric "
            "Source are public source-visible boundary artifacts. They support audit "
            "and integration review; they are not general products, health products, "
            "or broad MCP framework claims.",
            "- The Claim Verification Council is a public-facing capability name for "
            "claim-checking governance. Internal labels are not part of the public API.",
            "- The Capability Frontier is a way to describe measured capability and "
            "authority ceilings without collapsing them into a single agent score.",
            "- omg.lol weblog, RSS, social, DOI/archive, and other public fanout "
            "surfaces are governed publication-bus channels. Repository copy may "
            "point at published artifacts, but it must not imply direct public "
            "egress or cross-channel publication authority.",
            "",
            "## Support And Intake",
            "",
            "Issues are enabled as redirect surfaces. GitHub Discussions, Projects, and "
            "most wikis are not the operating venue for the work. Security, support, and "
            "commercial conversations follow the boundary files in each repository.",
            "",
            "## Claim Ceiling",
            "",
            "Current public material may describe shipped read paths, command preview, "
            "governed dispatch mechanisms, evidence ledgers, and source-available "
            "inspection surfaces. It must not claim autonomous write authority, full "
            "general lifecycle coverage, unrestricted portability, comparative ranking "
            "against other systems, or staffed community support unless the corresponding "
            "release gates have closed.",
            "",
        )
    )


def _public_first_party_repos(repos: Iterable[RepoSpec]) -> list[RepoSpec]:
    return sorted(
        (
            repo
            for repo in repos
            if repo.is_first_party and repo.visibility is RepoVisibility.PUBLIC
        ),
        key=_portfolio_order,
    )


def _portfolio_order(repo: RepoSpec) -> tuple[int, int, str]:
    preferred = {
        "reins": 0,
        "agentgov": 1,
        "hapax-council": 2,
        "hapax-constitution": 3,
        "hapax-officium": 4,
        "hapax-research-ledger": 5,
        "hapax-assets": 6,
        "hapax-mcp": 7,
        "hapax-phone": 8,
        "hapax-watch": 9,
    }
    class_order = {
        SurfaceClass.PRODUCT_FRONT_DOOR: 0,
        SurfaceClass.ADOPTION_COMMONS: 1,
        SurfaceClass.RESEARCH_APPARATUS: 2,
        SurfaceClass.GOVERNANCE_SPEC: 3,
        SurfaceClass.INTERNAL_APPARATUS: 4,
        SurfaceClass.EVIDENCE_ARTIFACT: 5,
        SurfaceClass.ASSET_MIRROR: 6,
    }
    return (
        preferred.get(repo.id, 50),
        class_order.get(repo.surface_class, 50),
        repo.id,
    )


def _entry_table(by_id: dict[str, RepoSpec]) -> str:
    rows = [
        "| Surface | What to expect | Reader value | License posture |",
        "|---|---|---|---|",
    ]
    for repo_id in (
        "reins",
        "agentgov",
        "hapax-council",
        "hapax-constitution",
        "hapax-officium",
        "hapax-research-ledger",
        "hapax-assets",
    ):
        repo = by_id[repo_id]
        rows.append(
            "| "
            f"[{repo.name}]({repo.github_url}) | "
            f"{_compact(repo.reader_promise)} | "
            f"{_compact(repo.reader_value)} | "
            f"{_compact(repo.license_posture)} |"
        )
    return "\n".join(rows)


def _supporting_table(by_id: dict[str, RepoSpec]) -> str:
    rows = [
        "| Surface | What to expect | Reader value | License posture |",
        "|---|---|---|---|",
    ]
    for repo_id in (
        "hapax-mcp",
        "hapax-phone",
        "hapax-watch",
    ):
        repo = by_id[repo_id]
        rows.append(
            "| "
            f"[{repo.name}]({repo.github_url}) | "
            f"{_compact(repo.reader_promise)} | "
            f"{_compact(repo.reader_value)} | "
            f"{_compact(repo.license_posture)} |"
        )
    return "\n".join(rows)


def _compact(value: str) -> str:
    """Collapse whitespace and avoid Markdown table-breaking pipes."""
    return " ".join(value.strip().replace("|", "/").split())


__all__ = ["ORG_PROFILE_PATH", "render"]
