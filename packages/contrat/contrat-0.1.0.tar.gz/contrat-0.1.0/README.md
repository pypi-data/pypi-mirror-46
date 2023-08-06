[![Build Status](https://travis-ci.org/4383/contrat.svg?branch=master)](https://travis-ci.org/4383/contrat)
![PyPI](https://img.shields.io/pypi/v/contrat.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/contrat.svg)
![PyPI - Status](https://img.shields.io/pypi/status/contrat.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
# contrat

Simple python module to keep function signature introspection compatibility between 
python versions

## Install

```shell
pip install contrat
```

## Usage

The following example work for python 2.7 and python 3.0+:

```python
#!/usr/bin/python
from contrat import getargspec

def sample(arg1, arg2=True, arg3=1):
    pass


print(str(getargspec(sample)))
# will display
# ArgSpec(args=['arg1', 'arg2', 'arg3'], varargs=None, keywords=None, defaults=(False, 1))
```
