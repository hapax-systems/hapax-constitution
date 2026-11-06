"""Shared governance primitives for Hapax Research Lab specifications."""

from __future__ import annotations

from commons.discourse_policy import (
    DI01_V2_SCHEMA,
    RULE_VERSION,
    VenuePosture,
    validate_di01_v2_receipt,
)
from commons.governance_case import BaseGovernanceCase
from commons.ordinal_stage import stage_from_label

__all__ = [
    "BaseGovernanceCase",
    "DI01_V2_SCHEMA",
    "RULE_VERSION",
    "VenuePosture",
    "stage_from_label",
    "validate_di01_v2_receipt",
]
