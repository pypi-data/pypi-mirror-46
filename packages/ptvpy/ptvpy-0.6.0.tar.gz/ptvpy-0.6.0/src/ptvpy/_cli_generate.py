"""Command-group `generate`."""


from pathlib import Path

import click

from .utils import LazyImporter
from ._cli_root import root_group, CliSpinner


#: Accessor for lazily loaded modules
lazy = LazyImporter(
    imports={
        "tqdm": "tqdm",
        "np": "numpy",
        "imageio": "imageio",
        "generate": "..generate",
    },
    package=__name__,
)


def _has_images(directory: Path) -> bool:
    """Check if `directory` contains files matching "image_*.tiff"."""
    if not directory.is_dir():
        directory.mkdir()
        click.echo(f"Created '{directory}'")
    try:
        next(directory.glob("image_*.tiff"))
    except StopIteration:
        return False
    else:
        return True


def _save_frames(progress_bar, directory, frame_count, frames):
    """Save frames into given directory.

    Parameters
    ----------
    progress_bar : tqdm.tqdm
        A progressbar to give visual feedback.
    directory : Path
        Directory to write to.
    frame_count: int
        The number of frames to write.
    frames : Iterable[numpy.ndarray]
        Iterable that yields the generated frames.
    """
    pad_width = int(lazy.np.ceil(lazy.np.log10(frame_count)))
    path_template = str(directory / f"image_{{:0>{pad_width}}}.tiff")
    with progress_bar:
        for i, frame in enumerate(frames):
            # Ensure that allowed value range of storage format is not exceeded
            frame = frame.clip(0, 255).astype(lazy.np.uint8)
            with lazy.imageio.get_writer(path_template.format(i)) as writer:
                writer.append_data(frame, {"compress": 2})
            progress_bar.update()


def _basic_generate_api(func):
    """Add basic options and arguments to generate subcommands.

    Adds the arguments DIRECTORY and FRAME_COUNT as well as other common
    options.
    """
    # Arguments must be added in reverse order compared to usual order if
    # added as properties
    func = click.argument("frame_count", type=click.IntRange(min=1))(func)
    func = click.argument("directory", type=click.Path(file_okay=False))(func)
    func = click.option(
        "--white-noise",
        metavar="FLOAT FLOAT",
        type=click.FLOAT,
        nargs=2,
        help="Add white noise to each frame by specifying the mean value and"
        "variance of the noise. Pixel values are limited between 0 and 255.",
    )(func)
    func = click.option(
        "--particle-brightness",
        metavar="FLOAT FLOAT",
        type=click.FloatRange(min=0),
        nargs=2,
        default=(100, 10),
        help="Two values describing the average particle brightness a and its variance "
        "at the center. Pixel values are limited between 0 and 255. Default: 100 10",
    )(func)
    func = click.option(
        "--particle-size",
        metavar="FLOAT FLOAT",
        type=click.FloatRange(min=0),
        nargs=2,
        default=(5, 0.5),
        help="Two values describing the average particle size and its variance "
        "in pixels. The particle size corresponds to the variance of the gaussian "
        "blobs representing the particles. Default: 5 0.5",
    )(func)
    func = click.option(
        "--particle-count",
        metavar="INTEGER",
        type=click.IntRange(min=1),
        default=20,
        help="Number of particles in each frame. Default: 20",
    )(func)
    return func


@root_group.group(name="generate")
def generate_group():
    """Generate synthetic images.

    These commands will generate artificial images with particles moving in a
    defined pattern across the generated frames. The starting position, size
    and brightness of each particle are randomized while other parameters are
    configurable.

    Currently only the TIFF format is supported.
    """
    pass


@generate_group.command(name="lines")
@_basic_generate_api
@click.option(
    "--frame-size",
    metavar="INTEGER INTEGER",
    help="Size of the X and Y dimension of the created frames in pixels. "
    "Default: 200 200",
    type=click.IntRange(min=1),
    nargs=2,
    default=(200, 200),
)
@click.option(
    "--velocity",
    metavar="FLOAT FLOAT",
    help="Velocity vector of the particles giving the step (X, Y) in pixels "
    "per frame. Default: 2 0",
    type=click.FloatRange(min=0),
    nargs=2,
    default=(2, 0),
)
@click.option(
    "--jitter",
    metavar="FLOAT",
    type=click.FloatRange(min=0),
    default=0,
    help="Add noise drawn from a Gaussian distribution with the given "
    "variance to the particle positions.",
)
@click.option("--seed", help="Seed the random number generator.", type=click.INT)
def lines_command(**kwargs):
    """Generate particles moving along lines.

    Will create a FRAME_COUNT images in DIRECTORY. These images display
    particles moving along straight lines at the same velocity. The initial
    start position is randomized.
    """
    directory = Path(kwargs["directory"])
    if _has_images(directory):
        click.echo(
            "Warning: directory already contains files matching "
            "'image_*.tiff'. Delete these files first."
        )
        return

    with CliSpinner("Preparing particle data"):
        particles = lazy.generate.describe_lines(
            frame_count=kwargs["frame_count"],
            particle_count=kwargs["particle_count"],
            x_max=kwargs["frame_size"][0],
            y_max=kwargs["frame_size"][1],
            x_vel=kwargs["velocity"][0],
            y_vel=kwargs["velocity"][1],
            wrap=True,
            seed=kwargs["seed"],
        )
        particles = lazy.generate.add_properties(
            particles,
            size=kwargs["particle_size"],
            brightness=kwargs["particle_brightness"],
            seed=kwargs["seed"],
        )
        particles = lazy.generate.jitter(
            particles, x=kwargs["jitter"], y=kwargs["jitter"]
        )
        if kwargs["white_noise"]:
            background = lazy.generate.white_noise(
                shape=kwargs["frame_size"],
                mu=kwargs["white_noise"][0],
                variance=kwargs["white_noise"][1],
                seed=kwargs["seed"],
            )
        else:
            background = lazy.np.zeros(kwargs["frame_size"])
        frames = lazy.generate.render_frames(particles, background)

    progress_bar = lazy.tqdm.tqdm(
        desc="Generating frames", total=kwargs["frame_count"], ascii=True
    )
    _save_frames(progress_bar, directory, kwargs["frame_count"], frames)


@generate_group.command(name="whirlpool")
@_basic_generate_api
@click.option(
    "--radius",
    metavar="FLOAT",
    type=click.FloatRange(min=0),
    default=100,
    help="Radius of the whirlpool in pixels. Default: 100",
)
@click.option(
    "--angle-vel",
    metavar="FLOAT",
    type=click.FloatRange(min=0),
    default=0.3,
    help="Maximal angular velocity in radians per frame at the center of the "
    "whirlpool. The speed decreases linearly to zero for particles closer to "
    "the edge. Default: 0.3",
)
@click.option(
    "--jitter",
    metavar="FLOAT",
    type=click.FloatRange(min=0),
    default=0,
    help="Add noise drawn from a Gaussian distribution with the given "
    "variance to the particle positions.",
)
@click.option("--seed", help="Seed the random number generator.", type=click.INT)
def whirlpool_command(**kwargs):
    """Generate particles moving in a whirlpool.

    Will create a FRAME_COUNT images in DIRECTORY. These images display
    particles moving inside a whirlpool. The initial start position is
    randomized (within a polar coordinate system). Particles closer to the
    whirlpools center move faster.
    """
    directory = Path(kwargs["directory"])
    if _has_images(directory):
        click.echo(
            "Warning: directory already contains files matching "
            "'image_*.tiff'. Delete these files first."
        )
        return

    with CliSpinner("Preparing particle data"):
        particles = lazy.generate.describe_whirlpool(
            frame_count=kwargs["frame_count"],
            particle_count=kwargs["particle_count"],
            radius=kwargs["radius"],
            angle_vel=kwargs["angle_vel"],
            seed=kwargs["seed"],
        )
        particles = lazy.generate.add_properties(
            particles,
            size=kwargs["particle_size"],
            brightness=kwargs["particle_brightness"],
            seed=kwargs["seed"],
        )
        particles = lazy.generate.jitter(
            particles, x=kwargs["jitter"], y=kwargs["jitter"]
        )
        diameter = int(lazy.np.ceil(kwargs["radius"])) * 2
        if kwargs["white_noise"]:
            background = lazy.generate.white_noise(
                shape=(diameter, diameter),
                mu=kwargs["white_noise"][0],
                variance=kwargs["white_noise"][1],
                seed=kwargs["seed"],
            )
        else:
            background = lazy.np.zeros((diameter, diameter))
        frames = lazy.generate.render_frames(particles, background)

    progress_bar = lazy.tqdm.tqdm(
        desc="Generating frames", total=kwargs["frame_count"], ascii=True
    )
    _save_frames(progress_bar, directory, kwargs["frame_count"], frames)
