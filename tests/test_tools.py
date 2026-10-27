import pytest

from agent.tools import evaluate_design


def test_evaluate_design_returns_verified_simulation():
    result = evaluate_design(5.0)

    assert result["status"] == "verified_simulation"
    assert result["experimental_validation"] is False


def test_evaluate_design_reports_requested_strain():
    result = evaluate_design(5.0)

    assert result["strain_percent"] == 5.0


def test_system_energy_is_below_material_energy():
    result = evaluate_design(5.0)

    assert (
        result["system_specific_energy_Wh_kg"]
        < result["material_specific_energy_Wh_kg"]
    )


def test_tool_rejects_negative_strain():
    with pytest.raises(ValueError):
        evaluate_design(-1.0)


def test_tool_rejects_excessive_strain():
    with pytest.raises(ValueError):
        evaluate_design(30.0)