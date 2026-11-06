"""codemeta.json renderer (CodeMeta v3.0 JSON-LD).

Schema reference: codemeta.github.io. v3.0 ships JSON-LD with
schema.org alignment per researchsoft.org software-citation guidance.

Public repository metadata uses institutional authorship (Hapax Research Lab).
"""

from __future__ import annotations

import json

from sdlc.render.repo_registry import OperatorIdentity, RepoSpec, SurfaceClass

PUBLIC_CREATOR_NAME = "Hapax Research Lab"
PUBLIC_CREATOR_EMAIL = "hrl-han@hapaxresearch.com"
PUBLIC_CREATOR_URL = "https://hapaxresearch.com"


def render(repo: RepoSpec, identity: OperatorIdentity) -> str:
    """Return codemeta.json (JSON-LD) body for ``repo``."""
    author: dict[str, object] = {
        "@type": "Organization",
        "name": PUBLIC_CREATOR_NAME,
        "email": PUBLIC_CREATOR_EMAIL,
        "url": PUBLIC_CREATOR_URL,
    }
    public_url = (
        "https://hapax-systems.github.io/hapax-assets/"
        if repo.surface_class is SurfaceClass.ASSET_MIRROR
        else repo.github_url
    )

    codemeta: dict[str, object] = {
        "@context": "https://w3id.org/codemeta/3.0",
        "@type": "SoftwareSourceCode",
        "name": repo.name,
        "description": repo.description.strip(),
        "codeRepository": repo.github_url,
        "url": public_url,
        "license": _spdx_url(repo.license_class.value),
        "author": [author],
        "applicationCategory": _category_for(repo.repo_type),
        "developmentStatus": "inactive" if repo.archived else "active",
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
    if license_class == "CC-BY-4.0":
        return "https://creativecommons.org/licenses/by/4.0/"
    if license_class == "CC-BY-SA-4.0":
        return "https://creativecommons.org/licenses/by-sa/4.0/"
    if license_class == "CC0-1.0":
        return "https://creativecommons.org/publicdomain/zero/1.0/"
    return f"https://spdx.org/licenses/{license_class}.html"


def _category_for(repo_type: str) -> str:
    return {
        "runtime": "ResearchInfrastructure",
        "engine": "ResearchInfrastructure",
        "app": "DeveloperApplication",
        "spec": "Specification",
        "library": "SoftwareLibrary",
        "data": "Dataset",
        "android": "MobileApplication",
        "wear-os": "WearableApplication",
        "fork": "UpstreamFork",
    }.get(repo_type, "ResearchInfrastructure")


def _default_keywords() -> list[str]:
    return [
        "research-software",
        "philosophy-of-science",
        "governance",
        "infrastructure-as-argument",
    ]
