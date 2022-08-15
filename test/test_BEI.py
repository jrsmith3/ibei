# -*- coding: utf-8 -*-
import astropy.units
import ibei
import pytest

from contextlib import nullcontext as does_not_raise


# BEI tests
# ---------
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
            bei = ibei.models.BEI(**valid_constructor_args)


    def test_args_with_default_values(self, valid_constructor_args):
        """
        BEI can be instantiated with valid args incl. ones with defaults
        """
        with does_not_raise():
            bei = ibei.models.BEI(**valid_constructor_args)


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
            bei = ibei.models.BEI(**valid_constructor_args)


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
            bei = ibei.models.BEI(**valid_constructor_quantity_args)


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
            bei = ibei.models.BEI(**valid_constructor_args)


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
            bei = ibei.models.BEI(**invalid_constructor_args)


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
            bei = ibei.models.BEI(**invalid_constructor_args)


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
        bei = ibei.models.BEI(**invalid_constructor_args)


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
        bei = ibei.models.BEI(**invalid_constructor_args)


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
        bei = ibei.models.BEI(**invalid_constructor_args)


# uibei tests
# -----------
class TestIssues():
    """
    Tests corresponding to issues raised due to bugs
    """
    def test_issue_2_uibei(self):
        """
        Refactor of issue 2 focusing on uibei
        """
        with does_not_raise():
            ibei.models.uibei(2, 1.15, 5762., 1.2)

    def test_issue_4(self):
        """
        uibei shouldn't fail when energy_lo == chem_potential
        """
        with does_not_raise():
            ibei.models.uibei(2, 1., 300., 1.)

    def test_issue_31(self):
        """
        Passing `energy_lo=0` with `chem_potential=0` should yield nonzero result
        """
        energy_flux = ibei.models.uibei(3, 0., 300., 0.)
        assert energy_flux > 0


@pytest.mark.parametrize("argname,val", [
            ("energy_lo", astropy.units.s),
            ("temp", astropy.units.s),
            ("chem_potential", astropy.units.s),
        ]
    )
def test_arg_incompatible_unit(valid_quantity_args, argname, val):
    """
    Incompatible units raise `astropy.units.UnitConversionError`
    """
    valid_arg_value = valid_quantity_args[argname].value

    invalid_args = valid_quantity_args.copy()
    invalid_args[argname] = astropy.units.Quantity(valid_arg_value, val)

    with pytest.raises(astropy.units.UnitConversionError):
        val = ibei.models.uibei(**invalid_args)


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
        val = ibei.models.uibei(**invalid_args)


# Pytest fixture definitions
# ==========================
# Fixtures for uibei
# ------------------
@pytest.fixture
def valid_quantity_args():
    """
    Valid arguments for `ibei.models.uibei` function
    """
    args = {
        "order": 2,
        "energy_lo": astropy.units.Quantity(1.15, astropy.units.eV),
        "temp": astropy.units.Quantity(5762., astropy.units.K),
        "chem_potential": astropy.units.Quantity(0.5, astropy.units.eV),
    }

    return args


@pytest.fixture(params=[(lambda x: x), (lambda x: getattr(x, "value", x))])
def valid_args(request, valid_quantity_args):
    args = {key: request.param(val) for key, val in valid_quantity_args.items()}

    return args


# Fixtures for BEI
# ----------------
@pytest.fixture
def valid_constructor_quantity_args():
    """
    Valid constructor arguments for ibei.models.BEI
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


# Comparison of BEI.upper to uibei
# ================================
import logging
import numpy as np

logger = logging.getLogger(__name__)

@pytest.fixture
def valid_uibei_args():
    rng = np.random.default_rng()
    energy_lo = 10 * rng.random()

    args = dict(
        order=rng.integers(low=1, high=11),
        energy_lo=energy_lo,
        temp=1e4 * rng.random(),
        chem_potential=energy_lo * rng.random(),
    )

    return args


@pytest.mark.parametrize("dummy", range(10000))
def test_compare_upper_to_uibei(valid_uibei_args, dummy):
    """
    Output of `uibei` should match `BEI.upper`
    """
    valid_BEI_args = {
        "order": valid_uibei_args["order"],
        "energy_bound": valid_uibei_args["energy_lo"],
        "temperature": valid_uibei_args["temp"],
        "chemical_potential": valid_uibei_args["chem_potential"],
    }

    logger.info(valid_uibei_args)
    logger.info(valid_BEI_args)

    uibei_result = ibei.models.uibei(**valid_uibei_args)
    bei_result = ibei.models.BEI(**valid_BEI_args).upper()

    assert uibei_result == bei_result


