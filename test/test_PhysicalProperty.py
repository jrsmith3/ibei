# -*- coding: utf-8 -*-
from astropy import units
import unittest
from ibei.physicalproperty import PhysicalProperty

# Classes used in tests
# =====================
class MockClassEmpty(object):
    """
    Class containing nothing.
    """
    pass


class MockClassDefaultInstantiation(object):
    """
    Default instantiated `PhysicalProperty` public data attribute.
    """
    attrib = PhysicalProperty()


class MockClassUserDefinedUnitAmp(object):
    """
    `PhysicalProperty` public data attribute w/ user-defined unit as amp.
    """
    attrib = PhysicalProperty(unit = "A")

    def __init__(self, current = 1):
        """
        Initialize the `PhysicalProperty` public data attribute.
        """
        self.attrib = current


# Tests
# =====
class StandaloneInstantiation(unittest.TestCase):
    """
    PhysicalProperty instantiated as a standalone object.
    """
    def test_instantiate_lo_bnd_greater_than_up_bnd(self):
        """
        ValueError raised if instantiated with up_bnd < lo_bnd.
        """
        self.assertRaises(ValueError, PhysicalProperty, "A", -1, 1)


    # __set__ method tests
    # ====================
    def test_set_non_numeric(self):
        """
        Set with non-numeric, non-Quantity input raises TypeError
        """
        pp = PhysicalProperty()
        self.assertRaises(TypeError, pp.__set__, MockClassEmpty, "not a number")

    def test_set_Quantity_incompatible_units(self):
        """
        Raise UnitsException when setting with Quantity of incompatible units.
        """
        pp = PhysicalProperty()
        qty = units.Quantity(100., "km")
        
        self.assertRaises(units.UnitsError, pp.__set__, MockClassEmpty, qty)

    def test_set_numeric_above_up_bnd(self):
        """
        Raises ValueError when attempting to set with numeric above up_bnd.
        """
        ubnd = 10.

        pp = PhysicalProperty(up_bnd = ubnd)
        self.assertRaises(ValueError, pp.__set__, MockClassEmpty, 12.)

    def test_set_numeric_below_lo_bnd(self):
        """
        Raises ValueError when attempting to set with numeric below lo_bnd.
        """
        lbnd = -10.

        pp = PhysicalProperty(lo_bnd = lbnd)
        self.assertRaises(ValueError, pp.__set__, MockClassEmpty, -12.)

    def test_set_Quantity_above_up_bnd_same_units(self):
        """
        Raises ValueError when attempting to set with Quantity in same units above up_bnd.
        """
        ubnd = 10.
        unit = "mm"
        pp = PhysicalProperty(unit = unit, up_bnd = ubnd)

        qty = units.Quantity(12., unit)
        self.assertRaises(ValueError, pp.__set__, MockClassEmpty, qty)

    def test_set_Quantity_above_up_bnd_compatible_units(self):
        """
        Raises ValueError when attempting to set with Quantity in compatible units above up_bnd.
        """
        ubnd = 10.
        unit = "mm"
        pp = PhysicalProperty(unit = unit, up_bnd = ubnd)

        # Note 1e3mm = 1m. Thus, 1m > 10mm.
        qty = units.Quantity(1., "m")
        self.assertRaises(ValueError, pp.__set__, MockClassEmpty, qty)

    def test_set_Quantity_below_lo_bnd_same_units(self):
        """
        Raises ValueError when attempting to set with Quantity in same units below lo_bnd.
        """
        lbnd = -10.
        unit = "mm"
        pp = PhysicalProperty(unit = unit, lo_bnd = lbnd)

        qty = units.Quantity(-12., unit)
        self.assertRaises(ValueError, pp.__set__, MockClassEmpty, qty)

    def test_set_Quantity_below_lo_bnd_compatible_units(self):
        """
        Raises ValueError when attempting to set with Quantity in compatible units below lo_bnd.
        """
        lbnd = -10.
        unit = "mm"
        pp = PhysicalProperty(unit = unit, lo_bnd = lbnd)

        # Note 1e3mm = 1m. Thus, 1m > 10mm.
        qty = units.Quantity(-1., "m")
        self.assertRaises(ValueError, pp.__set__, MockClassEmpty, qty)

class SimpleInstantiation(unittest.TestCase):
    """
    Instantiation with no arguments from within an owner class.

    These tests require some simple manipulation of the owner class's `PhysicalProperty` data attribute via the `PhysicalProperty.__set__` and `PhysicalProperty.__get__` methods.
    """
    def setUp(self):
        """
        A MockClassDefaultInstantiation instance for the tests.
        """
        self.mcdi = MockClassDefaultInstantiation()

    def tearDown(self):
        """
        I'm pretty sure I have to destroy self.mcdi.
        """
        del self.mcdi


    def test_default_value(self):
        """
        Default value should be `None`.
        """
        self.assertEqual(self.mcdi.attrib, None)

    def test_modifying_value_returns_Quantity(self):
        """
        Valid `__set__` yields `astropy.units.Quantity` on later `__get__` call
        """
        self.mcdi.attrib = 7.
        self.assertIsInstance(self.mcdi.attrib, units.Quantity)

    def test_default_unit(self):
        """
        Default unit is `astropy.units.dimensionless_unscaled`.
        """
        self.mcdi.attrib = 7.
        self.assertEqual(self.mcdi.attrib.unit, units.dimensionless_unscaled)


class InstantiationWithUnitArg(unittest.TestCase):
    """
    Instantiation with unit arguments from within an owner class.
    """
    def setUp(self):
        """
        A MockClassUserDefinedUnitAmp instance for the tests.
        """
        self.mcudua = MockClassUserDefinedUnitAmp()

    def tearDown(self):
        """
        Destroy the mock class used in the test.
        """
        del self.mcudua


    def test_unit(self):
        """
        Units are in amps.
        """
        self.assertEqual(self.mcudua.attrib.unit, "A")

    def test_set_with_number_roundtrip(self):
        """
        Set `attrib` with numeric type yields same numeric value on later `__get__` call.
        """
        number = 100.
        self.mcudua.attrib = number
        self.assertEqual(self.mcudua.attrib.value, number)

    def test_set_with_Quantity_stores_a_copy(self):
        """
        When setting the object with a Quantity, the object should store a new copy of the Quantity and not simply point to the original.

        This test tests two things:
        1. `__set__`ting with an `astropy.units.Quantity` works.
        2. The `PhysicalProperty` object stores a Quantity object that's different from the one passed to its `__set__` method.
        """
        qty = units.Quantity(100., "A")
        self.mcudua.attrib = qty

        self.assertIsNot(self.mcudua.attrib, qty)

    def test_set_with_Quantity_units_dont_change(self):
        """
        Set with Quantity with compatible units doesn't change `attrib` units.
        """
        qty = units.Quantity(100., "C/s")
        self.mcudua.attrib = qty

        self.assertEqual(self.mcudua.attrib.unit, "A")


class MultipleOwnerInstances(unittest.TestCase):
    """
    Multiple owner instances shouldn't interfere with one another.
    """
    def test_two_owners_individually_set_attribute(self):
        """
        Changing a `PhysicalProperty` attribute value of one owner instance shouldn't alter another owner instance.
        """
        val1 = 10.
        val2 = 3.

        mock1 = MockClassDefaultInstantiation()
        mock2 = MockClassDefaultInstantiation()

        mock1.attrib = val1
        mock2.attrib = val2

        self.assertEqual(mock1.attrib.value, val1)
