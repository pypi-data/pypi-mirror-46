.. note::

   PtvPy is still in its early development and significant changes should be expected.
   Of course you are already welcome to try it out! Your feedback and suggestions will
   be of great value at this stage.


================================
Welcome to PtvPy's documentation
================================

.. image:: https://gitlab.com/tud-mst/ptvpy/uploads/5848c59eaa82b4458245a0a58c3db1cb/try-out-vector.svg
   :width: 19%
.. image:: https://gitlab.com/tud-mst/ptvpy/uploads/3ecbfdd3e1d6373a4b15354e32084dc6/workflow-scatter3d-x-y-v.png
   :width: 19%
.. image:: https://gitlab.com/tud-mst/ptvpy/uploads/6b156ed9d954eadf6ec04fbcaf770bb0/workflow-map-x-y-dy.png
   :width: 19%
.. image:: https://gitlab.com/tud-mst/ptvpy/uploads/7b52f8f5a1b1279c19f5e6ac6ea96bec/workflow-relationship-mass-size.png
   :width: 19%
.. image:: https://gitlab.com/tud-mst/ptvpy/uploads/1c5d67c083baf20863c1af362b85f8cb/workflow-slideshow-2.svg
   :width: 19%

PtvPy is a command line program and Python library for particle tracking velocimetry.
Its goal is to give domain experts an intuitive tool that provides reproducible and
reliable results without requiring programming skills.
PtvPy heavily depends on and extends functionality from the excellent library trackpy_.
It furthermore provides a periphery to visualize, analyze and export the data involved.

PtvPy is available for Python 3.6 and higher and can be :ref:`installed <installation>`
from PyPI or conda-forge.
The source is hosted on GitLab_. Your are welcome to `open a new issue`_ if you want to
suggest new features, report bugs or get in contact with the developers.

.. _trackpy: https://soft-matter.github.io/trackpy/
.. _GitLab: https://gitlab.com/tud-mst/ptvpy/
.. _open a new issue: https://gitlab.com/tud-mst/ptvpy/issues/new?issue

.. toctree::
   :caption: Guides

   getting_started
   example_workflow
   faq
   contributing

.. toctree::
   :caption: Reference
   :maxdepth: 2

   _generated/profile
   _generated/cli
   _generated/api
   changelog
   license


History
=======
PtvPy was developed as an internal tool at the `Chair of Measurement & Sensor System
Technique`_ at the TU Dresden to facilitate data analysis. It was eventually published
in 2019 as open source software.

.. _Chair of Measurement & Sensor System Technique:
   https://tu-dresden.de/ing/elektrotechnik/iee/mst
