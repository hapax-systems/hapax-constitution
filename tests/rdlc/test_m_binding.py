"""M binding: a measured negative (UNDETERMINED) is the instrument WORKING -> LIT;
DARK is reserved for "no M here" (no run, or a not-scorable correspondent)."""

from ndcvb.correspondent import Correspondent, CorrespondentStatus
from ndcvb.scorer import Measurement
from ndcvb.verdict import VerdictKind
from rdlc.gate_status import GateStatus
from rdlc.m_binding import construct_validity_gate


def _scorable():
    return Correspondent("sycophancy", CorrespondentStatus.READY, substrate="diffmean")


def _corroborated():
    return Measurement(
        _scorable(), expressed_substrate_agreement=0.9, detection_bound=0.8, detection_floor=0.5
    )


def _below_floor():
    return Measurement(
        _scorable(), expressed_substrate_agreement=0.9, detection_bound=0.3, detection_floor=0.5
    )


def _frontier():
    fr = Correspondent("experiential", CorrespondentStatus.FRONTIER)
    return Measurement(
        fr, expressed_substrate_agreement=0.9, detection_bound=0.8, detection_floor=0.5
    )


def test_no_run_is_per_case_dark():
    r = construct_validity_gate(None)
    assert r.status is GateStatus.DARK
    assert r.verdict is None


def test_corroborated_run_is_lit():
    r = construct_validity_gate(_corroborated())
    assert r.status is GateStatus.LIT
    assert r.verdict.kind is VerdictKind.CORROBORATED


def test_measured_negative_is_lit_not_dark():
    r = construct_validity_gate(_below_floor())
    assert r.status is GateStatus.LIT  # the instrument ran — a measured negative is LIT
    assert r.verdict.kind is VerdictKind.UNDETERMINED


def test_not_scorable_correspondent_is_dark():
    r = construct_validity_gate(_frontier())
    assert r.status is GateStatus.DARK  # no validated substrate -> no M here
