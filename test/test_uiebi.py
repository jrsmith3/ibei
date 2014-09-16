# -*- coding: utf-8 -*-
import numpy as np
import ibei
from astropy import units
import unittest

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


class CalculatorsArgsWrongType(unittest.TestCase):
    """
    Tests calling with args of invalid type.
    """
    pass


class CalculatorsArgsWrongUnits(unittest.TestCase):
    """
    Tests calling with args with incorrect units.
    """
    pass


class CalculatorsArgsOutsideConstraints(unittest.TestCase):
    """
    Tests calling with args are outside constraints.
    """
    pass


if __name__ == "__main__":
    pass
