"""Root of the command line interface."""


import os
import sys
import time
import warnings
from itertools import cycle
from pathlib import Path
from threading import Event, Thread

import click

from . import __version__
from .utils import LazyImporter
from ._profile import autodetect_profile


#: Accessor for lazily loaded modules
lazy = LazyImporter(
    imports={
        "sqlite3": "sqlite3",
        "tqdm": "tqdm",
        "scipy_io": "scipy.io",
        "io": "..io",
    },
    package=__name__,
)


class CliSpinner:
    """Context manager to show a spinning icon while performing an operation.

    Parameters
    ----------
    message : str
        A message to prefix the spinner with. The string ': ' is automatically
        appended.
    animated : bool, optional
        If True, the progress indicator is animated otherwise a static message
        informs the user that the spinner was started. If None, the indicator
        is animated if the used `stream` is interactive.
    stream : io.StringIO, optional
        The text buffer to use. Defaults to `sys.stdout` if not supplied.

    Notes
    -----
    This class_ is adapted from a class in the conda package licensed under the
    BSD 3-clause License.

    Copyright (c) 2012, Continuum Analytics, Inc.

    .. _class: https://github.com/conda/conda/blob/4.5.x/conda/common/io.py#L297-L346
    """

    animated_indicator = cycle("/-\\|")
    static_indicator = "...working... "
    fail_message = "failed"
    success_message = "done"

    def __init__(self, message, animated=None, stream=None):
        self.message = message
        self.stream = sys.stdout if stream is None else stream
        self.animated = bool(animated) or self.stream.isatty()

        self._stop_running = Event()
        self._spinner_thread = Thread(target=self._start_spinning)
        self._indicator_length = len(next(self.animated_indicator)) + 1

    def start(self):
        if self.animated:
            self._spinner_thread.start()
        else:
            self.stream.write(self.static_indicator)
            self.stream.flush()

    def stop(self):
        if self.animated:
            self._stop_running.set()
            self._spinner_thread.join()

    def _start_spinning(self):
        while not self._stop_running.is_set():
            self.stream.write(next(self.animated_indicator) + " ")
            self.stream.flush()
            time.sleep(0.10)
            self.stream.write("\b" * self._indicator_length)

    def __enter__(self):
        self.stream.write(f"{self.message}: ")
        self.stream.flush()
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        if exc_type or exc_val:
            self.stream.write(self.fail_message + "\n")
        else:
            self.stream.write(self.success_message + "\n")
        self.stream.flush()


def profile_option(func):
    """Add the profile option to a command."""
    return click.option(
        "-p",
        "--profile",
        help="Use profile from the given file. If not given try to autodetect "
        'in current directory. Enter "ptvpy profile -h" for more information.',
        type=click.Path(dir_okay=False),
    )(func)


def force_profile_option(func):
    """Add the option to force a profile to a command."""
    return click.option(
        "--force-profile",
        is_flag=True,
        help="Don't validate the used profile. Use this option with care as an "
        "invalid profile can have unintended consequences.",
    )(func)


def _open_html_documentation(ctx, param, value):
    """Callback for eager option: open online documentation and exit."""
    if not value or ctx.resilient_parsing:
        # Callback is called regardless of the options value so we need to
        # do nothing and return control. See
        # https://click.palletsprojects.com/en/7.x/options/#callbacks-and-eager-options
        return
    url = "https://tud-mst.gitlab.io/ptvpy"
    click.echo(f"Opening '{url}'")
    click.launch(url, wait=False)
    ctx.exit()


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--debug",
    help="Enable debug mode (show full traceback, warnings, ...).",
    is_flag=True,
)
@click.version_option(version=__version__)
@click.option(
    "--documentation",
    is_flag=True,
    expose_value=False,
    is_eager=True,
    callback=_open_html_documentation,
    help="Open online documentation and exit.",
)
@click.pass_context
def root_group(ctx, **kwargs):
    """Command line tool for particle tracking velocimetry.

    The functionality of PtvPy is modularized into several subcommands. Call
    a subcommand with the help option "-h" to print a message with usage
    information.
    """
    if ctx.obj is None:
        ctx.obj = dict()
    if kwargs["debug"]:
        os.environ["PTVPY_DEBUG"] = "1"
    if not os.environ.get("PTVPY_DEBUG"):
        warnings.simplefilter("ignore", FutureWarning)


@root_group.command(name="export")
@click.argument("destination", type=click.Path(dir_okay=False, writable=True))
@click.option(
    "--type",
    help="Override the export type and ignore file extension if provided.",
    type=click.Choice(["csv", "xlsx", "mat", "sqlite"]),
)
@profile_option
@force_profile_option
def export_command(**kwargs):
    """Export processed data.

    Process results can be exported to different file formats with the help of
    this subcommand. A file path specifies the DESTINATION of the exported
    data. If the export format is not specified manually (see --type) PtvPy
    tries to guess the format from the file extension in DESTINATION.
    """
    _, profile = autodetect_profile(
        kwargs["profile"], validate=(not kwargs["force_profile"])
    )

    export_type = kwargs["type"] or Path(kwargs["destination"]).suffix[1:]
    export_type = export_type.lower()

    with CliSpinner("Exporting"):
        with lazy.io.HdfFile(profile["general.storage_file"]) as file:
            data = file.load_df("particles")

        if export_type == "csv":
            data.to_csv(kwargs["destination"])

        elif export_type == "xlsx":
            try:
                data.to_excel(kwargs["destination"])
            except ImportError as error:
                if "openpyxl" in error.msg:
                    print("'openpyxl' is needed for this export option")
                else:
                    raise

        elif export_type == "mat":
            mdict = {name: data[name].values for name in data}
            # Append "_" to column names which clash with builtin MATLAB symbols
            for name in ("size", "angle"):
                if name in mdict:
                    mdict[name + "_"] = mdict.pop(name)
            lazy.scipy_io.savemat(file_name=kwargs["destination"], mdict=mdict)

        elif export_type == "sqlite":
            with lazy.sqlite3.connect(kwargs["destination"]) as con:
                data.to_sql(name="ptvpy_particle_data", con=con)

        else:
            raise ValueError(f"export type '{export_type}' is not supported")

    click.echo(f"Exported to '{kwargs['destination']}'")


def main(*args, **kwargs):
    """Entry point of the application.

    Parameters
    ----------
    *args, **kwargs
        Same as `click.BaseCommand.main`.
    """
    try:
        # Raises SystemExit if no exceptions occurred, certain exceptions such
        # as KeyboardInterrupt are handled by click itself
        root_group.main(*args, **kwargs)
    except Exception as error:
        # If Debug mode is enabled, propagate the error
        if os.environ.get("PTVPY_DEBUG"):
            raise error
        # otherwise print only the error itself
        click.echo(f"\nError: {error}", err=True)
        return 1


# Import modules with subcommands which adds these implicitly to the root
# command group, do so after root_group is defined to avoid circular imports
from . import _cli_generate
from . import _cli_process
from . import _cli_profile
from . import _cli_view
