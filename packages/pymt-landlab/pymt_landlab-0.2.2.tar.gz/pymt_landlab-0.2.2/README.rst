============
pymt_landlab
============


.. image:: https://img.shields.io/badge/CSDMS-Basic%20Model%20Interface-green.svg
        :target: https://bmi.readthedocs.io/
        :alt: Basic Model Interface

.. image:: https://img.shields.io/badge/recipe-pymt_landlab-green.svg
        :target: https://anaconda.org/conda-forge/pymt_landlab

.. image:: https://img.shields.io/travis/pymt-lab/pymt_landlab.svg
        :target: https://travis-ci.org/pymt-lab/pymt_landlab

.. image:: https://readthedocs.org/projects/pymt_landlab/badge/?version=latest
        :target: https://pymt_landlab.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/csdms/pymt
        :alt: Code style: black


PyMT plugins for landlab components


* Free software: MIT license
* Documentation: https://landlab.readthedocs.io.




================================ ==========================================================
Component                        PyMT
================================ ==========================================================
OverlandFlow                     `from pymt.models import OverlandFlow`
Flexure                          `from pymt.models import Flexure`
LinearDiffuser                   `from pymt.models import LinearDiffuser`
ExponentialWeatherer             `from pymt.models import ExponentialWeatherer`
TransportLengthHillslopeDiffuser `from pymt.models import TransportLengthHillslopeDiffuser`
Vegetation                       `from pymt.models import Vegetation`
SoilMoisture                     `from pymt.models import SoilMoisture`
================================ ==========================================================

---------------
Installing pymt
---------------

Installing `pymt` from the `conda-forge` channel can be achieved by adding
`conda-forge` to your channels with:

.. code::

  conda config --add channels conda-forge

*Note*: Before installing `pymt`, you may want to create a separate environment
into which to install it. This can be done with,

.. code::

  conda create -n pymt python=3.6
  conda activate pymt

Once the `conda-forge` channel has been enabled, `pymt` can be installed with:

.. code::

  conda install pymt

It is possible to list all of the versions of `pymt` available on your platform with:

.. code::

  conda search pymt --channel conda-forge

-----------------------
Installing pymt_landlab
-----------------------

Once `pymt` is installed, the dependencies of `pymt_landlab` can
be installed with:

.. code::

  conda install landlab

To install `pymt_landlab`,

.. code::

  conda install pymt_landlab
