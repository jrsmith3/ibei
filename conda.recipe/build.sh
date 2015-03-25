#!/usr/bin/env bash

# Define version from `ibei/version.py`
VERSION=`python -c 'execfile("ibei/version.py")
print(__version__)'`

echo $VERSION > __conda_version__.txt

# Install package
$PYTHON setup.py install
