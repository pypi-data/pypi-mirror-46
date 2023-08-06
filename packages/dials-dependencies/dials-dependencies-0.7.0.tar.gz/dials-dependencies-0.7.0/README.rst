==================
DIALS Dependencies
==================

.. image:: https://img.shields.io/pypi/v/dials-dependencies.svg
        :target: https://pypi.python.org/pypi/dials-dependencies
        :alt: PyPI release

.. image:: https://img.shields.io/conda/vn/conda-forge/dials-dependencies.svg
        :target: https://anaconda.org/conda-forge/dials-dependencies
        :alt: Conda release

.. image:: https://img.shields.io/pypi/l/dials-dependencies.svg
        :target: https://pypi.python.org/pypi/dials-dependencies
        :alt: BSD license

.. image:: https://img.shields.io/pypi/pyversions/dials-dependencies.svg
        :target: https://pypi.org/project/dials-dependencies
        :alt: Supported Python versions

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/ambv/black
        :alt: Code style: black

A meta-package describing DIALS_ dependencies.

To make a release run::

     libtbx.bumpversion minor

     python setup.py sdist bdist_wheel upload

.. _DIALS: https://dials.github.io
