"""
SpiralAI iterative design agent.

Created during the Meta Global AI Developer Hackathon.

Architecture:
Muse Spark Open proposes a candidate.
Deterministic Python calculates the physics.
An independent verifier evaluates the evidence.
Verified feedback is returned to Muse for the next iteration.

All results are theoretical/simulated screening estimates.
They are not experimental validation.
"""

import json
import os
import re
from dataclasses import asdict

from openai import OpenAI

from agent.tools import evaluate_design
from verification.verifier import (
    VerificationStatus,
    verify_design,
)


MODEL = "meta-models/muse-spark-open-1026"
MAX_ITERATIONS = 6
MAX_SCREENING_STRAIN_PERCENT = 10.0


client = OpenAI(
    api_key=os.environ["BASETEN_API_KEY"],
    base_url="https://inference.baseten.co/v1",
)


def parse_json_response(text: str) -> dict:
    """Extract and validate JSON returned by Muse Spark."""

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    proposal = json.loads(text)

    if "strain_percent" not in proposal:
        raise ValueError(
            "Muse response is missing strain_percent."
        )

    strain = float(proposal["strain_percent"])

    if not 0.0 <= strain <= 25.0:
        raise ValueError(
            f"Invalid proposed strain: {strain}%. "
            "Allowed model range is 0-25%."
        )

    proposal["strain_percent"] = strain

    return proposal


def request_candidate(
    target_wh_kg: float,
    history: list[dict],
) -> dict:
    """
    Ask Muse Spark Open for the next candidate.

    Muse receives verified history but does not calculate physics.
    """

    history_json = json.dumps(
        history,
        indent=2,
    )

    prompt = f"""
You are the scientific design component of SpiralAI.

Objective:
Find a graphene mechanical energy-storage candidate with a
system-level theoretical specific energy of at least
{target_wh_kg:.2f} Wh/kg.

A separate deterministic Python physics engine performs every
numerical calculation.

An independent verifier decides whether each result passes.

Current analytical screening boundary:
0 to {MAX_SCREENING_STRAIN_PERCENT:.2f}% strain.

Important rules:
- Propose only one new strain value.
- Do not calculate energy density yourself.
- Use the verified iteration history below.
- Do not repeat a previously tested strain.
- Prefer the smallest strain likely to reach the target.
- Remain within the analytical screening boundary when possible.
- Do not claim experimental validation.
- Do not claim replacement of lithium-ion batteries.
- If the available evidence is insufficient, state that clearly.

Verified iteration history:
{history_json}

Return only valid JSON with these keys:

{{
    "strain_percent": <number>,
    "reason": "<brief reason based on verified history>"
}}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    text = response.choices[0].message.content

    return parse_json_response(text)


def run_iterative_design(
    target_wh_kg: float = 50.0,
    max_iterations: int = MAX_ITERATIONS,
) -> dict:
    """
    Run the iterative propose-calculate-verify-redesign loop.
    """

    print("\n=== SpiralAI Iterative Design Agent ===")
    print(
        f"Target system specific energy: "
        f"{target_wh_kg:.2f} Wh/kg"
    )

    history = []
    tested_strains = set()
    final_status = "MAX_ITERATIONS_REACHED"

    for iteration in range(
        1,
        max_iterations + 1,
    ):
        print(f"\n--- Iteration {iteration} ---")

        try:
            proposal = request_candidate(
                target_wh_kg=target_wh_kg,
                history=history,
            )

        except (
            ValueError,
            json.JSONDecodeError,
        ) as error:
            print(
                f"Invalid model output: {error}"
            )

            final_status = "INVALID_MODEL_OUTPUT"
            break

        strain = float(
            proposal["strain_percent"]
        )

        rounded_strain = round(strain, 6)

        if rounded_strain in tested_strains:
            print(
                f"Muse repeated {strain:.3f}% strain."
            )

            final_status = "NO_IMPROVEMENT"
            break

        tested_strains.add(rounded_strain)

        print(
            f"Muse proposed: {strain:.3f}% strain"
        )

        print(
            f"Reason: {proposal.get('reason', '')}"
        )

        physics_result = evaluate_design(
            strain_percent=strain,
        )

        verification = verify_design(
            physics_result=physics_result,
            target_wh_kg=target_wh_kg,
            max_screening_strain_percent=(
                MAX_SCREENING_STRAIN_PERCENT
            ),
        )

        achieved = physics_result[
            "system_specific_energy_Wh_kg"
        ]

        print(
            f"Verified physics: "
            f"{achieved:.2f} Wh/kg"
        )

        print(
            f"Verifier status: "
            f"{verification.status.value}"
        )

        print(
            f"Verifier message: "
            f"{verification.message}"
        )

        record = {
            "iteration": iteration,
            "proposal": proposal,
            "physics_result": physics_result,
            "verification": {
                **asdict(verification),
                "status": (
                    verification.status.value
                ),
            },
        }

        history.append(record)

        if (
            verification.status
            == VerificationStatus.TARGET_REACHED
        ):
            final_status = "TARGET_REACHED"
            break

        if (
            verification.status
            == VerificationStatus.MORE_VALIDATION_REQUIRED
        ):
            final_status = (
                "MORE_VALIDATION_REQUIRED"
            )
            break

        if (
            verification.status
            == VerificationStatus.INVALID_RESULT
        ):
            final_status = "INVALID_RESULT"
            break

    final_report = {
        "target_Wh_kg": target_wh_kg,
        "final_status": final_status,
        "iterations_completed": len(history),
        "history": history,
        "evidence_type": (
            "THEORETICAL_SIMULATION"
        ),
        "experimental_validation": False,
        "disclaimer": (
            "Results are theoretical/simulated "
            "screening estimates based on published "
            "graphene properties. Higher-fidelity "
            "physics and experimental validation are "
            "required before practical claims."
        ),
    }

    print("\n=== Final Result ===")
    print(
        f"Status: {final_status}"
    )

    print(
        f"Iterations completed: {len(history)}"
    )

    print(
        "Evidence: THEORETICAL_SIMULATION"
    )

    print(
        "Experimental validation: NO"
    )

    return final_report


if __name__ == "__main__":
    run_iterative_design(
        target_wh_kg=50.0,
    )