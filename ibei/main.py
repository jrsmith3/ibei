# -*- coding: utf-8 -*-

import numpy as np
from astropy import constants
from astropy import units
from sympy.mpmath import polylog


def uibei(order, energy_lo, temp, chem_potential):
    """
    Upper incomplete Bose-Einstein integral.
    """
    kT = temp * constants.k_B

    reduced_energy_lo = energy_lo / kT
    reduced_chem_potential = chem_potential / kT

    prefactor = (2 * np.pi * np.math.factorial(order) * kT**(order + 1)) / \
        (constants.h**3 * constants.c**2)

    summand = 0

    for indx in range(1, order + 2):
        expt = (reduced_chem_potential - reduced_energy_lo).decompose()
        term = reduced_energy_lo**(order - indx + 1) * polylog(indx, np.exp(expt)) / np.math.factorial(order - indx + 1)
        summand += term

    return summand


def bb_rad_power(temp):
    """
    Blackbody radiant power (Stefan-Boltzmann).
    """
    return constants.sigma_sb * temp**4


def devos_power(bandgap, temp_sun, temp_planet, voltage):
    """
    Power calculated according to DeVos Eq. 6.4.
    """
    sun = uibei(2, bandgap, temp_sun, 0)
    solar_cell = uibei(2, bandgap, temp_sun, constants.q * voltage)
    return voltage * constants.e * (sun - solar_cell)

