========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/chlamys/badge/?style=flat
    :target: https://readthedocs.org/projects/chlamys
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/dougmvieira/chlamys.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/dougmvieira/chlamys

.. |codecov| image:: https://codecov.io/github/dougmvieira/chlamys/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/dougmvieira/chlamys

.. |version| image:: https://img.shields.io/pypi/v/chlamys.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/chlamys

.. |commits-since| image:: https://img.shields.io/github/commits-since/dougmvieira/chlamys/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/dougmvieira/chlamys/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/chlamys.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/chlamys

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/chlamys.svg
    :alt: Supported versions
    :target: https://pypi.org/project/chlamys

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/chlamys.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/chlamys


.. end-badges

Smooth interpolation on scattered data with levels and slopes.

* Free software: MIT license

Installation
============

::

    pip install chlamys

Documentation
=============


https://chlamys.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
