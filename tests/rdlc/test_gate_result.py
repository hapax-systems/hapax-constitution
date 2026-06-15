"""The decisive honest-dark canary: a DARK/PARTIAL GateResult carrying a verdict is
UNCONSTRUCTABLE (the {*} terminal-stalk theorem encoded as a constructor invariant)."""

import pytest

from ndcvb.verdict import Verdict, VerdictKind
from rdlc.gate_result import GateResult
from rdlc.gate_status import GateStatus


def _verdict():
    return Verdict(kind=VerdictKind.CORROBORATED, bound=0.9, correspondent="sycophancy")


def test_lit_requires_a_verdict():
    with pytest.raises(ValueError):
        GateResult("g", GateStatus.LIT)


def test_dark_carrying_a_verdict_is_type_illegal():
    with pytest.raises(ValueError, match="type-illegal"):
        GateResult("g", GateStatus.DARK, verdict=_verdict())


def test_partial_carrying_a_verdict_is_type_illegal():
    with pytest.raises(ValueError, match="type-illegal"):
        GateResult("g", GateStatus.PARTIAL, verdict=_verdict())


def test_dark_without_verdict_is_a_stalk():
    r = GateResult("g", GateStatus.DARK)
    assert r.status is GateStatus.DARK
    assert r.verdict is None


def test_lit_with_verdict_is_valid():
    v = _verdict()
    r = GateResult("g", GateStatus.LIT, verdict=v)
    assert r.verdict is v
