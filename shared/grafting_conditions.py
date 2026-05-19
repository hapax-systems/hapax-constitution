"""Grafting-conditions framework and habit-baseline comparator.

Defines the 6 conditions for productive perspective-grafting between human
and computational system (from the 25-agent research), plus a simple Markov
baseline comparator that tests whether eigenform trajectories are
distinguishable from memoryless habit.

Authority: CASE-PERSPECTIVE-001
"""

from __future__ import annotations

import math
from datetime import datetime

from pydantic import BaseModel, Field, computed_field


class GraftingCondition(BaseModel):
    """A single condition for productive perspective-grafting."""

    name: str = Field(description="Snake_case identifier for the condition")
    description: str = Field(description="Human-readable description of what the condition entails")
    evidence_refs: list[str] = Field(
        default_factory=list,
        description="References to episodes/documents providing evidence",
    )
    satisfied: bool | None = Field(
        default=None,
        description="Whether the condition is satisfied (None = not yet evaluated)",
    )
    evaluation_notes: str | None = Field(
        default=None,
        description="Notes from evaluator about how this condition was assessed",
    )


class GraftingConditionSet(BaseModel):
    """The complete set of grafting conditions with aggregate evaluation."""

    conditions: list[GraftingCondition] = Field(
        description="The 6 grafting conditions for perspective-grafting"
    )
    evaluated_at: datetime | None = Field(
        default=None,
        description="Timestamp of most recent evaluation",
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def overall_satisfied(self) -> bool | None:
        """All conditions must be satisfied for overall satisfaction.

        Returns None if any condition is unevaluated.
        Returns False if any condition is explicitly unsatisfied.
        Returns True only if all conditions are satisfied.
        """
        statuses = [c.satisfied for c in self.conditions]
        if any(s is None for s in statuses):
            return None
        if any(s is False for s in statuses):
            return False
        return True


def default_condition_set() -> GraftingConditionSet:
    """Return the canonical 6-condition set with descriptions, unevaluated."""
    conditions = [
        GraftingCondition(
            name="structural_dissimilarity",
            description=(
                "The graft brings topology the host cannot generate — "
                "novel structural patterns inaccessible to the host's native cognition"
            ),
        ),
        GraftingCondition(
            name="non_internalizability",
            description=(
                "The graft remains foreign, cannot be learned away — "
                "the host cannot absorb the graft into its own repertoire"
            ),
        ),
        GraftingCondition(
            name="non_fungibility",
            description=(
                "Computationally intractable for the other party — "
                "the perspective cannot be replicated by the non-grafting party"
            ),
        ),
        GraftingCondition(
            name="biologically_impossible_registers",
            description=(
                "Operates where human neurology has hard floors — "
                "timescales, bandwidths, or simultaneities beyond biological limits"
            ),
        ),
        GraftingCondition(
            name="gestalt_coherence",
            description=(
                "Coheres as a unified perceptual style, not a feature set — "
                "the graft presents as a whole perspective, not isolated capabilities"
            ),
        ),
        GraftingCondition(
            name="persistent_unsettlement",
            description=(
                "Remains unpredictable relative to host — "
                "the graft continues to produce surprise, never fully domesticated"
            ),
        ),
    ]
    return GraftingConditionSet(conditions=conditions)


def habit_baseline_test(trajectory: list[float], order: int = 1) -> dict:
    """Test whether a memoryless Markov model explains the trajectory.

    Fits an order-1 Markov transition model by discretizing the trajectory
    into bins, building a transition matrix, and comparing prediction quality
    against a higher-order model. If the order-1 model predicts as well as
    order-2, the trajectory has no long-range structure beyond habit.

    The key insight: eigenform convergence should exhibit higher-order temporal
    structure (the path matters, not just the current state). If an order-1
    Markov model explains the data as well as an order-2 model, then current
    state alone determines the future — this is habit, not eigenform.

    If the Markov model explains the trajectory equally well (p_value > 0.05),
    then the convergence claim fails — it's just habit, not eigenform.

    Args:
        trajectory: Sequence of float values (e.g., eigenform convergence scores).
        order: Markov model order for the baseline (default 1).

    Returns:
        Dictionary with:
        - p_value: Approximate significance of discrimination (0 = clearly not Markov)
        - markov_explains: Whether the Markov model is sufficient (p > 0.05)
        - prediction_error_markov: Mean squared prediction error of order-1 model
        - prediction_error_actual: Mean squared error of higher-order model
    """
    n = len(trajectory)

    # Edge case: too short to discriminate
    if n < 4:
        return {
            "p_value": 1.0,
            "markov_explains": True,
            "prediction_error_markov": 0.0,
            "prediction_error_actual": 0.0,
        }

    # Discretize into bins for transition matrix
    n_bins = _choose_bins(n)
    binned = _discretize(trajectory, n_bins)

    # Compute prediction error for order-1 Markov model
    mse_order1 = _markov_prediction_error(binned, trajectory, n_bins, order=1)

    # Compute prediction error for order-2 Markov model (captures longer deps)
    higher_order = min(order + 1, 3)
    mse_higher = _markov_prediction_error(binned, trajectory, n_bins, order=higher_order)

    # Also compute serial dependence beyond order-1 via runs test
    # Count how often consecutive predictions from order-1 have correlated errors
    runs_p = _runs_test_on_residuals(binned, trajectory, n_bins, order=1)

    # Combine: if order-1 is as good as order-2 AND residuals show no serial
    # dependence, then Markov explains the trajectory
    if mse_order1 < 1e-12 and mse_higher < 1e-12:
        # Both perfect — Markov explains
        p_value = 1.0
    elif mse_higher < 1e-12:
        # Higher order perfect but order-1 isn't — structure exists
        p_value = 0.0
    else:
        # Compare the two: how much does higher-order improve over order-1?
        improvement_ratio = (mse_order1 - mse_higher) / mse_order1 if mse_order1 > 1e-12 else 0.0
        # Scale by sample size for statistical power
        test_stat = improvement_ratio * math.sqrt(n)
        # Also incorporate runs test
        combined_stat = max(test_stat, (1.0 - runs_p) * math.sqrt(n) / 2.0)
        # Convert to p-value (higher combined_stat = more evidence against Markov)
        p_value = math.exp(max(-50.0, -combined_stat))
        p_value = min(1.0, max(0.0, p_value))

    return {
        "p_value": p_value,
        "markov_explains": p_value > 0.05,
        "prediction_error_markov": mse_order1,
        "prediction_error_actual": mse_higher,
    }


def _markov_prediction_error(
    binned: list[int], trajectory: list[float], n_bins: int, order: int
) -> float:
    """Compute MSE of an order-N Markov model's predictions."""
    n = len(trajectory)
    if n <= order:
        return 0.0

    # Build transition counts
    transition_counts: dict[tuple[int, ...], dict[int, int]] = {}
    for i in range(order, n):
        state = tuple(binned[i - order : i])
        next_val = binned[i]
        if state not in transition_counts:
            transition_counts[state] = {}
        transition_counts[state][next_val] = transition_counts[state].get(next_val, 0) + 1

    # Compute prediction errors
    errors: list[float] = []
    mean_val = sum(trajectory) / n
    for i in range(order, n):
        state = tuple(binned[i - order : i])
        counts = transition_counts.get(state, {})
        if counts:
            total = sum(counts.values())
            expected_bin = sum(b * c for b, c in counts.items()) / total
            predicted = _bin_to_value(expected_bin, n_bins, trajectory)
            errors.append((trajectory[i] - predicted) ** 2)
        else:
            errors.append((trajectory[i] - mean_val) ** 2)

    return sum(errors) / len(errors) if errors else 0.0


def _runs_test_on_residuals(
    binned: list[int], trajectory: list[float], n_bins: int, order: int
) -> float:
    """Runs test on prediction residuals to detect serial dependence.

    Returns a p-value for the null hypothesis that residuals are independent.
    Low p-value means residuals have serial structure (evidence against Markov).
    """
    n = len(trajectory)
    if n <= order + 2:
        return 1.0

    # Build transition counts
    transition_counts: dict[tuple[int, ...], dict[int, int]] = {}
    for i in range(order, n):
        state = tuple(binned[i - order : i])
        next_val = binned[i]
        if state not in transition_counts:
            transition_counts[state] = {}
        transition_counts[state][next_val] = transition_counts[state].get(next_val, 0) + 1

    # Compute residuals (signed errors)
    residuals: list[float] = []
    mean_val = sum(trajectory) / n
    for i in range(order, n):
        state = tuple(binned[i - order : i])
        counts = transition_counts.get(state, {})
        if counts:
            total = sum(counts.values())
            expected_bin = sum(b * c for b, c in counts.items()) / total
            predicted = _bin_to_value(expected_bin, n_bins, trajectory)
            residuals.append(trajectory[i] - predicted)
        else:
            residuals.append(trajectory[i] - mean_val)

    if len(residuals) < 3:
        return 1.0

    # Count runs (sequences of same-sign residuals)
    signs = [1 if r >= 0 else -1 for r in residuals]
    n_pos = sum(1 for s in signs if s == 1)
    n_neg = len(signs) - n_pos

    if n_pos == 0 or n_neg == 0:
        return 1.0  # All same sign — cannot compute

    # Count number of runs
    runs = 1
    for i in range(1, len(signs)):
        if signs[i] != signs[i - 1]:
            runs += 1

    # Expected runs and variance under independence
    n_total = n_pos + n_neg
    expected_runs = 1 + (2 * n_pos * n_neg) / n_total
    if n_total <= 2:
        return 1.0
    variance_runs = (2 * n_pos * n_neg * (2 * n_pos * n_neg - n_total)) / (
        n_total * n_total * (n_total - 1)
    )

    if variance_runs <= 0:
        return 1.0

    # Z-score (too few runs = positive serial correlation)
    z = (runs - expected_runs) / math.sqrt(variance_runs)

    # Two-tailed p-value approximation using normal CDF
    # Using the complementary error function approximation
    p_value = 2.0 * _normal_cdf(-abs(z))
    return min(1.0, max(0.0, p_value))


def _normal_cdf(x: float) -> float:
    """Approximate standard normal CDF using error function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _choose_bins(n: int) -> int:
    """Choose number of discretization bins based on trajectory length."""
    # Sturges' rule approximation, clamped
    bins = max(3, min(10, int(1 + math.log2(n))))
    return bins


def _discretize(trajectory: list[float], n_bins: int) -> list[int]:
    """Discretize continuous trajectory into bin indices."""
    if not trajectory:
        return []

    min_val = min(trajectory)
    max_val = max(trajectory)
    range_val = max_val - min_val

    if range_val < 1e-12:
        # All values identical
        return [0] * len(trajectory)

    binned = []
    for v in trajectory:
        b = int((v - min_val) / range_val * (n_bins - 1) + 0.5)
        b = max(0, min(n_bins - 1, b))
        binned.append(b)
    return binned


def _bin_to_value(bin_idx: float, n_bins: int, trajectory: list[float]) -> float:
    """Convert a (possibly fractional) bin index back to value space."""
    min_val = min(trajectory)
    max_val = max(trajectory)
    range_val = max_val - min_val
    if range_val < 1e-12:
        return min_val
    return min_val + (bin_idx / (n_bins - 1)) * range_val
