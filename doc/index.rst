.. ibei documentation master file, created by
   sphinx-quickstart on Sat Sep 20 16:05:43 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ibei - Calculator for incomplete Bose-Einstein integral
=======================================================

.. toctree::
   :maxdepth: 2


Scope
=====
The Bose-Einstein integral appears when calculating quantities pertaining to photons. Perhaps best known, it appears when calculating the detailed balance limit of a solar cell as described by Shockley and Queisser :cite:`10.1063/1.1736034` , but also when calculating the photo-enhanced thermoelectron emission from a material first described by Schwede et.al. :cite:`10.1038/nmat2814` .

The upper incomplete Bose-Einstein integral is given by

.. math::

    F_{m}(E_{A},T,\mu) = \frac{2 \pi}{h^{3}c^{2}} \int_{E_{A}}^{\infty} E^{m} \frac{1}{\exp \left( \frac{E - \mu}{kT} \right) - 1} dE 

where :math:`E` is the photon energy, :math:`\mu` is the photon chemical potential, :math:`E_{A}` is the lower limit of integration, :math:`T` is the absolute temperature of the blackbody radiator, :math:`h` is Planck's constant, :math:`c` is the speed of light, :math:`k` is Boltzmann's constant, and :math:`m` is the integer order of the integration. For a value of :math:`m = 2` , this integral returns the photon particle flux, whereas for :math:`m = 3` , the integral yields the photon power flux.

The :mod:`ibei` python module implements a calculation of the upper-incomplete Bose-Einstein integral which is given in terms of the `polylogarithm <https://en.wikipedia.org/wiki/Polylogarithm>`_ function and described by Smith :cite:`ADD_CITATION`. The :mod:`ibei` module provides a function, `uibei`, which returns the value of the upper incomplete Bose-Einstein integral as well as two convenience classes for calculating the power density and efficiency of a single-junction solar cell according to Shockley and Queisser :cite:`10.1063/1.1736034` and deVos :cite:`9780198513926`.


Installation
============

Prerequisites
-------------
The :mod:`ibei` module is implemented in python and depends on:

* `numpy <http://www.numpy.org>`_
* `astropy <http://www.astropy.org>`_
* `sympy <http://sympy.org/en/index.html>`_
* `physicalproperty <https://physicalproperty.rtfd.org>`_

Since this package depends on `numpy`, I've eschewed the tradiational pip/pypi approach for packaging and distribution and instead opted for `conda <http://conda.pydata.org/docs/index.html>`_/`binstar <https://binstar.org>`_. I recommend using the most recent release of the `Anaconda scientific python distribution <https://store.continuum.io/cshop/anaconda/>`_ by `Continuum Analytics <https://www.continuum.io>`_ to mitigate the difficulty of installing `numpy` on your system. Once you've installed anaconda, you can install the most recent version of `ibei` like so::

    conda install -c jrsmith3 ibei


Examples
========
Calculate the number of above-bandgap photons from Si at 300K::

    >>> import ibei
    >>> temp = 300
    >>> bandgap = 1.1
    >>> ibei.uibei(2, bandgap, temp, 0.)
    <Quantity 10549122.240303338 1 / (m2 s)>

Verify Shockley and Queisser's result :cite:`10.1063/1.1736034` that the efficiency of a silicon solar cell is 44%::

    >>> import ibei
    >>> input_params = {"temp_sun": 6000, "bandgap": 1.1}
    >>> sc = ibei.SQSolarcell(input_params)
    >>> sc.calc_efficiency()
    0.43866804270206095

Plot efficiency vs. bandgap of a single-junction solar cell as in Shockley and Queisser's Fig. 3 :cite:`10.1063/1.1736034`::

    >>> import ibei
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt

    >>> bandgaps = np.linspace(0, 3.25, 100)
    >>> efficiencies = []
    >>> for bandgap in bandgaps:
    ...     input_params = {"temp_sun": 6000, "bandgap": bandgap}
    ...     sc = ibei.SQSolarcell(input_params)
    ...     efficiency = sc.calc_efficiency()
    ...     efficiencies.append(efficiency)
    >>> plt.plot(bandgaps, efficiencies)
    >>> plt.show()

.. image:: _static/eta_vs_eg.png


License
=======
The code is licensed under the `MIT license <http://opensource.org/licenses/MIT>`_. You can use this code in your project without telling me, but it would be great to hear about who's using the code. You can reach me at joshua.r.smith@gmail.com.


Contributing
============
The repository is hosted on `github <https://github.com/jrsmith3/ibei>`_ . Feel free to fork this project and/or submit a pull request. Please notify me of any issues using the `issue tracker <https://github.com/jrsmith3/ibei/issues>`_ .

In the unlikely event that a community forms around this project, please adhere to the `Python Community code of conduct <https://www.python.org/psf/codeofconduct/>`_.

Version numbers follow the `PEP440 <https://www.python.org/dev/peps/pep-0440/>`_ rubric. Versions will have three components: major.minor.patch. These components can be understood within the `semver <http://semver.org/>`_ rubric.


Citing
======
TBD


API Reference
=============
.. toctree::
    :maxdepth: 2

    api


Bibliography
============
.. bibliography:: bib.bib
