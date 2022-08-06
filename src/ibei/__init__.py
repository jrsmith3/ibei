# -*- coding: utf-8 -*-
"""
Base Library (:mod:`ibei`)
==========================

.. currentmodule:: ibei
"""

from .uibei import uibei

try:
    from ._version import __version__
except ModuleNotFoundError:
    __version__ = ""

