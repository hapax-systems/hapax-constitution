"""The RDLC ledger is a second ledger on the same append-only mechanism, isolated
from the authority-case ledger by path."""

from pathlib import Path

from rdlc.research_ledger import (
    DEFAULT_RESEARCH_LEDGER_PATH,
    read_entries,
    record_transition,
)


def test_default_path_is_distinct_research_ledger():
    assert DEFAULT_RESEARCH_LEDGER_PATH == Path("evidence/research-case-ledger.jsonl")


def test_record_and_read_isolated(tmp_path):
    p = tmp_path / "research-case-ledger.jsonl"
    record_transition(
        "rc1",
        "R1_protocol",
        "R2_preregister",
        "operator",
        "preregistration",
        "froze protocol",
        ledger_path=p,
    )
    entries = read_entries(ledger_path=p)
    assert len(entries) == 1
    assert entries[0].case_id == "rc1"
    assert entries[0].to_stage == "R2_preregister"
