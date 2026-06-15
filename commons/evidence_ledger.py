"""Append-only evidence ledger for AuthorityCase gate transitions.

Every stage transition records an entry with the evidence justifying the
transition. The ledger is JSONL (one JSON object per line) for atomic
append and git-friendly diffs.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel

log = logging.getLogger(__name__)

DEFAULT_LEDGER_PATH = Path("evidence/authority-case-ledger.jsonl")


class EvidenceEntry(BaseModel):
    case_id: str
    from_stage: str
    to_stage: str
    timestamp: str
    actor: str
    evidence_type: str
    evidence_summary: str
    artifacts: list[str] = []
    no_go_snapshot: dict[str, bool] = {}

    model_config = {"extra": "allow"}


def append_entry(
    entry: EvidenceEntry,
    *,
    ledger_path: Path | None = None,
) -> None:
    """Append a single evidence entry to the ledger file."""
    path = ledger_path or DEFAULT_LEDGER_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(entry.model_dump_json() + "\n")


def read_entries(
    *,
    case_id: str | None = None,
    ledger_path: Path | None = None,
) -> list[EvidenceEntry]:
    """Read all entries, optionally filtered by case_id."""
    path = ledger_path or DEFAULT_LEDGER_PATH
    if not path.exists():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8").strip().splitlines():
        if not line.strip():
            continue
        entry = EvidenceEntry.model_validate_json(line)
        if case_id is None or entry.case_id == case_id:
            entries.append(entry)
    return entries


def record_transition(
    case_id: str,
    from_stage: str,
    to_stage: str,
    actor: str,
    evidence_type: str,
    evidence_summary: str,
    *,
    artifacts: list[str] | None = None,
    no_go_snapshot: dict[str, bool] | None = None,
    ledger_path: Path | None = None,
) -> EvidenceEntry:
    """Record a stage transition in the evidence ledger."""
    entry = EvidenceEntry(
        case_id=case_id,
        from_stage=from_stage,
        to_stage=to_stage,
        timestamp=datetime.now(UTC).isoformat(),
        actor=actor,
        evidence_type=evidence_type,
        evidence_summary=evidence_summary,
        artifacts=artifacts or [],
        no_go_snapshot=no_go_snapshot or {},
    )
    append_entry(entry, ledger_path=ledger_path)
    return entry
