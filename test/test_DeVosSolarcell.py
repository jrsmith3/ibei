# -*- coding: utf-8 -*-
import numpy as np
import ibei
from astropy import units
import unittest

temp_sun = 5762.
temp_earth = 288.
bandgap = 1.15

input_params = {"temp_sun": temp_sun,
                "temp_planet": temp_earth,
                "bandgap": bandgap,
                "voltage": 0.5,}

class Issues(unittest.TestCase):
    """
    Tests output types of the calculator methods.
    """

    def test_issue_3_DeVosSolarcell(self):
        """
        Inconsistent units cause exception when chem_potential > energy_lo.
        """
        ip = {"temp_sun": 5762,
              "temp_planet": 288,
              "bandgap": 0.1,
              "voltage": 0.5,}
        sc = ibei.DeVosSolarcell(ip)
        try:
            sc.calc_power_density()
        except:
            self.fail("Succumbing to issue #3.")


class CalculatorsReturnUnits(unittest.TestCase):
    """
    Tests units of the calculator methods returned values.
    """
    def setUp(self):
        """
        Initialize DeVosSolarcell object from input_params
        """
        self.solarcell = ibei.DeVosSolarcell(input_params)

    def test_calc_power_density(self):
        """
        calc_power_density should return value with unit of W m^-2.
        """
        tested_unit = self.solarcell.calc_power_density().unit
        target_unit = units.Unit("W/m2")
        self.assertEqual(tested_unit, target_unit)

    def test_calc_power_density_zero_bandgap(self):
        """
        calc_power_density should return value with unit of W m^-2.
        """
        self.solarcell.bandgap = 0
        tested_unit = self.solarcell.calc_power_density().unit
        target_unit = units.Unit("W/m2")
        self.assertEqual(tested_unit, target_unit)


class CalculatorsReturnValue(unittest.TestCase):
    """
    Tests special values of the calculator methods.
    """
    def setUp(self):
        """
        Initialize DeVosSolarcell object from input_params
        """
        self.solarcell = ibei.DeVosSolarcell(input_params)

    def test_calc_power_density(self):
        """
        calc_power_density should return 0 when bandgap = 0.
        """
        self.solarcell.bandgap = 0
        self.assertEqual(0, self.solarcell.calc_power_density())


if __name__ == "__main__":
    pass
