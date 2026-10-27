"""
Physics tool wrappers for the SpiralAI agent.

Created during the Meta Global AI Developer Hackathon.

These tools expose deterministic physics calculations to the AI agent.
The AI proposes candidate parameters; Python performs the calculation.

All outputs are theoretical/simulated screening estimates,
not experimental measurements.
"""

from physics.graphene import (
    strain_energy_density,
    theoretical_specific_energy,
    system_specific_energy,
)


def evaluate_design(
    strain_percent: float,
    active_mass_fraction: float = 0.30,
    recovery_efficiency: float = 0.60,
) -> dict:
    """
    Evaluate one graphene mechanical energy-storage candidate.

    Parameters
    ----------
    strain_percent:
        Engineering strain in percent.
        Example: 5.0 means 5%.

    active_mass_fraction:
        Fraction of total system mass that is active graphene.

    recovery_efficiency:
        Fraction of stored elastic energy recovered as useful energy.

    Returns
    -------
    dict
        Verified physics results suitable for the AI agent.
    """

    strain = strain_percent / 100.0

    energy_area = strain_energy_density(strain)

    material_energy = theoretical_specific_energy(strain)

    system_energy = system_specific_energy(
        strain=strain,
        active_mass_fraction=active_mass_fraction,
        recovery_efficiency=recovery_efficiency,
    )

    return {
        "status": "verified_simulation",
        "strain_percent": strain_percent,
        "active_mass_fraction": active_mass_fraction,
        "recovery_efficiency": recovery_efficiency,
        "strain_energy_density_J_m2": energy_area,
        "material_specific_energy_Wh_kg": material_energy,
        "system_specific_energy_Wh_kg": system_energy,
        "experimental_validation": False,
        "note": (
            "Theoretical/simulated screening result using "
            "published graphene material properties."
        ),
    }