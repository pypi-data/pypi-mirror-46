.. _workflow:

================
Example workflow
================

This document aims to give a brief tour and overview of PtvPy's functionality.
The different sections build on one another and demonstrate a possible workflow
when using the tool.

.. highlight:: none

.. note:: This document is not finished yet.

.. contents:: Content
   :local:


Generating an artificial dataset
================================

PtvPy provides the means to :ref:`generate <cli-ptvpy-generate>` artificial
data for different scenarios.
This is not only useful when testing the application but also to demonstrate its
capabilities.
Starting our work inside an empty directory we will create a dataset of 200 images
(or frames) inside the subdirectory ``data/`` with the following command::

    ptvpy generate whirlpool --seed 42 --white-noise 40 10 -- data/ 200

As you may have guessed this dataset simulates particles floating inside a whirlpool.
The option ``--white-noise 40 10`` will add white noise (mean: 40, variance: 10)
to the background and ``--seed 42`` will ensure that PtvPy will generate the
same data as used by this guide.
For non-specified options, PtvPy will use default values (compare
:ref:`command <cli-ptvpy-generate-whirlpool>`).
At this point you can already inspect the images with a conventional image viewer.


Creating a new profile
======================

To do anything meaningful with a dataset PtvPy requires a profile file that
informs it how to find the input data and how to process it.
You can create a new profile file using the command ::

    ptvpy profile create

You'll be asked to provide a pattern_ matching the image files created in the
previous section.
In this case the pattern is quite simply ``data/*.tiff``.
PtvPy will check that the pattern is valid and then create the new profile
``profile.ptvpy.toml`` inside the current directory.

.. _pattern: https://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html


Particle tracking & fine-tuning a profile
=========================================

Now we are ready to start processing. For now we only want to track the particles
without linking them by calling::

    ptvpy process --step locate

PtvPy will start by averaging each pixel across all frames (calculating the background).
This background will be subtracted from each frame before searching for particles
which will suppress background noise and isolate the dynamic parts: moving particles.
PtvPy will try to inform you about the progress which can take some time for large
datasets.
Once it's done it will show you a summary of the results which should look like
this::

    Calculating background: done
    Locating particles: 100%|#################################| 200/200 [00:01<00:00, 116.16it/s]
    Particle statistics (summary):
                      y             x          mass          size           ecc  \
    count  19264.000000  19264.000000  19264.000000  19264.000000  19264.000000
    mean      99.378071     99.514501    114.124951      2.529149      0.264548
    std       55.751874     55.806127    123.580979      0.476125      0.148719
    min        3.357558      3.395238     21.070591      1.458642      0.003097
    25%       51.178019     50.767314     56.276556      2.211290      0.135279
    50%       99.083210     99.307805     67.508123      2.589611      0.248646
    75%      147.976992    147.778505     83.245164      2.882891      0.370317
    max      195.501661    195.531579    626.914116      3.829045      0.780934

                 signal      raw_mass            ep         frame
    count  19264.000000  19264.000000  12160.000000  19264.000000
    mean       8.983435    439.357264     -0.346099     99.704682
    std        9.973106    223.799783     48.414316     57.726140
    min        2.036503    160.850000  -4813.712969      0.000000
    25%        4.251701    324.332500     -0.275444     50.000000
    50%        4.988159    363.560000     -0.000000    100.000000
    75%        6.142398    415.211250      0.113522    150.000000
    max       45.401406   1490.410000   1203.972737    199.000000


At this point we have tried to find particles using the default values given in
a new profile.
However these are rarely optimal as can be easily seen when plotting the results
with the :ref:`slideshow command <cli-ptvpy-view-slideshow>`::

    ptvpy view slideshow

.. image:: https://gitlab.com/tud-mst/ptvpy/uploads/c34143425700d7c5cefa733e50dae7d8/workflow-slideshow-1.svg
   :align: center

Due to the background noise PtvPy detected fake particles that we don't want in
the final results.
To resolve this we have to find a property that effectively differentiates fake
particles from true ones.
At this stage, the `mass` and `size` of the detected particles are often the two
most meaningful properties to do so.
Plotting them with ::

    ptvpy view relationship mass size

.. image:: https://gitlab.com/tud-mst/ptvpy/uploads/7b52f8f5a1b1279c19f5e6ac6ea96bec/workflow-relationship-mass-size.png
   :align: center

will show us that the particles can be effectively grouped this way into fake (group
to the left with a small `mass` and large variance in `size`) and true particles
(group to the right).
After setting the profile field :ref:`profile-trackpy_locate.minmass` to
150 we process the dataset a second time, this time including all processing steps::

    ptvpy process

and visualize the results again with ::

    ptvpy view slideshow

.. image:: https://gitlab.com/tud-mst/ptvpy/uploads/1c5d67c083baf20863c1af362b85f8cb/workflow-slideshow-2.svg
   :align: center

While the results are still not perfect were are detecting only valid particles now.
We could improve upon this by tweaking other parameters inside the profile.
Parameters that often prove useful are:

- :ref:`profile-trackpy_locate.minmass` - Particles can often be clustered based on
  their `mass`. As such this parameter is useful to suppress small particles or "fake"
  ones detected due to background noise.
- :ref:`profile-trackpy_locate.diameter` - The expected diameter of of particles.
  If in doubt choose a larger value (must always be odd).
- :ref:`profile-trackpy_locate.separation` - If not given this one defaults to
  "`diameter` + 1" which might not be optimal when the particle density is high.
- :ref:`profile-trackpy_link.search_range` - This parameter should match the maximal
  expected particle velocity.
- :ref:`profile-trackpy_link.memory` - Increasing this parameter helps tracking
  particles over multiple frames when they weren't detected in all consecutive frames.


.. Todo Visualizing results

.. Todo Exporting results
