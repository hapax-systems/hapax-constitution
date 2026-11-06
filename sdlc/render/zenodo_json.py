""".zenodo.json renderer.

Schema reference: developers.zenodo.org. The ``related_identifiers``
block carries the DataCite RelatedIdentifier graph across the public
portfolio and portal surfaces.

The ``creators:`` block uses institutional authorship (Hapax Research Lab)
for public repository metadata.
"""

from __future__ import annotations

import json

from sdlc.render.repo_registry import OperatorIdentity, RepoSpec

PUBLIC_CREATOR_NAME = "Hapax Research Lab"


def render(repo: RepoSpec, identity: OperatorIdentity) -> str:
    """Return .zenodo.json body for ``repo``."""
    creator: dict[str, object] = {"name": PUBLIC_CREATOR_NAME}

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
    }
    if repo.zenodo_doi:
        body["doi"] = repo.zenodo_doi
    if repo.zenodo_concept_doi:
        body["conceptdoi"] = repo.zenodo_concept_doi
    if notes := _license_notes(repo.license_class.value):
        body["notes"] = notes
    if repo.repo_type == "spec":
        body["upload_type"] = "publication"
        body["publication_type"] = "other"

    return json.dumps(body, indent=2, ensure_ascii=False) + "\n"


def _zenodo_license(license_class: str) -> str:
    """Zenodo accepts SPDX identifiers; map the registry's enum values."""
    if license_class == "upstream":
        return "UPSTREAM"
    if license_class in {"PolyForm-Strict-1.0.0", "BUSL-1.1"}:
        return "other-closed"
    return license_class


def _license_notes(license_class: str) -> str | None:
    if license_class == "PolyForm-Strict-1.0.0":
        return (
            "Repository license: PolyForm Strict 1.0.0 "
            "(https://polyformproject.org/licenses/strict/1.0.0/)."
        )
    if license_class == "BUSL-1.1":
        return (
            "Repository license: Business Source License 1.1 (source-available, "
            "non-Open-Source until the Change Date converts the work to Apache-2.0; "
            "source inspection is open while competing hosted-service use remains reserved)."
        )
    return None


def _upload_type(repo_type: str) -> str:
    return {
        "runtime": "software",
        "engine": "software",
        "app": "software",
        "spec": "publication",
        "library": "software",
        "data": "dataset",
        "android": "software",
        "wear-os": "software",
        "fork": "software",
    }.get(repo_type, "software")


def _default_keywords() -> list[str]:
    return [
        "research-software",
        "philosophy-of-science",
        "governance",
        "infrastructure-as-argument",
    ]
