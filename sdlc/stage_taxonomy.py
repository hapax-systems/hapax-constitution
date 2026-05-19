"""AuthorityCase stage taxonomy — S0 through S11.

Each stage is a discrete state in the AuthorityCase lifecycle.
No stage implies the next; every transition requires explicit evidence.
"""

from __future__ import annotations

from enum import IntEnum


class Stage(IntEnum):
    S0_SCRATCH = 0
    S1_RESEARCH = 1
    S2_PLAN_DRAFT = 2
    S3_EXACT_REVIEW = 3
    S4_ACCEPTANCE_REVIEW = 4
    S5_AUTHORIZATION_PACKET = 5
    S6_IMPLEMENTATION = 6
    S7_VERIFICATION = 7
    S8_RELEASE = 8
    S9_RUNTIME_WITNESS = 9
    S10_PUBLIC_CURRENT = 10
    S11_CLOSURE = 11

    @classmethod
    def from_label(cls, label: str) -> Stage:
        """Parse a stage from its YAML label (e.g. 'S2_plan_draft')."""
        normalized = label.upper().replace("-", "_")
        for member in cls:
            if member.name == normalized:
                return member
            if normalized == f"S{member.value}":
                return member
        raise ValueError(f"Unknown stage: {label!r}")

    def allows_source_mutation(self) -> bool:
        return self == Stage.S6_IMPLEMENTATION

    def allows_release(self) -> bool:
        return self >= Stage.S8_RELEASE

    def requires_axiom_check(self) -> bool:
        return self in (
            Stage.S3_EXACT_REVIEW,
            Stage.S5_AUTHORIZATION_PACKET,
            Stage.S7_VERIFICATION,
        )
