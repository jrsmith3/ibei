ibei - Calculator for incomplete Bose-Einstein integral
=======================================================

This README is a quickstart. See the [full documentation](https://ibei.readthedocs.org) for more details.


Scope
=====
The `ibei` python module implements a calculation of the upper-incomplete Bose-Einstein integral which is given in terms of the [polylogarithm](https://en.wikipedia.org/wiki/Polylogarithm) function and described by [Smith](https://github.com/jrsmith3/paper-2014-08_incomplete_bose_einstein_integral).


Installation
============
The `ibei` package is available on binstar.org and can be installed via `conda` since it depends on `numpy` (among other packages). I recommend installing [Anaconda scientific python distribution](https://store.continuum.io/cshop/anaconda/) by [Continuum Analytics](https://www.continuum.io) instead of trying to roll your own `numpy` install.

Once anaconda and `conda` are installed, installation of `ibei` is simple:

```
$ conda install -c jrsmith3 ibei
```


Example
=======
Calculate the number of above-bandgap photons from Si at 300K.

```python
>>> import ibei
>>> temp = 300
>>> bandgap = 1.1
>>> ibei.uibei(2, bandgap, temp, 0.)
<Quantity 10549122.240303338 1 / (m2 s)>

```


License
=======
MIT


Documentation
=============
Full documenation can be found in the `doc` directory, at the official [documentation page](https://ibei.readthedocs.org), and within the module's docstrings.
