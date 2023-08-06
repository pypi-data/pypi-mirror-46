"""Command-group `view` with subcommands."""


import click

from .utils import LazyImporter
from ._profile import autodetect_profile
from ._cli_root import root_group, profile_option, force_profile_option, CliSpinner


#: Accessor for lazily loaded modules
lazy = LazyImporter(
    imports={
        "pd": "pandas",
        "plt": "matplotlib.pyplot",
        "trackpy": "trackpy",
        "io": "..io",
        "plot": "..plot",
        "process": "..process",
    },
    package=__name__,
)


@root_group.group(name="view", chain=True)
@profile_option
@force_profile_option
@click.pass_context
def view_group(ctx, **kwargs):
    """Inspect and plot processed data.

    \b
    Examples:
      ptvpy view vector -h
      ptvpy view relationship x v
      ptvpy view -p my_profile.toml summary
    """
    _, profile = autodetect_profile(
        kwargs["profile"], validate=(not kwargs["force_profile"])
    )
    ctx.obj["profile"] = profile


@view_group.resultcallback()
def view_resultcallback(results, **_):
    """Show plots after chain of subcommands has run."""
    if any(results):
        click.echo("Showing plot(s)...")
        lazy.plt.show()


def _particle_data(profile):
    with lazy.io.HdfFile(profile["general.storage_file"]) as file:
        try:
            return file.load_df("particles")
        except KeyError:
            return None


@view_group.command(name="background")
@click.pass_context
def background_command(ctx):
    """Plot average per pixel for used frames."""
    with CliSpinner("Preparing background"):
        profile = ctx.obj["profile"]
        loader = lazy.io.FrameLoader(
            pattern=profile["general.data_files"],
            slice_=slice(*profile["general.subset"][["start", "stop", "step"]]),
        )
        background = loader.load_background(profile["general.storage_file"])
        figure, axes = lazy.plt.subplots()
        axes.imshow(background, origin="lower", cmap="gray")
        figure.canvas.set_window_title("PtvPy: Background")
        return figure


@view_group.command(name="histogram")
@click.argument("x", type=click.STRING)
@click.option("--kde", is_flag=True, help="Plot as a gaussian kernel density estimate.")
@click.pass_context
def histogram_command(ctx, x, kde):
    """Plot histogram of X."""
    with CliSpinner("Preparing histogram"):
        profile = ctx.obj["profile"]
        particle_data = _particle_data(profile)
        figure, _ = lazy.plot.plot_histogram(
            particle_data, x, distplot_kws=dict(kde=kde)
        )
        figure.canvas.set_window_title(f"PtvPy: Histogram '{x}'")
        return figure


@view_group.command(name="map")
@click.argument("x", type=click.STRING)
@click.argument("y", type=click.STRING)
@click.argument("z", type=click.STRING)
@click.option(
    "--extrapolate",
    help="Extrapolate values outside convex hull of the data points.",
    is_flag=True,
)
@click.pass_context
def map_command(ctx, x, y, z, extrapolate):
    """Plot map of Z in X & Y."""
    with CliSpinner("Preparing map"):
        profile = ctx.obj["profile"]
        particle_data = _particle_data(profile)
        out = lazy.process.scatter_to_regular(
            [x, y, z], data=particle_data, extrapolate=extrapolate
        )
        figure, _ = lazy.plot.plot_map(x, y, z, data=out)
        figure.canvas.set_window_title(f"PtvPy: Map {[x, y, z]}")
        return figure


@view_group.command(name="relationship")
@click.argument("x", type=click.STRING)
@click.argument("y", type=click.STRING)
@click.pass_context
def relationship_command(ctx, x, y):
    """Plot relationship between X and Y."""
    with CliSpinner("Preparing relationship plot"):
        profile = ctx.obj["profile"]
        particle_data = _particle_data(profile)
        grid = lazy.plot.plot_relationship(x, y, particle_data)
        grid.fig.canvas.set_window_title(f"PtvPy: Relationship {[x, y]}")
        return grid


@view_group.command(name="scatter3d")
@click.argument("x", type=click.STRING)
@click.argument("y", type=click.STRING)
@click.argument("z", type=click.STRING)
@click.option(
    "--color", help="Use variable to color the data points.", type=click.STRING
)
@click.pass_context
def scatter_3d_command(ctx, x, y, z, color):
    """Plot scatter plot in X, Y, Z"""
    # TODO replace with trackpy.scatter3d?
    with CliSpinner("Preparing scatter plot"):
        profile = ctx.obj["profile"]
        particle_data = _particle_data(profile)
        figure, _ = lazy.plot.plot_scatter_3d(x, y, z, color, data=particle_data)
        title = f"PtvPy: Scatter plot in 3D {[x, y, z]}"
        figure.canvas.set_window_title(title)
        return figure


@view_group.command(name="slideshow")
@click.option(
    "--autostart", is_flag=True, help="Autostart animation of the slide show."
)
@click.option("--no-annotation", is_flag=True, help="Don't display annotations.")
@click.pass_context
def slideshow_command(ctx, autostart, no_annotation):
    """Show slide show of annotated frames.

    The animated slide show can be (un)paused with the space key. The slider
    can be controlled by dragging with the mouse or using the arrow keys.
    Clicking near a tracked particle will display its properties and path; use
    the left mouse button to unselect.
    """
    with CliSpinner("Preparing slideshow"):
        profile = ctx.obj["profile"]
        particle_data = None if no_annotation else _particle_data(profile)
        loader = lazy.io.FrameLoader(
            pattern=profile["general.data_files"],
            slice_=slice(*profile["general.subset"][["start", "stop", "step"]]),
        )
        if profile["step_locate.remove_background"]:
            loader.queue_background_removal(profile["general.storage_file"])
        frames = loader.lazy_frame_sequence()
        slide_show_plot = lazy.plot.SlideShowPlot(frames, particle_data, autostart)
        slide_show_plot.figure.canvas.set_window_title("PtvPy: Slide show")
        return slide_show_plot


@view_group.command(name="subpixel")
@click.pass_context
def subpixel_command(ctx):
    """Show fractional parts of the x & y positions."""
    with CliSpinner("Preparing subpixel plot"):
        profile = ctx.obj["profile"]
        particle_data = _particle_data(profile)
        lazy.trackpy.subpx_bias(particle_data)
        return True


@view_group.command(name="summary")
@click.pass_context
def summary_command(ctx):
    """Print summarizing statistics."""
    click.echo("Particle statistics (summary):")
    profile = ctx.obj["profile"]
    with lazy.pd.option_context("display.max_columns", None):
        click.echo(_particle_data(profile).describe())


@view_group.command(name="trajectories")
@click.option(
    "--names",
    default=["x", "y"],
    help="Names of the first and second coordinate.",
    nargs=2,
    type=click.STRING,
)
@click.pass_context
def trajectories_command(ctx, names):
    """Plot trajectories of detected particles."""
    names = list(names)
    with CliSpinner("Preparing trajectory plot"):
        profile = ctx.obj["profile"]
        particle_data = _particle_data(profile)
        figure, ax_traj = lazy.plt.subplots()
        lazy.trackpy.plot_traj(particle_data, ax=ax_traj, pos_columns=names)
        figure.canvas.set_window_title("PtvPy: Particle trajectories")
        return figure


@view_group.command(name="vector")
@click.argument("x", type=click.STRING)
@click.argument("y", type=click.STRING)
@click.argument("u", type=click.STRING)
@click.argument("v", type=click.STRING)
@click.option(
    "--extrapolate",
    help="Extrapolate values outside convex hull of the data points.",
    is_flag=True,
)
@click.pass_context
def vector_command(ctx, x, y, u, v, extrapolate):
    """Plot vector field of U & V in X & Y."""
    with CliSpinner("Preparing vector field"):
        profile = ctx.obj["profile"]
        particle_data = _particle_data(profile)
        u_out = lazy.process.scatter_to_regular(
            (x, y, u), data=particle_data, extrapolate=extrapolate
        )
        v_out = lazy.process.scatter_to_regular(
            (x, y, v), data=particle_data, extrapolate=extrapolate
        )
        data = lazy.pd.merge(u_out, v_out, how="outer")
        figure, _ = lazy.plot.plot_vector(x, y, u, v, data=data)
        figure.canvas.set_window_title(f"PtvPy: Vector field {[u, v]} in {[x, y]}")
        return figure
