""".zenodo.json renderer.

Schema reference: developers.zenodo.org. The ``related_identifiers``
block carries the DataCite RelatedIdentifier graph that federates the
constellation into DataCite Commons / ORCID without touching social
platforms. Per drop 4 (cross-account-promotion), this is the highest-
leverage academic-spectacle mechanic.

The ``creators:`` block is the third formal-address-required context;
legal name surfaces here. ORCID iD is included when present so the
auto-update bridge to the operator's ORCID record fires on first mint.

REFUSED-status anti-patterns (Bandcamp/Discogs/RYM, etc.) get registered
here as DataCite ``IsObsoletedBy`` relations per the
``xprom-refusal-as-related-identifier`` cc-task.
"""

from __future__ import annotations

import json

from sdlc.render.repo_registry import OperatorIdentity, RepoSpec


def render(repo: RepoSpec, identity: OperatorIdentity) -> str:
    """Return .zenodo.json body for ``repo``."""
    creator: dict[str, object] = {"name": identity.full_name}
    if identity.orcid:
        # Zenodo expects bare ORCID (no URL prefix) here.
        orcid_bare = identity.orcid.replace("https://orcid.org/", "")
        creator["orcid"] = orcid_bare

    related: list[dict[str, str]] = []
    for ri in repo.related_identifiers:
        related.append(
            {
                "identifier": ri["identifier"],
                "relation": ri["relation"],
                "scheme": ri.get("scheme", "url"),
            }
        )

    body: dict[str, object] = {
        "title": repo.name,
        "description": repo.description.strip(),
        "creators": [creator],
        "license": _zenodo_license(repo.license_class.value),
        "access_right": "open",
        "upload_type": _upload_type(repo.repo_type),
        "keywords": list(repo.topics) if repo.topics else _default_keywords(),
        "related_identifiers": related,
        "communities": [{"identifier": "hapax-publications"}],
    }
    if repo.repo_type == "spec":
        body["upload_type"] = "publication"
        body["publication_type"] = "other"

    return json.dumps(body, indent=2, ensure_ascii=False) + "\n"


def _zenodo_license(license_class: str) -> str:
    """Zenodo accepts SPDX identifiers; map the registry's enum values."""
    if license_class == "upstream":
        return "UPSTREAM"
    return license_class


def _upload_type(repo_type: str) -> str:
    return {
        "runtime": "software",
        "spec": "publication",
        "library": "software",
        "android": "software",
        "wear-os": "software",
        "fork": "software",
    }.get(repo_type, "software")


def _default_keywords() -> list[str]:
    return [
        "research-software",
        "single-operator",
        "philosophy-of-science",
        "governance",
        "infrastructure-as-argument",
    ]
