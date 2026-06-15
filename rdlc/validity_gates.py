"""ψ — the RDLC validity-gate set, each with its HONEST status.

Net: 1 LIT (ψ1, M-bound, per-case), 3 PARTIAL (ψ2–4: machinery exists at M but no
RDLC-level enforcement yet), 2 DARK (ψ5 freeze-lock never fired; ψ6 reflexive-dogfood is
vapor). RDLC is off the dark stalk only via ψ1=M — exactly the honest accounting the
framework requires. None of these fabricate a pass; the dark gates return DARK and claim
no protection.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rdlc.gate_result import GateResult
from rdlc.gate_status import GateStatus
from rdlc.m_binding import construct_validity_gate

if TYPE_CHECKING:
    from ndcvb.scorer import Measurement


def psi1_construct_validity(measurement: Measurement | None) -> GateResult:
    """ψ1 — construct validity via M=NDCVB. LIT as a capability; per-case-dark until a run binds."""
    return construct_validity_gate(measurement)


def psi2_preregistration() -> GateResult:
    """ψ2 — pre-registration. PARTIAL: the artifact exists as documents, but there is no mechanical
    check yet that the freeze PRECEDES collection."""
    return GateResult("psi2_preregistration", GateStatus.PARTIAL)


def psi3_null_results_publish() -> GateResult:
    """ψ3 — null-results-publish. PARTIAL: M already emits UNDETERMINED/DISSOCIATED first-class, but
    no RDLC ledger policy yet FORCES a null into the record."""
    return GateResult("psi3_null_results_publish", GateStatus.PARTIAL)


def psi4_goodhart_guard() -> GateResult:
    """ψ4 — Goodhart/gaming guard. PARTIAL: the confound gate lives inside M (scorer Gate 4 +
    layer-0); the RDLC-level probeset-drift guard does not exist yet. Not double-counted as a
    second firewall."""
    return GateResult("psi4_goodhart_guard", GateStatus.PARTIAL)


def psi5_freeze_lock() -> GateResult:
    """ψ5 — the R5 freeze-lock. DARK: it has never fired (no implementation). Its first firing is
    its own acceptance test before it can be trusted."""
    return GateResult("psi5_freeze_lock", GateStatus.DARK)


def psi6_reflexive_dogfood() -> GateResult:
    """ψ6 — the reflexive-dogfood gate. DARK: vapor (it was misattributed in prior work). No
    protection is claimed."""
    return GateResult("psi6_reflexive_dogfood", GateStatus.DARK)
