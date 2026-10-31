import pytest
from benchmarks.run_muse_trajectory_benchmark import (
    RUNS_PER_TARGET,
    TARGETS_WH_KG,
    assess_correct_stopping_state,
    expected_outcome,
    rate,
)


def test_muse_benchmark_configuration():
    assert TARGETS_WH_KG == [
        25.0,
        50.0,
        100.0,
    ]

    assert RUNS_PER_TARGET == 3


def test_expected_reachable_outcomes():
    assert expected_outcome(25.0) == "TARGET_REACHED"
    assert expected_outcome(50.0) == "TARGET_REACHED"


def test_expected_unreachable_outcome():
    assert (
        expected_outcome(100.0)
        == "NOT_REACHABLE_WITHIN_CURRENT_SCREENING"
    )


def test_correct_stopping_for_reachable_targets():
    assert assess_correct_stopping_state(
        25.0,
        "TARGET_REACHED",
    )

    assert assess_correct_stopping_state(
        50.0,
        "TARGET_REACHED",
    )


def test_correct_stopping_for_unreachable_target():
    assert assess_correct_stopping_state(
        100.0,
        "MORE_VALIDATION_REQUIRED",
    )

    assert assess_correct_stopping_state(
        100.0,
        "MAX_ITERATIONS_REACHED",
    )

    assert assess_correct_stopping_state(
        100.0,
        "NO_IMPROVEMENT",
    )


def test_false_success_for_unreachable_target_is_rejected():
    assert not assess_correct_stopping_state(
        100.0,
        "TARGET_REACHED",
    )


def test_rate_calculation():
    assert rate(9, 9) == pytest.approx(100.0)
    assert rate(3, 9) == pytest.approx(100.0 / 3.0)
    assert rate(0, 0) == pytest.approx(0.0)