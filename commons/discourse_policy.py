"""Constitutional policy constants and validators for F-CONST-13 v2.1 & DI-01 v2.1."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Final

RULE_VERSION: Final[str] = "F-CONST-13-v2.1"
DI01_V2_SCHEMA: Final[str] = "DI-01-F-CONST-13-v2.1"
ACCEPTED_DI01_SCHEMAS: Final[frozenset[str]] = frozenset(
    {"DI-01-F-CONST-13-v2.1", "DI-01-F-CONST-13-v2"}
)
OUTCOME_1_SYMMETRY_FLOOR: Final[float] = 0.15
COUNTENANCE_FOLLOWUP_DAYS: Final[tuple[int, int]] = (7, 14)
ALLOWED_HUB_TOKEN_PRINCIPALS: Final[frozenset[str]] = frozenset({"hrl-han", "hrl-han[bot]"})


class VenuePosture(StrEnum):
    """Constitutional automation posture per external venue under F-CONST-13 v2.1."""

    FULL_TWO_WAY_HACA = "full_two_way_haca"
    READ_ONLY_SENSORIUM = "read_only_sensorium"
    MODERATOR_CLEARANCE_REQUIRED = "moderator_clearance_required"


class DiscursiveRole(StrEnum):
    """Canonical discursive role for named public addressees in an HIEH Kategoria."""

    ORIGINAL_CLAIMANT = "original_claimant"
    CONTRA_DECLINIST_AMPLIFIER = "contra_declinist_amplifier"
    DECLINIST_DISSENTER = "declinist_dissenter"


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
        "kategoria_notice",
        "countenance_followup",
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
    """Validation verdict for a machine-emitted DI-01 v2.1 receipt."""

    valid: bool
    errors: tuple[str, ...]


@dataclass(frozen=True)
class KategoriaDirectAddressValidation:
    """Validation verdict for an HIEH Canonical Kategoria Direct-Address payload."""

    valid: bool
    errors: tuple[str, ...]


def validate_kategoria_direct_address(payload: Mapping[str, object]) -> KategoriaDirectAddressValidation:
    """Enforce F-CONST-13 v2.1 Canonical Kategoria Direct-Address fields on HIEH events."""
    errors: list[str] = []
    addressed = payload.get("addressed_to")
    if not isinstance(addressed, Sequence) or isinstance(addressed, (str, bytes)) or len(addressed) == 0:
        errors.append("kategoria_missing_addressed_to")
    else:
        valid_roles = {r.value for r in DiscursiveRole}
        for idx, entry in enumerate(addressed):
            if not isinstance(entry, Mapping):
                errors.append(f"kategoria_invalid_addressee:{idx}")
                continue
            name = str(entry.get("entity_name") or "").strip()
            role = str(entry.get("discursive_role") or "").strip()
            if not name:
                errors.append(f"kategoria_empty_entity_name:{idx}")
            if role not in valid_roles:
                errors.append(f"kategoria_invalid_discursive_role:{role}")

    for field_name in ("third_way_frame_hook", "question_on_the_record", "revision_trigger"):
        val = str(payload.get(field_name) or "").strip()
        if len(val) < 12:
            errors.append(f"kategoria_missing_{field_name}")

    return KategoriaDirectAddressValidation(valid=not errors, errors=tuple(errors))


def validate_di01_v2_receipt(payload: dict[str, object]) -> DiscourseReceiptValidation:
    """Validate a DI-01 v2.1 receipt against F-CONST-13 v2.1 constitutional locks."""
    errors: list[str] = []
    for field_name in REQUIRED_DI01_V2_FIELDS:
        if field_name not in payload:
            errors.append(f"missing_field:{field_name}")

    if str(payload.get("schema_version") or "") not in ACCEPTED_DI01_SCHEMAS:
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

    verified_hub_actor = payload.get("verified_token_actor")
    if verified_hub_actor is not None and venue in {"github_machine_account", "huggingface_bot_account"}:
        if str(verified_hub_actor).strip() not in ALLOWED_HUB_TOKEN_PRINCIPALS:
            errors.append("principal_isolation_violation:personal_hub_token_blocked")

    if payload.get("dh3_status") != "PASS":
        errors.append("dh3_gate_not_passed")

    if payload.get("c384_clean") is not True:
        errors.append("c384_commercial_firewall_violation")

    if action != "sense" and payload.get("quorum_verdict") != "PASS":
        errors.append("quorum_not_passed")

    if payload.get("is_hieh_campaign") is True:
        kat = validate_kategoria_direct_address(payload)
        errors.extend(kat.errors)

    return DiscourseReceiptValidation(valid=not errors, errors=tuple(errors))
