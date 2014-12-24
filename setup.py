# -*- coding: utf-8 -*-
from distutils.core import setup
import ibei

setup(name = "ibei",
      version = ibei.__version__,
      author = "Joshua Ryan Smith",
      author_email = "joshua.r.smith@gmail.com",
      packages = ["ibei", "physicalproperty"],
      url = "https://github.com/jrsmith3/ibei",
      description = "Calculator for incomplete Bose-Einstein integral",
      classifiers = ["Programming Language :: Python",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                     "Development Status :: 3 - Alpha",
                     "Intended Audience :: Science/Research",
                     "Topic :: Scientific/Engineering :: Physics",
                     "Natural Language :: English",],
      install_requires = ["numpy",
                          "sympy",
                          "astropy"],)
