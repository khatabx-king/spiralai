import pytest

from physics.graphene import (
    strain_energy_density,
    theoretical_specific_energy,
    system_specific_energy,
)


def test_zero_strain_has_zero_energy():
    assert strain_energy_density(0.0) == 0.0


def test_energy_is_positive():
    assert strain_energy_density(0.05) > 0


def test_specific_energy_increases_with_strain():
    e1 = theoretical_specific_energy(0.01)
    e5 = theoretical_specific_energy(0.05)

    assert e5 > e1


def test_system_energy_is_lower_than_material_energy():
    material = theoretical_specific_energy(0.05)

    system = system_specific_energy(
        0.05,
        active_mass_fraction=0.30,
        recovery_efficiency=0.60,
    )

    assert system < material


def test_negative_strain_is_rejected():
    with pytest.raises(ValueError):
        strain_energy_density(-0.01)


def test_excessive_strain_is_rejected():
    with pytest.raises(ValueError):
        strain_energy_density(0.30)