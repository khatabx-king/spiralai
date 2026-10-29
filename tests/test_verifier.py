from agent.tools import evaluate_design
from verification.verifier import (
    VerificationStatus,
    verify_design,
)


def test_target_reached():
    physics = evaluate_design(5.0)

    result = verify_design(
        physics_result=physics,
        target_wh_kg=25.0,
    )

    assert result.status == VerificationStatus.TARGET_REACHED
    assert result.passed is True
    assert result.evidence_type == "THEORETICAL_SIMULATION"


def test_target_not_reached():
    physics = evaluate_design(3.0)

    result = verify_design(
        physics_result=physics,
        target_wh_kg=25.0,
    )

    assert result.status == VerificationStatus.TARGET_NOT_REACHED
    assert result.passed is False


def test_high_strain_requires_more_validation():
    physics = evaluate_design(15.0)

    result = verify_design(
        physics_result=physics,
        target_wh_kg=25.0,
    )

    assert (
        result.status
        == VerificationStatus.MORE_VALIDATION_REQUIRED
    )

    assert result.passed is False


def test_unverified_result_is_rejected():
    fake_result = {
        "status": "ai_generated",
        "strain_percent": 5.0,
        "system_specific_energy_Wh_kg": 1000.0,
        "experimental_validation": False,
    }

    result = verify_design(
        physics_result=fake_result,
        target_wh_kg=25.0,
    )

    assert result.status == VerificationStatus.INVALID_RESULT
    assert result.passed is False


def test_false_experimental_claim_is_rejected():
    fake_result = {
        "status": "verified_simulation",
        "strain_percent": 5.0,
        "system_specific_energy_Wh_kg": 26.0,
        "experimental_validation": True,
    }

    result = verify_design(
        physics_result=fake_result,
        target_wh_kg=25.0,
    )

    assert result.status == VerificationStatus.INVALID_RESULT
    assert result.passed is False


def test_missing_physics_fields_are_rejected():
    incomplete_result = {
        "status": "verified_simulation",
        "strain_percent": 5.0,
    }

    result = verify_design(
        physics_result=incomplete_result,
        target_wh_kg=25.0,
    )

    assert result.status == VerificationStatus.INVALID_RESULT
    assert result.passed is False