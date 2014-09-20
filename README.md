ibei - Calculator for incomplete Bose-Einstein integral
=======================================================

This README is a quickstart. See the [full documentation]() for more details.


Scope
=====
The `ibei` python module implements a calculation of the upper-incomplete Bose-Einstein integral which is given in terms of the [polylogarithm](https://en.wikipedia.org/wiki/Polylogarithm) function and described by Smith \ref{}.


Installation
============
```bash
$ pip install git+git://github.com/jrsmith3/ibei.git
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
Full documenation can be found in the `doc` directory, at the official [documentation page](), and within the module's docstrings.
