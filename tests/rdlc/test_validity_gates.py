"""The honest gate ledger: with a bound run, exactly 1 LIT (ψ1), 3 PARTIAL (ψ2–4),
2 DARK (ψ5–6). RDLC is off the dark stalk only via ψ1=M."""

from collections import Counter

from ndcvb.correspondent import Correspondent, CorrespondentStatus
from ndcvb.scorer import Measurement
from rdlc import validity_gates as vg
from rdlc.gate_status import GateStatus


def _measurement():
    c = Correspondent("sycophancy", CorrespondentStatus.READY, substrate="diffmean")
    return Measurement(
        c, expressed_substrate_agreement=0.9, detection_bound=0.8, detection_floor=0.5
    )


def test_psi1_per_case_dark_without_run():
    assert vg.psi1_construct_validity(None).status is GateStatus.DARK


def test_psi1_lit_with_run():
    assert vg.psi1_construct_validity(_measurement()).status is GateStatus.LIT


def test_psi2_3_4_are_partial():
    assert vg.psi2_preregistration().status is GateStatus.PARTIAL
    assert vg.psi3_null_results_publish().status is GateStatus.PARTIAL
    assert vg.psi4_goodhart_guard().status is GateStatus.PARTIAL


def test_psi5_6_are_dark():
    assert vg.psi5_freeze_lock().status is GateStatus.DARK
    assert vg.psi6_reflexive_dogfood().status is GateStatus.DARK


def test_honest_dark_ledger_counts():
    results = [
        vg.psi1_construct_validity(_measurement()),
        vg.psi2_preregistration(),
        vg.psi3_null_results_publish(),
        vg.psi4_goodhart_guard(),
        vg.psi5_freeze_lock(),
        vg.psi6_reflexive_dogfood(),
    ]
    counts = Counter(r.status for r in results)
    assert counts[GateStatus.LIT] == 1
    assert counts[GateStatus.PARTIAL] == 3
    assert counts[GateStatus.DARK] == 2
