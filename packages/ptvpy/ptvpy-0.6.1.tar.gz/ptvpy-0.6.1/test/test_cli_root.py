"""Test the Command line interface of PtvPy."""


import os
import time
import re

import pytest
import pandas as pd
import matplotlib.pyplot as plt
from numpy.testing import assert_allclose
from scipy.io import loadmat

from ptvpy.errors import ProfileError
from ptvpy.io import hash_arrays, FrameLoader
from ptvpy import _cli_root


plt.ion()  # Enable interactive mode, so that plotting doesn't block


def test_basic_workflow(tmpdir, runner):
    """Test the basic workflow using the command line.

    Notes
    -----
    For some reason `hash_files` doesn't return a persistent hash between test
    runs. Hashing the generated TIFF-files will yield a different hash every
    time even though the hash of the loaded frames is persistent.

    Furthermore when comparing the processing results the distribution of
    particle numbers seems to fluctuate. However the summary (see
    `pandas.DataFrame.describe`) of all other columns is persistent within a
    relative tolerance of 1e-7.
    """
    os.chdir(tmpdir)

    # Generate synthetic images (supply image-nr with prompt)
    result = runner("generate lines --seed 42 -- data/ 20")
    assert result.exit_code == 0
    for i in range(20):
        assert os.path.isfile(f"data/image_{i:0>2}.tiff")
    frames = FrameLoader(str(tmpdir) + "/data/*.tiff").lazy_frame_sequence()
    assert hash_arrays(frames) == "2fe12b049eda0a3c6d7e555eb635d9d5e5c169a0"

    # Create a profile file
    result = runner("profile create", input="data/image_*.tiff")
    assert result.exit_code == 0
    assert os.path.isfile("profile.ptvpy.toml")

    # And check
    result = runner("profile check")
    assert result.exit_code == 0
    assert "contains a valid profile" in result.output

    # Process images
    result = runner("process")
    assert result.exit_code == 0
    assert os.path.isfile("storage.ptvpy.hdf5")

    # View images
    result = runner("view summary scatter3d x size v")
    assert result.exit_code == 0

    # Export data
    result = runner("export data.csv")
    assert result.exit_code == 0

    # Check exported data
    exported = pd.read_csv("data.csv")
    assert exported.shape == (317, 14)
    assert exported["frame"].unique().size == 20
    assert exported["particle"].unique().size == 17

    # Canary to detect subtle changes (doesn't actually test correctness)
    # Created with print(np.array(exported[["y", "x", "v"]].describe([])).tolist())
    assert_allclose(
        exported[["y", "x", "v"]].describe([]),
        [
            [317.0, 317.0, 300.0],
            [86.242_254_371_042_35, 97.143_176_117_153_4, 2.019_970_314_665_066_7],
            [52.103_957_904_146_74, 53.033_270_874_143_35, 0.032_304_834_224_797_48],
            [8.953_187_485_297_576, 6.007_376_444_553_724, 1.956_812_380_206_148_8],
            [88.029_623_238_423_92, 92.843_195_266_272_2, 2.001_455_956_308_703_3],
            [193.446_366_782_006_86, 194.508_241_137_954_4, 2.094_400_047_382_338_3],
        ],
    )


def test_export(full_project, runner):
    """Basic tests for export command."""
    assert runner("export test.csv").exit_code == 0
    assert os.path.isfile("./test.csv")
    data = pd.read_csv("./test.csv")
    assert data.shape == (321, 14)

    assert runner("export test.xlsx").exit_code == 0
    assert os.path.isfile("./test.xlsx")

    assert runner("export test.mat").exit_code == 0
    assert os.path.isfile("./test.mat")
    data = loadmat("./test.mat")
    assert len(data.keys()) == 16  # + 3 meta variables
    for key, value in data.items():
        if key.startswith("_"):
            continue
        assert value.size == 321

    assert runner("export test.sqlite").exit_code == 0
    assert os.path.isfile("./test.sqlite")


def test_force_profile_option(full_project, runner):
    """Check that the --force-profile option does what it promises."""
    with open("profile.ptvpy.toml", "a") as stream:
        # Add an unsupported option that won't break anything but would fail
        # validation
        stream.write("\nunkown_option = true\n")

    result = runner("profile check")
    assert "unknown field" in result.stdout

    result = runner("process --step diff")
    assert result.exit_code == 1
    assert "only found invalid profile(s)" in result.exception.args[0]
    # Using force option should run the command without error
    result = runner("process --force-profile --step diff")
    assert result.exit_code == 0

    result = runner("view summary")
    assert result.exit_code == 1
    assert "only found invalid profile(s)" in result.exception.args[0]
    # Using force option should run the command without error
    result = runner("view --force-profile summary")
    assert result.exit_code == 0

    result = runner("export particles.csv")
    assert result.exit_code == 1
    assert "only found invalid profile(s)" in result.exception.args[0]
    # Using force option should run the command without error
    result = runner("export --force-profile particles.csv")
    assert result.exit_code == 0


class Test_CliSpinner:
    class FakeError(Exception):
        pass

    def test_animated(self, capsys):
        spinner = _cli_root.CliSpinner("animated", animated=True)
        with spinner:
            time.sleep(0.3)
        stdout, stderr = capsys.readouterr()
        assert re.match(r"animated: [/\-\\|\b ]+done", stdout)

        spinner = _cli_root.CliSpinner("animated", animated=True)
        try:
            with spinner:
                time.sleep(0.3)
                raise self.FakeError()
        except self.FakeError:
            pass
        stdout, stderr = capsys.readouterr()
        assert re.match(r"animated: [/\-\\|\b ]+failed", stdout)

    @pytest.mark.parametrize("argument", [None, False])
    def test_not_animated(self, capsys, argument):
        spinner = _cli_root.CliSpinner("not animated", animated=argument)
        with spinner:
            pass
        stdout, stderr = capsys.readouterr()
        assert "not animated: ...working... done" in stdout

        spinner = _cli_root.CliSpinner("not animated", animated=argument)
        try:
            with spinner:
                raise self.FakeError()
        except self.FakeError:
            pass
        stdout, stderr = capsys.readouterr()
        assert "not animated: ...working... failed" in stdout


def test_main(capsys, monkeypatch):
    """Test PtvPy's main method."""
    # Normal usage
    with pytest.raises(SystemExit) as exc_info:
        _cli_root.main(args=["--version"])
    stdout, stderr = capsys.readouterr()
    assert exc_info.value.code == 0
    assert "version" in stdout

    # With debug mode
    with monkeypatch.context() as m:
        m.setitem(os.environ, "PTVPY_DEBUG", "1")
        with pytest.raises(ProfileError, match="auto-detection was not successful"):
            _cli_root.main(args=["process"])

    # and without debug mode
    with monkeypatch.context() as m:
        m.delitem(os.environ, "PTVPY_DEBUG")
        assert _cli_root.main(args=["process"]) == 1
    stdout, stderr = capsys.readouterr()
    assert "Error: auto-detection was not successful" in stderr
    assert "Traceback" not in stderr
