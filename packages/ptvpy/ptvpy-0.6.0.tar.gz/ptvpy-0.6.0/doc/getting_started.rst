===============
Getting started
===============

.. highlight:: none


.. _installation:

Installation
============

Anaconda (recommended)
----------------------

.. warning:: This doesn't work yet!

If you haven't yet installed the `Anaconda distribution`_ please do so before
continuing.
Once this is done open the `Anaconda Command Prompt`_ and type ::

    conda --version

to verify that you have access to the package manager.
PtvPy and some of its dependencies are not available in Anaconda's official
repositories.
Therefore we need to append the community managed repository `conda forge`_ to its
search path [#]_ with the command::

    conda config --append channels conda-forge

Then you can simply install PtvPy with::

    conda install ptvpy

.. _Anaconda distribution: https://www.anaconda.com/download/
.. _Anaconda Command Prompt: https://docs.anaconda.com/anaconda/user-guide/getting-started/#open-anaconda-prompt
.. _conda forge: https://conda-forge.org/

.. [#] When installing or updating packages, conda will still search the official
       repositories first.
       Only if the desired package is not found will it look to conda-forge.

Pip
---

.. warning:: This doesn't work yet!

PtvPy is available on the `Python Package Index`_ as well.
Open a command prompt where pip_ is available and type::

    pip install ptvpy


.. _Python Package Index: https://pypi.org/
.. _pip: https://pip.pypa.io/en/stable/


.. _overview:

Overview
========

PtvPy is controlled through its :ref:`cli` consisting of the following subcommands:

- :ref:`cli-ptvpy-process` detects particles inside a given dataset.
  The way the data is processed and analyzed is mainly controlled by and configured
  through :ref:`profile files <profile-config>`.
- :ref:`cli-ptvpy-view` can be used to inspect and visualize the dataset and
  processing results.
- :ref:`cli-ptvpy-profile` assists the user in managing profile files. It can create,
  validate, edit and show profiles.
- :ref:`cli-ptvpy-export` is used to make processing results available in commonly
  supported file formats.


Try it out
==========

If you want to see PtvPy in action you can follow the steps and commands below
for a quick demonstration:

1. First create a synthetic dataset and a matching profile file::

    ptvpy generate whirlpool data/ 100
    ptvpy profile create --pattern "data/*.tiff"

2. Perform particle tracking velocimetry on the new dataset::

    ptvpy process

3. And finally, inspect the results frame by frame::

    ptvpy view slideshow

.. image:: https://gitlab.com/tud-mst/ptvpy/uploads/21b9c5e7f5ef669a699e819a754c5e19/try-out-slideshow.svg
   :align: center

or calculate a vector field for the moving particles::

    ptvpy view vector x y dx dy

.. image:: https://gitlab.com/tud-mst/ptvpy/uploads/5848c59eaa82b4458245a0a58c3db1cb/try-out-vector.svg
   :align: center

A thorough walkthrough with more examples and explanations check the the :ref:`next
guide <workflow>`.
