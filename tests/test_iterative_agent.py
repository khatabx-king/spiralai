from unittest.mock import patch

from agent.iterative_agent import run_iterative_design


def proposal(strain):
    return {
        "strain_percent": strain,
        "reason": "test proposal",
    }


@patch("agent.iterative_agent.request_candidate")
def test_target_reached_stops_loop(mock_request):
    mock_request.side_effect = [
        proposal(5.0),
        proposal(7.0),
        proposal(7.1),
    ]

    report = run_iterative_design(
        target_wh_kg=50.0,
        max_iterations=6,
    )

    assert report["final_status"] == "TARGET_REACHED"
    assert report["iterations_completed"] == 3


@patch("agent.iterative_agent.request_candidate")
def test_repeated_candidate_returns_no_improvement(mock_request):
    mock_request.side_effect = [
        proposal(5.0),
        proposal(5.0),
    ]

    report = run_iterative_design(
        target_wh_kg=50.0,
        max_iterations=6,
    )

    assert report["final_status"] == "NO_IMPROVEMENT"


@patch("agent.iterative_agent.request_candidate")
def test_high_strain_requires_more_validation(mock_request):
    mock_request.return_value = proposal(15.0)

    report = run_iterative_design(
        target_wh_kg=50.0,
        max_iterations=6,
    )

    assert (
        report["final_status"]
        == "MORE_VALIDATION_REQUIRED"
    )


@patch("agent.iterative_agent.request_candidate")
def test_invalid_model_output_is_reported(mock_request):
    mock_request.side_effect = ValueError(
        "invalid model response"
    )

    report = run_iterative_design(
        target_wh_kg=50.0,
        max_iterations=6,
    )

    assert (
        report["final_status"]
        == "INVALID_MODEL_OUTPUT"
    )


@patch("agent.iterative_agent.request_candidate")
def test_max_iterations_is_respected(mock_request):
    mock_request.side_effect = [
        proposal(1.0),
        proposal(2.0),
        proposal(3.0),
    ]

    report = run_iterative_design(
        target_wh_kg=100.0,
        max_iterations=3,
    )

    assert (
        report["final_status"]
        == "MAX_ITERATIONS_REACHED"
    )

    assert report["iterations_completed"] == 3


def test_every_record_has_verified_physics_and_verification():
    with patch(
        "agent.iterative_agent.request_candidate",
        side_effect=[
            proposal(5.0),
            proposal(7.0),
            proposal(7.1),
        ],
    ):
        report = run_iterative_design(
            target_wh_kg=50.0,
            max_iterations=6,
        )

    for record in report["history"]:
        assert (
            record["physics_result"]["status"]
            == "verified_simulation"
        )

        assert "verification" in record
        assert (
            record["physics_result"][
                "experimental_validation"
            ]
            is False
        )