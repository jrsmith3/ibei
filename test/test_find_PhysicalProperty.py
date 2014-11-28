# -*- coding: utf-8 -*-
import unittest
from physicalproperty import PhysicalProperty, find_PhysicalProperty

# Classes used in tests
# =====================
class MockBaseClass(object):
    """
    Class with single PhysicalProperty attribute.

    This class also features an attribute called `my_PhysicalProperties` which is a list of the names of the class attributes implemented using `PhysicalProperty` descriptors.
    """
    attrib = PhysicalProperty()

    def __init__(self):
        self.attrib = 1.2
        self.my_PhysicalProperties = ["attrib"]


class MockSubclass(MockBaseClass):
    """
    Subclass of MockBaseClass with additional PhysicalProperty attributes.

    This class features to attributes called `my_PhysicalProperties` and `family_PhysicalProperties`. The first is a list of all the PhysicalProperty data attributes implemented at the level of this class. The second is a list of all the PhysicalProperty data attributes exposed by this class, including any defined in the parent class.
    """
    sub_attrib_1 = PhysicalProperty()
    sub_attrib_2 = PhysicalProperty()

    def __init__(self):
        self.attrib = 1.2
        self.sub_attrib_1 = 1.3
        self.sub_attrib_2 = 1.4

        self.my_PhysicalProperties = ["sub_attrib_1", 
            "sub_attrib_2",]

        self.family_PhysicalProperties = ["attrib",
            "sub_attrib_1", 
            "sub_attrib_2",]

# Tests
# =====
class test_find_PhysicalProperty(unittest.TestCase):
    """
    Tests functionality of `find_PhysicalProperty`.
    """

    def setUp(self):
        """
        MockBaseClass and MockSubclass instances for the tests.
        """
        self.mbc = MockBaseClass()
        self.msc = MockSubclass()

    def tearDown(self):
        """
        Destroy dummy objects after each test.
        """
        del self.mbc
        del self.msc

    def test_on_MockBaseClass(self):
        """
        PhysicalProperty attribs of MockBaseClass given by my_PhysicalProperties.
        """
        PhysicalProperties = set(find_PhysicalProperty(self.mbc))

        self.assertEqual(PhysicalProperties, set(self.mbc.my_PhysicalProperties))

    def test_on_MockSubclass(self):
        """
        PhysicalProperty attribs of MockSubclass given by family_PhysicalProperties.
        """
        PhysicalProperties = set(find_PhysicalProperty(self.msc))

        self.assertEqual(PhysicalProperties, set(self.msc.family_PhysicalProperties))
