"""M — the binding to the NDCVB instrument (RDLC's derived internal model).

This is the ONLY module in ``rdlc`` that touches ``ndcvb``. It calls the instrument's
``score()`` and lifts its native ``Verdict`` into a ``GateResult``; it re-derives nothing
(no shadow M'). The import is lazy, so the governance package never hard-depends on the
research repo: if the instrument is not installed, M is honestly DARK, not an import
crash.

Honest-dark discipline (the per-case rule): M is LIT *as a capability* — the instrument
is built and validated — but a GIVEN ResearchCase is per-case DARK on ψ1 until a real
``Measurement`` is bound (no run -> no input -> stalk). So ``construct_validity_gate(None)``
is DARK, never a fabricated pass.

LIT-vs-DARK (the load-bearing distinction): a MEASURED NEGATIVE (DISSOCIATED /
UNDETERMINED) is the instrument WORKING -> LIT + verdict (admission then fails on
``kind != CORROBORATED``). DARK is reserved strictly for "no M exists here" — instrument
absent, correspondent not scorable, or the substrate is a prompt artifact. Conflating
"the model failed the check" with "the check does not exist" would re-fake the dark stalk.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rdlc.gate_result import GateResult
from rdlc.gate_status import GateStatus

if TYPE_CHECKING:
    from ndcvb.scorer import Measurement

GATE_ID = "psi1_construct_validity"


def construct_validity_gate(measurement: Measurement | None) -> GateResult:
    """ψ1's evaluator: call the instrument, lift its Verdict into a GateResult."""
    # per-case-dark: no measurement bound yet -> a stalk, not a pass
    if measurement is None:
        return GateResult(GATE_ID, GateStatus.DARK)
    try:
        from ndcvb.correspondent import NotScorableError
        from ndcvb.scorer import InvalidSubstrateError, score
    except ImportError:
        # the instrument is not wired into this environment -> honest dark, not a crash
        return GateResult(GATE_ID, GateStatus.DARK)
    try:
        verdict = score(measurement)  # ndcvb owns ALL decision logic
    except (NotScorableError, InvalidSubstrateError):
        # not scorable / substrate is an artifact -> no M here -> honest dark
        return GateResult(GATE_ID, GateStatus.DARK)
    return GateResult(GATE_ID, GateStatus.LIT, verdict=verdict)
