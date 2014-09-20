ibei - Calculator for incomplete Bose-Einstein integral
=======================================================

The Bose-Einstein integral appears when calculating quantities pertaining to photons. Perhaps best known, it appears when calculating the detailed balance limit of a solar cell as described by Shockley and Queisser \ref{}, but also when calculating the photo-enhanced thermoelectron emission from a material first described by Schwede et.al. \ref{}.

The upper incomplete Bose-Einstein integral is given by

$F_{m}(E_{A},T,\mu) &= \frac{2 \pi}{h^{3}c^{2}} \int_{E_{A}}^{\infty} E^{m} \frac{1}{\exp \left( \frac{E - \mu}{kT} \right) - 1} dE \nonumber \\
 &= \frac{2 \pi (kT)^{m+1}}{h^{3}c^{2}} \int_{x_{A}}^{\infty} x^{m} \frac{1}{\exp(x-u) - 1} dx$

where $E$ is the photon energy, $\mu$ is the photon chemical potential, $E_{A}$ is the lower limit of integration, $T$ is the absolute temperature of the blackbody radiator, $h$ is Planck's constant, $c$ is the speed of light, $k$ is Boltzmann's constant, and $m$ is the integer order of the integration. For a value of $m = 2$, this integral returns the photon particle flux, whereas for $m = 3$, the integral yields the photon power flux.

The `ibei` python module implements a calculation of the upper-incomplete Bose-Einstein integral which is given in terms of the [polylogarithm](https://en.wikipedia.org/wiki/Polylogarithm) function and described by Smith \ref{}. The `ibei` module provides a function, `uibei`, which returns the value of the upper incomplete Bose-Einstein integral as well as two convenience classes for calculating the power density and efficiency of a single-junction solar cell according to Shockley and Queisser \ref{} and deVos \ref{}.
