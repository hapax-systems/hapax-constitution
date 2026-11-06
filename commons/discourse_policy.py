"""Constitutional policy constants and validator for F-CONST-13 v2 & DI-01 v2."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

RULE_VERSION: Final[str] = "F-CONST-13-v2"
DI01_V2_SCHEMA: Final[str] = "DI-01-F-CONST-13-v2"
OUTCOME_1_SYMMETRY_FLOOR: Final[float] = 0.15
COURTESY_NOTICE_MAX_PER_EXAMINATION: Final[int] = 1


class VenuePosture(StrEnum):
    """Constitutional automation posture per external venue under F-CONST-13 v2."""

    FULL_TWO_WAY_HACA = "full_two_way_haca"
    READ_ONLY_SENSORIUM = "read_only_sensorium"
    MODERATOR_CLEARANCE_REQUIRED = "moderator_clearance_required"


VENUE_POSTURE_MATRIX: Final[dict[str, VenuePosture]] = {
    "bluesky_atproto": VenuePosture.FULL_TWO_WAY_HACA,
    "x_api_v2": VenuePosture.FULL_TWO_WAY_HACA,
    "activitypub_mastodon": VenuePosture.FULL_TWO_WAY_HACA,
    "github_machine_account": VenuePosture.FULL_TWO_WAY_HACA,
    "huggingface_bot_account": VenuePosture.FULL_TWO_WAY_HACA,
    "hrl_han_authenticated_email": VenuePosture.FULL_TWO_WAY_HACA,
    "hacker_news": VenuePosture.READ_ONLY_SENSORIUM,
    "lesswrong_forum_magnum": VenuePosture.MODERATOR_CLEARANCE_REQUIRED,
}

AUTHORIZED_ACTIONS: Final[frozenset[str]] = frozenset(
    {
        "sense",
        "follow",
        "curate_list",
        "post",
        "repost",
        "quote",
        "comment",
        "reply",
        "multi_turn_followup",
        "courtesy_correspondence",
    }
)

REQUIRED_DI01_V2_FIELDS: Final[tuple[str, ...]] = (
    "schema_version",
    "receipt_id",
    "timestamp_utc",
    "venue",
    "action_kind",
    "actor_principal",
    "draft_sha256",
    "bound_witness_refs",
    "excluded_vendor_families",
    "quorum_verdict",
    "dh3_status",
    "c384_clean",
    "tos_mode",
)


@dataclass(frozen=True)
class DiscourseReceiptValidation:
    """Validation verdict for a machine-emitted DI-01 v2 receipt."""

    valid: bool
    errors: tuple[str, ...]


def validate_di01_v2_receipt(payload: dict[str, object]) -> DiscourseReceiptValidation:
    """Validate a DI-01 v2 receipt against F-CONST-13 v2 constitutional locks."""
    errors: list[str] = []
    for field_name in REQUIRED_DI01_V2_FIELDS:
        if field_name not in payload:
            errors.append(f"missing_field:{field_name}")

    if payload.get("schema_version") != DI01_V2_SCHEMA:
        errors.append("invalid_schema_version")

    venue = str(payload.get("venue") or "")
    action = str(payload.get("action_kind") or "")
    posture = VENUE_POSTURE_MATRIX.get(venue)
    if posture is None:
        errors.append(f"unknown_venue:{venue}")
    elif posture is VenuePosture.READ_ONLY_SENSORIUM and action != "sense":
        errors.append(f"venue_read_only_violation:{venue}:{action}")

    if action and action not in AUTHORIZED_ACTIONS:
        errors.append(f"unauthorized_action:{action}")

    if payload.get("actor_principal") != "hrl-han":
        errors.append("principal_isolation_violation:actor_must_be_hrl_han")

    if payload.get("dh3_status") != "PASS":
        errors.append("dh3_gate_not_passed")

    if payload.get("c384_clean") is not True:
        errors.append("c384_commercial_firewall_violation")

    if action != "sense" and payload.get("quorum_verdict") != "PASS":
        errors.append("quorum_not_passed")

    return DiscourseReceiptValidation(valid=not errors, errors=tuple(errors))
