=========
Changelog
=========

.. Once 1.0.0 is reached, use https://semver.org/spec/v2.0.0.html

Version 0.6.0 (latest)
======================

Released on 2019-05-17. This release marks the transition to an open-source project.
While there are new features the focus was on improving the infrastructure of the
project itself and preparing the releases on PyPI and conda-forge.

The highlights of this release are included below.

.. rubric:: New

- The new option ``--pattern`` was added to the :ref:`cli-ptvpy-profile-create`
  command. This option allows to use the command even if no input prompt is desired,
  e.g. when PtvPy is used programmatically.
- Added the new option ``--documentation`` to the root command :ref:`cli-ptvpy` which
  will open the online documentation inside the default browser.
- Released PtvPy under the BSD 3-Clause License as free and open-source software.
- New functions in :mod:`~.generate` module providing a more powerful API for
  frame generation. Generation of particles moving in a whirlpool was added as
  a new scenario, the optional addition of white noise to the background
  of frames and helper functions to render a frames with helix pairs.
- New wrapper class :class:`~.HdfFile` that allows round-tripping pandas's DataFrames
  while exposing the more powerful API of h5py_. This makes the removing the dependency
  pytables_ possible.
- After processing the used profile is stored as a string alongside the results
  making them reproducible using only the storage file alone.
- Created a new logo to make the project more recognizable.

.. rubric:: Changed

- New commands :ref:`cli-ptvpy-generate-whirlpool` and
  :ref:`cli-ptvpy-generate-lines` replaced the old ``generate`` command.
- Renamed ``calculate_background`` to :func:`~.mean_frame`.
- Renamed ``process_helix_frame`` to :func:`~.find_helix_particles`.

.. rubric:: Removed

- Private parts of the Python API are no longer included by default in the HTML
  documentation.
- Removed the dependency on pytables_.

.. rubric:: Fixed

- Highlighting particles using the :ref:`slideshow <cli-ptvpy-view-slideshow>` will no
  longer fail if the linking step hasn't been performed and particle IDs are not
  available yet.
- In certain situations a particle would be assigned to more than one helix pair despite
  :ref:`profile-helix.unique` being ``true``. As part of the fix the implementation of
  the responsible function was rewritten and is now covered by tests.

.. _pytables: http://www.pytables.org/


Version 0.5.0
=============

Released on 2019-02-11.

.. rubric:: New

- All possible configuration options are now listed inside a profile file (see
  :ref:`profile-config`) and completely covered by an extended validation
  schema (see :mod:`~._schema`).
- Add command :ref:`cli-ptvpy-view-background` to make inspection of
  this intermediate result possible.
- Add option ``--force-profile`` to the commands :ref:`cli-ptvpy-view`,
  :ref:`cli-ptvpy-process` and :ref:`cli-ptvpy-export`.
- Added runtime dependencies h5py_ and `toml (Python package)`_ and updated
  existing dependencies.
- Extended the coverage of the test suite (now at 78%).

.. rubric:: Changed

- Profile files now use the `TOML language`_ and a new template.
- Replaced ``load_frames`` with :class:`~.FrameLoader` to allow finer control
  without wasting CPU-time or memory. This new class allows to cache and reuse
  the background between consecutive runs with the same input data (frames).
  On the first run the computed background is stored in the ``storage_file`` with
  a hash of the used data. The cached result is then reused the next time if the
  hash and thus the data stayed the same. Otherwise the background is computed
  again.
- Changed command line options of the :ref:`cli-ptvpy-process` command.
- The :ref:`cli-ptvpy-process` command no longer loads all frames into
  memory at once but sequentially when required. Thus the input data is no longer
  required to fit into memory all at once. In this regard the new function
  ``calculate_background`` was added. It calculates the average of frames
  sequentially without loading all frames into memory at once.
- Added functions :func:`~.hash_files` and :func:`~.hash_arrays`. These are
  useful when summarizing data on disk or in memory.
- The profile documentation is no longer included as a raw template but is
  automatically generated as a RestructuredText document (see :ref:`profile-config`).
- Renamed ``LazyLoadingSequence`` to :class:`~.LazyMapSequence`.
- Moved modules inside the subpackage ``_app`` to the top level and removed
  the subpackage.

.. rubric:: Removed

- Removed supported for multiple iterations of the location step. This might get
  readded in the future when detection of duplicates is implemented.
- Remove ``ptvpy.process.locate``, ``ptvpy.process.link`` and
  ``ptvpy.process.locate_helix_pairs``. The former two where wrappers around
  trackpy_ functions which are now directly used in :mod:`~._cli_process`.

.. rubric:: Fixed

- Removed unjustified scaling of frames with the factor 1/255 when removing
  the background (average per pixel of all used frames). This means that ``minmass``
  values derived from old profiles must be increased by the factor 255 to yield
  the same results (see :ref:`profile-trackpy_locate.minmass`).

.. _h5py: http://docs.h5py.org/en/stable/index.html
.. _toml (Python package): https://github.com/uiri/toml
.. _TOML language: https://github.com/toml-lang/toml


Version 0.4.0
=============

Released on 2018-12-12.

.. rubric:: New

- Add basic test coverage for the commands :ref:`cli-ptvpy-profile`,
  :ref:`cli-ptvpy-view` and :ref:`cli-ptvpy-export`.
- Add `pytest fixtures`_ which create dummy projects during testing.

.. rubric:: Changed

- Change backend of command :ref:`cli-ptvpy-view-slideshow` and introduce
  several improvements. The slide show is now animated (pause-able) and shows tracked
  particles. Upon clicking on a tracked particle it will display its properties
  and trajectory.
- Rename subcommand ``ptvpy view subpixel-bias`` to
  :ref:`cli-ptvpy-view-subpixel`.
- Switch to `Python 3.7`_ and update dependencies.

.. rubric:: Fixed

- Exports to MAT files will no longer contain the column names "angle" and "size"
  which clash with MATLAB's builtin symbols. Instead an "_" will be appended to
  those names (see :ref:`cli-ptvpy-export`).
- The subcommand :ref:`cli-ptvpy-profile-check` can deal with more error
  cases now and its output should be more useful even for unexpected errors.

.. rubric:: Removed

- Remove ``ptvpy view annotated-frame`` command which is obsolete now.

.. _Python 3.7: https://docs.python.org/3.7/whatsnew/3.7.html
.. _pytest fixtures: https://docs.pytest.org/en/latest/fixture.html


Version 0.3.0
=============

Released on 2018-10-02.

.. rubric:: New

- New CLI command ``section-cli-ptvpy-generate`` that can generate synthetic
  images for particle tracking velocimetry.
- Add new functions :func:`~.overlay_gaussian_blob` and
  ``constant_velocity_generator`` and remove old functions in :mod:`~.generate`.
- New tests that cover the basic workflow a user might have when using the CLI:
  image generation, profile creation, processing, viewing and exporting.
- Extend the developer guide with a description of
  how to setup the environment, run the test suite, make a release and build the
  documentation.
- Add a tutorial documenting the basic workflow <section-first-steps
  when using the CLI.
- New build script that nearly fully automates the documentation of the CLI and
  API.

.. rubric:: Changed

- Steps in the command :ref:`cli-ptvpy-process` are now supplied as arguments.
- Rename subpackages with conciser names which are more inline with other scientific
  libraries and make the subpackage containing the CLI application private.
- Use a new HTML theme from `Read the docs`_ with several CSS tweaks.
- Use the :file:`setup.py` as the single truth for the current version and generate
  a :file:`src/ptvpy/version.py` (including the git-commit hash of HEAD) during
  installation.
- Use the `src/package layout`_ (`see also`_).

.. rubric:: Fixed

- Patched several bugs in Sphinx when documenting functions that were jitted with
  numba_ or whose docstrings contain special characters used by click_.

.. _src/package layout: https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure
.. _see also: https://hynek.me/articles/testing-packaging/
.. _Read the docs: https://sphinx-rtd-theme.readthedocs.io/en/latest/
.. _numba: http://numba.pydata.org/


Version 0.2.1
=============

Released on 2018-09-18.

- Redesign configuration file to profile file
- Definition of a schema for the profile file using Cerberus_
- Validate profiles files with schema
- Multiple iteration steps for particle location
- Redesign command line interface (CLI) with click_
- Full integration of new profile module into the workflow of the CLI
- Use explicit lazy imports for heavy libraries for the CLI
- Setup pytest and integrate into conda-build process
- Automatic generation of reference documentation

.. _Cerberus: https://github.com/pyeve/cerberus
.. _click: http://click.pocoo.org/5/


Version 0.1.1
=============

- Basic command line interface with ``argparse``
- Configuration of processing steps with YAML document
- Particle tracking in 2 dimensions with trackpy_
- Particle tracking in 3 dimensions with double helix
- Distributable as conda_ package
- Basic HTML documentation
- Export functionality to common formats: CSV, MAT, XLSX, SQLITE

.. _trackpy: https://github.com/soft-matter/trackpy
.. _conda: https://conda.io/
