# coding=utf-8

import astropy.units
import pytest

from contextlib import nullcontext as does_not_raise
from ibei import SQSolarcell


class TestSQSolarcellConstructorHappyPath():
    """
    Circumstances under which SQSolarcell instance can be instantiated
    """
    def test_args_without_default_values(self, valid_constructor_args):
        """
        SQSolarcell can be instantiated with valid args that don't have defaults
        """
        valid_constructor_args.pop("solar_temperature")

        with does_not_raise():
            solarcell = SQSolarcell(**valid_constructor_args)


@pytest.mark.parametrize("args,method_under_test,expected_output", [
            (
                # Special case.
                {
                    "solar_temperature": 5762,
                    "bandgap": 0.,
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
    solarcell = SQSolarcell(**args)
    output = getattr(solarcell, method_under_test)()

    assert output == expected_output


@pytest.mark.parametrize("method_under_test,expected_unit,args_mod", [
            ("power_density", "W/m2", {}),
            ("power_density", "W/m2", {"bandgap": 0.}),  # Special case.
            ("efficiency", astropy.units.dimensionless_unscaled, {}),
            ("efficiency", astropy.units.dimensionless_unscaled, {"bandgap": 0.}),  # Special case.
        ]
    )
def test_methods_units(method_under_test, expected_unit, valid_constructor_args, args_mod):
    """
    Units of returned value should match what's documented.
    """
    valid_constructor_args |= args_mod
    solarcell = SQSolarcell(**valid_constructor_args)
    output = getattr(solarcell, method_under_test)()

    assert output.unit.is_equivalent(expected_unit)


# Pytest fixture definitions
# ==========================
@pytest.fixture
def valid_constructor_args():
    args = {
        "solar_temperature": 5762,
        "bandgap": 1.15,
        }

    return args
