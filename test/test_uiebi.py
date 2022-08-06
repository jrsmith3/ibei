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


@pytest.mark.parametrize("argname,val", [
            ("energy_lo", units.s),
            ("temp", units.s),
            ("chem_potential", units.s),
        ]
    )
def test_arg_incompatible_unit(valid_quantity_args, argname, val):
    """
    Incompatible units raise `astropy.units.UnitConversionError`
    """
    valid_arg_value = valid_quantity_args[argname].value

    invalid_args = valid_quantity_args.copy()
    invalid_args[argname] = units.Quantity(valid_arg_value, val)

    with pytest.raises(units.UnitConversionError):
        val = ibei.uibei(**invalid_args)


@pytest.mark.parametrize("argname", [
            "energy_lo",
            "temp",
            "chem_potential",
        ]
    )
def test_arg_lt_0(valid_args, argname):
    """
    Arguments outside constraints raise `ValueError`
    """
    invalid_args = valid_args.copy()
    invalid_args[argname] *= -1

    assert invalid_args[argname] < 0

    with pytest.raises(ValueError):
        val = ibei.uibei(**invalid_args)


# Pytest fixture definitions
# ==========================
@pytest.fixture
def valid_quantity_args():
    """
    Valid arguments for `ibei.uibei` function
    """
    args = {
        "order": 2,
        "energy_lo": units.Quantity(1.15, units.eV),
        "temp": units.Quantity(5762., units.K),
        "chem_potential": units.Quantity(0.5, units.eV),
    }

    return args


@pytest.fixture(params=[(lambda x: x), (lambda x: getattr(x, "value", x))])
def valid_args(request, valid_quantity_args):
    args = {key: request.param(val) for key, val in valid_quantity_args.items()}

    return args
