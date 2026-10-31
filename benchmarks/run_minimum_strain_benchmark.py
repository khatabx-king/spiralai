"""
SpiralAI deterministic minimum-strain benchmark.

Runs the verified minimum-strain optimizer over fixed energy targets
and writes append-only provenance records to JSONL.

This benchmark does not call Muse Spark and therefore does not consume
LLM inference tokens.

All results are theoretical/simulated screening estimates.
"""

from pathlib import Path

from optimization.minimum_strain import find_minimum_strain
from provenance.run_log import (
    append_jsonl_record,
    build_run_record,
)


TARGETS_WH_KG = [
    10.0,
    25.0,
    50.0,
    100.0,
    250.0,
    1000.0,
]

OUTPUT_PATH = Path(
    "results/minimum_strain_benchmark.jsonl"
)


def run_benchmark() -> list[dict]:
    """Run deterministic optimization across all benchmark targets."""

    records = []

    print(
        "\n=== SpiralAI Minimum-Strain Benchmark ==="
    )

    for target in TARGETS_WH_KG:
        result = find_minimum_strain(
            target_wh_kg=target,
        )

        record = build_run_record(
            objective="minimum_strain_benchmark",
            target_wh_kg=target,
            final_status=result.status,
            iterations=result.iterations,
            minimum_strain_percent=(
                result.minimum_strain_percent
            ),
            verified_energy_wh_kg=(
                result.verified_energy_Wh_kg
            ),
            history=result.history,
            metadata={
                "benchmark_name": (
                    "spiralai_minimum_strain_v1"
                ),
                "screening_boundary_percent": (
                    result.upper_bound_percent
                ),
                "tolerance_percent": (
                    result.tolerance_percent
                ),
            },
        )

        append_jsonl_record(
            record,
            OUTPUT_PATH,
        )

        records.append(record)

        print(
            f"\nTarget: {target:.2f} Wh/kg"
        )

        print(
            f"Status: {result.status}"
        )

        if (
            result.minimum_strain_percent
            is not None
        ):
            print(
                "Minimum strain: "
                f"{result.minimum_strain_percent:.4f}%"
            )

            print(
                "Verified energy: "
                f"{result.verified_energy_Wh_kg:.4f} Wh/kg"
            )

        else:
            print(
                "Minimum strain: N/A"
            )

            print(
                "Verified energy: N/A"
            )

        print(
            f"Iterations: {result.iterations}"
        )

    return records


def summarize(records: list[dict]) -> None:
    """Print a compact deterministic benchmark summary."""

    unreachable_status = (
        "TARGET_UNREACHABLE_WITHIN_SCREENING_BOUNDARY"
    )

    reachable = [
        record
        for record in records
        if record["final_status"] == "MINIMUM_STRAIN_FOUND"
    ]

    unreachable = [
        record
        for record in records
        if record["final_status"] == unreachable_status
    ]

    print("\n=== Benchmark Summary ===")
    print(f"Targets evaluated: {len(records)}")
    print(f"Reachable targets: {len(reachable)}")
    print(f"Unreachable targets: {len(unreachable)}")
    print("Evidence type: THEORETICAL_SIMULATION")
    print("Experimental validation: NO")
    print(f"JSONL provenance: {OUTPUT_PATH}")


if __name__ == "__main__":
    results = run_benchmark()
    summarize(results)