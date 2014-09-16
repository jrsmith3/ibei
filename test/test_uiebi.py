# -*- coding: utf-8 -*-
import numpy as np
import ibei
from astropy import units
import unittest

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
    pass


class CalculatorsArgsOutsideConstraints(unittest.TestCase):
    """
    Tests calling with args are outside constraints.
    """
    pass


if __name__ == "__main__":
    pass
