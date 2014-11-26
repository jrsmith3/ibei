# -*- coding: utf-8 -*-

import numpy as np
from astropy import constants, units
from sympy.mpmath import polylog
from physicalproperty import PhysicalProperty, find_PhysicalProperty


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
