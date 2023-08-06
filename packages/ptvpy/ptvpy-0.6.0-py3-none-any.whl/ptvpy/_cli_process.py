"""Subcommand `process`."""


from multiprocessing.pool import ThreadPool

import click

from .utils import LazyImporter
from ._profile import autodetect_profile
from ._cli_root import root_group, profile_option, force_profile_option, CliSpinner


#: Accessor for lazily loaded modules
lazy = LazyImporter(
    imports={
        "np": "numpy",
        "pd": "pandas",
        "h5py": "h5py",
        "trackpy": "trackpy",
        "tqdm": "tqdm",
        "process": "..process",
        "io": "..io",
    },
    package=__name__,
)


def _to_dataframe(hdf_dataset):
    return lazy.pd.DataFrame.from_records(hdf_dataset)


def _step_locate(profile, particle_shape=None):
    """Handle multi-threaded particle location.

    Parameters
    ----------
    profile : ChainedKeyMap
        Mapping like object containing the profile configuration.
    particle_shape : {"blob", "helix"}, optional
        If given, overwrites the profile value with the same name.

    Returns
    -------
    particles : pandas.DataFrame[frame, x, y, ...]
        Located particle positions and their properties.
    """
    if not particle_shape:
        particle_shape = profile["step_locate.particle_shape"]

    # Load frames
    loader = lazy.io.FrameLoader(
        pattern=profile["general.data_files"],
        slice_=slice(*profile["general.subset"][["start", "stop", "step"]]),
    )
    if profile["step_locate.remove_background"]:
        with CliSpinner("Calculating background") as spinner:
            loader.queue_background_removal(profile["general.storage_file"])
            if loader.used_background_cache:
                spinner.success_message = "done (used cache)"
    frames = loader.lazy_frame_sequence()

    # Prepare input for ThreadPool's worker function (_locate_worker)
    locate_kwargs = profile["step_locate.trackpy_locate"]
    if particle_shape == "helix":
        helix_kwargs = profile["step_locate.helix"]
    else:
        helix_kwargs = None

    def worker(i):
        # Make sure to load the frame only inside the worker as ThreadPool
        # will evaluate generators passed to its map-like methods at once.
        # So doing something like pool.imap(worker, enumerate(frames))
        # would load all frames into memory at once.
        particles = lazy.trackpy.locate(frames[i], **locate_kwargs)
        particles["frame"] = i
        if helix_kwargs:
            particles = lazy.process.find_helix_particles(particles, **helix_kwargs)
        return particles

    lazy.trackpy.quiet()  # Ensure that output of trackpy is suppressed
    progress_bar = lazy.tqdm.tqdm(
        desc=f"Locating particles", total=len(frames), ascii=True
    )
    particles = []
    with progress_bar:
        with ThreadPool(profile["step_locate.parallel"]) as pool:
            for results in pool.imap_unordered(worker, range(len(frames))):
                # TODO maybe, write directly to file, see "unlimited" keyword in
                # http://docs.h5py.org/en/latest/high/dataset.html#resizable-datasets
                particles.append(results)
                progress_bar.update()
    particles = lazy.pd.concat(particles, ignore_index=True)
    return particles


def _step_link(profile, particles):
    """Handle particle linking.

    Parameters
    ----------
    profile : ChainedKeyMap
        Mapping like object containing the profile configuration.
    particles : pandas.DataFrame[frame, x, y, ...]
        Located particle positions and their properties.

    Returns
    -------
    linked_particles : pandas.DataFrame[frame, particle, x, y, ...]
        Linked particles, their positions and their properties.
    """
    lazy.trackpy.quiet()  # Ensure that output of trackpy is suppressed
    with CliSpinner("Linking particles"):
        particles = lazy.trackpy.link(particles, **profile["step_link.trackpy_link"])
        particles = lazy.trackpy.filter_stubs(
            particles, **profile["step_link.trackpy_filter_stubs"]
        )
        particles.reset_index(drop=True, inplace=True)
    return particles


def _step_diff(profile, particles):
    """Handle calculation of particle velocities.

    Parameters
    ----------
    profile : ChainedKeyMap
        Mapping like object containing the profile configuration.
    particles : pandas.DataFrame[frame, particle, x, y, ...]
        Linked particles, their positions and their properties.

    Returns
    -------
    diffed_particles : pandas.DataFrame[frame, particle, x, y, dx, dy, v, ...]
        Velocities of the particles and other properties.
    """
    with CliSpinner("Calculating velocities"):
        particles = lazy.process.xy_velocity(particles, profile["step_diff.diff_step"])
        particles = lazy.process.absolute_velocity(particles)
    return particles


@root_group.command(name="process")
@click.option(
    "--step",
    type=click.Choice(["locate", "link", "diff"]),
    help="Only do the given processing step. If not provided all steps given "
    "in the profile option will be used.",
)
@click.option(
    "--particle-shape",
    type=click.Choice(["blob", "helix"]),
    help="Overwrite the expected particle shape. If not provided the option "
    "given in the profile will be used.",
)
@profile_option
@force_profile_option
def process_command(step, particle_shape, profile, force_profile):
    """Process a data set.

    This command is controlled via a profile (see "ptvpy profile -h") that
    tells PtvPy where the data is stored and how to process it. Some profile
    options may be temporarily overwritten with the options listed below.
    """
    profile_path, profile = autodetect_profile(profile, validate=(not force_profile))
    storage_path = profile["general.storage_file"]
    steps = [step] if step else profile["general.default_steps"]

    # Load previous results if they already exist
    with lazy.io.HdfFile(storage_path) as file:
        if "particles" in file:
            particles = file.load_df("particles")
        else:
            particles = None

    try:
        if "locate" in steps:
            particles = _step_locate(profile, particle_shape)
        if "link" in steps:
            particles = _step_link(profile, particles)
        if "diff" in steps:
            particles = _step_diff(profile, particles)

    finally:
        if particles is not None:
            # Save current profile content using h5py
            with open(profile_path) as stream:
                profile_string = stream.read()
            with lazy.io.HdfFile(storage_path, "a") as file:
                # Remove old results if existing
                if "profile" in file:
                    del file["profile"]
                # Before storing, convert to ASCII string
                file["profile"] = lazy.np.string_(profile_string)
                # And finally store matching results
                file.save_df("particles", particles)

    click.echo("Particle statistics (summary):")
    # Ensure columns are not truncated when printing the summary
    with lazy.pd.option_context("display.max_columns", None):
        click.echo(particles.describe())
