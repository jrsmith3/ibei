# coding=utf-8
"""
Bose-Einstein integral calculators (:mod:`ibei.models`)
=======================================================
"""

import astropy.constants
import astropy.units
import attrs
import functools
import mpmath
import numpy as np


def _temperature_converter(value):
    try:
        temperature = astropy.units.Quantity(value, astropy.units.K)
    except astropy.units.UnitConversionError:
        temperature = value.to(astropy.units.K, equivalencies=astropy.units.temperature())

    return temperature


def _int_converter(value):
    if isinstance(value, str):
        try:
            int(value)
        except ValueError:
            raise TypeError("Argument must be coercible to type int.")

    elif int(value) != value:
        # I have to do some validation in this converter because if I were
        # to simply
        #
        # ```
        # return int(value)
        # ```
        #
        # I'd not be able to catch this case because the attribute
        # would be assigned to the possibly truncated value.
        raise TypeError("Argument must be coercible to type int without truncation.")

    return int(value)


def _validate_is_scalar(instance, attribute, value):
    if not value.isscalar:
        raise TypeError("Attributes must be scalar")


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


    Attributes
    ----------
    Same as parameters.


    Raises
    ------
    These exceptions define constraints on the arguments and attributes.

    TypeError
        If non-scalar arguments are passed to the constructor.
    TypeError
        If `order` not int type or not coercible to int without truncation.
    ValueError
        If `energy_bound` < 0
    ValueError
        If `temperature` <= 0
    ValueError
        If `chemical_potential` < 0


    Notes
    -----
    Instance attributes of `BEI` objects are of type
    `astropy.units.Quantity`. Computations involving units can be tricky,
    and the use of `Quantity` objects throughout will expose arithmetic
    implementation errors and unit conversion errors.
    """
    order: int = attrs.field(
            converter=_int_converter,
        )
    energy_bound: float | astropy.units.Quantity[astropy.units.eV] = attrs.field(
            converter=functools.partial(astropy.units.Quantity, unit=astropy.units.eV),
            validator=[
                _validate_is_scalar,
                attrs.validators.ge(0),
            ]
        )
    temperature: float | astropy.units.Quantity[astropy.units.K] = attrs.field(
            converter=_temperature_converter,
            validator=[
                _validate_is_scalar,
                attrs.validators.gt(0),
            ]
        )
    chemical_potential: float | astropy.units.Quantity[astropy.units.eV] = attrs.field(
            default=0.,
            converter=functools.partial(astropy.units.Quantity, unit=astropy.units.eV),
            validator=[
                _validate_is_scalar,
                attrs.validators.ge(0),
            ]
        )


    def lower(self) -> astropy.units.Quantity:
        """
        Lower incomplete Bose-Einstein integral.

        Returns
        -------
        astropy.units.Quantity
            Value of the Bose-Einstein integral.
        """
        bei = self.full() - self.upper()

        return bei


    def upper(self) -> astropy.units.Quantity:
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


        Returns
        -------
        astropy.units.Quantity
            Value of upper-incomplete Bose-Einstein integral.


        References
        ----------
        .. [1] :cite:`10.1016/j.sse.2006.06.017`
        """
        expt = self.reduced_chemical_potential - self.reduced_energy_bound
        real_arg = np.exp(expt.value)

        if self.reduced_chemical_potential == 0 and self.reduced_energy_bound == 0:
            # Specify this condition just to skip the next condition.
            term = float(mpmath.polylog(self.order + 1, real_arg))
            bei = term * self.prefactor * np.math.factorial(self.order)

        elif self.reduced_chemical_potential >= self.reduced_energy_bound:
            bei = 0 * self.prefactor * np.math.factorial(self.order)

        elif real_arg == 0:
            # When the lower bound of the integral approaches
            # infinity, the value of the integral approaches zero.
            bei = 0 * self.prefactor * np.math.factorial(self.order)

        else:
            summand = 0
            for indx in range(1, self.order + 2):
                index = self.order - indx + 1

                term = self.reduced_energy_bound**index * float(mpmath.polylog(indx, real_arg)) / np.math.factorial(index)

                summand += term

            bei = self.prefactor * summand * np.math.factorial(self.order)

        return bei


    def full(self) -> astropy.units.Quantity:
        """
        Full Bose-Einstein integral.

        Returns
        -------
        astropy.units.Quantity
            Value of the Bose-Einstein integral.
        """
        expt = self.reduced_chemical_potential
        real_arg = np.exp(expt.value)

        if self.reduced_chemical_potential > 0:
            bei = 0 * self.prefactor

        else:
            bei = self.prefactor * float(mpmath.gamma(self.order + 1)) * float(mpmath.polylog(self.order + 1, real_arg))

        return bei


    def photon_flux(self) -> astropy.units.Quantity[astropy.units.Unit("1/(m2 s)")]:
        """
        Number of photons radiated per unit time per unit area.

        Notes
        -----
        This convenience method is a special case of `BEI.full`. This method
        assumes the value of `order` is 2.
        """
        flux = (4 * np.pi * float(mpmath.zeta(3)) * self.kT**3) / \
            (astropy.constants.h**3 * astropy.constants.c**2)

        return flux.to("1/(m2 s)")


    def radiant_power_flux(self) -> astropy.units.Quantity[astropy.units.Unit("J/(m2 s)")]:
        """
        Energy radiated per unit time per unit area.

        Notes
        -----
        This convenience method implements the Stefan-Boltzmann law and is a
        special case of the `BEI.full`. This method assumes the value of
        `order` is 3.
        """
        power_flux = astropy.constants.sigma_sb * self.temperature**4

        return power_flux.to("J/(m2 s)")


    @property
    def kT(self) -> astropy.units.Quantity[astropy.units.dimensionless_unscaled]:
        """
        Product of Boltzmann's constant and temperature.
        """
        return (self.temperature * astropy.constants.k_B).decompose()

    @property
    def reduced_energy_bound(self) -> astropy.units.Quantity[astropy.units.dimensionless_unscaled]:
        """
        Dimensionless energy bound in units of kT.
        """
        return (self.energy_bound / self.kT).decompose()

    @property
    def reduced_chemical_potential(self) -> astropy.units.Quantity[astropy.units.dimensionless_unscaled]:
        """
        Dimensionless chemical potential in units of kT.
        """
        return (self.chemical_potential / self.kT).decompose()

    @property
    def prefactor(self) -> astropy.units.Quantity:
        """
        Factor preceding Bose-Einstein integral integration result.

        Note
        ----
        For `order=3`, this factor is NOT equal to the Stefan-Boltzmann
        constant. This factor is missing the Riemann-Zeta term.
        """
        return (2 * np.pi * self.kT**(self.order + 1)) / \
            (astropy.constants.h**3 * astropy.constants.c**2)


@attrs.frozen
class SQSolarcell():
    """
    Shockley-Queisser single-junction solar cell

    This class implements a solar cell as described by Shockley and
    Queisser :cite:`10.1063/1.1736034`.

    An :class:`SQSolarcell` is instantiated with a :class:`dict` having
    keys identical to the class's public data attributes. Each key's
    value must satisfy the constraints noted with the corresponding
    public data attribute. Dictionary values can be some kind of numeric
    type or of type :class:`astropy.units.Quantity` so long as the units
    are compatible with what's listed.    
    """
    bei = attrs.field(init=False)
    bandgap: float | astropy.units.Quantity[astropy.units.eV] = attrs.field(
            converter=functools.partial(astropy.units.Quantity, unit=astropy.units.eV),
            validator=[
                _validate_is_scalar,
                attrs.validators.ge(0),
            ]
        )
    solar_temperature: float | astropy.units.Quantity[astropy.units.K] = attrs.field(
            default=5772.,
            converter=_temperature_converter,
            validator=[
                _validate_is_scalar,
                attrs.validators.gt(0),
            ]
        )


    def __attrs_post_init__(self):
        bei = BEI(order=2, energy_bound=self.bandgap, temperature=self.solar_temperature, chemical_potential=0.)
        object.__setattr__(self, "bei", bei)


    def power_density(self) -> astropy.units.Quantity[astropy.units.Unit("W/m2")]:
        """
        Solar cell power density

        The output power density is calculated according to a slight
        modification of Shockley & Queisser's :cite:`10.1063/1.1736034` Eq.
        2.4. This method returns values of
        type :class:`astropy.units.Quantity` with units of [W m^-2].
        """
        if self.bandgap == 0:
            solar_flux = astropy.units.Quantity(0., "1/(m2 s)")
        else:
            solar_flux = self.bei.upper()

        power_density = self.bandgap * solar_flux

        return power_density.to("W/m2")


    def efficiency(self) -> astropy.units.Quantity[astropy.units.dimensionless_unscaled]:
        """
        Solar cell efficiency

        The efficiency is calculated according to Shockley &
        Queisser's :cite:`10.1063/1.1736034` Eq. 2.8. This method returns
        a :class:`float`.
        """
        power_density = self.power_density()
        solar_power_density = self.bei.radiant_power_flux()
        efficiency = power_density/solar_power_density

        return efficiency.decompose()


@attrs.frozen
class DeVosSolarcell(SQSolarcell):
    """
    DeVos single-junction solar cell

    This class implements a solar cell as described by
    DeVos :cite:`9780198513926` Ch. 6.

    An DeVosSolarcell is instantiated with a :class:`dict` having keys
    identical to the class's public data attributes. Each key's value
    must satisfy the constraints noted with the corresponding public data
    attribute. Dictionary values can be some kind of numeric type or of
    type :class:`astropy.units.Quantity` so long as the units are
    compatible with what's listed.
    """
    planetary_temperature: float | astropy.units.Quantity[astropy.units.K] = attrs.field(
            default=300.,
            converter=_temperature_converter,
            validator=[
                _validate_is_scalar,
                attrs.validators.gt(0),
            ]
        )
    voltage: float | astropy.units.Quantity[astropy.units.V] = attrs.field(
            default=0.,
            converter=functools.partial(astropy.units.Quantity, unit=astropy.units.V),
            validator=[
                _validate_is_scalar,
            ]
        )


    def power_density(self) -> astropy.units.Quantity[astropy.units.Unit("W/m2")]:
        """
        Solar cell power density

        The output power density is calculated according to
        DeVos's :cite:`9780198513926` Eq. 6.4. Note that this expression
        assumes fully concentrated sunlight and is therefore not completely
        general.

        This method returns values of type :class:`astropy.units.Quantity`
        with units of [W m^-2].
        """
        electron_energy = astropy.constants.e.si * self.voltage

        if self.bandgap == 0:
            solar_flux = astropy.units.Quantity(0., "1/(m2 s)")
            solar_cell_flux = astropy.units.Quantity(0., "1/(m2 s)")
        else:
            bei = BEI(
                    order=2,
                    energy_bound=self.bandgap,
                    temperature=self.planetary_temperature,
                    chemical_potential=electron_energy
                )
            solar_flux = self.bei.upper()
            solar_cell_flux = bei.upper()

        power_density = electron_energy * (solar_flux - solar_cell_flux)

        return power_density.to("W/m2")
