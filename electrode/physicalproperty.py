# -*- coding: utf-8 -*-

from weakref import WeakKeyDictionary
import constants
import numpy as np
import scipy
from astropy import units

class PhysicalProperty(object):
    """
    Descriptor class of a public data attribute of a physical property.

    Physical properties have several characteristics that are different from plain numerical data:

    * upper and/or lower bounds
    * numerical type
    * units

    The purpose of this class is to constrain data that represents a physical quantity according to the specifications in the above list.
    """
    def __init__(self, unit = units.dimensionless_unscaled, up_bnd = np.inf, lo_bnd = -np.inf):
        if up_bnd < lo_bnd:
            raise ValueError("up_bnd must be greater than lo_bnd.")

        self._default = None
        self._data = WeakKeyDictionary()
        self._unit = units.Unit(unit)
        self._up_bnd = units.Quantity(up_bnd, self._unit)
        self._lo_bnd = units.Quantity(lo_bnd, self._unit)

    def __get__(self, instance, owner):
        return self._data.get(instance, self._default)

    def __set__(self, instance, val):
        if type(val) == units.Quantity:
            val = val.to(self._unit)
        else:
            try:
                val = float(val)
            except ValueError:
                raise TypeError("PhysicalProperty must be set with type numeric.")
            val = units.Quantity(val, self._unit)

        if val < self._lo_bnd:
            raise ValueError("Cannot set less than %s" % str(self._lo_bnd))
        elif val > self._up_bnd:
            raise ValueError("Cannot set greater than %s" % str(self._up_bnd))

        self._data[instance] = val
