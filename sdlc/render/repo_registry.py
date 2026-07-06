"""Repository registry — single source of truth for per-repo metadata.

The registry covers first-party Hapax Systems repositories plus upstream
forks where this render mechanism is intentionally inert (NOTICE.md is
gitignored via ``.git/info/exclude`` per the operational checklist).

Operator identity (legal name, ORCID iD, email) is loaded from
``hapax-constitution/sdlc/operator.yaml``. The file is **not** committed
to the repository if ORCID/email are populated; the canonical YAML in
this repo carries placeholder strings so CI runs deterministically.
Production renders supply real values via env-var overrides or a local
``operator.local.yaml`` (gitignored).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import yaml

REGISTRY_PATH = Path(__file__).resolve().parent / "repos.yaml"
OPERATOR_PATH = Path(__file__).resolve().parent.parent.parent / "sdlc" / "operator.yaml"
OPERATOR_LOCAL_PATH = OPERATOR_PATH.with_suffix(".local.yaml")
DEFAULT_GITHUB_OWNER = "hapax-systems"


class LicenseClass(str, Enum):
    """License classes the renderer knows how to attribute."""

    POLYFORM_STRICT_1_0_0 = "PolyForm-Strict-1.0.0"
    BUSL_1_1 = "BUSL-1.1"
    CC_BY_NC_ND_4_0 = "CC-BY-NC-ND-4.0"
    CC0_1_0 = "CC0-1.0"
    MIT = "MIT"
    APACHE_2_0 = "Apache-2.0"
    CC_BY_SA_4_0 = "CC-BY-SA-4.0"
    UPSTREAM = "upstream"  # tabbyAPI / atlas-voice — preserve upstream license

    @property
    def is_first_party(self) -> bool:
        return self is not LicenseClass.UPSTREAM


class ValuePartition(str, Enum):
    """Consumer-facing value partition for license and copy policy."""

    ADOPTION_COMMONS = "adoption_commons"
    COMMERCIAL_MOAT = "commercial_moat"
    INTERNAL_APPARATUS = "internal_apparatus"
    EVIDENCE_ARTIFACT = "evidence_artifact"
    UPSTREAM = "upstream"


class SurfaceClass(str, Enum):
    """Reader-facing class used by frontmatter and support posture."""

    ADOPTION_COMMONS = "adoption_commons"
    PRODUCT_FRONT_DOOR = "product_front_door"
    RUNTIME_MECHANISM = "runtime_mechanism"
    RESEARCH_APPARATUS = "research_apparatus"
    GOVERNANCE_SPEC = "governance_spec"
    INTERNAL_APPARATUS = "internal_apparatus"
    ECOSYSTEM_BRIDGE = "ecosystem_bridge"
    EVIDENCE_ARTIFACT = "evidence_artifact"
    ASSET_MIRROR = "asset_mirror"
    UPSTREAM = "upstream"


class RepoVisibility(str, Enum):
    """Intended GitHub visibility / publication boundary."""

    PUBLIC = "public"
    PRIVATE = "private"
    LOCAL_ONLY = "local_only"


class SourceOfTruth(str, Enum):
    """Where the public-facing facts for a repo are canonically maintained."""

    CONSTITUTION_REGISTRY = "constitution_registry"
    COUNCIL_SOURCE = "council_source"
    REPO_BODY = "repo_body"
    UPSTREAM = "upstream"


@dataclass(frozen=True)
class RepoSpec:
    """One repository's identity in the constellation graph."""

    id: str
    name: str
    description: str
    repo_type: str  # "runtime" | "spec" | "library" | "android" | "wear-os" | "fork"
    role_in_constellation: str
    license_class: LicenseClass
    value_partition: ValuePartition
    license_posture: str
    reader_promise: str = ""
    claim_ceiling: str = ""
    primary_audience: tuple[str, ...] = ()
    surface_class: SurfaceClass = SurfaceClass.INTERNAL_APPARATUS
    visibility: RepoVisibility = RepoVisibility.PRIVATE
    source_of_truth: SourceOfTruth = SourceOfTruth.CONSTITUTION_REGISTRY
    public_files: tuple[str, ...] = ()
    dependency_order: int = 0
    dependencies: tuple[str, ...] = ()  # other repo ids this depends on
    topics: tuple[str, ...] = ()
    is_first_party: bool = True
    github_owner: str = DEFAULT_GITHUB_OWNER
    zenodo_concept_doi: str | None = None  # populated post-first-mint; None pre-mint
    related_identifiers: tuple[dict[str, str], ...] = field(default_factory=tuple)

    @property
    def github_url(self) -> str:
        """Canonical GitHub URL for this repository."""
        return github_repo_url(self.name, self.github_owner)


@dataclass(frozen=True)
class OperatorIdentity:
    """Operator's formal-context identity. Used only in author fields.

    Body text of every rendered file uses ``OperatorReferent`` instead.
    """

    full_name: str
    orcid: str | None
    contact_url: str  # operator-public URL, NOT email — Sigstore disclosure path
    omg_lol_address: str = "hapax"


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, RepoSpec]:
    """Load the repo registry from ``repos.yaml``."""
    text = path.read_text(encoding="utf-8")
    raw: dict[str, Any] = yaml.safe_load(text)
    raw_repos: dict[str, Any] = raw.get("repos", {})
    dependency_orders = _derive_dependency_orders(raw_repos)
    repos: dict[str, RepoSpec] = {}
    for repo_id, payload in raw_repos.items():
        if "dependency_order" in payload:
            raise ValueError(
                f"{repo_id}: dependency_order is derived from dependencies; remove the YAML field"
            )
        license_class = LicenseClass(payload["license_class"])
        value_partition = ValuePartition(
            payload.get(
                "value_partition",
                "upstream" if license_class is LicenseClass.UPSTREAM else "internal_apparatus",
            )
        )
        repos[repo_id] = RepoSpec(
            id=repo_id,
            name=payload["name"],
            description=payload["description"],
            repo_type=payload["repo_type"],
            role_in_constellation=payload["role_in_constellation"],
            license_class=license_class,
            value_partition=value_partition,
            license_posture=payload.get("license_posture", license_class.value),
            reader_promise=payload.get("reader_promise", ""),
            claim_ceiling=payload.get("claim_ceiling", ""),
            primary_audience=tuple(payload.get("primary_audience", [])),
            surface_class=SurfaceClass(
                payload.get(
                    "surface_class",
                    "upstream" if license_class is LicenseClass.UPSTREAM else "internal_apparatus",
                )
            ),
            visibility=RepoVisibility(
                payload.get(
                    "visibility",
                    "local_only" if license_class is LicenseClass.UPSTREAM else "private",
                )
            ),
            source_of_truth=SourceOfTruth(
                payload.get(
                    "source_of_truth",
                    "upstream"
                    if license_class is LicenseClass.UPSTREAM
                    else "constitution_registry",
                )
            ),
            public_files=tuple(payload.get("public_files", [])),
            dependency_order=dependency_orders[repo_id],
            dependencies=tuple(payload.get("dependencies", [])),
            topics=tuple(payload.get("topics", [])),
            is_first_party=payload.get("is_first_party", True),
            github_owner=payload.get("github_owner", DEFAULT_GITHUB_OWNER),
            zenodo_concept_doi=payload.get("zenodo_concept_doi"),
            related_identifiers=tuple(payload.get("related_identifiers", [])),
        )
    return repos


def _derive_dependency_orders(raw_repos: dict[str, Any]) -> dict[str, int]:
    """Return a dependency depth for each repo from the dependency graph.

    The field is intentionally not read from YAML. Repo-order-sensitive
    frontmatter and exports can sort by this derived depth and then by repo id
    without creating a second hand-maintained graph.
    """

    dependencies_by_id = {
        repo_id: tuple(payload.get("dependencies", [])) for repo_id, payload in raw_repos.items()
    }
    orders: dict[str, int] = {}
    visiting: set[str] = set()

    def visit(repo_id: str) -> int:
        if repo_id in orders:
            return orders[repo_id]
        if repo_id in visiting:
            raise ValueError(f"cyclic repository dependency graph at {repo_id}")
        if repo_id not in dependencies_by_id:
            raise ValueError(f"unknown repository dependency: {repo_id}")
        visiting.add(repo_id)
        dependency_depths = [visit(dep) for dep in dependencies_by_id[repo_id]]
        visiting.remove(repo_id)
        orders[repo_id] = 0 if not dependency_depths else max(dependency_depths) + 1
        return orders[repo_id]

    for repo_id in dependencies_by_id:
        visit(repo_id)
    return orders


def github_repo_url(repo_name: str, owner: str = DEFAULT_GITHUB_OWNER) -> str:
    """Return the canonical GitHub URL for a Hapax Systems repository."""
    return f"https://github.com/{owner}/{repo_name}"


def load_operator_identity(
    path: Path = OPERATOR_PATH,
    local_path: Path = OPERATOR_LOCAL_PATH,
) -> OperatorIdentity:
    """Load operator identity, preferring a gitignored local override."""
    target = local_path if local_path.exists() else path
    if not target.exists():
        # Render package must function without operator.yaml in CI; return
        # placeholder identity so dry-run / --check work.
        return OperatorIdentity(
            full_name="<operator-name-unset>",
            orcid=None,
            contact_url="https://example.invalid/contact",
        )
    raw = yaml.safe_load(target.read_text(encoding="utf-8")) or {}
    return OperatorIdentity(
        full_name=raw.get("full_name", "<operator-name-unset>"),
        orcid=raw.get("orcid"),
        contact_url=raw.get("contact_url", "https://example.invalid/contact"),
        omg_lol_address=raw.get("omg_lol_address", "hapax"),
    )
