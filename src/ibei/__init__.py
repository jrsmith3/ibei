# coding=utf-8
"""
Base Library (:mod:`ibei`)
==========================

The Bose-Einstein integral appears when calculating quantities
pertaining to photons. It is used to derive the Stefan-Boltzmann law,
and it also appears when calculating the detailed balance limit of a
solar cell and other devices.

The :mod:`ibei` module provides functionality to calculate various
forms of the Bose-Einstein integral, along with well-known models of
photovoltaic devices. The :class:`BEI` class implements the
full, upper-incomplete, and lower-incomplete Bose-Einstein integrals
and is the main feature of this module.


Notes
-----
Arguments passed to the constructor of the :class:`BEI` class
correspond to symbols in the expressions given below. The
correspondence is noted in the "Parameters" section of the class
docstring.


The (full) Bose-Einstein integral is denoted by :math:`G_{m} (T, \mu)`
and given by

.. math::
    G_{m}(T, \mu) = \\frac{2 \pi}{h^{3} c^{2}} \int_{0}^{\infty} E^{m} \\frac{1}{\exp(\\frac{E-\mu}{kT}) - 1} dE

(a glossary of symbols is given at the end of the docstring). The full
Bose-Einstein integral can be expressed as a sum of an
upper-incomplete (denoted :math:`G_{m} (E_{g}, T, \mu)`) and
lower-incomplete integral (denoted :math:`g_{m} (E_{g}, T, \mu)`)

.. math::
    G_{m} (T, \mu) = G_{m} (E_{g}, T, \mu) + g_{m} (E_{g}, T, \mu)

where

.. math::
    G_{m} (E_{g}, T, \mu) = \\frac{2 \pi}{h^{3} c^{2}} \int_{E_{g}}^{\infty} E^{m} \\frac{1}{\exp(\\frac{E-\mu}{kT}) - 1} dE

and

.. math::
    g_{m} (E_{g}, T, \mu) = \\frac{2 \pi}{h^{3} c^{2}} \int_{0}^{E_{g}} E^{m} \\frac{1}{\exp(\\frac{E-\mu}{kT}) - 1} dE

This module provides functionality to compute each integral given
above via the :class:`BEI` class.

Symbols used in the above equations are given as follows.

.. glossary::

    :math:`h`: Planck's constant
    :math:`c`: Speed of light
    :math:`\mu`: Chemical potential of photons
    :math:`E`: Energy of photons
    :math:`T`: Absolute temperature of the radiator
    :math:`k`: Boltzmann's constant
"""

from .models import BEI, SQSolarcell, DeVosSolarcell

try:
    from ._version import __version__
except ModuleNotFoundError:
    __version__ = ""
