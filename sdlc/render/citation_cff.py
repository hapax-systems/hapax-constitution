"""CITATION.cff renderer (Citation File Format v1.2.0).

Schema reference: citation-file-format/citation-file-format#schema-guide
v1.2.0. Validates against the published JSON schema.

Public repository metadata uses organization authorship. Operator identity is
not emitted by default because first-party public surfaces are owned by
``hapax-systems``.
"""

from __future__ import annotations

import yaml

from sdlc.render.repo_registry import OperatorIdentity, RepoSpec

PUBLIC_CREATOR_NAME = "Hapax Systems"


def render(repo: RepoSpec, identity: OperatorIdentity) -> str:
    """Return a CITATION.cff body text for ``repo``."""
    cff: dict[str, object] = {
        "cff-version": "1.2.0",
        "message": ("If you use this software in your research, please cite it as below."),
        "type": "software",
        "title": repo.name,
        "abstract": repo.description.strip(),
        "authors": [{"name": PUBLIC_CREATOR_NAME}],
        "repository-code": repo.github_url,
        "url": repo.github_url,
        "license": _spdx_for_license(repo.license_class.value),
        "keywords": list(repo.topics) if repo.topics else _default_keywords(),
    }
    citation_doi = repo.zenodo_doi or repo.zenodo_concept_doi
    if citation_doi:
        cff["doi"] = citation_doi
        cff["identifiers"] = [
            {
                "type": "doi",
                "value": citation_doi,
                "description": "Zenodo repository snapshot DOI",
            }
        ]

    body = yaml.safe_dump(
        cff,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
        width=80,
    )
    return body


def _spdx_for_license(license_class: str) -> str:
    """Map LicenseClass values to SPDX identifiers used by CFF."""
    if license_class == "upstream":
        return "UPSTREAM"
    return license_class


def _default_keywords() -> list[str]:
    return [
        "research-software",
        "single-operator",
        "philosophy-of-science",
        "governance",
        "infrastructure-as-argument",
    ]
