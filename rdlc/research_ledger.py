"""The RDLC evidence ledger — a second ledger on the SAME append-only mechanism.

Reusing the mechanism verbatim — only the ledger PATH differs — is the proof the
commons is inherited, not re-invented.

INTERIM IMPORT NOTE: the ledger mechanism is plant-agnostic and belongs in ``commons``,
but currently lives in ``sdlc/``. Until the governance-authorized extraction, rdlc reuses
it from there (a sanctioned ``rdlc -> sdlc`` edge for a primitive). The follow-up
repoints this import to ``commons``.
"""

from __future__ import annotations

from pathlib import Path

from commons.evidence_ledger import (
    EvidenceEntry,
    append_entry,
    read_entries,
    record_transition,
)

DEFAULT_RESEARCH_LEDGER_PATH = Path("evidence/research-case-ledger.jsonl")

__all__ = [
    "DEFAULT_RESEARCH_LEDGER_PATH",
    "EvidenceEntry",
    "append_entry",
    "read_entries",
    "record_transition",
]
