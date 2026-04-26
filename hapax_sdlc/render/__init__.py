"""hapax_sdlc.render — published-package alias for sdlc.render.

Re-exports the rendering API under the canonical ``hapax_sdlc.render``
import path. CLI entry point ``python -m hapax_sdlc.render`` delegates
to ``sdlc.render.cli``.
"""

from sdlc.render import (
    citation_cff,
    cli,
    codemeta_json,
    contributing_md,
    governance_md,
    notice_md,
    operator_referent,
    readme_section,
    repo_registry,
    repo_settings,
    security_md,
    zenodo_json,
)
from sdlc.render.cli import main
from sdlc.render.repo_registry import (
    LicenseClass,
    OperatorIdentity,
    RepoSpec,
    load_operator_identity,
    load_registry,
)
from sdlc.render.repo_settings import (
    DriftReport,
    RepoSettings,
    detect_drift,
    first_party_repos,
)

__all__ = [
    "DriftReport",
    "LicenseClass",
    "OperatorIdentity",
    "RepoSettings",
    "RepoSpec",
    "citation_cff",
    "cli",
    "codemeta_json",
    "contributing_md",
    "detect_drift",
    "first_party_repos",
    "governance_md",
    "load_operator_identity",
    "load_registry",
    "main",
    "notice_md",
    "operator_referent",
    "readme_section",
    "repo_registry",
    "repo_settings",
    "security_md",
    "zenodo_json",
]
