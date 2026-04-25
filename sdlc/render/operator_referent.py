"""Non-formal operator referent picker (constitution-side mirror).

Parallels ``hapax-council/shared/operator_referent.py``. Sticky-per-document:
seeded from ``repo_id``, so the same repo's CITATION.cff body, NOTICE.md
body, README preamble, etc. all use the *same* referent for that repo's
render pass. Different repos get independent referents.

Per directive 2026-04-24, body text in ALL non-formal contexts uses one
of four referents. Legal name is restricted to formal-address fields:
CITATION.cff ``authors:``, codemeta.json ``author:``, .zenodo.json
``creators:``.
"""

from __future__ import annotations

import hashlib

REFERENTS: tuple[str, ...] = (
    "The Operator",
    "Oudepode",
    "Oudepode The Operator",
    "OTO",
)


class OperatorReferentPicker:
    """Equal-weighted picker over the four ratified operator referents."""

    @staticmethod
    def pick_for_artifact(repo_id: str) -> str:
        """Sticky-per-repo. Same repo id → same referent across all render
        targets within that repo's pass.
        """
        digest = hashlib.sha256(f"repo-pres-{repo_id}".encode("utf-8")).hexdigest()
        idx = int(digest, 16) % len(REFERENTS)
        return REFERENTS[idx]
