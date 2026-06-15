"""Integration: a ResearchCase at R4 with a corroborated M run admits a claim; a
dissociated/undetermined/absent run does not, and a claim requiring a DARK gate never
admits — the fail-closed disposition path of the SCED loop."""

from datetime import datetime

from ndcvb.correspondent import Correspondent, CorrespondentStatus
from ndcvb.scorer import Measurement
from rdlc import ResearchCase, assertion_admitted
from rdlc.validity_gates import psi1_construct_validity, psi5_freeze_lock

PSI1 = "psi1_construct_validity"


def _r4_case() -> ResearchCase:
    return ResearchCase(
        case_id="rc",
        version=1,
        stage="R4_analysis",
        status="open",
        created_utc=datetime(2026, 1, 1),
        originator="operator",
        assertion_authorized=True,
        preregistration_record="osf:x",
        ruler_hash="h",
        criterion_ladder=[3.0, 3.5, 4.0],
        ndcvb_run_ref="run:1",
    )


def _measurement(agreement: float) -> Measurement:
    c = Correspondent("sycophancy", CorrespondentStatus.READY, substrate="diffmean")
    return Measurement(
        c, expressed_substrate_agreement=agreement, detection_bound=0.8, detection_floor=0.5
    )


def test_r4_case_is_structurally_clean():
    assert _r4_case().no_go_violations() == []


def test_corroborated_run_admits_claim():
    gate = psi1_construct_validity(_measurement(0.9))
    assert assertion_admitted([gate], required={PSI1}) is True


def test_dissociated_run_blocks_claim():
    gate = psi1_construct_validity(_measurement(0.1))
    assert assertion_admitted([gate], required={PSI1}) is False


def test_claim_requiring_dark_gate_never_admits():
    gate1 = psi1_construct_validity(_measurement(0.9))
    gate5 = psi5_freeze_lock()
    assert assertion_admitted([gate1, gate5], required={PSI1, "psi5_freeze_lock"}) is False


def test_no_run_means_no_admission():
    gate = psi1_construct_validity(None)
    assert assertion_admitted([gate], required={PSI1}) is False
