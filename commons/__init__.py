"""Tier-0 commons — the shared functor base every governed lifecycle instantiates.

Currently the genuinely-shared, plant-agnostic pieces are the governance-case
spine and the ordinal-stage helper. ``RiskTier`` and the evidence ledger remain in
``sdlc/`` for now (their canonical home pending a governance-authorized extraction);
see ``rdlc``'s interim import note. Keep tier-0 pure: this package must never import
from a lifecycle (``sdlc``/``rdlc``) or a model (``ndcvb``).
"""

from commons.governance_case import BaseGovernanceCase
from commons.ordinal_stage import stage_from_label

__all__ = ["BaseGovernanceCase", "stage_from_label"]
