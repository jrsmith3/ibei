# -*- coding: utf-8 -*-
"""
Base Library (:mod:`ibei`)
==========================

.. currentmodule:: ibei
"""

from . import models

try:
    from ._version import __version__
except ModuleNotFoundError:
    __version__ = ""

