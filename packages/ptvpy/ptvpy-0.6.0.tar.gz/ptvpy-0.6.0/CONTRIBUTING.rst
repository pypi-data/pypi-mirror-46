.. _contributing:

=========================
Contributing & Developing
=========================

Basic knowledge concerning the command line and tools such as Python, git and conda will
be helpful to understand this guide.

.. contents:: Content
   :local:


Development workflow
====================

This section will guide you through setting up the development environment and how to
perform common development tasks.


Getting the source code
-----------------------

> Requires git_

Fork the repository_ (referred to as `upstream`) on GitLab.com by clicking the
appropriate button and clone your fork into a local directory with (replace
``USERNAME`` with your actual username)::

    git clone https://gitlab.com/USERNAME/ptvpy.git ptvpy
    cd ptvpy
    git remote add upstream https://gitlab.com/tud-mst/ptvpy.git

The local repository is now linked to two remote repositories:

- `origin` - referring to your personal copy (fork) of the source code
- `upstream` - referring to the repository your fork points to.

Changes to the upstream repository are not automatically pushed to origin and your
local copy.
However you can update those with::

    git checkout master
    git pull upstream master
    git push origin master

.. _git: https://git-scm.com/doc
.. _repository: https://gitlab.com/tud-mst/ptvpy


Creating the development environment
------------------------------------

> Requires Anaconda_ or miniconda_

It is recommended to use a conda_ environment. If you haven't done so already add the
channel conda-forge to conda's search path with ::

    conda config --append channels conda-forge

Then create a new conda environment by initially installing ``ptvpy`` itself and the
development dependencies::

    conda create --name ENVNAME ptvpy pytest-cov black sphinx_rtd_theme

You can replace ``ENVNAME`` with any desired name. Activate the development environment
with (omit ``source`` on Windows) ::

    source activate ENVNAME

and replace ``ptvpy`` with version installed in editable mode which points to the local
source directory::

    pip install --editable .

This command must be executed in the directory containing the ``setup.py`` file.
If the installation was successful you should be able to type ::

    ptvpy --version

which should output a version number suffixed with the revision number of the current
checkout (compare with output of ``git describe --tags --dirty --always``).

.. _Anaconda: https://www.anaconda.com/distribution/
.. _miniconda: https://docs.conda.io/en/latest/miniconda.html
.. _conda: https://docs.conda.io/

.. _testing:

Testing
-------

If all steps in the previous section were followed correctly the tests can be
run by executing ::

    pytest

in the project directory. Adding the flag ``--cov`` will record the test coverage as
well and display a basic summary. To generate a detailed report use ::

    coverage html -d build/coverage

and open the file ``build/coverage/index.html`` with a browser. The implicit
configuration of how pytest_ and the coverage analysis runs are configured in the
:file:`setup.cfg` and :file:`.coveragerc`.

.. _pytest: https://docs.pytest.org


Building the documentation
--------------------------

PtvPy's online documentation is build with the static site generator Sphinx_ and the
`Read The Docs Sphinx Theme`_. Its configuration can be found inside the file
:file:`doc/conf.py`.

The reference part of the documentation is directly generated from PtvPy's APIs. In case
of the Python API this is accomplished via Sphinx's autodoc extension. However the
source files for the the command line interface and profile file are generated with the
script :file:`build_doc.py` before invoking Sphinx. This script manages both steps
directly and may be called like this::

   python doc/build_doc.py build/html-doc

To include private parts of the Python API as well, add the flag ``--show-private``
behind ``build_doc.py``. Supply the ``--help`` option to display a full list of its
options.

.. _Sphinx: http://www.sphinx-doc.org/en/stable/index.html
.. _Read The Docs Sphinx Theme: https://sphinx-rtd-theme.readthedocs.io/en/stable/


Creating a merge request
------------------------

Merge requests (GitHub calls these pull requests) are a way to contribute changes even
without commit rights to PtvPy's repository. Start by creating a new branch for the
feature or change you want to contribute::

    git checkout master
    git pull upstream master
    git checkout -b FEATURE-BRANCH

Then you can commit local changes to this branch using the ``git add`` and
``git commit`` commands. You can find a good introduction on recording changes
here_. You then need to push these changes to your fork with ::

    git push -u origin FEATURE-BRANCH

You only need to add the ``-u`` flag the first time you do this. If that was successful
git will display a link inside the console to create a new merge request. Otherwise
just head to your fork on GitLab.com and click on `Merge Requests > New merge request`.

Before suggesting any changes in a new merge request make sure that you have read the
:ref:`guidelines` in the next section. It's often useful to run the test suite locally
beforehand as well.

.. _here: https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository


.. _guidelines:

Guidelines
==========

- Use the code formatter black_ to style your code. E.g. ``black src/ptvpy/process.py``.
  Sometimes big, deeply nested structures may be significantly more readable if
  formatted manually. To preserve the format for these exceptions you can wrap the code
  block into `# fmt: off ... # fmt: on` statements.
- Every module, class or function should include documentation in the form of
  docstrings. Their format should follow the `NumPy style`_.
- New functionality or changes especially to the public API should be covered by tests.
- Make sure that your contributions are compatible with this project's :ref:`license`
  (see also :ref:`stackoverflow`).
- Try to write concise and useful commit messages. To see why and how have a look at
  this guide_.

Generally follow good practices already established in the scientific Python community.
It's often useful to look at content already present and try to follow its style. If in
doubt feel free to ask.

.. _black: https://black.readthedocs.io/en/stable/
.. _NumPy style: https://numpydoc.readthedocs.io/en/latest/format.html
.. _guide: https://chris.beams.io/posts/git-commit/

.. _stackoverflow:

Using Stack Overflow
--------------------

.. important::

   Please avoid copying code snippets directly from Stack Overflow unless the author
   has explicitly placed the content under a compatible license!

By default `content on Stack Overflow`_ is licensed under the `CC BY-SA 3.0`_ which
demands derivative work to be licensed under a compatible license.
As of now only CC-licenses are `listed as compatible`_ which excludes most common
open source licenses.
Using Stack Overflow as a knowledge base and point of reference should be okay
though. [#f]_
In this case please include a hyperlink to the appropriate comment or answer.

Further reading:

- `Proposal to use the MIT License`_ for code on Stack Overflow and the follow-up_
- Blogpost `Stack Overflow Code Snippets`_ by Sebastian Baltes.

.. [#f] This is not legal advice. So if in doubt please consult an attorney or
        avoid the issue altogether.

.. _content on Stack Overflow: https://stackoverflow.com/legal/terms-of-service
.. _CC BY-SA 3.0: https://creativecommons.org/licenses/by-sa/3.0/
.. _listed as compatible: https://creativecommons.org/share-your-work/licensing-considerations/compatible-licenses
.. _Proposal to use the MIT License: https://meta.stackexchange.com/q/271080
.. _follow-up: https://meta.stackexchange.com/q/272956
.. _Stack Overflow Code Snippets: https://empirical-software.engineering/blog/so-snippets-in-gh-projects


Releasing a new version
=======================

.. note:: Work in progress.

Commit and tag the change::

   git commit -m "Prepare release <BASE_VERSION>"
   git tag -s "<BASE_VERSION>"

Now build the release files (conda package & documentation) with the Bash script
:file:`release.sh`. Afterwards increase the number in ``BASE_VERSION`` in
:file:`setup.py` in anticipation of the next release and re-append ``.dev`` again


Useful Links
============

* `trackpy <http://soft-matter.github.io/trackpy>`_
* `conda-build <https://docs.conda.io/projects/conda-build>`_
* `Python Packaging User Guide <https://packaging.python.org/>`_
