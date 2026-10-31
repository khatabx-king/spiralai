from benchmarks.run_minimum_strain_benchmark import (
    TARGETS_WH_KG,
)
from optimization.minimum_strain import find_minimum_strain


def test_benchmark_has_six_targets():
    assert TARGETS_WH_KG == [
        10.0,
        25.0,
        50.0,
        100.0,
        250.0,
        1000.0,
    ]


def test_reachable_benchmark_targets():
    for target in [10.0, 25.0, 50.0]:
        result = find_minimum_strain(target)

        assert result.status == "MINIMUM_STRAIN_FOUND"
        assert result.minimum_strain_percent is not None
        assert result.verified_energy_Wh_kg >= target


def test_unreachable_benchmark_targets():
    expected = (
        "TARGET_UNREACHABLE_WITHIN_SCREENING_BOUNDARY"
    )

    for target in [100.0, 250.0, 1000.0]:
        result = find_minimum_strain(target)

        assert result.status == expected
        assert result.minimum_strain_percent is None


def test_50_whkg_benchmark_regression():
    result = find_minimum_strain(50.0)

    assert 7.0 <= result.minimum_strain_percent <= 7.1
    assert result.verified_energy_Wh_kg >= 50.0


def test_benchmark_evidence_is_theoretical():
    result = find_minimum_strain(25.0)

    assert result.evidence_type == "THEORETICAL_SIMULATION"
    assert result.experimental_validation is False


def test_reachable_strain_increases_with_target():
    results = [
        find_minimum_strain(target)
        for target in [10.0, 25.0, 50.0]
    ]

    strains = [
        result.minimum_strain_percent
        for result in results
    ]

    assert strains[0] < strains[1] < strains[2]