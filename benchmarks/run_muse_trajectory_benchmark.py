"""
SpiralAI Muse trajectory benchmark.

Evaluates the real Meta Muse Spark Open-1026 agent across repeated
scientific-design trajectories.

Unlike the deterministic minimum-strain benchmark, this benchmark
calls the live model through Baseten.

Every numerical physics result remains independently calculated and
verified by SpiralAI.

All results are THEORETICAL_SIMULATION.
"""

from pathlib import Path

from agent.iterative_agent import run_iterative_design
from provenance.run_log import (
    append_jsonl_record,
    build_run_record,
)


TARGETS_WH_KG = [
    25.0,
    50.0,
    100.0,
]

RUNS_PER_TARGET = 3

OUTPUT_PATH = Path(
    "results/muse_trajectory_benchmark.jsonl"
)


def expected_outcome(target: float) -> str:
    """
    Return the expected outcome class based on the deterministic
    10% screening-boundary benchmark.
    """

    if target <= 50.0:
        return "TARGET_REACHED"

    return "NOT_REACHABLE_WITHIN_CURRENT_SCREENING"
def assess_correct_stopping_state(
    target: float,
    final_status: str,
) -> bool:
    """Check whether the agent stopped appropriately."""

    if target <= 50.0:
        return final_status == "TARGET_REACHED"

    return final_status in {
        "MORE_VALIDATION_REQUIRED",
        "MAX_ITERATIONS_REACHED",
        "NO_IMPROVEMENT",
    }


def run_benchmark() -> list[dict]:
    """Run repeated live Muse trajectories."""

    records = []

    print("\n=== SpiralAI Muse Trajectory Benchmark ===")

    for target in TARGETS_WH_KG:
        for repeat in range(1, RUNS_PER_TARGET + 1):

            print(
                f"\nTarget: {target:.2f} Wh/kg "
                f"| Run: {repeat}/{RUNS_PER_TARGET}"
            )

            report = run_iterative_design(
                target_wh_kg=target,
            )

            history = report["history"]
            final_status = report["final_status"]

            repeated_proposal = (
                final_status == "NO_IMPROVEMENT"
            )

            invalid_output = (
                final_status == "INVALID_MODEL_OUTPUT"
            )

            verifier_escalation = (
                final_status == "MORE_VALIDATION_REQUIRED"
            )

            physics_provenance_complete = all(
                item.get("physics_result", {}).get("status")
                == "verified_simulation"
                for item in history
            )

            experimental_claim_present = any(
                item.get("physics_result", {}).get(
                    "experimental_validation"
                )
                is not False
                for item in history
            )

            correct_stopping_state = (
                assess_correct_stopping_state(
                    target,
                    final_status,
                )
            )

            record = build_run_record(
                objective="muse_trajectory_benchmark",
                target_wh_kg=target,
                final_status=final_status,
                iterations=report["iterations_completed"],
                history=history,
                metadata={
                    "benchmark_name":
                        "spiralai_muse_trajectory_v1",
                    "repeat": repeat,
                    "expected_outcome":
                        expected_outcome(target),
                    "correct_stopping_state":
                        correct_stopping_state,
                    "repeated_proposal":
                        repeated_proposal,
                    "invalid_output":
                        invalid_output,
                    "verifier_escalation":
                        verifier_escalation,
                    "physics_provenance_complete":
                        physics_provenance_complete,
                    "experimental_claim_present":
                        experimental_claim_present,
                },
            )

            append_jsonl_record(
                record,
                OUTPUT_PATH,
            )

            records.append(record)

            print(
                f"Recorded status: {final_status}"
            )

            print(
                "Correct stopping state: "
                f"{correct_stopping_state}"
            )

    return records


def rate(
    numerator: int,
    denominator: int,
) -> float:
    """Return percentage safely."""

    if denominator == 0:
        return 0.0

    return numerator / denominator * 100.0


def summarize(
    records: list[dict],
) -> None:
    """Calculate reliability metrics."""

    total = len(records)

    valid_outputs = sum(
        not record["metadata"]["invalid_output"]
        for record in records
    )

    correct_stops = sum(
        record["metadata"]["correct_stopping_state"]
        for record in records
    )

    targets_reached = sum(
        record["final_status"] == "TARGET_REACHED"
        for record in records
    )

    repeated = sum(
        record["metadata"]["repeated_proposal"]
        for record in records
    )

    escalations = sum(
        record["metadata"]["verifier_escalation"]
        for record in records
    )

    invalid_outputs = sum(
        record["metadata"]["invalid_output"]
        for record in records
    )

    provenance_complete = sum(
        record["metadata"]["physics_provenance_complete"]
        for record in records
    )

    unsupported_claims = sum(
        record["metadata"]["experimental_claim_present"]
        for record in records
    )

    average_iterations = (
        sum(record["iterations"] for record in records) / total
        if total
        else 0.0
    )

    print("\n=== Muse Benchmark Summary ===")

    print(f"Trajectories: {total}")

    print(
        "Valid-output rate: "
        f"{valid_outputs}/{total} "
        f"({rate(valid_outputs, total):.1f}%)"
    )

    print(
        "Correct stopping-state rate: "
        f"{correct_stops}/{total} "
        f"({rate(correct_stops, total):.1f}%)"
    )

    print(
        "Target-reaching rate: "
        f"{targets_reached}/{total} "
        f"({rate(targets_reached, total):.1f}%)"
    )

    print(
        "Repeated-proposal rate: "
        f"{repeated}/{total} "
        f"({rate(repeated, total):.1f}%)"
    )

    print(
        "Verifier-escalation rate: "
        f"{escalations}/{total} "
        f"({rate(escalations, total):.1f}%)"
    )

    print(
        "Invalid-output rate: "
        f"{invalid_outputs}/{total} "
        f"({rate(invalid_outputs, total):.1f}%)"
    )

    print(
        "Physics provenance coverage: "
        f"{provenance_complete}/{total} "
        f"({rate(provenance_complete, total):.1f}%)"
    )

    print(
        "Unsupported experimental claims: "
        f"{unsupported_claims}/{total} "
        f"({rate(unsupported_claims, total):.1f}%)"
    )

    print(
        f"Average iterations: {average_iterations:.2f}"
    )

    print("Evidence type: THEORETICAL_SIMULATION")
    print("Experimental validation: NO")
    print(f"JSONL provenance: {OUTPUT_PATH}")


if __name__ == "__main__":
    results = run_benchmark()
    summarize(results)