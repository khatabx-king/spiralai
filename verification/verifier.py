"""
SpiralAI independent verification layer.

Created during the Meta Global AI Developer Hackathon.

The verifier operates independently of the AI design agent.
Muse Spark may propose designs, but it cannot decide whether its
own proposal passes verification.

All physics results are theoretical/simulated screening estimates,
not experimental validation.
"""

from dataclasses import dataclass
from enum import Enum


class VerificationStatus(str, Enum):
    TARGET_REACHED = "TARGET_REACHED"
    TARGET_NOT_REACHED = "TARGET_NOT_REACHED"
    PHYSICAL_CONSTRAINT_VIOLATION = "PHYSICAL_CONSTRAINT_VIOLATION"
    MORE_VALIDATION_REQUIRED = "MORE_VALIDATION_REQUIRED"
    INVALID_RESULT = "INVALID_RESULT"


@dataclass
class VerificationResult:
    status: VerificationStatus
    passed: bool
    message: str
    evidence_type: str
    next_step: str


def verify_design(
    physics_result: dict,
    target_wh_kg: float,
    max_screening_strain_percent: float = 10.0,
) -> VerificationResult:
    """
    Independently verify a SpiralAI physics result.

    Parameters
    ----------
    physics_result:
        Result returned by the deterministic physics tool.

    target_wh_kg:
        Requested system-level energy-density target.

    max_screening_strain_percent:
        Conservative operating boundary for the current public
        screening model.

    Returns
    -------
    VerificationResult
    """

    required_fields = {
        "status",
        "strain_percent",
        "system_specific_energy_Wh_kg",
        "experimental_validation",
    }

    missing = required_fields - physics_result.keys()

    if missing:
        return VerificationResult(
            status=VerificationStatus.INVALID_RESULT,
            passed=False,
            message=f"Physics result is missing required fields: {sorted(missing)}",
            evidence_type="INVALID",
            next_step="Reject result and rerun the verified physics tool.",
        )

    if physics_result["status"] != "verified_simulation":
        return VerificationResult(
            status=VerificationStatus.INVALID_RESULT,
            passed=False,
            message="Result did not originate from the verified simulation tool.",
            evidence_type="INVALID",
            next_step="Use the verified SpiralAI physics tool.",
        )

    strain = float(physics_result["strain_percent"])
    energy = float(physics_result["system_specific_energy_Wh_kg"])

    if strain < 0:
        return VerificationResult(
            status=VerificationStatus.PHYSICAL_CONSTRAINT_VIOLATION,
            passed=False,
            message="Negative strain is physically invalid for this screening task.",
            evidence_type="THEORETICAL_SIMULATION",
            next_step="Propose a non-negative strain value.",
        )

    if strain > max_screening_strain_percent:
        return VerificationResult(
            status=VerificationStatus.MORE_VALIDATION_REQUIRED,
            passed=False,
            message=(
                f"Candidate uses {strain:.2f}% strain, above the current "
                f"{max_screening_strain_percent:.2f}% conservative "
                "screening boundary."
            ),
            evidence_type="THEORETICAL_SIMULATION",
            next_step=(
                "Require higher-fidelity validation such as molecular dynamics, "
                "finite-element analysis, fatigue modelling, or experiment."
            ),
        )

    if physics_result["experimental_validation"] is not False:
        return VerificationResult(
            status=VerificationStatus.INVALID_RESULT,
            passed=False,
            message=(
                "The current SpiralAI public physics model cannot claim "
                "experimental validation."
            ),
            evidence_type="INVALID",
            next_step="Relabel the evidence honestly as theoretical simulation.",
        )

    if energy >= target_wh_kg:
        return VerificationResult(
            status=VerificationStatus.TARGET_REACHED,
            passed=True,
            message=(
                f"Target reached in theoretical screening: "
                f"{energy:.2f} Wh/kg >= {target_wh_kg:.2f} Wh/kg."
            ),
            evidence_type="THEORETICAL_SIMULATION",
            next_step=(
                "Candidate requires higher-fidelity physics and experimental "
                "validation before any practical-performance claim."
            ),
        )

    return VerificationResult(
        status=VerificationStatus.TARGET_NOT_REACHED,
        passed=False,
        message=(
            f"Target not reached: "
            f"{energy:.2f} Wh/kg < {target_wh_kg:.2f} Wh/kg."
        ),
        evidence_type="THEORETICAL_SIMULATION",
        next_step=(
            "Return the verified result to the design agent "
            "and request a revised candidate."
        ),
    )