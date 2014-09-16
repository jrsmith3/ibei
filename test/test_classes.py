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

    # def test_issue_1_devos_efficiency(self):
    #     """
    #     Unit system needs to be specified for astropy.constants.e to work.
    #     """
    #     try:
    #         ibei.devos_efficiency(bandgap, temp_sun, temp_earth, 1.09)
    #     except:
    #         self.fail("Unit system not initialized.")
