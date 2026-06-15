"""Risk tier classification for AuthorityCases.

T0 = trivial (typo fix, comment update)
T1 = low (single-file implementation, no enforcement change)
T2 = moderate (enforcement change, multi-file, reversible)
T3 = constitutional (governance spec, axiom modification, cross-repo)
"""

from __future__ import annotations

from enum import IntEnum


class RiskTier(IntEnum):
    T0_TRIVIAL = 0
    T1_LOW = 1
    T2_MODERATE = 2
    T3_CONSTITUTIONAL = 3

    @classmethod
    def from_label(cls, label: str) -> RiskTier:
        normalized = label.upper().replace("-", "_")
        for member in cls:
            if member.name == normalized:
                return member
            if normalized == f"T{member.value}":
                return member
        raise ValueError(f"Unknown risk tier: {label!r}")

    def requires_six_lane_review(self) -> bool:
        return self >= RiskTier.T2_MODERATE

    def requires_axiom_scan(self) -> bool:
        return self >= RiskTier.T2_MODERATE
