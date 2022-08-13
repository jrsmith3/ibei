# -*- coding: utf-8 -*-

import astropy.constants
import astropy.units
import attrs
import mpmath
import numpy as np


def uibei(order, energy_lo, temp, chem_potential):
    """
    Upper incomplete Bose-Einstein integral.

    The upper incomplete Bose-Einstein integral is given by the following
    expression [1]_ for condition :math:`\mu < E_{A}`, and is equal to
    zero when this condition is not met.

    .. math::

        F_{m}(E_{A},T,\mu) = \\frac{2 \pi}{h^{3}c^{2}} \int_{E_{A}}^{\infty} E^{m} \\frac{1}{\exp \left( \\frac{E - \mu}{kT} \\right) - 1} dE 

    The quantities are as follows: :math:`E` is the photon
    energy, :math:`\mu` is the photon chemical potential, :math:`E_{A}` is
    the lower limit of integration, :math:`T` is the absolute temperature
    of the blackbody radiator, :math:`h` is Planck's constant, :math:`c`
    is the speed of light, :math:`k` is Boltzmann's constant,
    and :math:`m` is the integer order of the integration. For a value
    of :math:`m = 2` , this integral returns the photon particle flux,
    whereas for :math:`m = 3` , the integral yields the photon power
    flux.

    
    Parameters
    ----------
    order: int
        Order of Bose-Einstein integral. Corresponds to :math:`m`.
    energy_lo: float or astropy.units.Quantity[units.eV]
        Lower bound of integral. Corresponds to :math:`E_{A}`.
    temp: float or astropy.units.Quantity[units.K]
        Temperature of photon ensemble. Corresponds to :math:`T`.
    chem_potential: float or astropy.units.Quantity
        Chemical potential of photon ensemble. Corresponds to:math:`\mu`.
    

    Returns
    -------
    astropy.units.Quantity
        Value of upper-incomplete Bose-Einstein integral.


    Raises
    ------
    ValueError
        If `energy_lo` <= 0
    ValueError
        If `temp` <= 0
    ValueError
        If `chem_potential` < 0


    References
    ----------
    .. [1] :cite:`10.1016/j.sse.2006.06.017`
    """
    if energy_lo < 0:
        raise ValueError("energy_lo < 0")
    elif temp < 0:
        raise ValueError("temp < 0")
    elif chem_potential < 0:
        raise ValueError("chem_potential < 0")

    energy_lo = astropy.units.Quantity(energy_lo, "eV")
    temp = astropy.units.Quantity(temp, "K")
    chem_potential = astropy.units.Quantity(chem_potential, "eV")

    kT = temp * astropy.constants.k_B

    reduced_energy_lo = energy_lo / kT
    reduced_chem_potential = chem_potential / kT

    prefactor = (2 * np.pi * np.math.factorial(order) * kT**(order + 1)) / \
        (astropy.constants.h**3 * astropy.constants.c**2)

    expt = (reduced_chem_potential - reduced_energy_lo).decompose()
    real_arg = np.exp(expt.value)

    if reduced_chem_potential == 0 and reduced_energy_lo == 0:
        # Specify this condition just to skip the next condition.
        term = float(mpmath.polylog(order + 1, real_arg))
        return term * prefactor
    elif reduced_chem_potential >= reduced_energy_lo:
        return 0 * prefactor

    summand = 0
    for indx in range(1, order + 2):
        index = order - indx + 1

        term = reduced_energy_lo**index * float(mpmath.polylog(indx, real_arg)) / np.math.factorial(index)

        summand += term

    return prefactor * summand


@attrs.frozen
class BEI():
    """
    Bose-Einstein integrals

    Parameters
    ----------
    order:
        Order of Bose-Einstein integral. Corresponds to :math:`m`.
    energy_bound:
        Upper or lower bound of integral depending on which integration method
        is called. Corresponds to :math:`E_{A}`.
    temperature:
        Temperature of photon ensemble. Corresponds to :math:`T`.
    chemical_potential:
        Chemical potential of photon ensemble. Corresponds to:math:`\mu`.
    """
    order: int = attrs.field()
    energy_bound: float | astropy.units.Quantity[astropy.units.eV] = attrs.field()
    temperature: float | astropy.units.Quantity[astropy.units.K] = attrs.field()
    chemical_potential: float | astropy.units.Quantity[astropy.units.eV] = attrs.field()
