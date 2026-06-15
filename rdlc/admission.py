"""β-consumer — fail-closed admission of a claim against its required ψ-gates.

A claim is assertable iff EVERY required gate is LIT and CORROBORATED. Absence, DARK,
PARTIAL, UNDETERMINED, and DISSOCIATED all fail. Gate status is read by identity (never
``bool()``-coerced); the verdict kind is compared by its value string so this module
needs no ``ndcvb`` import (only ``m_binding`` binds M).

The ``required`` set is the per-case ψ-set the operator ratifies (the β / RATIFY edge). A
claim that lists a DARK gate (e.g. ``psi5_freeze_lock``) in ``required`` is never
admissible until that gate first fires — "first firing is its own acceptance test"
encoded as a hard dependency.
"""

from __future__ import annotations

from collections.abc import Iterable

from rdlc.gate_result import GateResult
from rdlc.gate_status import GateStatus

# the legal "pass" verdict kind, by value (avoids importing ndcvb here)
_CORROBORATED_VALUE = "corroborated"


def assertion_admitted(results: Iterable[GateResult], *, required: set[str]) -> bool:
    """Return True iff every required gate is LIT and CORROBORATED."""
    by_id = {r.gate_id: r for r in results}
    for gate_id in required:
        result = by_id.get(gate_id)
        if result is None:
            return False  # absence is a stalk, not a pass
        if result.status is not GateStatus.LIT:
            return False
        if result.verdict is None:
            return False
        if result.verdict.kind.value != _CORROBORATED_VALUE:
            return False
    return True
