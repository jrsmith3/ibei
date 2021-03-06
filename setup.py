# -*- coding: utf-8 -*-
from setuptools import setup
execfile("ibei/version.py")

setup(name="ibei",
      version=__version__,
      author="Joshua Ryan Smith",
      author_email="joshua.r.smith@gmail.com",
      packages=["ibei"],
      url="https://github.com/jrsmith3/ibei",
      license="MIT",
      description="Calculator for incomplete Bose-Einstein integral",
      classifiers=["Programming Language :: Python",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Science/Research",
                   "Topic :: Scientific/Engineering :: Physics",
                   "Natural Language :: English", ],
      install_requires=["numpy",
                        "sympy",
                        "astropy",
                        "physicalproperty"],)
