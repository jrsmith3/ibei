# -*- coding: utf-8 -*-

import numpy as np
from astropy import constants
from astropy import units
from sympy.mpmath import polylog
from electrode import PhysicalProperty, find_PhysicalProperty


def uibei(order, energy_lo, temp, chem_potential):
    """
    Upper incomplete Bose-Einstein integral.

    The upper incomplete Bose-Einstein integral is given by (cf. [1]):

    $F_{m}(E_{A},T,\mu) = \frac{2 \pi}{h^{3}c^{2}} \int_{E_{A}}^{\infty} E^{m} \frac{1}{\exp \left( \frac{E - \mu}{kT} \right) - 1} dE$

    for condition $\mu < E_{A}$; the value of $F_{m}$ is zero when the previous condition is not met.

    :param int order: Order of Bose-Einstein integral. A value of 2 yields the particle flux, a value of 3 yields energy flux. Corresponds to $m$.
    :param float energy_lo: Lower bound of integral [eV]. Corresponds to $E_{A}$. Bound: > 0.
    :param float temp: Temperature of photon ensemble [K]. Corresponds to $T$. Bound: > 0.
    :param float chem_potential: Chemical potential of photon ensemble [eV]. Corresponds to $\mu$. Bound > 0.

    Note that the float quantities above can also be astropy.units.Quantity as long as the units are compatible.

    [1] Levy, M. Y. and Honsberg, C. (2006) Solid-State Electronics 50(78), 1400 – 1405, 10.1016/j.sse.2006.06.017.
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

    if reduced_chem_potential > reduced_energy_lo:
        return 0.

    prefactor = (2 * np.pi * np.math.factorial(order) * kT**(order + 1)) / \
        (constants.h**3 * constants.c**2)

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

    This class implements a solar cell as described by Shockley and Queisser [1].

    An SQSolarcell is instantiated with a dict having keys identical to the class's public data attributes. Each key's value must satisfy the constraints noted with the corresponding public data attribute. Dictionary values can be some kind of numeric type or of type `astropy.units.Quantity` so long as the units are compatible with what's listed.

    All numerical methods return data of type astropy.units.Quantity.

    [1] Shockley, W. and Queisser, H. J. (1961) Journal of Applied Physics 32(3), 510–519, 10.1063/1.1736034. 
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

        $W = \sigma T^{4}$

        where

        $\sigma = \frac{2 \pi^{5} k^{4}}{15 c^{2} h^{3}}

        and

        * $T$: Solar temperature
        * $k$: Boltzmann's constant
        * $h$: Planck's constant
        * $c$: Speed of light in vacuum

        This method returns values of type `astropy.units.Quantity` with units of [W m^-2].
        """
        radiant_power_density = constants.sigma_sb * self.temp_sun**4

        return radiant_power_density.to("W/m2")



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
