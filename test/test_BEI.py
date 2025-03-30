# coding=utf-8

import astropy.units
import numpy as np
import pytest

from contextlib import nullcontext as does_not_raise
from ibei import BEI


class TestBEIConstructorHappyPath():
    """
    Circumstances under which BEI instance can be instantiated
    """
    def test_args_without_default_values(self, valid_constructor_args):
        """
        BEI can be instantiated with valid args that don't have defaults
        """
        valid_constructor_args.pop("chemical_potential")

        with does_not_raise():
            bei = BEI(**valid_constructor_args)


    def test_args_with_default_values(self, valid_constructor_args):
        """
        BEI can be instantiated with valid args incl. ones with defaults
        """
        with does_not_raise():
            bei = BEI(**valid_constructor_args)


    @pytest.mark.parametrize("argname", [
                "energy_bound",
                "chemical_potential",
            ]
        )
    def test_args_that_can_equal_zero(self, valid_constructor_args, argname):
        """
        BEI can be instantiated with args not constrained to be nonzero
        """
        valid_constructor_args[argname] = 0

        with does_not_raise():
            bei = BEI(**valid_constructor_args)


    @pytest.mark.parametrize("argname,val", [
                ("energy_bound", astropy.units.Quantity(3.20435313e-19, astropy.units.J)),
                ("temperature", astropy.units.Quantity(5498.85, astropy.units.deg_C)),
                ("chemical_potential", astropy.units.Quantity(1e-19, astropy.units.J)),
            ]
        )
    def test_quantity_args_compatible_units(self, valid_constructor_quantity_args, argname, val):
        """
        BEI can be instantiated with args in compatible units
        """
        valid_constructor_quantity_args[argname] = val

        with does_not_raise():
            bei = BEI(**valid_constructor_quantity_args)


    @pytest.mark.parametrize("val", [
                "12",
                12.,
                12.0,
            ]
        )
    def test_order_arg_coercible_to_int(self, valid_constructor_args, val):
        """
        BEI can be instantiated with `order` value coercible to int type
        """
        assert not isinstance(val, int)

        valid_constructor_args["order"] = val

        with does_not_raise():
            bei = BEI(**valid_constructor_args)


class TestBEIConstructorArgsOutsideConstraints():
    """
    BEI should raise exceptions if args are outside their constraints
    """
    @pytest.mark.parametrize("argname", [
                "temperature",
            ]
        )
    def test_arg_eq_0(self, valid_constructor_args, argname):
        """
        BEI raises ValueError if arg equal to zero
        """
        invalid_constructor_args = valid_constructor_args.copy()
        invalid_constructor_args[argname] *= 0

        with pytest.raises(ValueError):
            bei = BEI(**invalid_constructor_args)


    @pytest.mark.parametrize("argname", [
                "energy_bound",
                "temperature",
                "chemical_potential",
            ]
        )
    def test_arg_lt_0(self, valid_constructor_args, argname):
        """
        BEI raises ValueError if arg less than zero
        """
        invalid_constructor_args = valid_constructor_args.copy()
        invalid_constructor_args[argname] *= -1

        with pytest.raises(ValueError):
            bei = BEI(**invalid_constructor_args)


@pytest.mark.parametrize("argname,val", [
            ("energy_bound", astropy.units.s),
            ("temperature", astropy.units.s),
            ("chemical_potential", astropy.units.s),
        ]
    )
def test_constructor_args_incompatible_units(valid_constructor_quantity_args, argname, val):
    """
    BEI raises astropy.units.UnitConversionError if arg has incompatible unit


    Notes
    -----
    There is only one test in this category so I am implementing it as a
    function instead of a method on a class.
    """
    valid_constructor_arg_value = valid_constructor_quantity_args[argname].value

    invalid_constructor_args = valid_constructor_quantity_args.copy()
    invalid_constructor_args[argname] = astropy.units.Quantity(valid_constructor_arg_value, val)

    with pytest.raises(astropy.units.UnitConversionError):
        bei = BEI(**invalid_constructor_args)


@pytest.mark.parametrize("argname", [
            "order",
            "energy_bound",
            "temperature",
            "chemical_potential",
        ]
    )
def test_constructor_args_non_scalar(valid_constructor_args, argname):
    """
    BEI raises TypeError if arg is non-scalar


    Notes
    -----
    There is only one test in this category so I am implementing it as a
    function instead of a method on a class.
    """
    invalid_constructor_args = valid_constructor_args.copy()
    val = valid_constructor_args[argname]
    invalid_constructor_args[argname] = [val, val]

    with pytest.raises(TypeError):
        bei = BEI(**invalid_constructor_args)


@pytest.mark.parametrize("val", [
            "12.2",
            12.2
        ]
    )
def test_order_arg_not_coercible_to_int(valid_constructor_args, val):
    """
    BEI raises TypeError if `order` not int type or not coercible to int without truncation
    """
    invalid_constructor_args = valid_constructor_args.copy()
    invalid_constructor_args["order"] = val

    with pytest.raises(TypeError):
        bei = BEI(**invalid_constructor_args)


class TestIssues():
    """
    Tests corresponding to issues raised due to bugs
    """
    def test_issue_2_uibei(self):
        """
        Refactor of issue 2 focusing on uibei
        """
        with does_not_raise():
            BEI(order=2, energy_bound=1.15, temperature=5762., chemical_potential=1.2).upper()

    def test_issue_4(self):
        """
        uibei shouldn't fail when energy_lo == chem_potential
        """
        with does_not_raise():
            BEI(order=2, energy_bound=1., temperature=300., chemical_potential=1.).upper()

    def test_issue_31(self):
        """
        Passing `energy_lo=0` with `chem_potential=0` should yield nonzero result
        """
        energy_flux = BEI(order=3, energy_bound=0., temperature=300., chemical_potential=0.).upper()
        assert energy_flux > 0


@pytest.mark.parametrize("args,method_under_test,expected_output", [
            (
                {
                    "order": 3,
                    "energy_bound": 1.1,
                    "temperature": 3000,
                    "chemical_potential": 0,
                },
                "lower",
                astropy.units.Quantity(2949919.81423557, "J/(m2 s)"),
            ),
            (
                {
                    "order": 2,
                    "energy_bound": 1.1,
                    "temperature": 300,
                    "chemical_potential": 0,
                },
                "upper",
                astropy.units.Quantity(10549122.240303338, "1/(m2 s)"),
            ),
            (
                {
                    "order": 3,
                    "energy_bound": 1.1,
                    "temperature": 300,
                    "chemical_potential": 0,
                },
                "full",
                astropy.units.Quantity(459.30032795, "W/m2"),
            ),
            (
                {
                    "order": 2,
                    "energy_bound": 1.1,
                    "temperature": 300,
                    "chemical_potential": 0,
                },
                "photon_flux",
                astropy.units.Quantity(4.1052443203614687e+22, "1/(m2 s)"),
            ),
            (
                {
                    "order": 2,
                    "energy_bound": 1.1,
                    "temperature": 300,
                    "chemical_potential": 0,
                },
                "radiant_power_flux",
                astropy.units.Quantity(459.30032795, "W/m2"),
            ),
            (
                {
                    "order": 2,
                    "energy_bound": 1.1,
                    "temperature": 300,
                    "chemical_potential": 0,
                },
                "kT",
                astropy.units.Quantity(4.141947e-21, "J"),
            ),
            (
                {
                    "order": 2,
                    "energy_bound": 1.1,
                    "temperature": 300,
                    "chemical_potential": 0,
                },
                "reduced_energy_bound",
                astropy.units.Quantity(42.54989978, astropy.units.dimensionless_unscaled),
            ),
            (
                {
                    "order": 2,
                    "energy_bound": 2.1,
                    "temperature": 300,
                    "chemical_potential": 1.1,
                },
                "reduced_chemical_potential",
                astropy.units.Quantity(42.54989978, astropy.units.dimensionless_unscaled),
            ),
            (
                {
                    "order": 2,
                    "energy_bound": 1.1,
                    "temperature": 300,
                    "chemical_potential": 0,
                },
                "prefactor",
                astropy.units.Quantity(1.70759151e+22, "1/(m2 s)"),
            ),
        ]
    )
def test_methods_regression(args, method_under_test, expected_output):
    """
    Methods' output values should match expected results

    Notes
    -----
    This test tests each of the methods of a `BEI` instance at least once.
    """
    bei = BEI(**args)
    method = getattr(bei, method_under_test)

    if callable(method):
        output = method()
    else:
        output = method

    assert astropy.units.allclose(expected_output, output)


@pytest.mark.parametrize("order,expected_unit", [
            (2, "1/(m2 s)"),
            (3, "J/(m2 s)"),
        ]
    )
@pytest.mark.parametrize("method_under_test", 
        (
            "lower",
            "upper",
            "full",
        )
    )
def test_methods_units(order, expected_unit, method_under_test, valid_constructor_quantity_args):
    """
    Methods' units should match known units for low orders

    Notes
    -----
    For `order==2` the calculator methods should return particle flux, for
    `order==3` the calculator methods should return energy flux.

    I am aware that the arguments of this function are in a different
    order than `test_methods_regression`. I have my reasons.
    """
    valid_constructor_quantity_args["order"] = order
    bei = BEI(**valid_constructor_quantity_args)

    output = getattr(bei, method_under_test)()

    assert output.unit.is_equivalent(expected_unit)


def test_consistency_upper_and_full_methods(valid_constructor_quantity_args):
    """
    When `energy_bound` is 0, `BEI.upper` should equal `BEI.full`.
    """
    valid_constructor_quantity_args["energy_bound"] = 0

    bei = BEI(**valid_constructor_quantity_args)

    assert astropy.units.allclose(bei.upper(), bei.full())


def test_consistency_lower_and_full_methods(valid_constructor_quantity_args):
    """
    When `energy_bound` is `np.inf`, `BEI.lower` should equal `BEI.full`.

    Notes
    -----
    This condition holds as long as `chemical_potential` equals zero.
    """
    valid_constructor_quantity_args["energy_bound"] = np.inf
    valid_constructor_quantity_args["chemical_potential"] = 0.

    bei = BEI(**valid_constructor_quantity_args)

    assert astropy.units.allclose(bei.lower(), bei.full())


@pytest.mark.parametrize("order,helper_method_name",[
            (2, "photon_flux"),
            (3, "radiant_power_flux"),
        ]
    )
def test_consistency_full_and_helper_methods(order, helper_method_name, valid_constructor_quantity_args):
    """
    `BEI.full` should equal `BEI.photon_flux` and `BEI.radiant_power_flux` for order 2 and 3, respectively.

    Notes
    -----
    This condition holds as long as `chemical_potential` equals zero.
    """
    valid_constructor_quantity_args["order"] = order
    valid_constructor_quantity_args["chemical_potential"] = 0.
    bei = BEI(**valid_constructor_quantity_args)
    output = getattr(bei, helper_method_name)()

    assert astropy.units.allclose(bei.full(), output)


# Pytest fixture definitions
# ==========================
@pytest.fixture
def valid_constructor_quantity_args():
    """
    Valid constructor arguments for BEI
    """
    args = {
        "order": 2,
        "energy_bound": astropy.units.Quantity(1.15, astropy.units.eV),
        "temperature": astropy.units.Quantity(5762., astropy.units.K),
        "chemical_potential": astropy.units.Quantity(0.5, astropy.units.eV),
    }

    return args


@pytest.fixture(params=[(lambda x: x), (lambda x: getattr(x, "value", x))])
def valid_constructor_args(request, valid_constructor_quantity_args):
    args = {key: request.param(val) for key, val in valid_constructor_quantity_args.items()}

    return args
