# RepositoryChecker [![Build Status](https://travis-ci.org/Nydareld/RepositoryChecker.svg?branch=master)](https://travis-ci.org/Nydareld/RepositoryChecker) [![Coverage Status](https://coveralls.io/repos/github/Nydareld/RepositoryChecker/badge.svg)](https://coveralls.io/github/Nydareld/RepositoryChecker) [![PyPI version](https://badge.fury.io/py/RepositoryChecker.svg)](https://badge.fury.io/py/RepositoryChecker) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/RepositoryChecker.svg)
Check repository and corect it with parametred actions



Gestionnaire de configuration en json, ini avec overide possible en variable d’environnement

## install

with pip :

    pip install RepositoryChecker

## how to use


## devlopping guide

we advise you to fork the depot, and if you have goot feature, we would appreciate pull request

### install developement environement

with virtualenv :

    virtualenv -p python3 .venv
    source .venv/bin/activate

install depenencies :

    pip install -r requirements.txt

### test

run tests :

    python -m unittest tests

### coverage

run coverage

    coverage run --source=ConfigEnv -m unittest tests

report coverage

    coverage report -m

### release

create package :
    python3 setup.py sdist bdist_wheel

publish :
    python -m twine upload dist/*
