"""CITATION.cff renderer (Citation File Format v1.2.0).

Schema reference: citation-file-format/citation-file-format#schema-guide
v1.2.0. Validates against the published JSON schema.

The ``authors:`` block is the only place legal name surfaces in body
fields; this is a formal-address-required context per the operator
referent policy. ORCID iD is included when known.
"""

from __future__ import annotations

import yaml

from sdlc.render.repo_registry import OperatorIdentity, RepoSpec


def render(repo: RepoSpec, identity: OperatorIdentity) -> str:
    """Return a CITATION.cff body text for ``repo``."""
    given, family = _split_name(identity.full_name)
    author_block: dict[str, str] = {"given-names": given, "family-names": family}
    if identity.orcid:
        author_block["orcid"] = identity.orcid

    cff: dict[str, object] = {
        "cff-version": "1.2.0",
        "message": ("If you use this software in your research, please cite it as below."),
        "type": "software",
        "title": repo.name,
        "abstract": repo.description.strip(),
        "authors": [author_block],
        "repository-code": f"https://github.com/ryanklee/{repo.name}",
        "url": f"https://github.com/ryanklee/{repo.name}",
        "license": _spdx_for_license(repo.license_class.value),
        "keywords": list(repo.topics) if repo.topics else _default_keywords(),
    }
    if repo.zenodo_concept_doi:
        cff["doi"] = repo.zenodo_concept_doi
        cff["identifiers"] = [
            {
                "type": "doi",
                "value": repo.zenodo_concept_doi,
                "description": "Concept DOI (resolves to latest version)",
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


def _split_name(full_name: str) -> tuple[str, str]:
    """Split ``"Given Family"`` style names into the CFF given/family pair."""
    parts = full_name.strip().split()
    if not parts:
        return ("", "")
    if len(parts) == 1:
        return (parts[0], "")
    return (" ".join(parts[:-1]), parts[-1])


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
