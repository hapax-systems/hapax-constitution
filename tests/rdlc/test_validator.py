"""The ResearchCase CLI validator: a clean R4 case passes; a pre-R4 case with the
dangerous default flags a no-go violation."""

from pathlib import Path

from rdlc.validator import validate_file

_CLEAN_R4 = (
    "---\n"
    "case_id: rc-clean\n"
    "stage: R4_analysis\n"
    "status: open\n"
    "created_utc: 2026-06-15T00:00:00Z\n"
    "originator: operator\n"
    "assertion_authorized: true\n"
    "preregistration_record: osf:abc\n"
    "ruler_hash: deadbeef\n"
    "---\n"
)

_DIRTY_R0 = (
    "---\n"
    "case_id: rc-dirty\n"
    "stage: R0_question\n"
    "status: open\n"
    "created_utc: 2026-06-15T00:00:00Z\n"
    "originator: operator\n"
    "assertion_authorized: true\n"
    "---\n"
)


def test_clean_r4_case_passes(tmp_path: Path):
    f = tmp_path / "clean.md"
    f.write_text(_CLEAN_R4, encoding="utf-8")
    assert validate_file(f) == []


def test_pre_r4_assertion_flagged(tmp_path: Path):
    f = tmp_path / "dirty.md"
    f.write_text(_DIRTY_R0, encoding="utf-8")
    issues = validate_file(f)
    assert any("assertion_authorized (pre-R4)" in i for i in issues)


def test_missing_file_is_reported():
    issues = validate_file(Path("/nonexistent/research-case.md"))
    assert issues and "cannot read file" in issues[0]
