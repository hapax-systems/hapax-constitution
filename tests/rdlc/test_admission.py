"""β admission is fail-closed: a claim is assertable iff every required gate is LIT and
CORROBORATED; absence, DARK, PARTIAL, UNDETERMINED, DISSOCIATED all fail."""

from ndcvb.verdict import Verdict, VerdictKind
from rdlc.admission import assertion_admitted
from rdlc.gate_result import GateResult
from rdlc.gate_status import GateStatus

PSI1 = "psi1_construct_validity"


def _lit(kind, bound, gid=PSI1):
    return GateResult(gid, GateStatus.LIT, verdict=Verdict(kind, bound, "sycophancy"))


def test_admits_when_required_gate_lit_and_corroborated():
    assert assertion_admitted([_lit(VerdictKind.CORROBORATED, 0.9)], required={PSI1}) is True


def test_rejects_dissociated():
    assert assertion_admitted([_lit(VerdictKind.DISSOCIATED, 0.9)], required={PSI1}) is False


def test_rejects_undetermined():
    assert assertion_admitted([_lit(VerdictKind.UNDETERMINED, None)], required={PSI1}) is False


def test_rejects_absent_required_gate():
    assert assertion_admitted([], required={PSI1}) is False


def test_rejects_when_a_required_gate_is_dark():
    required = {PSI1, "psi5_freeze_lock"}
    results = [_lit(VerdictKind.CORROBORATED, 0.9), GateResult("psi5_freeze_lock", GateStatus.DARK)]
    assert assertion_admitted(results, required=required) is False


def test_rejects_partial():
    results = [GateResult("psi2_preregistration", GateStatus.PARTIAL)]
    assert assertion_admitted(results, required={"psi2_preregistration"}) is False
