"""
SpiralAI - Graphene Physics Engine

Hackathon work:
Meta Global AI Developer Hackathon
Started: 27 October 2026

IMPORTANT
---------
This module is new hackathon work.

It does NOT contain equations or derivations from the author's
unpublished clock-spiral manuscript.

The model here uses published graphene material properties and
provides theoretical/simulated estimates only.
"""

from dataclasses import dataclass


# Published graphene material constants
# 2D elastic stiffness, N/m
GRAPHENE_E2D = 340.0

# Third-order nonlinear elastic stiffness, N/m
GRAPHENE_D2D = -690.0

# Areal mass density, kg/m^2
GRAPHENE_AREAL_DENSITY = 7.6e-7


@dataclass
class GrapheneResult:
    strain: float
    strain_percent: float
    energy_per_area_J_m2: float
    energy_density_J_kg: float
    energy_density_Wh_kg: float
    stress_2d_N_m: float


def graphene_energy_density(strain: float) -> GrapheneResult:
    """
    Estimate elastic energy stored in ideal monolayer graphene.

    Parameters
    ----------
    strain:
        Engineering strain as a decimal.
        Example: 0.05 means 5%.

    Returns
    -------
    GrapheneResult

    Notes
    -----
    Uses a nonlinear 2D constitutive approximation:

        sigma = E2D * strain + D2D * strain^2

    and its integrated strain-energy density:

        U/A = (E2D/2)*strain^2
              + (D2D/3)*strain^3

    Results are theoretical estimates for ideal graphene,
    not experimentally validated device performance.
    """

    if not 0 <= strain <= 0.25:
        raise ValueError(
            "strain must be between 0 and 0.25 "
            "(0% to 25%) for this screening model"
        )

    stress_2d = (
        GRAPHENE_E2D * strain
        + GRAPHENE_D2D * strain**2
    )

    energy_area = (
        0.5 * GRAPHENE_E2D * strain**2
        + (GRAPHENE_D2D / 3.0) * strain**3
    )

    energy_J_kg = energy_area / GRAPHENE_AREAL_DENSITY
    energy_Wh_kg = energy_J_kg / 3600.0

    return GrapheneResult(
        strain=strain,
        strain_percent=strain * 100.0,
        energy_per_area_J_m2=energy_area,
        energy_density_J_kg=energy_J_kg,
        energy_density_Wh_kg=energy_Wh_kg,
        stress_2d_N_m=stress_2d,
    )


if __name__ == "__main__":
    print("SpiralAI graphene physics screening")
    print("THEORETICAL / SIMULATED RESULTS\n")

    for strain in [0.01, 0.03, 0.05, 0.10]:
        result = graphene_energy_density(strain)

        print(
            f"{result.strain_percent:>5.1f}% strain | "
            f"{result.energy_density_Wh_kg:>8.2f} Wh/kg | "
            f"{result.stress_2d_N_m:>7.2f} N/m"
        )