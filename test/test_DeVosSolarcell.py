# coding=utf-8

import astropy.units
import pytest

from contextlib import nullcontext as does_not_raise
from ibei import DeVosSolarcell


class TestDeVosSolarcellConstructorHappyPath():
    """
    Circumstances under which DeVosSolarcell instance can be instantiated
    """
    def test_args_without_default_values(self, valid_constructor_args):
        """
        DeVosSolarcell can be instantiated with valid args that don't have defaults
        """
        valid_constructor_args.pop("solar_temperature")
        valid_constructor_args.pop("planetary_temperature")
        valid_constructor_args.pop("voltage")

        with does_not_raise():
            solarcell = DeVosSolarcell(**valid_constructor_args)


    def test_args_with_default_values(self, valid_constructor_args):
        """
        DeVosSolarcell can be instantiated with valid args incl. ones with defaults
        """
        with does_not_raise():
            solarcell = DeVosSolarcell(**valid_constructor_args)


    @pytest.mark.parametrize("argname", [
                "bandgap",
                "voltage"
            ]
        )
    def test_args_that_can_equal_zero(self, valid_constructor_args, argname):
        """
        DeVosSolarcell can be instantiated with args not constrained to be nonzero
        """
        valid_constructor_args[argname] = 0

        with does_not_raise():
            solarcell = DeVosSolarcell(**valid_constructor_args)


    @pytest.mark.parametrize("argname", [
                "voltage"
            ]
        )
    def test_args_that_can_be_lt_0(self, valid_constructor_args, argname):
        """
        DeVosSolarcell can be instantiated with args less than zero
        """
        valid_constructor_args[argname] *= -1

        with does_not_raise():
            solarcell = DeVosSolarcell(**valid_constructor_args)


    @pytest.mark.parametrize("argname,val", [
                ("solar_temperature", astropy.units.Quantity(5498.85, astropy.units.deg_C)),
                ("bandgap", astropy.units.Quantity(1e-19, astropy.units.J)),
                ("planetary_temperature", astropy.units.Quantity(27., astropy.units.deg_C)),
            ]
        )
    def test_quantity_args_compatible_units(self, valid_constructor_quantity_args, argname, val):
        """
        DeVosSolarcell can be instantiated with args in compatible units

        Note
        ----
        No unit is equivalent to volts.
        """
        valid_constructor_quantity_args[argname] = val

        with does_not_raise():
            solarcell = DeVosSolarcell(**valid_constructor_quantity_args)


class TestDeVosSolarcellConstructorArgsOutsideConstraints():
    """
    DeVosSolarcell should raise exceptions if args are outside their constraints
    """
    @pytest.mark.parametrize("argname", [
                "solar_temperature",
                "planetary_temperature",
            ]
        )
    def test_arg_eq_0(self, valid_constructor_args, argname):
        """
        DeVosSolarcell raises ValueError if arg equal to zero
        """
        invalid_constructor_args = valid_constructor_args.copy()
        invalid_constructor_args[argname] *= 0

        with pytest.raises(ValueError):
            solarcell = DeVosSolarcell(**invalid_constructor_args)


    @pytest.mark.parametrize("argname", [
                "bandgap",
                "solar_temperature",
                "planetary_temperature",
            ]
        )
    def test_arg_lt_0(self, valid_constructor_args, argname):
        """
        DeVosSolarcell raises ValueError if arg less than zero
        """
        invalid_constructor_args = valid_constructor_args.copy()
        invalid_constructor_args[argname] *= -1

        with pytest.raises(ValueError):
            solarcell = DeVosSolarcell(**invalid_constructor_args)


@pytest.mark.parametrize("argname,val", [
            ("bandgap", astropy.units.s),
            ("solar_temperature", astropy.units.s),
            ("planetary_temperature", astropy.units.s),
            ("voltage", astropy.units.s),
        ]
    )
def test_constructor_args_incompatible_units(valid_constructor_quantity_args, argname, val):
    """
    DeVosSolarcell raises astropy.units.UnitConversionError if arg has incompatible unit
    """
    valid_constructor_arg_value = valid_constructor_quantity_args[argname].value

    invalid_constructor_args = valid_constructor_quantity_args.copy()
    invalid_constructor_args[argname] = astropy.units.Quantity(valid_constructor_arg_value, val)

    with pytest.raises(astropy.units.UnitConversionError):
        solarcell = DeVosSolarcell(**invalid_constructor_args)


@pytest.mark.parametrize("argname", [
            "bandgap",
            "solar_temperature",
            "planetary_temperature",
            "voltage",
        ]
    )
def test_constructor_args_non_scalar(valid_constructor_args, argname):
    """
    DeVosSolarcell raises TypeError if arg is non-scalar
    """
    invalid_constructor_args = valid_constructor_args.copy()
    val = valid_constructor_args[argname]
    invalid_constructor_args[argname] = [val, val]

    with pytest.raises(TypeError):
        solarcell = DeVosSolarcell(**invalid_constructor_args)


@pytest.mark.parametrize("args,method_under_test,expected_output", [
            # Special case.
            (
                {
                    "solar_temperature": 5762.,
                    "planetary_temperature": 288.,
                    "bandgap": 0.,
                    "voltage": 0.5,
                },
                "power_density",
                astropy.units.Quantity(0., "W/m2"),
            ),
            (
                {
                    "solar_temperature": 5762.,
                    "planetary_temperature": 288.,
                    "bandgap": 1.15,
                    "voltage": 0.5,
                },
                "power_density",
                astropy.units.Quantity(11880930.46659443, "W/m2"),
            ),
            # Special case
            (
                {
                    "solar_temperature": 5762.,
                    "planetary_temperature": 288.,
                    "bandgap": 0.,
                    "voltage": 0.5,
                },
                "efficiency",
                astropy.units.Quantity(0.),
            ),
            (
                {
                    "solar_temperature": 5762.,
                    "planetary_temperature": 288.,
                    "bandgap": 1.15,
                    "voltage": 0.5,
                },
                "efficiency",
                astropy.units.Quantity(0.19008406),
            ),
        ]
    )
def test_methods_regression(args, method_under_test, expected_output):
    """
    Methods' output values should match expected results
    """
    solarcell = DeVosSolarcell(**args)
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
    solarcell = DeVosSolarcell(**valid_constructor_args)
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
        solarcell = DeVosSolarcell(**args)

        with does_not_raise:
            solarcell.power_density()


# Pytest fixture definitions
# ==========================
@pytest.fixture
def valid_constructor_quantity_args():
    args = {
        "solar_temperature": astropy.units.Quantity(5762., astropy.units.K),
        "planetary_temperature": astropy.units.Quantity(288., astropy.units.K),
        "bandgap": astropy.units.Quantity(1.15, astropy.units.eV),
        "voltage": astropy.units.Quantity(0.1, astropy.units.V),
        }

    return args


@pytest.fixture(params=[(lambda x: x), (lambda x: getattr(x, "value", x))])
def valid_constructor_args(request, valid_constructor_quantity_args):
    args = {key: request.param(val) for key, val in valid_constructor_quantity_args.items()}

    return args
