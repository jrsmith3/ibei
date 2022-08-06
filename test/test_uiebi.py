# -*- coding: utf-8 -*-
import ibei
import numpy as np
import pytest
import unittest

from astropy import units


temp_sun = 5762.
temp_earth = 288.
bandgap = 1.15


class Issues(unittest.TestCase):
    """
    Tests output types of the calculator methods.
    """
    def test_issue_2_uibei(self):
        """
        Refactor of issue 2 focusing on uibei
        """
        try:
            ibei.uibei(2, bandgap, temp_sun, 1.2)
        except:
            self.fail("Error raised with arguments.")

    def test_issue_4(self):
        """
        uibei shouldn't fail when energy_lo == chem_potential
        """
        try:
            ibei.uibei(2, 1., 300., 1.)
        except:
            self.fail("uibei fails when energy_lo == chem_potential")

    def test_issue_31(self):
        """
        Passing `energy_lo=0` with `chem_potential=0` should yield nonzero result
        """
        energy_flux = ibei.uibei(3, 0., 300., 0.)
        self.assertGreater(energy_flux, 0)


class CalculatorsArgsWrongType(unittest.TestCase):
    """
    Tests calling with args of invalid type.
    """
    def test_uibei_order_nonint(self):
        """
        uibei should raise TypeError for non-int order.
        """
        order = "not even numeric"
        self.assertRaises(TypeError, ibei.uibei, [order, bandgap, temp_sun, 0.])

    def test_uibei_order_float(self):
        """
        uibei should raise TypeError for order of type float.
        """
        order = 2.3
        self.assertRaises(TypeError, ibei.uibei, [order, bandgap, temp_sun, 0.])

    def test_uibei_energy_lo_nonnumeric(self):
        """
        uibei should raise TypeError for non-numeric energy_lo.
        """
        energy_lo = "non numeric"
        self.assertRaises(TypeError, ibei.uibei, [2, energy_lo, temp_sun, 0.])

    def test_uibei_temp_nonnumeric(self):
        """
        uibei should raise TypeError for non-numeric temp.
        """
        temp = "non numeric"
        self.assertRaises(TypeError, ibei.uibei, [2, bandgap, temp, 0.])

    def test_uibei_chem_potential_nonnumeric(self):
        """
        uibei should raise TypeError for non-numeric chem_potential.
        """
        cp = "non numeric"
        self.assertRaises(TypeError, ibei.uibei, [2, bandgap, temp_sun, cp])


class CalculatorsArgsWrongUnits(unittest.TestCase):
    """
    Tests calling with args with incorrect units.
    """
    def test_uibei_energy_lo(self):
        """
        uibei should raise UnitsError for energy_lo with units not energy.
        """
        energy_lo = units.Quantity(1.)
        self.assertRaises(units.UnitsError, ibei.uibei, 2, energy_lo, temp_sun, 0.)

    def test_uibei_temp(self):
        """
        uibei should raise UnitsError for temp with units not temperature.
        """
        temp = units.Quantity(1.)
        self.assertRaises(units.UnitsError, ibei.uibei, 2, bandgap, temp, 0.)

    def test_uibei_chem_potential(self):
        """
        uibei should raise UnitsError for chem_potential with units not energy.
        """
        cp = units.Quantity(1.)
        self.assertRaises(units.UnitsError, ibei.uibei, 2, bandgap, temp_sun, cp)


class CalculatorsArgsOutsideConstraints(unittest.TestCase):
    """
    Tests calling with args are outside constraints.
    """
    def test_uibei_energy_lo(self):
        """
        uibei should raise UnitsError for energy_lo values < 0.
        """
        energy_lo = -1.
        self.assertRaises(ValueError, ibei.uibei, 2, energy_lo, temp_sun, 0.)

    def test_uibei_temp(self):
        """
        uibei should raise UnitsError for temp values < 0.
        """
        temp = -1.
        self.assertRaises(ValueError, ibei.uibei, 2, bandgap, temp, 0.)

    def test_uibei_chem_potential(self):
        """
        uibei should raise UnitsError for chem_potential values < 0.
        """
        cp = -1.
        self.assertRaises(ValueError, ibei.uibei, 2, bandgap, temp_sun, cp)


@pytest.fixture
def valid_quantity_args():
    """
    Valid arguments for `ibei.uibei` function
    """
    args = {
        "order": 2,
        "energy_lo": units.Quantity(1.15, units.eV),
        "temp": units.Quantity(5762., units.K),
        "chem_potential": units.Quantity(0., units.eV),
    }

    return args
