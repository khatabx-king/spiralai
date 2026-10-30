"""
SpiralAI minimum-strain optimization.

Created during the Meta Global AI Developer Hackathon.

The optimizer searches for the lowest strain that satisfies a requested
system-level specific-energy target within the verified analytical
screening boundary.

Muse Spark may choose the scientific objective and interpret the result.
Numerical candidate selection, physics calculation, and verification are
performed deterministically.

All outputs are theoretical/simulated screening estimates.
They are not experimentally validated device results.
"""

from dataclasses import asdict, dataclass

from agent.tools import evaluate_design
from verification.verifier import (
    VerificationStatus,
    verify_design,
)


@dataclass
class MinimumStrainResult:
    target_Wh_kg: float
    status: str
    minimum_strain_percent: float | None
    verified_energy_Wh_kg: float | None
    iterations: int
    tolerance_percent: float
    lower_bound_percent: float
    upper_bound_percent: float
    history: list[dict]
    evidence_type: str
    experimental_validation: bool
    disclaimer: str


def find_minimum_strain(
    target_wh_kg: float,
    min_strain_percent: float = 0.0,
    max_strain_percent: float = 10.0,
    tolerance_percent: float = 0.01,
    max_iterations: int = 30,
) -> MinimumStrainResult:
    """
    Find the lowest verified strain that reaches a target energy density.

    The method uses deterministic bisection within the current analytical
    screening boundary.

    Parameters
    ----------
    target_wh_kg:
        Required system-level specific energy in Wh/kg.

    min_strain_percent:
        Lower search boundary.

    max_strain_percent:
        Upper verified screening boundary.

    tolerance_percent:
        Stop when the strain interval is this small.

    max_iterations:
        Maximum number of bisection iterations.
    """

    if target_wh_kg <= 0:
        raise ValueError("target_wh_kg must be greater than zero.")

    if min_strain_percent < 0:
        raise ValueError("min_strain_percent cannot be negative.")

    if max_strain_percent <= min_strain_percent:
        raise ValueError(
            "max_strain_percent must be greater than "
            "min_strain_percent."
        )

    if tolerance_percent <= 0:
        raise ValueError("tolerance_percent must be greater than zero.")

    if max_iterations <= 0:
        raise ValueError("max_iterations must be greater than zero.")

    history: list[dict] = []

    # First determine whether the target is reachable at the upper boundary.
    upper_physics = evaluate_design(max_strain_percent)

    upper_verification = verify_design(
        physics_result=upper_physics,
        target_wh_kg=target_wh_kg,
        max_screening_strain_percent=max_strain_percent,
    )

    history.append(
        {
            "iteration": 0,
            "role": "feasibility_check",
            "strain_percent": max_strain_percent,
            "physics_result": upper_physics,
            "verification": {
                **asdict(upper_verification),
                "status": upper_verification.status.value,
            },
        }
    )

    if upper_verification.status != VerificationStatus.TARGET_REACHED:
        return MinimumStrainResult(
            target_Wh_kg=target_wh_kg,
            status="TARGET_UNREACHABLE_WITHIN_SCREENING_BOUNDARY",
            minimum_strain_percent=None,
            verified_energy_Wh_kg=None,
            iterations=0,
            tolerance_percent=tolerance_percent,
            lower_bound_percent=min_strain_percent,
            upper_bound_percent=max_strain_percent,
            history=history,
            evidence_type="THEORETICAL_SIMULATION",
            experimental_validation=False,
            disclaimer=(
                "The target was not reached within the current "
                "verified analytical screening boundary."
            ),
        )

    lower = float(min_strain_percent)
    upper = float(max_strain_percent)

    best_strain = upper
    best_physics = upper_physics

    iterations_completed = 0

    for iteration in range(1, max_iterations + 1):
        iterations_completed = iteration

        midpoint = (lower + upper) / 2.0

        physics_result = evaluate_design(midpoint)

        verification = verify_design(
            physics_result=physics_result,
            target_wh_kg=target_wh_kg,
            max_screening_strain_percent=max_strain_percent,
        )

        history.append(
            {
                "iteration": iteration,
                "role": "minimum_strain_search",
                "strain_percent": midpoint,
                "physics_result": physics_result,
                "verification": {
                    **asdict(verification),
                    "status": verification.status.value,
                },
            }
        )

        if verification.status == VerificationStatus.TARGET_REACHED:
            best_strain = midpoint
            best_physics = physics_result
            upper = midpoint
        elif verification.status == VerificationStatus.TARGET_NOT_REACHED:
            lower = midpoint
        else:
            return MinimumStrainResult(
                target_Wh_kg=target_wh_kg,
                status=verification.status.value,
                minimum_strain_percent=None,
                verified_energy_Wh_kg=None,
                iterations=iterations_completed,
                tolerance_percent=tolerance_percent,
                lower_bound_percent=lower,
                upper_bound_percent=upper,
                history=history,
                evidence_type="THEORETICAL_SIMULATION",
                experimental_validation=False,
                disclaimer=verification.message,
            )

        if upper - lower <= tolerance_percent:
            break

    return MinimumStrainResult(
        target_Wh_kg=target_wh_kg,
        status="MINIMUM_STRAIN_FOUND",
        minimum_strain_percent=best_strain,
        verified_energy_Wh_kg=best_physics[
            "system_specific_energy_Wh_kg"
        ],
        iterations=iterations_completed,
        tolerance_percent=tolerance_percent,
        lower_bound_percent=lower,
        upper_bound_percent=upper,
        history=history,
        evidence_type="THEORETICAL_SIMULATION",
        experimental_validation=False,
        disclaimer=(
            "Minimum strain is a theoretical screening estimate based "
            "on the current public physics model and assumptions. "
            "Higher-fidelity simulation and experimental validation "
            "are required before practical claims."
        ),
    )


if __name__ == "__main__":
    result = find_minimum_strain(
        target_wh_kg=50.0,
    )

    print("\n=== SpiralAI Minimum-Strain Optimization ===")
    print(f"Target: {result.target_Wh_kg:.2f} Wh/kg")
    print(f"Status: {result.status}")
    print(f"Iterations: {result.iterations}")

    if result.minimum_strain_percent is not None:
        print(
            "Minimum verified strain: "
            f"{result.minimum_strain_percent:.4f}%"
        )

        print(
            "Verified energy: "
            f"{result.verified_energy_Wh_kg:.4f} Wh/kg"
        )

    print(f"Evidence: {result.evidence_type}")
    print(
        "Experimental validation: "
        f"{result.experimental_validation}"
    )
    print(f"Disclaimer: {result.disclaimer}")