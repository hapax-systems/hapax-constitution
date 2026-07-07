"""Canonical repo-presentation export.

This module is the compatibility bridge for downstream tools that should not
re-implement or copy ``repos.yaml``. It emits plain JSON-serializable data from
the typed registry plus the settings policy.
"""

from __future__ import annotations

from typing import Any

from sdlc.render.org_profile_readme import ORG_PROFILE_PATH
from sdlc.render.repo_registry import RepoSpec, RepoVisibility, SurfaceClass, load_registry
from sdlc.render.repo_settings import desired_settings

SCHEMA_VERSION = 1

GENERATED_ARTIFACTS: tuple[str, ...] = (
    "CITATION.cff",
    "codemeta.json",
    ".zenodo.json",
    "NOTICE.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "SUPPORT.md",
    "GOVERNANCE.md",
    ".github/ISSUE_TEMPLATE/config.yml",
    "README.md",
)


def build_export(registry: dict[str, RepoSpec] | None = None) -> dict[str, Any]:
    """Build a JSON-serializable canonical export for repo-presentation tools."""
    registry = registry or load_registry()
    repos = [
        _repo_to_export(repo)
        for repo in sorted(
            registry.values(),
            key=lambda r: (r.dependency_order, r.id),
        )
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "source": "hapax-constitution:sdlc/render/repos.yaml",
        "generated_artifacts": list(GENERATED_ARTIFACTS),
        "settings_policy": {
            "issues": "redirect",
            "wiki": "disabled_except_hapax_constitution",
            "projects": "disabled",
            "discussions": "disabled",
            "funding": "no_perk_research_support_only",
        },
        "organization_profile": {
            "repository": "hapax-systems/.github",
            "path": ORG_PROFILE_PATH,
            "source": "hapax-constitution:sdlc.render.org_profile_readme",
        },
        "repos": repos,
    }


def _repo_to_export(repo: RepoSpec) -> dict[str, Any]:
    settings = desired_settings(repo) if repo.is_first_party else None
    return {
        "id": repo.id,
        "name": repo.name,
        "github_owner": repo.github_owner,
        "github_url": repo.github_url,
        "description": repo.description,
        "repo_type": repo.repo_type,
        "role_in_constellation": repo.role_in_constellation,
        "license_class": repo.license_class.value,
        "value_partition": repo.value_partition.value,
        "license_posture": repo.license_posture,
        "reader_promise": repo.reader_promise,
        "claim_ceiling": repo.claim_ceiling,
        "primary_audience": list(repo.primary_audience),
        "surface_class": repo.surface_class.value,
        "visibility": repo.visibility.value,
        "source_of_truth": repo.source_of_truth.value,
        "public_files": list(repo.public_files),
        "dependency_order": repo.dependency_order,
        "dependencies": list(repo.dependencies),
        "topics": list(repo.topics),
        "is_first_party": repo.is_first_party,
        "zenodo_doi": repo.zenodo_doi,
        "zenodo_concept_doi": repo.zenodo_concept_doi,
        "related_identifiers": list(repo.related_identifiers),
        "generated_artifacts": list(GENERATED_ARTIFACTS) if repo.is_first_party else [],
        "github_settings": None
        if settings is None
        else {
            "has_issues": settings.has_issues,
            "has_wiki": settings.has_wiki,
            "has_projects": settings.has_projects,
            "has_discussions": settings.has_discussions,
        },
        "support_posture": support_posture(repo),
    }


def support_posture(repo: RepoSpec) -> str:
    """Return the compact support/intake posture for exported frontmatter data."""
    if not repo.is_first_party or repo.surface_class is SurfaceClass.UPSTREAM:
        return "upstream_preserved"
    if repo.surface_class is SurfaceClass.ADOPTION_COMMONS:
        return "bounded_adoption_redirect"
    if repo.visibility is RepoVisibility.PUBLIC:
        return "inspection_citation_redirect"
    return "internal_redirect"


__all__ = ["GENERATED_ARTIFACTS", "SCHEMA_VERSION", "build_export", "support_posture"]
