"""Test cli_view module.

Currently the tests in this module are very basic and only check if the given
command will execute successfully (exit code of 0).

Uses fixtures in "test/conftest.py".
"""


import os

import pytest
import matplotlib.pyplot as plt


# Check if the tests are run in continuous integration (used to skip certain tests)
running_ci = bool(os.environ.get("CI"))

plt.ion()  # Enable interactive mode, so that plotting doesn't block

# Add fixtures used implicitly in all functions
pytestmark = pytest.mark.usefixtures("close_plots")


@pytest.mark.usefixtures("static_full_project")
class TestStatic:
    """Test subcommands in a way that doesn't require modifying the project."""

    def test_help_option(self, runner):
        subcommands = [
            "",  # Test view command itself
            "histogram",
            "map",
            "relationship",
            "scatter3d",
            "slideshow",
            "subpixel",
            "summary",
            "trajectories",
            "vector",
            "slideshow",
        ]
        for cmd in subcommands:
            result = runner(f"view {cmd} -h")
            assert result.exit_code == 0
            result = runner(f"view {cmd} --help")
            assert result.exit_code == 0

    def test_background(self, runner):
        result = runner("view background")
        assert result.exit_code == 0
        assert len(plt.get_fignums()) == 1

    def test_histogram(self, runner):
        result = runner("view histogram x")
        assert result.exit_code == 0
        result = runner("view histogram --kde y")
        assert result.exit_code == 0
        assert len(plt.get_fignums()) == 2

    def test_map(self, runner):
        result = runner("view map x y v")
        assert result.exit_code == 0
        result = runner("view map --extrapolate x y v")
        assert result.exit_code == 0
        assert len(plt.get_fignums()) == 2

    @pytest.mark.skipif(
        running_ci,
        reason="Doesn't work with SVG backend which is used in CI. Raises an "
        "AttributeError: 'FigureCanvasAgg' object has no attribute 'manager' "
        "Figure.show works only for figures managed by pyplot, normally "
        "created by pyplot.figure().",
    )
    def test_relationship(self, runner):
        result = runner("view relationship size mass")
        assert result.exit_code == 0
        assert len(plt.get_fignums()) == 1

    def test_scatter3d(self, runner):
        result = runner("view scatter3d x y v")
        assert result.exit_code == 0
        result = runner("view scatter3d --color size x y v")
        assert result.exit_code == 0
        assert len(plt.get_fignums()) == 2

    def test_slideshow(self, runner):
        result = runner("view slideshow")
        assert result.exit_code == 0
        result = runner("view slideshow --autostart")
        assert result.exit_code == 0
        result = runner("view slideshow --no-annotation")
        assert result.exit_code == 0
        assert len(plt.get_fignums()) == 3

    def test_subpixel(self, runner):
        result = runner("view subpixel")
        assert result.exit_code == 0
        assert len(plt.get_fignums()) == 1

    def test_summary(self, runner):
        result = runner("view summary")
        assert result.exit_code == 0

    def test_trajectories(self, runner):
        result = runner("view trajectories")
        assert result.exit_code == 0
        result = runner("view trajectories --names dx dy")
        assert result.exit_code == 0
        assert len(plt.get_fignums()) == 2

    def test_vector(self, runner):
        result = runner("view vector x y dx dy")
        assert result.exit_code == 0
        result = runner("view vector --extrapolate x y dx dy")
        assert result.exit_code == 0
        assert len(plt.get_fignums()) == 2

    def test_chained_commands(self, runner):
        result = runner("view summary scatter3d --color size x y v slideshow")
        assert result.exit_code == 0
        assert len(plt.get_fignums()) == 2


def test_profile_option(runner, full_project):
    os.rename("profile.ptvpy.toml", "profile.hidden")
    # Verify auto-detection fails
    result = runner("view slideshow")
    assert result.exit_code != 0
    assert "auto-detection was not successful" in result.exception.args[0]
    # ... and works if profile is specified
    result = runner("view --profile profile.hidden slideshow")
    assert result.exit_code == 0
