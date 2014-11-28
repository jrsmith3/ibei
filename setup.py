# -*- coding: utf-8 -*-
from distutils.core import setup
import physicalproperty

setup(name = "physicalproperty",
      version = physicalproperty.__version__,
      author = "Joshua Ryan Smith",
      author_email = "joshua.r.smith@gmail.com",
      packages = ["physicalproperty"],
      url = "https://github.com/jrsmith3/physicalproperty",
      description = "Descriptor class for physical property attributes",
      classifiers = ["Programming Language :: Python",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                     "Development Status :: 3 - Alpha",
                     "Intended Audience :: Science/Research",
                     "Topic :: Scientific/Engineering :: Physics",
                     "Natural Language :: English",],
      install_requires = ["numpy",
                          "astropy"],)
