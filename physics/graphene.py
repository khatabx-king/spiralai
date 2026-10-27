"""
SpiralAI graphene physics tools.

Created during the Meta Global AI Developer Hackathon.

This module uses published graphene material properties only.
It does NOT contain equations or derivations from the author's
unpublished pre-hackathon clock-spiral manuscript.

All calculated results are theoretical/simulated estimates,
not experimental measurements.
"""

GRAPHENE_2D_STIFFNESS = 340.0       # N/m
GRAPHENE_AREAL_DENSITY = 7.6e-7     # kg/m^2
GRAPHENE_THIRD_ORDER = -690.0       # N/m


def strain_energy_density(strain: float) -> float:
    """
    Calculate nonlinear elastic strain energy per graphene area.

    Parameters
    ----------
    strain:
        Engineering strain expressed as a decimal.
        Example: 0.05 = 5%.

    Returns
    -------
    float
        Elastic energy density in J/m^2.
    """

    if strain < 0:
        raise ValueError("Strain cannot be negative.")

    if strain > 0.25:
        raise ValueError(
            "Strain exceeds the model's 25% screening limit."
        )

    linear = 0.5 * GRAPHENE_2D_STIFFNESS * strain**2

    nonlinear = (
        GRAPHENE_THIRD_ORDER / 3.0
    ) * strain**3

    return linear + nonlinear


def theoretical_specific_energy(strain: float) -> float:
    """
    Theoretical specific elastic energy of active graphene.

    Returns
    -------
    float
        Energy density in Wh/kg.
    """

    energy_area = strain_energy_density(strain)

    energy_mass = (
        energy_area / GRAPHENE_AREAL_DENSITY
    )

    return energy_mass / 3600.0


def system_specific_energy(
    strain: float,
    active_mass_fraction: float = 0.30,
    recovery_efficiency: float = 0.60,
) -> float:
    """
    Estimate system-level specific energy.

    This is a screening estimate, not a validated device prediction.
    """

    if not 0 < active_mass_fraction <= 1:
        raise ValueError(
            "Active mass fraction must be between 0 and 1."
        )

    if not 0 < recovery_efficiency <= 1:
        raise ValueError(
            "Recovery efficiency must be between 0 and 1."
        )

    material_energy = theoretical_specific_energy(strain)

    return (
        material_energy
        * active_mass_fraction
        * recovery_efficiency
    )