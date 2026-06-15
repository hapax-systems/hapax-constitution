"""Tests for the AuthorityCase schema, stage taxonomy, risk tiers, evidence
ledger, and validator CLI.

Canary: validates against the actual SDLC reform case files when available.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from sdlc.authority_case import AuthorityCase
from sdlc.evidence_ledger import EvidenceEntry, append_entry, read_entries, record_transition
from sdlc.risk_tier import RiskTier
from sdlc.stage_taxonomy import Stage
from sdlc.validator import validate_file


# --- Stage taxonomy ---


class TestStageTaxonomy:
    def test_stage_ordering(self) -> None:
        assert Stage.S0_SCRATCH < Stage.S6_IMPLEMENTATION < Stage.S11_CLOSURE

    def test_from_label_full(self) -> None:
        assert Stage.from_label("S2_PLAN_DRAFT") == Stage.S2_PLAN_DRAFT

    def test_from_label_short(self) -> None:
        assert Stage.from_label("S6") == Stage.S6_IMPLEMENTATION

    def test_from_label_case_insensitive(self) -> None:
        assert Stage.from_label("s3_exact_review") == Stage.S3_EXACT_REVIEW

    def test_from_label_unknown_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown stage"):
            Stage.from_label("S99")

    def test_source_mutation_only_at_s6(self) -> None:
        for s in Stage:
            if s == Stage.S6_IMPLEMENTATION:
                assert s.allows_source_mutation()
            else:
                assert not s.allows_source_mutation()

    def test_release_only_at_s8_plus(self) -> None:
        for s in Stage:
            if s >= Stage.S8_RELEASE:
                assert s.allows_release()
            else:
                assert not s.allows_release()

    def test_axiom_check_stages(self) -> None:
        axiom_stages = {s for s in Stage if s.requires_axiom_check()}
        assert axiom_stages == {
            Stage.S3_EXACT_REVIEW,
            Stage.S5_AUTHORIZATION_PACKET,
            Stage.S7_VERIFICATION,
        }


# --- Risk tiers ---


class TestRiskTier:
    def test_tier_ordering(self) -> None:
        assert RiskTier.T0_TRIVIAL < RiskTier.T3_CONSTITUTIONAL

    def test_from_label(self) -> None:
        assert RiskTier.from_label("T2") == RiskTier.T2_MODERATE
        assert RiskTier.from_label("T3_CONSTITUTIONAL") == RiskTier.T3_CONSTITUTIONAL

    def test_six_lane_review_threshold(self) -> None:
        assert not RiskTier.T0_TRIVIAL.requires_six_lane_review()
        assert not RiskTier.T1_LOW.requires_six_lane_review()
        assert RiskTier.T2_MODERATE.requires_six_lane_review()
        assert RiskTier.T3_CONSTITUTIONAL.requires_six_lane_review()


# --- AuthorityCase model ---


VALID_S2_FRONTMATTER = """\
---
case_id: CASE-TEST-001
version: 0
stage: S2_PLAN_DRAFT
status: plan_draft
created_utc: 2026-05-08T14:00:00Z
originator: test
source_mutation_authorized: false
docs_mutation_authorized: false
vault_mutation_authorized: false
implementation_authorized: false
release_authorized: false
public_current: false
axiom_mutation_authorized: false
plan_accepted: false
plan_grants_implementation_authority: false
---

# Test Case
"""

VALID_S6_FRONTMATTER = """\
---
case_id: CASE-TEST-002
version: 0
stage: S6_IMPLEMENTATION
status: implementing
created_utc: 2026-05-08T14:00:00Z
originator: test
risk_tier: T2
source_mutation_authorized: true
docs_mutation_authorized: true
vault_mutation_authorized: false
implementation_authorized: true
release_authorized: false
public_current: false
axiom_mutation_authorized: false
plan_accepted: true
plan_grants_implementation_authority: false
axiom_compliance_checked: true
axiom_compliance_result: "no violations"
---

# Implementation Case
"""


class TestAuthorityCaseModel:
    def test_valid_s2_case(self) -> None:
        case = AuthorityCase.from_yaml(VALID_S2_FRONTMATTER)
        assert case.case_id == "CASE-TEST-001"
        assert case.parsed_stage() == Stage.S2_PLAN_DRAFT
        assert not case.source_mutation_authorized
        assert not case.implementation_authorized
        assert case.no_go_violations() == []

    def test_valid_s6_case(self) -> None:
        case = AuthorityCase.from_yaml(VALID_S6_FRONTMATTER)
        assert case.parsed_stage() == Stage.S6_IMPLEMENTATION
        assert case.source_mutation_authorized
        assert case.no_go_violations() == []

    def test_fail_closed_defaults(self) -> None:
        """Omitted no-go fields default to True (dangerous) per fail-closed."""
        minimal = """\
---
case_id: CASE-MINIMAL
version: 0
stage: S0_SCRATCH
status: scratch
created_utc: 2026-05-08T00:00:00Z
originator: test
---
"""
        case = AuthorityCase.from_yaml(minimal)
        assert case.source_mutation_authorized is True
        assert case.implementation_authorized is True
        violations = case.no_go_violations()
        assert len(violations) > 0

    def test_source_mutation_at_wrong_stage_is_violation(self) -> None:
        bad = """\
---
case_id: CASE-BAD
version: 0
stage: S2_PLAN_DRAFT
status: draft
created_utc: 2026-05-08T00:00:00Z
originator: test
source_mutation_authorized: true
docs_mutation_authorized: false
vault_mutation_authorized: false
implementation_authorized: false
release_authorized: false
public_current: false
axiom_mutation_authorized: false
plan_accepted: false
plan_grants_implementation_authority: false
---
"""
        case = AuthorityCase.from_yaml(bad)
        violations = case.no_go_violations()
        assert "source_mutation_authorized" in violations

    def test_shadow_denial_violation(self) -> None:
        bad = """\
---
case_id: CASE-SHADOW
version: 0
stage: S4_ACCEPTANCE_REVIEW
status: accepted
created_utc: 2026-05-08T00:00:00Z
originator: test
source_mutation_authorized: false
docs_mutation_authorized: false
vault_mutation_authorized: false
implementation_authorized: false
release_authorized: false
public_current: false
axiom_mutation_authorized: false
plan_accepted: true
plan_grants_implementation_authority: true
---
"""
        case = AuthorityCase.from_yaml(bad)
        violations = case.no_go_violations()
        assert any("shadow-denial" in v for v in violations)

    def test_isap_at_s5_may_grant_mutation(self) -> None:
        """S5 authorization packets legitimately set source_mutation=true."""
        isap = """\
---
case_id: CASE-ISAP
version: 0
stage: S5_AUTHORIZATION_PACKET
status: authorized
created_utc: 2026-05-08T14:00:00Z
originator: test
risk_tier: T2
source_mutation_authorized: true
docs_mutation_authorized: true
vault_mutation_authorized: false
implementation_authorized: true
release_authorized: false
public_current: false
axiom_mutation_authorized: false
plan_accepted: true
plan_grants_implementation_authority: false
axiom_compliance_checked: true
---
"""
        case = AuthorityCase.from_yaml(isap)
        assert case.no_go_violations() == []

    def test_no_frontmatter_raises(self) -> None:
        with pytest.raises(ValueError, match="No YAML frontmatter"):
            AuthorityCase.from_yaml("# Just a heading")


# --- Evidence ledger ---


class TestEvidenceLedger:
    def test_append_and_read(self, tmp_path: Path) -> None:
        ledger = tmp_path / "ledger.jsonl"
        entry = EvidenceEntry(
            case_id="CASE-001",
            from_stage="S2_PLAN_DRAFT",
            to_stage="S3_EXACT_REVIEW",
            timestamp="2026-05-08T14:00:00Z",
            actor="beta",
            evidence_type="review_complete",
            evidence_summary="All 6 lanes returned",
            artifacts=["relay/lane-outputs/"],
        )
        append_entry(entry, ledger_path=ledger)
        entries = read_entries(ledger_path=ledger)
        assert len(entries) == 1
        assert entries[0].case_id == "CASE-001"

    def test_filter_by_case_id(self, tmp_path: Path) -> None:
        ledger = tmp_path / "ledger.jsonl"
        record_transition("CASE-A", "S0", "S1", "alpha", "init", "started", ledger_path=ledger)
        record_transition("CASE-B", "S0", "S1", "beta", "init", "started", ledger_path=ledger)
        a_entries = read_entries(case_id="CASE-A", ledger_path=ledger)
        assert len(a_entries) == 1
        assert a_entries[0].case_id == "CASE-A"

    def test_empty_ledger(self, tmp_path: Path) -> None:
        ledger = tmp_path / "nonexistent.jsonl"
        assert read_entries(ledger_path=ledger) == []

    def test_record_transition_returns_entry(self, tmp_path: Path) -> None:
        ledger = tmp_path / "ledger.jsonl"
        entry = record_transition(
            "CASE-X",
            "S5_AUTHORIZATION_PACKET",
            "S6_IMPLEMENTATION",
            "alpha",
            "isap_accepted",
            "ISAP reviewed and accepted",
            artifacts=["isap-slice1.md"],
            no_go_snapshot={"source_mutation_authorized": True},
            ledger_path=ledger,
        )
        assert entry.case_id == "CASE-X"
        assert entry.no_go_snapshot["source_mutation_authorized"] is True


# --- Validator CLI ---


class TestValidator:
    def test_valid_file_passes(self, tmp_path: Path) -> None:
        case_file = tmp_path / "case.md"
        case_file.write_text(VALID_S2_FRONTMATTER)
        issues = validate_file(case_file)
        assert issues == []

    def test_invalid_file_reports_issues(self, tmp_path: Path) -> None:
        case_file = tmp_path / "bad.md"
        case_file.write_text("not yaml at all")
        issues = validate_file(case_file)
        assert len(issues) > 0

    def test_strict_mode_catches_missing_fields(self, tmp_path: Path) -> None:
        minimal = """\
---
case_id: CASE-STRICT
version: 0
stage: S0_SCRATCH
status: scratch
created_utc: 2026-05-08T00:00:00Z
originator: test
---
"""
        case_file = tmp_path / "minimal.md"
        case_file.write_text(minimal)
        issues = validate_file(case_file, strict=True)
        missing = [i for i in issues if "missing no-go field" in i]
        assert len(missing) > 0

    def test_missing_file(self, tmp_path: Path) -> None:
        issues = validate_file(tmp_path / "ghost.md")
        assert any("cannot read" in i for i in issues)


# --- Canary: validate against actual SDLC reform case ---


_RELAY_DIR = Path(os.environ.get("HAPAX_RELAY_DIR", ""))
_SDLC_REFORM_PLAN = _RELAY_DIR / "sdlc-reform-authority-case-plan-draft-v0-20260508.md"
_SDLC_REFORM_ISAP = _RELAY_DIR / "isap-slice1-spec-schema-20260508.md"


class TestCanary:
    @pytest.mark.skipif(not _SDLC_REFORM_PLAN.exists(), reason="SDLC reform plan not on disk")
    def test_sdlc_reform_plan_parses(self) -> None:
        case = AuthorityCase.from_file(str(_SDLC_REFORM_PLAN))
        assert case.case_id == "CASE-SDLC-REFORM-001"
        assert not case.source_mutation_authorized
        assert not case.implementation_authorized

    @pytest.mark.skipif(not _SDLC_REFORM_ISAP.exists(), reason="ISAP Slice 1 not on disk")
    def test_sdlc_reform_isap_parses(self) -> None:
        case = AuthorityCase.from_file(str(_SDLC_REFORM_ISAP))
        assert case.case_id == "CASE-SDLC-REFORM-001"
        assert case.source_mutation_authorized
        assert case.implementation_authorized
        assert case.axiom_compliance_checked
        assert case.no_go_violations() == []
