# -*- coding: utf-8 -*-

import numpy as np
from astropy import constants
from astropy import units
from sympy.mpmath import polylog


def uibei(order, energy_lo, temp, chem_potential):
    """
    Upper incomplete Bose-Einstein integral.

    :param int order: Order of Bose-Einstein integral. A value of 2 yields the particle flux, a value of 3 yields energy flux.
    :param float energy_lo: Lower bound of integral [eV].
    :param float temp: Temperature of photon ensemble [K].
    :param float chem_potential: Chemical potential of photon ensemble [eV].

    Note that the float quantities above can also be astropy.units.Quantity.
    """
    energy_lo = units.Quantity(energy_lo, "eV")
    temp = units.Quantity(temp, "K")
    chem_potential = units.Quantity(chem_potential, "eV")

    kT = temp * constants.k_B

    reduced_energy_lo = energy_lo / kT
    reduced_chem_potential = chem_potential / kT

    prefactor = (2 * np.pi * np.math.factorial(order) * kT**(order + 1)) / \
        (constants.h**3 * constants.c**2)

    summand = 0

    for indx in range(1, order + 2):
        index = order - indx + 1
        expt = (reduced_chem_potential - reduced_energy_lo).decompose()
        real_arg = np.exp(expt.value)

        term = reduced_energy_lo**index * float(polylog(indx, real_arg)) / np.math.factorial(index)

        summand += term

    return prefactor * summand


def bb_rad_power(temp):
    """
    Blackbody radiant power (Stefan-Boltzmann).
    """
    temp = units.Quantity(temp, "K")
    return constants.sigma_sb * temp**4


def devos_power(bandgap, temp_sun, temp_planet, voltage):
    """
    Power calculated according to DeVos Eq. 6.4. (9780198513926).

    This method assumes fully concentrated sunlight.
    """
    voltage = units.Quantity(voltage, "V")

    electron_energy = constants.e.si * voltage

    solar_flux = uibei(2, bandgap, temp_sun, 0)
    solar_cell_flux = uibei(2, bandgap, temp_planet, electron_energy)

    return electron_energy * (solar_flux - solar_cell_flux)

def devos_efficiency(bandgap, temp_sun, temp_planet, voltage):
    """
    Efficiency calculated according to DeVos Eqs. 6.4 and prior.
    """
    cell_power = devos_power(bandgap, temp_sun, temp_planet, voltage)
    solar_power = bb_rad_power(temp_sun)

    efficiency = cell_power/solar_power

    return efficiency.decompose().value

def sq_power(bandgap, temp_sun):
    """
    Power calculated according to Shockley & Queisser Eq. 2.4. (10.1063/1.1736034).
    """
    bandgap = units.Quantity(bandgap, "eV")
    temp_sun = units.Quantity(temp_sun, "K")

    solar_flux = uibei(2, bandgap, temp_sun, 0)

    return bandgap * solar_flux

def sq_efficiency(bandgap, temp_sun):
    """
    Efficiency calculated according to Shockley & Queisser Eq. 2.8. (10.1063/1.1736034).
    """
    cell_power = sq_power(bandgap, temp_sun)
    solar_power = bb_rad_power(temp_sun)

    efficiency = cell_power/solar_power

    return efficiency.decompose().value
