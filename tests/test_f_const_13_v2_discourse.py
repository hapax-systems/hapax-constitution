"""Tests for F-CONST-13 v2 Full-Spectrum Governed Autonomous Discourse & DI-01 v2."""

from __future__ import annotations

from pathlib import Path

from commons.discourse_policy import (
    AUTHORIZED_ACTIONS,
    COURTESY_NOTICE_MAX_PER_EXAMINATION,
    DI01_V2_SCHEMA,
    OUTCOME_1_SYMMETRY_FLOOR,
    RULE_VERSION,
    VENUE_POSTURE_MATRIX,
    VenuePosture,
    validate_di01_v2_receipt,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def _valid_receipt(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "schema_version": DI01_V2_SCHEMA,
        "receipt_id": "DI01V2-20261106-0001",
        "timestamp_utc": "2026-11-06T02:40:00Z",
        "venue": "bluesky_atproto",
        "action_kind": "quote",
        "actor_principal": "hrl-han",
        "draft_sha256": "a" * 64,
        "bound_witness_refs": [
            "585bdaf333a09d0b111d9753bafd55d7c481121adfa39eeeb1c1810d5edf088c"
        ],
        "excluded_vendor_families": ["openai"],
        "quorum_verdict": "PASS",
        "dh3_status": "PASS",
        "c384_clean": True,
        "tos_mode": "official_xrpc_bot_labeled",
    }
    base.update(overrides)
    return base


def test_f_const_13_v2_governance_doc_present_and_hygienic() -> None:
    doc_path = REPO_ROOT / "docs" / "governance" / "f-const-13-v2-autonomous-discourse-20261106.md"
    assert doc_path.is_file()
    text = doc_path.read_text(encoding="utf-8")
    assert chr(36) not in text
    assert "F-CONST-13 v2" in text
    assert "DI-01-F-CONST-13-v2" in text
    assert "Hapax Research LLC" in text
    assert "OUTCOME_1" in text
    assert "C-384" in text
    assert "D-H3" in text
    assert "CHANC" in text
    assert "Hacker News" in text


def test_constants_and_full_spectrum_actions() -> None:
    assert RULE_VERSION == "F-CONST-13-v2"
    assert OUTCOME_1_SYMMETRY_FLOOR == 0.15
    assert COURTESY_NOTICE_MAX_PER_EXAMINATION == 1
    for required in (
        "follow",
        "curate_list",
        "post",
        "repost",
        "quote",
        "comment",
        "reply",
        "multi_turn_followup",
        "courtesy_correspondence",
    ):
        assert required in AUTHORIZED_ACTIONS


def test_valid_di01_v2_receipt_passes() -> None:
    verdict = validate_di01_v2_receipt(_valid_receipt())
    assert verdict.valid
    assert verdict.errors == ()


def test_hacker_news_blocks_outbound_writes() -> None:
    assert VENUE_POSTURE_MATRIX["hacker_news"] is VenuePosture.READ_ONLY_SENSORIUM
    blocked = validate_di01_v2_receipt(_valid_receipt(venue="hacker_news", action_kind="comment"))
    assert not blocked.valid
    assert "venue_read_only_violation:hacker_news:comment" in blocked.errors

    sense_ok = validate_di01_v2_receipt(_valid_receipt(venue="hacker_news", action_kind="sense"))
    assert sense_ok.valid


def test_principal_isolation_and_c384_and_dh3_enforced() -> None:
    bad_actor = validate_di01_v2_receipt(_valid_receipt(actor_principal="personal-user"))
    assert not bad_actor.valid
    assert "principal_isolation_violation:actor_must_be_hrl_han" in bad_actor.errors

    bad_c384 = validate_di01_v2_receipt(_valid_receipt(c384_clean=False))
    assert not bad_c384.valid
    assert "c384_commercial_firewall_violation" in bad_c384.errors

    bad_dh3 = validate_di01_v2_receipt(_valid_receipt(dh3_status="FAIL"))
    assert not bad_dh3.valid
    assert "dh3_gate_not_passed" in bad_dh3.errors
