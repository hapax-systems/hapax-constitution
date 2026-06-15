"""Ξ — the RDLC ladder (R0..R5) over the claim-assertion plant.

DISPOSITION-first: these predicates adjudicate *what may be claimed/asserted*, never
code mutation. There is deliberately **no** ``allows_source_mutation``/``allows_release``
here — those are SDLC-plant verbs; their presence would be the sibling-not-child
category error. R2 is RDLC's analogue of SDLC's S5 authorization-packet stage: the one
stage permitted to flip downstream authorizations (by committing the frozen protocol).
"""

from __future__ import annotations

from enum import IntEnum

from commons.ordinal_stage import stage_from_label


class RStage(IntEnum):
    R0_QUESTION = 0  # open question — no claim, no protocol (honest-dark default)
    R1_PROTOCOL = 1  # study design drafted (DV=ruler, IV=criterion ladder, analysis, threats)
    R2_PREREGISTER = 2  # protocol FROZEN: ruler-hash + criterion-ladder + registration committed
    R3_COLLECTION = 3  # data collection under the frozen protocol
    R4_ANALYSIS = 4  # analysis; M=NDCVB reads here; ψ validity gates convene
    R5_DISPOSITION = 5  # claim adjudicated (publishable / null / undetermined); operator ratify

    @classmethod
    def from_label(cls, label: str) -> RStage:
        return stage_from_label(cls, label, prefix="R")

    def allows_data_collection(self) -> bool:
        return self == RStage.R3_COLLECTION

    def allows_analysis(self) -> bool:
        return self == RStage.R4_ANALYSIS

    def allows_public_claim(self) -> bool:
        return self >= RStage.R5_DISPOSITION

    def requires_freeze_intact(self) -> bool:
        # Goodhart guard: once collection starts, the frozen protocol must be present
        return self >= RStage.R3_COLLECTION

    def requires_validity_gates(self) -> bool:
        return self in (RStage.R4_ANALYSIS, RStage.R5_DISPOSITION)
