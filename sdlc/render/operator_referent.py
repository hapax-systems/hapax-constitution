"""Institutional referent picker (constitution-side mirror).

Under A16 and HACA-SENDER-DETERMINATION-R3, all public-facing institutional
attributions use ``Hapax Research Lab`` and ``hrl-han`` exclusively. Legacy
Era I personal or pseudonymous referents are retired and never emitted.
"""

from __future__ import annotations

import hashlib

REFERENTS: tuple[str, ...] = (
    "Hapax Research Lab",
    "hrl-han",
)


class OperatorReferentPicker:
    """Deterministic sticky-per-repository institutional referent picker."""

    @staticmethod
    def pick_for_artifact(repo_id: str) -> str:
        """Sticky-per-repo. Same repo id -> same referent across all render
        targets within that repo's pass.
        """
        digest = hashlib.sha256(f"repo-pres-{repo_id}".encode("utf-8")).hexdigest()
        idx = int(digest, 16) % len(REFERENTS)
        return REFERENTS[idx]
