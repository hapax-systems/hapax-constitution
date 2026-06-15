"""AuthorityCase Pydantic model — the canonical schema for SDLC governance.

Every meaningful change in Hapax gets an AuthorityCase proportional to risk.
The model validates YAML frontmatter from case files and ISAPs.
"""

from __future__ import annotations


from pydantic import Field

from commons.governance_case import BaseGovernanceCase
from .risk_tier import RiskTier
from .stage_taxonomy import Stage

NO_GO_FIELDS = (
    "source_mutation_authorized",
    "docs_mutation_authorized",
    "vault_mutation_authorized",
    "implementation_authorized",
    "release_authorized",
    "public_current",
    "axiom_mutation_authorized",
)


class AuthorityCase(BaseGovernanceCase):
    """Canonical AuthorityCase schema.

    Validates the frontmatter of case YAML files. Fail-closed: omitting
    a no-go field is treated as if it were true (the dangerous default).
    """

    source_mutation_authorized: bool = Field(default=True)
    docs_mutation_authorized: bool = Field(default=True)
    vault_mutation_authorized: bool = Field(default=True)
    implementation_authorized: bool = Field(default=True)
    release_authorized: bool = Field(default=True)
    public_current: bool = Field(default=True)
    axiom_mutation_authorized: bool = Field(default=True)

    plan_accepted: bool = False
    plan_grants_implementation_authority: bool = Field(default=True)

    source_mutation_scope: str | None = None
    docs_mutation_scope: str | None = None
    implementation_scope: str | None = None

    axiom_compliance_checked: bool = False
    axiom_compliance_result: str | None = None
    consent_contract_required: bool | None = None
    consent_contract_reason: str | None = None

    model_config = {"extra": "allow"}

    def parsed_stage(self) -> Stage:
        return Stage.from_label(self.stage)

    def parsed_risk_tier(self) -> RiskTier | None:
        if self.risk_tier is None:
            return None
        return RiskTier.from_label(self.risk_tier)

    def no_go_violations(self) -> list[str]:
        """Return no-go fields that are dangerously true for the current stage.

        S5 (authorization-packet) is allowed to set source/docs/implementation
        authorized=true — that is the purpose of an ISAP. All other pre-S6
        stages must have those fields false.
        """
        violations = []
        stage = self.parsed_stage()
        is_isap = stage == Stage.S5_AUTHORIZATION_PACKET

        if not stage.allows_source_mutation() and not is_isap:
            if self.source_mutation_authorized:
                violations.append("source_mutation_authorized")
            if self.docs_mutation_authorized:
                violations.append("docs_mutation_authorized")
        if not stage.allows_release() and self.release_authorized:
            violations.append("release_authorized")
        if stage < Stage.S10_PUBLIC_CURRENT and self.public_current:
            violations.append("public_current")
        if (
            stage < Stage.S5_AUTHORIZATION_PACKET
            and self.plan_accepted
            and self.plan_grants_implementation_authority
        ):
            violations.append(
                "plan_grants_implementation_authority (shadow-denial: "
                "plan acceptance never grants implementation)"
            )
        if self.axiom_mutation_authorized and not self.axiom_compliance_checked:
            violations.append("axiom_mutation_authorized (without axiom_compliance_checked)")

        return violations
