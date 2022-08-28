# ibei - Calculator for incomplete Bose-Einstein integral
This README is a quickstart. See the
[full documentation](https://ibei.readthedocs.org) for more details.


## Scope
The `ibei` python module implements a calculation of the
upper-incomplete Bose-Einstein integral which is given in terms of
the [polylogarithm](https://en.wikipedia.org/wiki/Polylogarithm)
function and described by
[Smith](https://github.com/jrsmith3/paper-2014-08_incomplete_bose_einstein_integral).


## Installation
This package is installable via `pip`.

```bash
pip install ibei
```


Alternatively, download the source, install
[`hatch`](https://hatch.pypa.io/latest/), and build.

```bash
git clone git@github.com:jrsmith3/ibei.git
pip install hatch
hatch build
pip install dist/ibei-1.0.6.tar.gz  # Or whatever is the latest version in that directory.
```


## Example
Calculate the number of above-bandgap photons from Si at 300K.

```python
>>> import ibei
>>> bandgap = 1.1
>>> bei = ibei.BEI(order=2, energy_bound=bandgap, temperature=300., chemical_potential=0.)
<Quantity 10549124.09538381 1 / (m2 s)>
```


## License
MIT


## Documentation
Full documenation can be found in the `doc` directory, at the
official [documentation page](https://ibei.readthedocs.org), and
within the module's docstrings.
