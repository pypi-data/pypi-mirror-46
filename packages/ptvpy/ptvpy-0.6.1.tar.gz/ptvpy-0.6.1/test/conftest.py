"""Fixtures and tools to test the CLI."""


import os
import shutil
import tempfile
from pathlib import Path

import pytest
import imageio
import trackpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from click.testing import CliRunner

from ptvpy import generate, process, io, _profile
from ptvpy._cli_root import root_group


# Ensure that trackpy doesn't log messages
trackpy.quiet()

#: File permission masks
permissions = {"r-xr--r--": 0o544, "rwxr--r--": 0o744}


@pytest.fixture(scope="function")
def close_plots():
    """Closes all open matplotlib figures when the test function exits."""
    yield
    plt.close("all")


@pytest.fixture(scope="session")
def _temporary_directory():
    """Provide session specific directory for the static project fixtures.

    Is deleted when the session terminates.

    See Also
    --------
    static_fresh_project, static_full_project
    """
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        yield tmp_dir
    finally:
        for child in tmp_dir.iterdir():
            # Ensure permission to delete
            os.chmod(child, permissions["rwxr--r--"])
        shutil.rmtree(tmp_dir)


@pytest.fixture(scope="function")
def static_fresh_project(_temporary_directory):
    """Provides a readonly project directory without processing results.

    Using the static version where possible reduces the execution time and disk
    space needed by tests that use this fixture.

    Parameters
    ----------
    _temporary_directory : Path
        Path to a session specific temporary directory.

    Returns
    -------
    static_fresh_project : Path
        Path to a session specific readonly project directory.
    """
    static_dir = _temporary_directory / "fresh_project"

    if not static_dir.exists():
        # Create content only once
        static_dir.mkdir()
        particles = generate.describe_lines(
            frame_count=20,
            particle_count=20,
            x_max=200,
            y_max=200,
            x_vel=1,
            y_vel=0,
            seed=42,
        )
        particles = generate.add_properties(particles)
        frames = generate.render_frames(particles)
        path_template = "image_{:0>2}.tiff"
        for i, image in enumerate(frames):
            # Ensure that allowed value range of storage format is not exceeded
            image = (image * 255).astype(np.uint8).clip(0, 255)
            with imageio.get_writer(static_dir / path_template.format(i + 1)) as writer:
                writer.append_data(image, {"compress": 2})
        # Create matching profile file
        _profile.create_profile_file(
            static_dir / "profile.ptvpy.toml", image_files="image_*.tiff"
        )
        os.chmod(static_dir, permissions["r-xr--r--"])

    os.chdir(static_dir)  # Ensure test functions start in this directory
    return static_dir


@pytest.fixture(scope="function")
def fresh_project(tmp_path, static_fresh_project):
    """Provides a project directory without processing results.

    Consider using the the static version which reduces the execution time and
    disk space needed by tests that use this fixture.

    Parameters
    ----------
    tmp_path : Path
        Path to a function specific temporary directory.
    static_fresh_project : Path
        Path to a session specific readonly project directory.

    Returns
    -------
    fresh_project : Path
        Path to the new function specific project directory.
    """
    tmp_path.rmdir()  # copytree expects to create target dir
    shutil.copytree(static_fresh_project, tmp_path)
    os.chmod(tmp_path, permissions["rwxr--r--"])  # Mark as read & write
    os.chdir(tmp_path)
    return tmp_path


@pytest.fixture(scope="function")
def static_full_project(static_fresh_project, _temporary_directory):
    """Provides a readonly project directory with processing results.

    Using the static version where possible reduces the execution time and disk
    space needed by tests that use this fixture.

    Parameters
    ----------
    static_fresh_project : Path
        Path to a session specific readonly project directory.
    _temporary_directory : Path
        Path to a session specific temporary directory.

    Returns
    -------
    static_fresh_project : Path
        Path to a session specific readonly project directory.
    """
    static_dir = _temporary_directory / "full_project"

    if not static_dir.exists():
        # Create content only once
        shutil.copytree(static_fresh_project, static_dir)
        os.chmod(static_dir, permissions["rwxr--r--"])  # Mark as read & write

        # Change to new directory and autodetect
        os.chdir(static_dir)
        _, profile = _profile.autodetect_profile(static_dir / "profile.ptvpy.toml")

        # Lazy-load Frames
        loader = io.FrameLoader(
            pattern=profile["general.data_files"],
            slice_=slice(*profile["general.subset"][["start", "stop", "step"]]),
        )
        storage_file = profile["general.storage_file"]
        if profile["step_locate.remove_background"]:
            loader.queue_background_removal(storage_file)
        frames = loader.lazy_frame_sequence()

        # Locate particles
        particles = []
        for i, frame in enumerate(frames):
            result = trackpy.locate(frame, **profile["step_locate.trackpy_locate"])
            result["frame"] = i
            particles.append(result)
        particles = pd.concat(particles, ignore_index=True)

        # Link particles
        particles = trackpy.link(particles, **profile["step_link.trackpy_link"])
        particles = trackpy.filter_stubs(
            particles, **profile["step_link.trackpy_filter_stubs"]
        )
        particles.reset_index(drop=True, inplace=True)

        # Calculate velocities
        particles = process.xy_velocity(particles, profile["step_diff.diff_step"])
        particles = process.absolute_velocity(particles)

        # Store the content
        with io.HdfFile(static_dir / Path(storage_file).name) as file:
            file.save_df("particles", particles)
        os.chmod(static_dir, permissions["r-xr--r--"])  # Mark as readonly

    os.chdir(static_dir)
    return static_dir


@pytest.fixture(scope="function")
def full_project(tmp_path, static_full_project):
    """Provides a project directory with processing results.

    Consider using the the static version which reduces the execution time and
    disk space needed by tests that use this fixture.

    Parameters
    ----------
    tmp_path : Path
        Path to a function specific temporary directory.
    static_full_project : Path
        Path to a session specific readonly project directory.

    Returns
    -------
    static_fresh_project : Path
        Path to the new function specific project directory.
    """
    tmp_path.rmdir()  # copytree expects to create target dir
    shutil.copytree(static_full_project, tmp_path)
    os.chmod(tmp_path, permissions["rwxr--r--"])  # Mark as read & write
    os.chdir(tmp_path)
    return tmp_path


@pytest.fixture(scope="session")
def runner():
    """Session specific runner to execute PtvPy's console commands.

    Returns
    -------
    runner : callable
        Signature is the same as :func:`click.testing.CliRunner.invoke` without
        the first argument `cli`.
    """
    # TODO Currently, it's not possible to check if PtvPy writes to stderr.
    #  This is because Exceptions are only displayed in stderr after the
    #  command has run in the wrapping _cli_root.main method.
    runner = CliRunner(mix_stderr=False)

    def run(*args, **kwargs):
        return runner.invoke(root_group, *args, **kwargs)

    return run
