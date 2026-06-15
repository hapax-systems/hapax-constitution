"""Tier-0 commons: the ordinal-stage helper parses labels, and BaseGovernanceCase
supplies the shared frontmatter mechanics while leaving stage/no-go semantics
abstract (never a fabricated pass)."""

from datetime import datetime
from enum import IntEnum

import pytest

from commons.governance_case import BaseGovernanceCase
from commons.ordinal_stage import stage_from_label


class _Ladder(IntEnum):
    X0_ALPHA = 0
    X1_BETA = 1


def test_stage_from_label_by_name():
    assert stage_from_label(_Ladder, "x0_alpha", prefix="X") is _Ladder.X0_ALPHA


def test_stage_from_label_by_prefix_number():
    assert stage_from_label(_Ladder, "X1", prefix="X") is _Ladder.X1_BETA


def test_stage_from_label_normalizes_hyphen():
    assert stage_from_label(_Ladder, "x1-beta", prefix="X") is _Ladder.X1_BETA


def test_stage_from_label_unknown_raises():
    with pytest.raises(ValueError):
        stage_from_label(_Ladder, "nope", prefix="X")


class _Case(BaseGovernanceCase):
    pass


def test_base_from_yaml_parses_frontmatter():
    text = (
        "---\n"
        "case_id: c1\n"
        "version: 1\n"
        "stage: x0_alpha\n"
        "status: open\n"
        "created_utc: 2026-06-15T00:00:00Z\n"
        "originator: operator\n"
        "---\n"
        "body text\n"
    )
    case = _Case.from_yaml(text)
    assert case.case_id == "c1"
    assert case.version == 1


def test_base_from_yaml_no_frontmatter_raises():
    with pytest.raises(ValueError):
        _Case.from_yaml("no frontmatter here")


def test_base_abstract_methods_raise_not_implemented():
    case = _Case(
        case_id="c",
        version=0,
        stage="x0_alpha",
        status="open",
        created_utc=datetime(2026, 1, 1),
        originator="operator",
    )
    with pytest.raises(NotImplementedError):
        case.parsed_stage()
    with pytest.raises(NotImplementedError):
        case.no_go_violations()


def test_base_has_no_authorization_fields():
    # the type-level guarantee: no plant verbs leak across the functor by inheritance
    fields = set(BaseGovernanceCase.model_fields)
    assert "source_mutation_authorized" not in fields
    assert "assertion_authorized" not in fields
