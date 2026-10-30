import pytest

from optimization.minimum_strain import find_minimum_strain


def test_finds_minimum_strain_for_50_whkg():
    result = find_minimum_strain(
        target_wh_kg=50.0,
    )

    assert result.status == "MINIMUM_STRAIN_FOUND"
    assert result.minimum_strain_percent is not None
    assert result.verified_energy_Wh_kg >= 50.0

    # Current deterministic model should converge near 7.03%.
    assert 7.0 <= result.minimum_strain_percent <= 7.1


def test_minimum_strain_is_below_screening_ceiling():
    result = find_minimum_strain(
        target_wh_kg=50.0,
    )

    assert result.minimum_strain_percent < 10.0


def test_unreachable_target_is_reported_honestly():
    result = find_minimum_strain(
        target_wh_kg=1000.0,
    )

    assert (
        result.status
        == "TARGET_UNREACHABLE_WITHIN_SCREENING_BOUNDARY"
    )

    assert result.minimum_strain_percent is None


def test_invalid_target_is_rejected():
    with pytest.raises(ValueError):
        find_minimum_strain(
            target_wh_kg=0.0,
        )


def test_invalid_search_bounds_are_rejected():
    with pytest.raises(ValueError):
        find_minimum_strain(
            target_wh_kg=50.0,
            min_strain_percent=10.0,
            max_strain_percent=5.0,
        )


def test_tighter_tolerance_refines_solution():
    coarse = find_minimum_strain(
        target_wh_kg=50.0,
        tolerance_percent=0.1,
    )

    fine = find_minimum_strain(
        target_wh_kg=50.0,
        tolerance_percent=0.001,
    )

    assert (
        fine.tolerance_percent
        < coarse.tolerance_percent
    )

    assert fine.verified_energy_Wh_kg >= 50.0