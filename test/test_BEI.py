# -*- coding: utf-8 -*-
import astropy.units
import ibei
import pytest

from contextlib import nullcontext as does_not_raise


class TestBEIConstructorHappyPath():
    def test_params_without_default_values(valid_constructor_args):
        valid_constructor_args.pop("chemical_potential")

        with does_not_raise():
            bei = ibei.models.BEI(**valid_constructor_args)


    def test_params_with_default_values(valid_constructor_args):
        with does_not_raise():
            bei = ibei.models.BEI(**valid_constructor_args)


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


@pytest.fixture(params=[(lambda x: x), (lambda x: x.value)])
def valid_constructor_args(request, valid_constructor_quantity_args):
    args = {key: request.param(val) for key, val in valid_constructor_quantity_args.items()}

    return args
