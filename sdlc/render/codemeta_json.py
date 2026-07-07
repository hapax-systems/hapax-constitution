"""codemeta.json renderer (CodeMeta v3.0 JSON-LD).

Schema reference: codemeta.github.io. v3.0 ships JSON-LD with
schema.org alignment per researchsoft.org 2026 software-citation
roadmap. v4 alignment is forward-compatible since renamed fields are
all additive.

Public repository metadata uses organization authorship. Operator identity is
not emitted by default because first-party public surfaces are owned by
``hapax-systems``.
"""

from __future__ import annotations

import json

from sdlc.render.repo_registry import OperatorIdentity, RepoSpec

PUBLIC_CREATOR_NAME = "Hapax Systems"


def render(repo: RepoSpec, identity: OperatorIdentity) -> str:
    """Return codemeta.json (JSON-LD) body for ``repo``."""
    author: dict[str, object] = {
        "@type": "Organization",
        "name": PUBLIC_CREATOR_NAME,
        "url": "https://github.com/hapax-systems",
    }

    codemeta: dict[str, object] = {
        "@context": "https://w3id.org/codemeta/3.0",
        "@type": "SoftwareSourceCode",
        "name": repo.name,
        "description": repo.description.strip(),
        "codeRepository": repo.github_url,
        "url": repo.github_url,
        "license": _spdx_url(repo.license_class.value),
        "author": [author],
        "applicationCategory": _category_for(repo.repo_type),
        "developmentStatus": "active",
        "isAccessibleForFree": True,
        "keywords": list(repo.topics) if repo.topics else _default_keywords(),
    }
    citation_doi = repo.zenodo_doi or repo.zenodo_concept_doi
    if citation_doi:
        codemeta["identifier"] = f"https://doi.org/{citation_doi}"
    if repo.related_identifiers:
        codemeta["relatedLink"] = [
            ri["identifier"] for ri in repo.related_identifiers if ri.get("scheme") == "url"
        ]

    return json.dumps(codemeta, indent=2, ensure_ascii=False) + "\n"


def _spdx_url(license_class: str) -> str:
    if license_class == "upstream":
        return "UPSTREAM"
    if license_class == "PolyForm-Strict-1.0.0":
        return "https://polyformproject.org/licenses/strict/1.0.0/"
    if license_class == "CC-BY-NC-ND-4.0":
        return "https://creativecommons.org/licenses/by-nc-nd/4.0/"
    if license_class == "CC-BY-SA-4.0":
        return "https://creativecommons.org/licenses/by-sa/4.0/"
    return f"https://spdx.org/licenses/{license_class}"


def _category_for(repo_type: str) -> str:
    return {
        "runtime": "ResearchInfrastructure",
        "spec": "Specification",
        "library": "SoftwareLibrary",
        "android": "MobileApplication",
        "wear-os": "WearableApplication",
        "fork": "UpstreamFork",
    }.get(repo_type, "ResearchInfrastructure")


def _default_keywords() -> list[str]:
    return [
        "research-software",
        "single-operator",
        "philosophy-of-science",
        "governance",
        "infrastructure-as-argument",
    ]
