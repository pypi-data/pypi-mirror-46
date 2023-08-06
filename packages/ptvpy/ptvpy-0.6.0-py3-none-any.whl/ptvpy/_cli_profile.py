"""Command-group `profile` with subcommands."""


from pathlib import Path

import click

from .errors import PtvPyError
from ._cli_root import root_group, profile_option
from ._profile import (
    pattern_matches,
    create_profile_file,
    autodetect_profile,
    find_profiles,
    PROFILE_PATTERN,
    DEFAULT_PROFILE_NAME,
)


@root_group.group(name="profile")
def profile_group(**kwargs):
    """Manage profiles.

    This subcommand allows the creation, manipulation and validation of
    profiles. A profile is stored inside a TOML file and tells PtvPy how to
    process or handle a given data set. Only profiles that validate
    successfully against a schema are used.

    Many subcommands of PtvPy are able to autodetect profile files ending with
    ".ptvpy.toml" in the current working directory if no file is
    given explicitly with the "--profile" option.
    """
    pass


@profile_group.command(name="create")
@click.option(
    "-p",
    "--profile",
    help="Create a profile at the given path. Otherwise use default name and "
    "create inside the current directory.",
    type=click.STRING,
    default="profile.ptvpy.toml",
)
@click.option(
    "--pattern",
    type=click.STRING,
    help="A pattern matching the image files to process. If not provided, you "
    "will be prompted.",
)
def create_command(**kwargs):
    """Create a new profile."""
    # Use default name if not supplied
    path = Path(kwargs["profile"] or DEFAULT_PROFILE_NAME)
    if path.is_file():
        raise FileExistsError(f"already exists: {path}")

    pattern = kwargs["pattern"]
    if pattern and not pattern_matches(pattern, working_dir=path.parent, no_dirs=True):
        raise PtvPyError("\nPattern is not valid!")
    elif pattern is None:
        click.echo(
            "\nPlease specify a glob pattern matching the image files to process.\n"
            "Relative paths are *always* interpreted from the directory of the\n"
            "profile file."
        )
        for _ in range(99):
            pattern = click.prompt("Pattern")
            # Pattern must be valid from profile directory
            if pattern_matches(pattern, working_dir=path.parent, no_dirs=True):
                break
            click.echo("Warning: Pattern is not valid!")
            if not click.confirm("Try again?", default=True):
                break
        else:
            raise RuntimeError("Reached 99 prompts! Aborting.")

    create_profile_file(path, pattern)
    click.echo(f"\nCreated '{path}'")


@profile_group.command(name="check")
@click.option(
    "--dir",
    help="Specify the directory to check. If not given the current one chosen.",
    type=click.Path(exists=True, file_okay=False),
)
def check_command(**kwargs):
    """Check for valid profiles in a directory."""
    if kwargs["dir"]:
        pattern = Path(kwargs["dir"]) / PROFILE_PATTERN.name
    else:
        pattern = PROFILE_PATTERN

    valid, invalid = find_profiles(pattern)
    if not valid and not invalid:
        click.echo(f"\nNo matching files found with pattern '{pattern}'")

    for path in valid.keys():
        click.echo(f"\n'{path}' contains a valid profile")
    for path, error in invalid.items():
        click.echo(f"\n{error}")

    click.echo()


@profile_group.command(name="edit")
@profile_option
def edit_command(**kwargs):
    """Edit a profile."""
    path, profile = autodetect_profile(kwargs["profile"], validate=False)
    with open(path) as stream:
        content = stream.read()
    content = click.edit(content)
    if content:
        with open(path, "w") as stream:
            stream.write(content)
        click.echo(f"Updated '{path}'")
    else:
        click.echo(f"No changes to '{path}'")


@profile_group.command(name="show")
@profile_option
def show_command(**kwargs):
    """Display profile inside the terminal."""
    path, profile = autodetect_profile(kwargs["profile"], validate=False)
    with open(path) as stream:
        click.echo_via_pager(stream.read())
