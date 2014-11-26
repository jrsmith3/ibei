# -*- coding: utf-8 -*-

import numpy as np
from astropy import constants, units
from sympy.mpmath import polylog
from physicalproperty import PhysicalProperty, find_PhysicalProperty


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
