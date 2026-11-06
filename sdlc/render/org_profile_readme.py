"""GitHub organization profile README renderer.

GitHub renders the public organization profile from the public
``hapax-systems/.github`` repository at ``profile/README.md``. This renderer
keeps that page tied to the same repository registry as per-repo frontmatter,
filtering strictly on public repositories and including canonical A16
identity, legal-entity, contact, and HACA-C v0.3.15 outside provenance.
"""

from __future__ import annotations

from collections.abc import Iterable

from sdlc.render.notice_md import HACA_C_OUTSIDE_FOOTER, LEGAL_ENTITY_FILING
from sdlc.render.repo_registry import RepoSpec, RepoVisibility, SurfaceClass

ORG_PROFILE_PATH = "profile/README.md"


def render(registry: dict[str, RepoSpec]) -> str:
    """Render the public Hapax Research Lab organization profile README."""
    repos = list(_public_first_party_repos(registry.values()))
    by_id = {repo.id: repo for repo in repos}
    return "\n".join(
        (
            "# Hapax Research Lab",
            "",
            "**Hapax Research Lab** (`hrl-han`) evaluates AI capability and governance at the "
            "level of the situated Human-Agentic Network (`HAN`) — model weights operating inside "
            "explicit verification, routing, benchmark, and authority boundaries — rather than "
            "treating isolated model checkpoints as self-governing systems. Across research "
            "records and software, the lab enforces authority before action, receipts before "
            "claims, and visible scope limits, publishing misses and corrections alongside "
            "supported results so readers can inspect what is shipped, what is reserved, and "
            "what evidence would have to exist before a stronger claim is allowed.",
            "",
            "- **Research portal & commitments register:** [https://hapaxresearch.com](https://hapaxresearch.com)",
            "- **Research weblog & field notes:** [https://hapax.weblog.lol](https://hapax.weblog.lol)",
            "- **Identity outpost:** [https://hapax.omg.lol](https://hapax.omg.lol)",
            "- **Disclosures & corrections:** [hrl-han@hapaxresearch.com](mailto:hrl-han@hapaxresearch.com) ([contact & security policy](https://hapaxresearch.com/about/#contact))",
            "",
            "The public `hapax-systems` portfolio is partitioned by role and license: "
            "source-available commercial core (`BSL 1.1`), public-domain numeric evidence "
            "(`CC0 1.0`), constitutional governance specifications (`CC BY-NC-ND 4.0` / "
            "`Apache-2.0`), permissive integration tooling (`MIT`), and checksum-verified "
            "publication assets (`CC BY 4.0` plus per-asset upstream terms). The license on "
            "each repository is the sole license authority for that repository; do not infer "
            "broader portfolio or trademark rights.",
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
            "- **Reins (`reins`)** is the product front door: terminal observation and governed "
            "command preview (`reins --demo` runs offline on fixture data). It remains a "
            "read/preview surface until receipt-backed writes ship and are released.",
            "- **Runtime mechanism (`hapax-spine`)** is the source-available `BSL 1.1` mechanism "
            "layer behind Reins (append-only event ledgers, policy-backed routing, capability "
            "receipts, quota arithmetic, EDT projections); it is not a general-purpose lifecycle kernel.",
            "- **Governance anchor (`hapax-constitution`)** holds the axiom registry, interpretive "
            "canons, and deterministic `hapax-sdlc` frontmatter renderers.",
            "- **Numeric ledger (`hapax-research-ledger`)** publishes append-only `CC0 1.0` "
            "observations, controlled vocabularies, hashes, caveats, and public commitment witnesses.",
            "- **Logos MCP Bridge (`hapax-mcp`)** is an experimental `MIT` `stdio` bridge for "
            "existing Logos HTTP API deployments; internal research, coordination, and companion "
            "device runtimes operate privately inside `hrl-han` and are not supported public frameworks, "
            "consumer health products, or general MCP frameworks. Public research examinations and "
            "correction records are published at [https://hapaxresearch.com](https://hapaxresearch.com).",
            "- **Historical archive (`agentgov`)** is an archived early standalone governance-hook "
            "prototype (`MIT`, `v0.3.2` inactive) superseded by [reins](https://github.com/hapax-systems/reins).",
            "- **Capability Frontier & publication channels:** Capability routing scores are "
            "registry-asserted today; measured calibration is planned. Weblog, RSS, archive/DOI, "
            "and social syndication surfaces operate as governed publication-bus channels and must "
            "not imply unreviewed direct public egress.",
            "",
            "## Claim Ceiling",
            "",
            "Current public material describes shipped read paths, governed command preview, "
            "dispatch and receipt mechanisms, numeric evidence ledgers, and source-available "
            "inspection surfaces. It does not claim autonomous write authority, full general "
            "lifecycle coverage, unrestricted portability, comparative ranking without primary "
            "reproduction witnesses, or staffed community support.",
            "",
            "## Support, Identity, and Legal Boundary",
            "",
            "GitHub Issues are enabled only as redirect surfaces; GitHub Discussions, Projects, "
            "and Wikis are disabled across `hapax-systems`, and unsolicited pull requests are not "
            "accepted.",
            "",
            "- **Institution:** Hapax Research Lab (`hrl-han` — the research network of Hapax Research Lab)",
            f"- **{LEGAL_ENTITY_FILING}**",
            "- **Contact:** [hrl-han@hapaxresearch.com](mailto:hrl-han@hapaxresearch.com) ([https://hapaxresearch.com/about/#contact](https://hapaxresearch.com/about/#contact))",
            "- **Commitment:** The network commits to receipt, retention and published correction. It promises no response time.",
            "",
            "---",
            "",
            HACA_C_OUTSIDE_FOOTER,
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
        "hapax-spine": 1,
        "hapax-constitution": 2,
        "hapax-research-ledger": 3,
        "hapax-mcp": 4,
        "hapax-assets": 5,
        "agentgov": 6,
    }
    class_order = {
        SurfaceClass.PRODUCT_FRONT_DOOR: 0,
        SurfaceClass.RUNTIME_MECHANISM: 1,
        SurfaceClass.GOVERNANCE_SPEC: 2,
        SurfaceClass.EVIDENCE_ARTIFACT: 3,
        SurfaceClass.ECOSYSTEM_BRIDGE: 4,
        SurfaceClass.ASSET_MIRROR: 5,
        SurfaceClass.HISTORICAL_ARCHIVE: 6,
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
        "hapax-spine",
        "hapax-constitution",
        "hapax-research-ledger",
    ):
        if repo_id not in by_id:
            continue
        repo = by_id[repo_id]
        if repo.visibility is not RepoVisibility.PUBLIC or repo.archived:
            continue
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
        "hapax-assets",
        "agentgov",
    ):
        if repo_id not in by_id:
            continue
        repo = by_id[repo_id]
        if repo.visibility is not RepoVisibility.PUBLIC:
            continue
        label = (
            f"[{repo.name}]({repo.github_url}) *(archived)*"
            if repo.archived
            else f"[{repo.name}]({repo.github_url})"
        )
        rows.append(
            "| "
            f"{label} | "
            f"{_compact(repo.reader_promise)} | "
            f"{_compact(repo.reader_value)} | "
            f"{_compact(repo.license_posture)} |"
        )
    return "\n".join(rows)


def _compact(value: str) -> str:
    """Collapse whitespace and avoid Markdown table-breaking pipes."""
    return " ".join(value.strip().replace("|", "/").split())


__all__ = ["ORG_PROFILE_PATH", "render"]
