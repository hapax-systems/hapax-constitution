"""Φ — ResearchCase: the claim-assertion plant interface.

A SIBLING of ``AuthorityCase`` over the *claim-assertion* plant ("what may be
claimed"), inheriting the tier-0 ``BaseGovernanceCase`` spine. It carries claim-plant
content ONLY — it must NOT carry SDLC's code-mutation no-go fields
(``source_mutation_authorized`` etc.); that would be the sibling-not-child category
error, and the abstract base structurally has no slot for them.

Honest-dark by default is structural: with ``preregistration_record=None`` and an empty
``criterion_ladder``, the R5 freeze-lock is DARK until a real registration fires. There
is no ``freeze_lock_fired`` bool to flip into a fake green — freeze is provable only by
the presence of the frozen artifacts.

INTERIM IMPORT NOTE: ``RiskTier`` is plant-agnostic and belongs in ``commons``, but it
currently lives in ``sdlc/`` (its canonical home pending a governance-authorized
extraction). Until then ``ResearchCase`` imports it from ``sdlc.risk_tier``; this is the
one sanctioned ``rdlc -> sdlc`` edge for a primitive (alongside the ledger), enforced by
the import-graph lint. The follow-up extraction repoints it to ``commons``.
"""

from __future__ import annotations

from pydantic import Field

from commons.governance_case import BaseGovernanceCase
from rdlc.r_stage import RStage
from sdlc.risk_tier import RiskTier  # interim: see module note

RESEARCH_NO_GO_FIELDS = ("assertion_authorized",)


class ResearchCase(BaseGovernanceCase):
    """Claim-assertion plant case. Fail-closed: ``assertion_authorized`` defaults True."""

    # the one no-go (dangerous default True; the substantive gate is rdlc.admission)
    assertion_authorized: bool = Field(default=True)

    # claim scoping (claim-plant analogue of AuthorityCase's mutation scopes)
    claim_scope: str | None = None
    publication_scope: str | None = None  # private / studio / public

    # R2 freeze block (SCED "pre-registration = freeze"); empty => freeze DARK by default
    preregistration_record: str | None = None  # OSF id or signed SHA
    ruler_hash: str | None = None  # frozen DV / scoring-instrument hash
    criterion_ladder: list[float] = Field(default_factory=list)  # committed C_k IV steps
    deviation_log: str | None = None

    # M binding ref (Rule 4 — a reference, NOT a reimplementation of the instrument).
    # NOTE: there is deliberately no experiential field; encoding one is type-illegal
    # under ndcvb's verdict guard.
    ndcvb_run_ref: str | None = None

    # β edge (operator)
    plan_ratified_by_operator: bool = False

    def parsed_stage(self) -> RStage:
        return RStage.from_label(self.stage)

    def parsed_risk_tier(self) -> RiskTier | None:
        if self.risk_tier is None:
            return None
        return RiskTier.from_label(self.risk_tier)

    def no_go_violations(self) -> list[str]:
        """Cheap fail-closed structural check (the substantive ψ allow-list is admission).

        Catches the stage-illegal assertion flag and the phantom-freeze (claiming a
        post-freeze stage without the frozen artifacts — honest-dark at the case layer).
        """
        violations: list[str] = []
        stage = self.parsed_stage()

        if stage < RStage.R4_ANALYSIS and self.assertion_authorized:
            violations.append("assertion_authorized (pre-R4)")
        if (
            self.assertion_authorized
            and stage.allows_public_claim()
            and not self.plan_ratified_by_operator
        ):
            violations.append("assertion_authorized (public claim without operator β-ratification)")
        if stage.requires_freeze_intact() and not (self.preregistration_record and self.ruler_hash):
            violations.append(
                "post-freeze stage without a frozen registration+ruler (phantom freeze)"
            )
        return violations
