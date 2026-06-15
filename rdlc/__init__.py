"""RDLC — the Research Development Life Cycle regulator's interior blocks.

A sibling lifecycle of SDLC over the *claim-assertion* plant, instantiating the tier-0
``commons``. Interior blocks: Φ=``ResearchCase``, Ξ=``RStage``, ψ=``validity_gates``,
M=NDCVB (bound via ``m_binding``), β=``admission``. Rendered honest-dark — only blocks
that exist are lit; the binder/face/cockpit are out of scope.
"""

from rdlc.admission import assertion_admitted
from rdlc.gate_result import GateResult
from rdlc.gate_status import GateStatus
from rdlc.m_binding import construct_validity_gate
from rdlc.r_stage import RStage
from rdlc.research_case import RESEARCH_NO_GO_FIELDS, ResearchCase
from rdlc.research_ledger import DEFAULT_RESEARCH_LEDGER_PATH

__all__ = [
    "RStage",
    "ResearchCase",
    "RESEARCH_NO_GO_FIELDS",
    "GateStatus",
    "GateResult",
    "construct_validity_gate",
    "assertion_admitted",
    "DEFAULT_RESEARCH_LEDGER_PATH",
]
