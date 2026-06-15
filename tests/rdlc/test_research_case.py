"""Φ — ResearchCase: claim-plant fields only (no SDLC verbs), fail-closed no-go
semantics, and structural honest-dark (phantom-freeze)."""

from datetime import datetime

from rdlc.r_stage import RStage
from rdlc.research_case import RESEARCH_NO_GO_FIELDS, ResearchCase


def _case(**kw):
    base = dict(
        case_id="rc1",
        version=0,
        stage="R0_question",
        status="open",
        created_utc=datetime(2026, 1, 1),
        originator="operator",
    )
    base.update(kw)
    return ResearchCase(**base)


def test_no_sdlc_no_go_fields():
    # Rule 2 (sibling, not child) enforced at the type level
    fields = set(ResearchCase.model_fields)
    assert "source_mutation_authorized" not in fields
    assert "release_authorized" not in fields
    assert "implementation_authorized" not in fields
    assert RESEARCH_NO_GO_FIELDS == ("assertion_authorized",)


def test_pre_r4_assertion_is_violation():
    c = _case(stage="R0_question", assertion_authorized=True)
    assert "assertion_authorized (pre-R4)" in c.no_go_violations()


def test_clean_r4_case_has_no_violations():
    c = _case(
        stage="R4_analysis",
        assertion_authorized=True,
        preregistration_record="osf:abc",
        ruler_hash="deadbeef",
    )
    assert c.no_go_violations() == []


def test_public_claim_requires_operator_ratification():
    c = _case(
        stage="R5_disposition",
        assertion_authorized=True,
        preregistration_record="osf:abc",
        ruler_hash="deadbeef",
        plan_ratified_by_operator=False,
    )
    assert any("public claim without operator" in v for v in c.no_go_violations())


def test_public_claim_with_ratification_is_clean():
    c = _case(
        stage="R5_disposition",
        assertion_authorized=True,
        preregistration_record="osf:abc",
        ruler_hash="deadbeef",
        plan_ratified_by_operator=True,
    )
    assert c.no_go_violations() == []


def test_phantom_freeze_is_violation():
    # post-freeze stage (R3+) without the frozen artifacts = honest-dark at the case layer
    c = _case(stage="R3_collection", assertion_authorized=False)
    assert any("phantom freeze" in v for v in c.no_go_violations())


def test_parsed_stage_returns_rstage():
    assert _case(stage="R4_analysis").parsed_stage() is RStage.R4_ANALYSIS


def test_from_yaml_parses_research_case():
    text = (
        "---\n"
        "case_id: rc2\n"
        "stage: R1_protocol\n"
        "status: open\n"
        "created_utc: 2026-06-15T00:00:00Z\n"
        "originator: operator\n"
        "---\n"
    )
    c = ResearchCase.from_yaml(text)
    assert c.case_id == "rc2"
    assert c.parsed_stage() is RStage.R1_PROTOCOL
