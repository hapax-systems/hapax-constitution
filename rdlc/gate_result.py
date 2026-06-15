"""GateResult — a gate's outcome, with the {*} terminal-stalk theorem encoded as a
constructor invariant.

Only a LIT result may carry a ``Verdict``. DARK and PARTIAL are terminal stalks: carrying
a verdict on them is type-illegal and raises at construction. This makes "fake a dark
gate as a pass" *unconstructable* — the honest-dark rule enforced in code, not by
convention.

The ``Verdict`` type is NDCVB's; it is referenced only under ``TYPE_CHECKING`` (the
annotation is a string under ``from __future__ import annotations``), so this module has
no runtime ``ndcvb`` dependency — only ``m_binding`` binds M.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from rdlc.gate_status import GateStatus

if TYPE_CHECKING:
    from ndcvb.verdict import Verdict


@dataclass(frozen=True)
class GateResult:
    gate_id: str
    status: GateStatus
    verdict: Verdict | None = None

    def __post_init__(self) -> None:
        if self.status is GateStatus.LIT and self.verdict is None:
            raise ValueError(f"{self.gate_id}: LIT requires a Verdict")
        if self.status is not GateStatus.LIT and self.verdict is not None:
            raise ValueError(
                f"{self.gate_id}: {self.status.value} is a terminal stalk {{*}} and MUST NOT "
                "carry a verdict — fabricating one is type-illegal"
            )
