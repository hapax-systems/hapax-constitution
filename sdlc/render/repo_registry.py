"""Repository registry — single source of truth for per-repo metadata.

The constellation has nine repositories; seven are first-party, two are
upstream forks (tabbyAPI, atlas-voice-training) where this render
mechanism is intentionally inert (NOTICE.md is gitignored via
``.git/info/exclude`` per the operational checklist).

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


class LicenseClass(str, Enum):
    """License classes the renderer knows how to attribute."""

    POLYFORM_STRICT_1_0_0 = "PolyForm-Strict-1.0.0"
    CC_BY_NC_ND_4_0 = "CC-BY-NC-ND-4.0"
    MIT = "MIT"
    APACHE_2_0 = "Apache-2.0"
    CC_BY_SA_4_0 = "CC-BY-SA-4.0"
    UPSTREAM = "upstream"  # tabbyAPI / atlas-voice — preserve upstream license

    @property
    def is_first_party(self) -> bool:
        return self is not LicenseClass.UPSTREAM


@dataclass(frozen=True)
class RepoSpec:
    """One repository's identity in the constellation graph."""

    id: str
    name: str
    description: str
    repo_type: str  # "runtime" | "spec" | "library" | "android" | "wear-os" | "fork"
    role_in_constellation: str
    license_class: LicenseClass
    dependencies: tuple[str, ...] = ()  # other repo ids this depends on
    topics: tuple[str, ...] = ()
    is_first_party: bool = True
    zenodo_concept_doi: str | None = None  # populated post-first-mint; None pre-mint
    related_identifiers: tuple[dict[str, str], ...] = field(default_factory=tuple)


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
    repos: dict[str, RepoSpec] = {}
    for repo_id, payload in raw.get("repos", {}).items():
        license_class = LicenseClass(payload["license_class"])
        repos[repo_id] = RepoSpec(
            id=repo_id,
            name=payload["name"],
            description=payload["description"],
            repo_type=payload["repo_type"],
            role_in_constellation=payload["role_in_constellation"],
            license_class=license_class,
            dependencies=tuple(payload.get("dependencies", [])),
            topics=tuple(payload.get("topics", [])),
            is_first_party=payload.get("is_first_party", True),
            zenodo_concept_doi=payload.get("zenodo_concept_doi"),
            related_identifiers=tuple(payload.get("related_identifiers", [])),
        )
    return repos


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
