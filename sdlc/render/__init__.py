"""hapax-sdlc render subpackage.

Single chokepoint for repo-presentation file generation across the nine
hapax constellation repositories. Per drop 4 §6 (consolidated GitHub
repo-presentation research, 2026-04-25), a render command rather than
nine hand-edited file-sets is the constitutional shape: full-automation,
single-source-of-truth, drift-detectable.

Public entry point::

    python -m hapax_sdlc.render --repo <id>            # render one repo
    python -m hapax_sdlc.render --all                  # render every repo
    python -m hapax_sdlc.render --repo <id> --check    # dry-run; exit 1 on drift
    python -m hapax_sdlc.render --repo <id> --dry-run  # print to stdout, write nothing

Implementation notes:

- ``repo_registry`` is the single source of truth for per-repo metadata.
  Operator-set fields (legal name, ORCID iD, email) live in
  ``operator_identity`` and are loaded lazily so tests do not depend on
  the operator's personal data being on disk.
- Each renderer is a pure function ``render(repo: RepoSpec, identity:
  OperatorIdentity) -> str`` returning the file body. Composition + write
  is handled by the CLI wrapper.
- ``OperatorReferent`` picker (parallel to council's
  ``shared.operator_referent``) supplies the sticky-per-document
  non-formal referent for body text. Legal name only appears in
  CITATION.cff ``authors:``, codemeta.json ``author:``, .zenodo.json
  ``creators:``.
"""

from sdlc.render.repo_registry import (
    LicenseClass,
    OperatorIdentity,
    RepoSpec,
    load_operator_identity,
    load_registry,
)

__all__ = [
    "LicenseClass",
    "OperatorIdentity",
    "RepoSpec",
    "load_operator_identity",
    "load_registry",
]
