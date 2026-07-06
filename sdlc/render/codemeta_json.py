"""codemeta.json renderer (CodeMeta v3.0 JSON-LD).

Schema reference: codemeta.github.io. v3.0 ships JSON-LD with
schema.org alignment per researchsoft.org 2026 software-citation
roadmap. v4 alignment is forward-compatible since renamed fields are
all additive.

The ``author`` block is one of the formal-address-required contexts per
the operator referent policy; legal name surfaces here.
"""

from __future__ import annotations

import json

from sdlc.render.repo_registry import OperatorIdentity, RepoSpec


def render(repo: RepoSpec, identity: OperatorIdentity) -> str:
    """Return codemeta.json (JSON-LD) body for ``repo``."""
    given, family = _split_name(identity.full_name)
    author: dict[str, object] = {
        "@type": "Person",
        "givenName": given,
        "familyName": family,
    }
    if identity.orcid:
        author["@id"] = identity.orcid

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
    if repo.zenodo_concept_doi:
        codemeta["identifier"] = f"https://doi.org/{repo.zenodo_concept_doi}"
    if repo.related_identifiers:
        codemeta["relatedLink"] = [
            ri["identifier"] for ri in repo.related_identifiers if ri.get("scheme") == "url"
        ]

    return json.dumps(codemeta, indent=2, ensure_ascii=False) + "\n"


def _split_name(full_name: str) -> tuple[str, str]:
    parts = full_name.strip().split()
    if not parts:
        return ("", "")
    if len(parts) == 1:
        return (parts[0], "")
    return (" ".join(parts[:-1]), parts[-1])


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
