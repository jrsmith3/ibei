ibei - Calculator for incomplete Bose-Einstein integral
=======================================================

Scope
=====
The Bose-Einstein integral appears when calculating quantities pertaining to photons. Perhaps best known, it appears when calculating the detailed balance limit of a solar cell as described by Shockley and Queisser \ref{10.1063/1.1736034}, but also when calculating the photo-enhanced thermoelectron emission from a material first described by Schwede et.al. \ref{10.1038/nmat2814}.

The upper incomplete Bose-Einstein integral is given by

$F_{m}(E_{A},T,\mu) &= \frac{2 \pi}{h^{3}c^{2}} \int_{E_{A}}^{\infty} E^{m} \frac{1}{\exp \left( \frac{E - \mu}{kT} \right) - 1} dE \nonumber \\
 &= \frac{2 \pi (kT)^{m+1}}{h^{3}c^{2}} \int_{x_{A}}^{\infty} x^{m} \frac{1}{\exp(x-u) - 1} dx$

where $E$ is the photon energy, $\mu$ is the photon chemical potential, $E_{A}$ is the lower limit of integration, $T$ is the absolute temperature of the blackbody radiator, $h$ is Planck's constant, $c$ is the speed of light, $k$ is Boltzmann's constant, and $m$ is the integer order of the integration. For a value of $m = 2$, this integral returns the photon particle flux, whereas for $m = 3$, the integral yields the photon power flux.

The `ibei` python module implements a calculation of the upper-incomplete Bose-Einstein integral which is given in terms of the [polylogarithm](https://en.wikipedia.org/wiki/Polylogarithm) function and described by Smith \ref{}. The `ibei` module provides a function, `uibei`, which returns the value of the upper incomplete Bose-Einstein integral as well as two convenience classes for calculating the power density and efficiency of a single-junction solar cell according to Shockley and Queisser \ref{10.1063/1.1736034} and deVos \ref{9780198513926}.


Installation
============

Prerequisites
-------------
The `ibei` module is implemented in python and depends on [numpy](http://www.numpy.org), [astropy](http://www.astropy.org), and [sympy](http://sympy.org/en/index.html). It isn't required, but I recommend installing [ipython](http://ipython.org) as well. These packages and more are available via Continuum Analytics's [anaconda](http://continuum.io/downloads) distribution. Anaconda is likely the quickest way to get set up with the prerequisites.

ibei installation
-----------------
The code isn't on pypi, so you'll have to install from source. There are two ways to do it: 1. downloading and installing from the zip file and 2. installing with pip over git from github. If you don't understand the phrase, "installing over git from github", you want to use the first option.

Zip file install
----------------
Download the most recent copy of the zip file from the [releases](https://github.com/jrsmith3/ibei/releases) page and unzip it. Switch into the directory into which the zip file was uncompressed, then execute the following command at the command line.

    $ python setup.py install

pip + git + github
------------------
If you have pip installed, execute

    $ pip install git+git://github.com/jrsmith3/ibei.git

from the command line.


Examples
========
Calculate the number of above-bandgap photons from Si at 300K.

```python
>>> import ibei
>>> temp = 300
>>> bandgap = 1.1
>>> ibei.uibei(2, bandgap, temp, 0.)
<Quantity 10549122.240303338 1 / (m2 s)>

```

Verify Shockley and Queisser's result \ref{10.1063/1.1736034} that the efficiency of a silicon solar cell has an efficiency of 44%.

```python
>>> import ibei
>>> input_params = {"temp_sun": 6000, "bandgap": 1.1}
>>> sc = ibei.SQSolarcell(input_params)
>>> sc.calc_efficiency()
0.43866804270206095

```

Plot efficiency vs. bandgap of a single-junction solar cell as in Shockley and Queisser's Fig. 3 \ref{10.1063/1.1736034}

```python
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
# (ADD FIGURE)
```


License
=======
The code is licensed under the MIT license. You can use this code in your project without telling me, but it would be great to hear about who's using the code. You can reach me at joshua.r.smith@gmail.com.


Contributing
============
The repository is hosted on [github](https://github.com/jrsmith3/ibei). Feel free to fork this project and/or submit a pull request. Please notify me of any issues using the [issue tracker](https://github.com/jrsmith3/ibei/issues).


Citing
======
Github supports a [method of citable code](https://guides.github.com/activities/citable-code/).


API Reference
=============
(ADD)
