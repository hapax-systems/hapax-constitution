"""Tests for grafting-conditions framework and habit-baseline comparator."""

from shared.grafting_conditions import (
    GraftingCondition,
    default_condition_set,
    habit_baseline_test,
)


def test_grafting_condition_model():
    cond = GraftingCondition(
        name="structural_dissimilarity",
        description="The graft brings topology the host cannot generate",
        evidence_refs=[],
        satisfied=None,  # not yet evaluated
    )
    assert cond.name == "structural_dissimilarity"
    assert cond.satisfied is None
    assert cond.evidence_refs == []


def test_grafting_condition_with_evidence():
    cond = GraftingCondition(
        name="non_internalizability",
        description="The graft remains foreign, cannot be learned away",
        evidence_refs=["episode_001", "episode_042"],
        satisfied=True,
        evaluation_notes="Confirmed via 30-day longitudinal",
    )
    assert cond.satisfied is True
    assert len(cond.evidence_refs) == 2
    assert cond.evaluation_notes == "Confirmed via 30-day longitudinal"


def test_grafting_condition_set_has_six():
    conditions = default_condition_set()
    assert len(conditions.conditions) == 6


def test_grafting_condition_set_names():
    conditions = default_condition_set()
    names = [c.name for c in conditions.conditions]
    assert "structural_dissimilarity" in names
    assert "non_internalizability" in names
    assert "non_fungibility" in names
    assert "biologically_impossible_registers" in names
    assert "gestalt_coherence" in names
    assert "persistent_unsettlement" in names


def test_grafting_condition_set_overall_none_when_unevaluated():
    conditions = default_condition_set()
    assert conditions.overall_satisfied is None


def test_grafting_condition_set_overall_true_when_all_satisfied():
    conditions = default_condition_set()
    for c in conditions.conditions:
        c.satisfied = True
    assert conditions.overall_satisfied is True


def test_grafting_condition_set_overall_false_when_any_unsatisfied():
    conditions = default_condition_set()
    for c in conditions.conditions:
        c.satisfied = True
    conditions.conditions[2].satisfied = False
    assert conditions.overall_satisfied is False


def test_habit_baseline_returns_discrimination():
    # Synthetic data: alternating values (clearly not Markov)
    trajectory = [0.1, 0.9, 0.1, 0.9, 0.1, 0.9, 0.1, 0.9, 0.1, 0.9] * 5
    result = habit_baseline_test(trajectory)
    assert "p_value" in result
    assert "markov_explains" in result
    assert isinstance(result["p_value"], float)


def test_habit_baseline_detects_constant():
    # Constant trajectory — Markov should explain this perfectly
    trajectory = [0.5] * 50
    result = habit_baseline_test(trajectory)
    assert result["markov_explains"] is True


def test_habit_baseline_detects_structured_pattern():
    # Non-stationary pattern: accelerating drift that a stationary Markov
    # model cannot capture (values trend upward with increasing step size)
    import math

    trajectory = [math.sin(i * 0.3) * (1 + i * 0.05) for i in range(80)]
    # Normalize to [0, 1]
    mn, mx = min(trajectory), max(trajectory)
    trajectory = [(v - mn) / (mx - mn) for v in trajectory]
    result = habit_baseline_test(trajectory)
    # A first-order Markov model should struggle with non-stationary growth
    assert result["markov_explains"] is False


def test_habit_baseline_accepts_random_walk():
    # Random-walk-like trajectory (Markov-friendly)
    import random

    random.seed(42)
    trajectory = []
    val = 0.5
    for _ in range(100):
        val += random.gauss(0, 0.01)
        val = max(0.0, min(1.0, val))
        trajectory.append(val)
    result = habit_baseline_test(trajectory)
    # A random walk should be well-explained by a Markov model
    assert result["markov_explains"] is True


def test_habit_baseline_result_keys():
    trajectory = [0.3, 0.7, 0.3, 0.7] * 10
    result = habit_baseline_test(trajectory)
    assert "p_value" in result
    assert "markov_explains" in result
    assert "prediction_error_markov" in result
    assert "prediction_error_actual" in result
    assert 0.0 <= result["p_value"] <= 1.0


def test_habit_baseline_short_trajectory():
    # Very short trajectory — should still return a result without crashing
    trajectory = [0.5, 0.6, 0.7]
    result = habit_baseline_test(trajectory)
    assert "p_value" in result
    assert "markov_explains" in result
