=======================================================
ibei - Calculator for incomplete Bose-Einstein integral
=======================================================

The Bose-Einstein integral appears when calculating quantities
pertaining to photons. It is used to derive the Stefan-Boltzmann law,
and it also appears when calculating the detailed balance limit of a
solar cell as described by Shockley and
Queisser :cite:`10.1063/1.1736034` , but also when calculating the
photo-enhanced thermoelectron emission from a material first
described by Schwede et.al. :cite:`10.1038/nmat2814` .

The :mod:`ibei` module provides functionality to calculate various
forms of the Bose-Einstein integral, along with well-known models of
photovoltaic devices. See the
`Mathematical Description and Applications`_ section for the
mathematical details. The :mod:`ibei` module provides a :class:`BEI`
class which includes methods to compute the full, upper-incomplete,
and lower-incomplete Bose-Einstein integrals. It also includes two
convenience classes for calculating the power density and efficiency
of a single-junction solar cell according to Shockley and
Queisser :cite:`10.1063/1.1736034` and deVos :cite:`9780198513926`.


Installation (UPDATE THIS SECTION)
==================================
This section is subject to change.

Download the source, install `hatch <https://hatch.pypa.io/latest>`_
and build.

.. code-block:: bash

    git clone git@github.com:jrsmith3/ibei.git
    pip install hatch
    hatch build
    pip install dist/ibei-1.0.6.tar.gz


Examples
========
Calculate the number of above-bandgap photons from Si at 300K::

    >>> import ibei
    >>> bandgap = 1.1
    >>> bei = ibei.BEI(order=2, energy_bound=bandgap, temperature=300., chemical_potential=0.)
    <Quantity 10549124.09538381 1 / (m2 s)>

Verify Shockley and Queisser's result :cite:`10.1063/1.1736034` that
the efficiency of a silicon solar cell is 44%::

    >>> import ibei
    >>> solarcell = ibei.SQSolarcell(solar_temperature=6000., bandgap=1.1)
    >>> solarcell.efficiency()
    <Quantity 0.43866807>

Plot efficiency vs. bandgap of a single-junction solar cell as in
Shockley and Queisser's Fig. 3 :cite:`10.1063/1.1736034`::

    >>> import ibei
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt

    >>> bandgaps = np.linspace(0, 3.25, 100)
    >>> efficiencies = []
    >>> for bandgap in bandgaps:
    ...:     solarcell = ibei.SQSolarcell(solar_temperature=6000, bandgap=bandgap)
    ...:     efficiency = solarcell.efficiency()
    ...:     efficiencies.append(efficiency)

    >>> plt.plot(bandgaps, efficiencies)
    >>> plt.show()


.. image:: _static/eta_vs_eg.png
  :alt: Efficiency vs. bandgap of a photovoltaic using Shockley and Queisser's model.


API Reference
=============
.. toctree::
    :maxdepth: 1

    api


Mathematical Description and Applications
=========================================
The Bose-Einstein integral, subsequently referred to as the "full
Bose-Einstein integral" or "full integral", is given by Eq. (REF).

(EQUATION)

(DESCRIPTION OF TERMS)

Consider the two integrals G() and g(), called the upper-incomplete
Bose-Einstein integral and the lower-incomplete Bose-Einstein
integral, respectively, and given by Eq. (REF).

(EQUATION)

Note that the two integrals given above can be summed to yield a
relationship between them and the full integral.

(EQUATION)

(SHOW THE SOLUTION TO THE FULL AND UPPER-INCOMPLETE INTEGRALS).



The upper incomplete Bose-Einstein integral is given by

.. math::

    F_{m}(E_{A},T,\mu) = \frac{2 \pi}{h^{3}c^{2}} \int_{E_{A}}^{\infty} E^{m} \frac{1}{\exp \left( \frac{E - \mu}{kT} \right) - 1} dE

where :math:`E` is the photon energy, :math:`\mu` is the photon
chemical potential, :math:`E_{A}` is the lower limit of
integration, :math:`T` is the absolute temperature of the blackbody
radiator, :math:`h` is Planck's constant, :math:`c` is the speed of
light, :math:`k` is Boltzmann's constant, and :math:`m` is the
integer order of the integration. For a value of :math:`m = 2` , this
integral returns the photon particle flux, whereas for :math:`m =
3` , the integral yields the photon power flux.







License
=======
The code is licensed under the
`MIT license <http://opensource.org/licenses/MIT>`_. You can use this
code in your project without telling me, but it would be great to hear
about who's using the code. You can reach me at
joshua.r.smith@gmail.com.


Contributing
============

The repository is hosted on
`github <https://github.com/jrsmith3/ibei>`_ . Feel free to fork this
project and/or submit a pull request. Please notify me of any issues
using the `issue tracker <https://github.com/jrsmith3/ibei/issues>`_ .

In the unlikely event that a community forms around this project,
please adhere to the
`Python Community code of conduct <https://www.python.org/psf/codeofconduct/>`_.

Version numbers follow the
`PEP440 <https://www.python.org/dev/peps/pep-0440/>`_ rubric. Versions
will have three components: major.minor.patch. These components can
be understood within the `semver <http://semver.org/>`_ rubric.


Citing
======
TBD


Bibliography
============
.. bibliography:: bib.bib
