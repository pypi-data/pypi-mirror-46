========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations| |
.. |docs| image:: https://readthedocs.org/projects/pybpod-gui-plugin-emulator/badge/?style=flat
    :target: https://readthedocs.org/projects/pybpod-gui-plugin-emulator
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/pybpod-gui-plugin-emulator.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/pybpod-gui-plugin-emulator

.. |wheel| image:: https://img.shields.io/pypi/wheel/pybpod-gui-plugin-emulator.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/pybpod-gui-plugin-emulator

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pybpod-gui-plugin-emulator.svg
    :alt: Supported versions
    :target: https://pypi.org/project/pybpod-gui-plugin-emulator

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pybpod-gui-plugin-emulator.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/pybpod-gui-plugin-emulator


.. end-badges

Emulator for PyBpod to work with the Bpod's State Machine ports.

At the moment, the Emulator for PyBpod module works by overriding inputs and outputs on a running task protocol.
This will interact directly with a running State Machine in Bpod. As such, any event or state change that
would occur naturally from any of those input or output changes, will occur.


* Free software: MIT license

Current Features
================

* Allows to override the Port components (i.e., LED, Poke and Valve)
* BNC In and Out value override
* Wire inputs and outputs override for Bpod 0.7
* Override Serial message for the connected modules (sends a bytes message)
* Messages are sent while the State Machine is running, triggering the events
  and/or state changes as if the values were coming from the real inputs/outputs.


Installation
============

Please see Installation page.

Documentation
=============

https://pybpod-gui-plugin-emulator.readthedocs.io/


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
