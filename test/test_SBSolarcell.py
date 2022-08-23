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


    def test_args_with_default_values(self, valid_constructor_args):
        """
        SQSolarcell can be instantiated with valid args incl. ones with defaults
        """
        with does_not_raise():
            solarcell = SQSolarcell(**valid_constructor_args)


    @pytest.mark.parametrize("argname", [
                "bandgap",
            ]
        )
    def test_args_that_can_equal_zero(self, valid_constructor_args, argname):
        """
        SQSolarcell can be instantiated with args not constrained to be nonzero
        """
        valid_constructor_args[argname] = 0

        with does_not_raise():
            solarcell = SQSolarcell(**valid_constructor_args)


    @pytest.mark.parametrize("argname,val", [
                ("solar_temperature", astropy.units.Quantity(5498.85, astropy.units.deg_C)),
                ("bandgap", astropy.units.Quantity(1e-19, astropy.units.J)),
            ]
        )
    def test_quantity_args_compatible_units(self, valid_constructor_quantity_args, argname, val):
        """
        SQSolarcell can be instantiated with args in compatible units
        """
        valid_constructor_quantity_args[argname] = val

        with does_not_raise():
            solarcell = SQSolarcell(**valid_constructor_quantity_args)


class TestSQSolarcellConstructorArgsOutsideConstraints():
    """
    SQSolarcell should raise exceptions if args are outside their constraints
    """
    @pytest.mark.parametrize("argname", [
                "solar_temperature",
            ]
        )
    def test_arg_eq_0(self, valid_constructor_args, argname):
        """
        SQSolarcell raises ValueError if arg equal to zero
        """
        invalid_constructor_args = valid_constructor_args.copy()
        invalid_constructor_args[argname] *= 0

        with pytest.raises(ValueError):
            solarcell = SQSolarcell(**invalid_constructor_args)


    @pytest.mark.parametrize("argname", [
                "bandgap",
                "solar_temperature",
            ]
        )
    def test_arg_lt_0(self, valid_constructor_args, argname):
        """
        SQSolarcell raises ValueError if arg less than zero
        """
        invalid_constructor_args = valid_constructor_args.copy()
        invalid_constructor_args[argname] *= -1

        with pytest.raises(ValueError):
            solarcell = SQSolarcell(**invalid_constructor_args)


@pytest.mark.parametrize("argname,val", [
            ("bandgap", astropy.units.s),
            ("solar_temperature", astropy.units.s),
        ]
    )
def test_constructor_args_incompatible_units(valid_constructor_quantity_args, argname, val):
    """
    SQSolarcell raises astropy.units.UnitConversionError if arg has incompatible unit
    """
    valid_constructor_arg_value = valid_constructor_quantity_args[argname].value

    invalid_constructor_args = valid_constructor_quantity_args.copy()
    invalid_constructor_args[argname] = astropy.units.Quantity(valid_constructor_arg_value, val)

    with pytest.raises(astropy.units.UnitConversionError):
        solarcell = SQSolarcell(**invalid_constructor_args)


@pytest.mark.parametrize("argname", [
            "bandgap",
            "solar_temperature",
        ]
    )
def test_constructor_args_non_scalar(valid_constructor_args, argname):
    """
    SQSolarcell raises TypeError if arg is non-scalar
    """
    invalid_constructor_args = valid_constructor_args.copy()
    val = valid_constructor_args[argname]
    invalid_constructor_args[argname] = [val, val]

    with pytest.raises(TypeError):
        solarcell = SQSolarcell(**invalid_constructor_args)


@pytest.mark.parametrize("args,method_under_test,expected_output", [
            # Special case
            (
                {
                    "solar_temperature": 5762,
                    "bandgap": 0.,
                },
                "power_density",
                astropy.units.Quantity(0., "W/m2"),
            ),
            (
                {
                    "solar_temperature": 5762,
                    "bandgap": 1.15,
                },
                "power_density",
                astropy.units.Quantity(27326140.07319352, "W/m2"),
            ),
            # Special case
            (
                {
                    "solar_temperature": 5762,
                    "bandgap": 0.,
                },
                "efficiency",
                astropy.units.Quantity(0.),
            ),
            (
                {
                    "solar_temperature": 5762,
                    "bandgap": 1.15,
                },
                "efficiency",
                astropy.units.Quantity(0.43719334),
            ),
        ]
    )
def test_methods_regression(args, method_under_test, expected_output):
    """
    Methods' output values should match expected results
    """
    solarcell = SQSolarcell(**args)
    output = getattr(solarcell, method_under_test)()

    assert astropy.units.allclose(expected_output, output)


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
def valid_constructor_quantity_args():
    args = {
        "solar_temperature": astropy.units.Quantity(5762., astropy.units.K),
        "bandgap": astropy.units.Quantity(1.15, astropy.units.eV),
        }

    return args


@pytest.fixture(params=[(lambda x: x), (lambda x: getattr(x, "value", x))])
def valid_constructor_args(request, valid_constructor_quantity_args):
    args = {key: request.param(val) for key, val in valid_constructor_quantity_args.items()}

    return args
