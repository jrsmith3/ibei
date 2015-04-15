# -*- coding: utf-8 -*-

import numpy as np
from astropy import constants, units
from sympy.mpmath import polylog
from physicalproperty import PhysicalProperty, find_PhysicalProperty


def uibei(order, energy_lo, temp, chem_potential):
    """
    Upper incomplete Bose-Einstein integral.

    The upper incomplete Bose-Einstein integral is given by (cf. Levy and Honsberg :cite:`10.1016/j.sse.2006.06.017`):

    .. math::

        F_{m}(E_{A},T,\mu) = \\frac{2 \pi}{h^{3}c^{2}} \int_{E_{A}}^{\infty} E^{m} \\frac{1}{\exp \left( \\frac{E - \mu}{kT} \\right) - 1} dE 

    for condition :math:`\mu < E_{A}`; the value of :math:`F_{m}` is zero when the previous condition is not met.

    :param int order: Order of Bose-Einstein integral. A value of 2 yields the particle flux, a value of 3 yields energy flux. Corresponds to :math:`m`.
    :param float energy_lo: Lower bound of integral > 0 [eV]. Corresponds to :math:`E_{A}`.
    :param float temp: Temperature of photon ensemble > 0 [K]. Corresponds to :math:`T`.
    :param float chem_potential: Chemical potential of photon ensemble > 0 [eV]. Corresponds to :math:`\mu`.
    :rtype: :class:`astropy.units.Quantity`

    Note that the float quantities above can also be :class:`astropy.units.Quantity` as long as the units are compatible.
    """
    if energy_lo < 0:
        raise ValueError("energy_lo < 0")
    elif temp < 0:
        raise ValueError("temp < 0")
    elif chem_potential < 0:
        raise ValueError("chem_potential < 0")

    energy_lo = units.Quantity(energy_lo, "eV")
    temp = units.Quantity(temp, "K")
    chem_potential = units.Quantity(chem_potential, "eV")

    kT = temp * constants.k_B

    reduced_energy_lo = energy_lo / kT
    reduced_chem_potential = chem_potential / kT

    prefactor = (2 * np.pi * np.math.factorial(order) * kT**(order + 1)) / \
        (constants.h**3 * constants.c**2)

    expt = (reduced_chem_potential - reduced_energy_lo).decompose()
    real_arg = np.exp(expt.value)

    if reduced_chem_potential == 0 and reduced_energy_lo == 0:
        # Specify this condition just to skip the next condition.
        term = float(polylog(order + 1, real_arg))
        return term * prefactor
    elif reduced_chem_potential >= reduced_energy_lo:
        return 0 * prefactor

    summand = 0
    for indx in range(1, order + 2):
        index = order - indx + 1

        term = reduced_energy_lo**index * float(polylog(indx, real_arg)) / np.math.factorial(index)

        summand += term

    return prefactor * summand
