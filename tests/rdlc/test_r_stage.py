"""Ξ — the RStage ladder: members, label parsing, claim-plant predicates, and the
absence of SDLC-plant verbs (sibling, not child)."""

import pytest

from rdlc.r_stage import RStage


def test_members_are_r0_through_r5():
    assert [s.value for s in RStage] == [0, 1, 2, 3, 4, 5]


def test_from_label_by_name():
    assert RStage.from_label("R2_preregister") is RStage.R2_PREREGISTER


def test_from_label_by_number():
    assert RStage.from_label("R4") is RStage.R4_ANALYSIS


def test_from_label_rejects_sdlc_stage():
    # an SDLC stage label is not an RDLC stage — the ladders are distinct plants
    with pytest.raises(ValueError):
        RStage.from_label("S6_implementation")


def test_claim_plant_predicates():
    assert RStage.R3_COLLECTION.allows_data_collection()
    assert not RStage.R4_ANALYSIS.allows_data_collection()
    assert RStage.R4_ANALYSIS.allows_analysis()
    assert RStage.R5_DISPOSITION.allows_public_claim()
    assert not RStage.R4_ANALYSIS.allows_public_claim()
    assert RStage.R3_COLLECTION.requires_freeze_intact()
    assert not RStage.R2_PREREGISTER.requires_freeze_intact()
    assert RStage.R4_ANALYSIS.requires_validity_gates()
    assert RStage.R5_DISPOSITION.requires_validity_gates()


def test_no_sdlc_plant_verbs():
    # category-error guard: no code-mutation verbs on the claim-assertion ladder
    assert not hasattr(RStage.R0_QUESTION, "allows_source_mutation")
    assert not hasattr(RStage.R0_QUESTION, "allows_release")
