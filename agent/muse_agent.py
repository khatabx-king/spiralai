"""
SpiralAI - Muse Spark Open agent prototype.

Hackathon work: Oct 27, 2026.
Muse Spark proposes a design parameter.
Physics calculations are performed only by verified local tools.
Results are theoretical/simulated, not experimental validation.
"""

import json
import os
import re

from openai import OpenAI

from agent.tools import evaluate_design


MODEL = "meta-models/muse-spark-open"

client = OpenAI(
    api_key=os.environ["BASETEN_API_KEY"],
    base_url="https://inference.baseten.co/v1",
)


def ask_muse_for_design(target_wh_kg: float = 25.0) -> dict:
    """Ask Muse Spark Open to propose one candidate strain."""

    prompt = f"""
You are the design-reasoning component of SpiralAI.

Goal:
Explore a graphene mechanical energy-storage design with a target
system specific energy of {target_wh_kg} Wh/kg.

Rules:
- Propose design parameters only.
- A separate verified Python physics engine performs all calculations.
- Do not calculate energy density yourself.
- Do not claim experimental validation.
- Do not claim the technology replaces lithium-ion batteries.
- This is theoretical/simulation-based screening.
- Proposed strain must be between 0 and 25 percent.

Return ONLY valid JSON:

{{
    "strain_percent": 5.0,
    "reason": "brief engineering reason"
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

    text = response.choices[0].message.content.strip()

    # Remove markdown fences if the model adds them.
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    proposal = json.loads(text)

    # Verify required field exists.
    if "strain_percent" not in proposal:
        raise ValueError("Muse response does not contain strain_percent.")

    strain = float(proposal["strain_percent"])

    # Never allow the model to bypass the design boundary.
    if not 0.0 <= strain <= 25.0:
        raise ValueError(
            f"Muse proposed invalid strain: {strain}%. "
            "Allowed range is 0-25%."
        )

    return proposal


def run_once(target_wh_kg: float = 25.0) -> None:
    print("\n=== SpiralAI ===")
    print(f"Target system specific energy: {target_wh_kg:.2f} Wh/kg")

    proposal = ask_muse_for_design(target_wh_kg)

    print("\nMuse Spark proposal:")
    print(json.dumps(proposal, indent=2))

    strain = float(proposal["strain_percent"])

    # Numerical physics comes only from the verified local tool.
    result = evaluate_design(strain)

    print("\nVerified physics result:")
    print(json.dumps(result, indent=2))

    achieved = result["system_specific_energy_Wh_kg"]

    print("\nAssessment:")

    if achieved >= target_wh_kg:
        print(
            f"Target reached in theoretical screening: "
            f"{achieved:.2f} Wh/kg >= {target_wh_kg:.2f} Wh/kg"
        )
    else:
        print(
            f"Target not reached: "
            f"{achieved:.2f} Wh/kg < {target_wh_kg:.2f} Wh/kg"
        )

    print(
        "\nIMPORTANT: This is a theoretical/simulated screening result, "
        "not experimental validation."
    )


if __name__ == "__main__":
    run_once()