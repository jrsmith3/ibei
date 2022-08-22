# coding=utf-8

import astropy.units
import ibei
import pytest

from contextlib import nullcontext as does_not_raise


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


@pytest.mark.parametrize("method_under_test,expected_unit,args_mod", [
            ("power_density", "W/m2", {}),
            ("power_density", "W/m2", {"bandgap": 0.}),
            ("efficiency", astropy.units.dimensionless_unscaled, {}),
            ("efficiency", astropy.units.dimensionless_unscaled, {"bandgap": 0.}),
        ]
    )
def test_methods_units(method_under_test, expected_unit, valid_constructor_args, args_mod):
    """
    Units of returned value should match what's documented.
    """
    valid_constructor_args |= args_mod
    solarcell = ibei.DeVosSolarcell(**valid_constructor_args)
    output = getattr(solarcell, method_under_test)()

    assert output.unit.is_equivalent(expected_unit)


class Issues():
    """
    Tests corresponding to issues raised due to bugs
    """
    def test_issue_3_DeVosSolarcell(self):
        """
        Inconsistent units cause exception when chem_potential > energy_lo.
        """
        args = {
                "temp_sun": 5762,
                "temp_planet": 288,
                "bandgap": 0.1,
                "voltage": 0.5,
            }
        solarcell = ibei.DeVosSolarcell(**args)

        with does_not_raise:
            solarcell.power_density()


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
