# -*- coding: utf-8 -*-

import numpy as np
from astropy import constants
from astropy import units
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

    if reduced_chem_potential >= reduced_energy_lo:
        return 0 * prefactor

    summand = 0
    expt = (reduced_chem_potential - reduced_energy_lo).decompose()
    real_arg = np.exp(expt.value)

    for indx in range(1, order + 2):
        index = order - indx + 1

        term = reduced_energy_lo**index * float(polylog(indx, real_arg)) / np.math.factorial(index)

        summand += term

    return prefactor * summand


class SQSolarcell(object):
    """
    Shockley-Queisser single-junction solar cell

    This class implements a solar cell as described by Shockley and Queisser :cite:`10.1063/1.1736034`.

    An :class:`SQSolarcell` is instantiated with a :class:`dict` having keys identical to the class's public data attributes. Each key's value must satisfy the constraints noted with the corresponding public data attribute. Dictionary values can be some kind of numeric type or of type :class:`astropy.units.Quantity` so long as the units are compatible with what's listed.
    """

    temp_sun = PhysicalProperty(unit = "K", lo_bnd = 0)
    """
    Solar temperature > 0 [K]
    """

    bandgap = PhysicalProperty(unit = "eV", lo_bnd = 0)
    """
    Bandgap of single homojunction > 0 [eV]
    """

    def __init__(self, params):
        for attr in find_PhysicalProperty(self):
            setattr(self, attr, params[attr])

    def __repr__(self):
        return str(self._to_dict())

    def _to_dict(self):
        """
        Return a dictionary representation of the current object.
        """
        physical_prop_names = find_PhysicalProperty(self)
        physical_prop_vals = [getattr(self, prop) for prop in physical_prop_names]

        return dict(zip(physical_prop_names, physical_prop_vals))

    def calc_blackbody_radiant_power_density(self):
        """
        Stefan-Boltzmann radiant power density from sun

        The Stefan-Boltzmann radiant power density is given by 

        .. math::
            W = \sigma T^{4}

        where

        .. math::
            \sigma = \\frac{2 \pi^{5} k^{4}}{15 c^{2} h^{3}}

        and

        * :math:`T`: Solar temperature
        * :math:`k`: Boltzmann's constant
        * :math:`h`: Planck's constant
        * :math:`c`: Speed of light in vacuum

        This method returns values of type :class:`astropy.units.Quantity` with units of [W m^-2].
        """
        radiant_power_density = constants.sigma_sb * self.temp_sun**4

        return radiant_power_density.to("W/m2")

    def calc_power_density(self):
        """
        Solar cell power density

        The output power density is calculated according to a slight modification of Shockley & Queisser's :cite:`10.1063/1.1736034` Eq. 2.4. This method returns values of type :class:`astropy.units.Quantity` with units of [W m^-2].
        """
        if self.bandgap == 0:
            solar_flux = units.Quantity(0., "1/(m2*s)")
        else:
            solar_flux = uibei(2, self.bandgap, self.temp_sun, 0)
        power_density = self.bandgap * solar_flux

        return power_density.to("W/m^2")

    def calc_efficiency(self):
        """
        Solar cell efficiency

        The efficiency is calculated according to Shockley & Queisser's :cite:`10.1063/1.1736034` Eq. 2.8. This method returns a :class:`float`.
        """
        cell_power = self.calc_power_density()
        solar_power = self.calc_blackbody_radiant_power_density()
        efficiency = cell_power/solar_power

        return efficiency.decompose().value


class DeVosSolarcell(SQSolarcell):
    """
    DeVos single-junction solar cell

    This class implements a solar cell as described by DeVos :cite:`9780198513926` Ch. 6.

    An DeVosSolarcell is instantiated with a :class:`dict` having keys identical to the class's public data attributes. Each key's value must satisfy the constraints noted with the corresponding public data attribute. Dictionary values can be some kind of numeric type or of type :class:`astropy.units.Quantity` so long as the units are compatible with what's listed.
    """

    temp_planet = PhysicalProperty(unit = "K", lo_bnd = 0)
    """
    Planet temperature > 0 [K]
    """

    voltage = PhysicalProperty(unit = "V")
    """
    Bias voltage [V]
    """

    def calc_power_density(self):
        """
        Solar cell power density

        The output power density is calculated according to DeVos's :cite:`9780198513926` Eq. 6.4. Note that this expression assumes fully concentrated sunlight and is therefore not completely general.

        This method returns values of type :class:`astropy.units.Quantity` with units of [W m^-2].
        """
        electron_energy = constants.e.si * self.voltage

        if self.bandgap == 0:
            solar_flux = units.Quantity(0., "1/(m2*s)")
            solar_cell_flux = units.Quantity(0., "1/(m2*s)")
        else:
            solar_flux = uibei(2, self.bandgap, self.temp_sun, 0)
            solar_cell_flux = uibei(2, self.bandgap, self.temp_planet, electron_energy)
        power_density = electron_energy * (solar_flux - solar_cell_flux)

        return power_density.to("W/m^2")
