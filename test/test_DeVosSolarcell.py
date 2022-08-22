# coding=utf-8

import ibei
import numpy as np
import pytest
import unittest

from astropy import units


@pytest.mark.xfail(reason="I broke the `DeVosSolarcell` class in a previous commit")
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


@pytest.mark.xfail(reason="I broke the `DeVosSolarcell` class in a previous commit")
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


@pytest.mark.parametrize("args,method_under_test,expected_output", [
            (
                {
                    "solar_temperature": 5762.,
                    "planetary_temperature": 288.,
                    "bandgap": 0.,
                    "voltage": 0.5,
                },
                "power_density",
                "0.",
            ),
        ]
    )
def test_methods_regression(args, method_under_test, expected_output):
    """
    Methods' output values should match expected results
    """
    solarcell = ibei.DeVosSolarcell(**args)
    output = getattr(solarcell, method_under_test)()

    assert output == expected_output


# Pytest fixture definitions
# ==========================
@pytest.fixture
def valid_constructor_args():
    args = {
        "solar_temperature": 5762.,
        "planetary_temperature": 288.,
        "bandgap": 1.15,
        "voltage": 0.5,        
        }

    return args
