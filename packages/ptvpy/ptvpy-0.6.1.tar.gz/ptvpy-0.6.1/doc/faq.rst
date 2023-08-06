==========================
Frequently asked questions
==========================

Why is my profile file not accepted or found?
=============================================

When trying to auto-detect a valid profile file PtvPy will try to find files
suffixed with ".ptvpy.toml" in the current directory and validate these against
an internal rule set.
Only if exactly one valid profile is found PtvPy considers the auto-detection to
be unambiguous and proceeds.
Otherwise the flag ``--profile`` can be used to explicitly specify which profile
to use.

.. tip::

    You can check the current directory for valid profiles with the command
    :ref:`cli-ptvpy-profile-check` which will attempt to display detailed
    information about why a profile might be invalid.


How do I report an error?
=========================

Try to gather as much information about the error as you can and send an email
to the developers. Depending on the nature of the error you may first try several
of the steps below before reporting.

If the error happens while executing one of PtvPy's commands inside the terminal
you may insert the ``--debug`` flag right after ``ptvpy``, e.g::

    ptvpy process

should become ::

    ptvpy --debug process

This will increase the information PtvPy shows about the error.


How are processing results stored?
==================================

PtvPy stores all results inside the file configured in the profile field
:ref:`profile-storage_file`.
Unless changed this will point to the file :file:`storage.ptvpy.hdf5` inside the
same directory as the profile file.
Independent of the name and location the data will always be stored using the
`HDF5 format`_ which is a scientific hierarchical data format supported by a wide
range of applications and software.
PtvPy itself relies on the excellent implementation provided by h5py_ to work
with the HDF5 format.
This file will contain the results inside a group named "particles".
The groups content maps to a DataFrame with the same columns as displayed by the
:ref:`cli-ptvpy-view-summary` command.

.. tip::

    If you want to access the data using another format have a look at the
    :ref:`cli-ptvpy-export` command.

.. _HDF5 format: https://support.hdfgroup.org/HDF5/
.. _pandas.HDFStore: https://pandas.pydata.org/pandas-docs/stable/io.html#io-hdf5
.. _PyTables: http://www.pytables.org/index.html
.. _h5py: http://docs.h5py.org/en/stable/
