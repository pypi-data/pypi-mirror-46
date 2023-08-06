"""Test cli_profile module."""


import os
from pathlib import Path

from ptvpy import _profile


def test_help_option(runner):
    """Test "-h" and "--help" option for all view commands."""
    commands = ["", "create", "check", "edit", "show"]
    for cmd in commands:
        result = runner(f"profile {cmd} -h")
        assert result.exit_code == 0
        result = runner(f"profile {cmd} --help")
        assert result.exit_code == 0


class Test_create_command:
    """Test behavior of the `ptvpy profile create` command."""

    default_pattern = "path/to/dataset/*.tiff"

    @staticmethod
    def _same_as_template(path):
        with open(_profile.profile_template_path(), "r") as stream:
            template = stream.read()
        with open(path, "r") as stream:
            created = stream.read()
        assert created == template

    def test_prompt_invalid(self, runner, tmp_path):
        """Test behavior for prompts that don't match."""
        os.chdir(tmp_path)

        # Check in empty directory and repeat prompt a second time
        result = runner("profile create", input=f"foo\ny\n{self.default_pattern}\nn")
        assert result.exit_code == 0
        self._same_as_template("profile.ptvpy.toml")

        # Try to create a second time
        result = runner("profile create", input="baz\nn")
        # ... which should fail
        assert result.exit_code != 0
        assert "already exists" in result.exception.args[0]
        # ... and kept the previous profile
        self._same_as_template("profile.ptvpy.toml")

    def test_profile_option(self, runner, tmp_path):
        """Check behavior if the "--profile" option is used."""
        os.chdir(tmp_path)

        # Create with default name
        result = runner("profile create", input="foo\nn")
        assert result.exit_code == 0
        assert os.path.isfile("profile.ptvpy.toml")

        # Creating another one with different name should work
        result = runner("profile create -p hidden", input=f"{self.default_pattern}\nn")
        assert result.exit_code == 0
        self._same_as_template("hidden")

        # ... but should fail a second time
        result = runner("profile create --profile hidden", input="bar\nn")
        assert result.exit_code != 0
        assert "already exists" in result.exception.args[0]
        self._same_as_template("hidden")

    def test_pattern_option(self, runner, tmp_path):
        """Check behavior if the "--pattern" option is used."""
        os.chdir(tmp_path)

        # Empty directory, so pattern is wrong
        result = runner(f"profile create --pattern '{self.default_pattern}'")
        assert result.exit_code == 1
        assert "Pattern is not valid" in result.exception.args[0]
        assert len(os.listdir(".")) == 0

        # Create matching file
        Path(self.default_pattern).parent.mkdir(parents=True)
        with open(self.default_pattern.replace("*", "image"), "x") as stream:
            stream.write("dummy")
        # and repeat with existing file
        result = runner(f"profile create --pattern '{self.default_pattern}'")
        assert result.exit_code == 0

        # Validate content of file
        self._same_as_template("profile.ptvpy.toml")


def test_check_command(runner, fresh_project):
    """Test behavior of the `ptvpy profile check` command."""
    # Prepare test directories
    _profile.create_profile_file("1_valid.ptvpy.toml", "*.tiff")
    _profile.create_profile_file("2_invalid.ptvpy.toml", "invalid.tiff")
    with open("4_empty.ptvpy.toml", "x"):
        pass  # Create empty file
    with open("5_invalid_toml.ptvpy.toml", "x") as stream:
        stream.write("src_files: 1: 2")  # Create file with invalid toml
    with open("6_unrelated.toml", "x") as stream:
        stream.write("src_files: '*.tiff'")  # Create unrelated toml file
    # Subdirectory with 2 profiles (1 valid, 1 invalid)
    sub_dir_a = fresh_project / "sub_a"
    sub_dir_a.mkdir()
    _profile.create_profile_file("sub_a/7_parent.ptvpy.toml", "../*.tiff")
    _profile.create_profile_file("sub_a/8_local.ptvpy.toml", "*.tiff")
    # Empty Subdirectory
    sub_dir_b = fresh_project / "sub_b"
    sub_dir_b.mkdir()

    # Check current directory
    result = runner("profile check")
    assert result.exit_code == 0
    assert "'profile.ptvpy.toml' contains a valid profile" in result.stdout
    assert "'1_valid.ptvpy.toml' contains a valid profile" in result.stdout
    assert "'2_invalid.ptvpy.toml' violates rule(s):" in result.stdout
    assert "'4_empty.ptvpy.toml' is empty" in result.stdout
    assert "'5_invalid_toml.ptvpy.toml' is not a valid TOML file:" in result.stdout
    assert "6_unrelated.toml" not in result.stdout

    # Check subdirectory (from parent)
    result = runner("profile check --dir sub_a")
    assert result.exit_code == 0
    assert "'sub_a/8_local.ptvpy.toml' contains a valid profile" in result.stdout
    assert "'sub_a/7_parent.ptvpy.toml' violates rule(s):" in result.stdout
    assert "1_valid.ptvpy.toml" not in result.stdout

    # Check subdirectory (from inside)
    os.chdir("sub_a")
    result = runner("profile check")
    assert result.exit_code == 0
    assert "'7_parent.ptvpy.toml' contains a valid profile" in result.stdout
    assert "'8_local.ptvpy.toml' violates rule(s):" in result.stdout
    assert "1_valid.ptvpy.toml" not in result.stdout

    # Check parallel directory
    result = runner("profile check --dir ../sub_b")
    assert result.exit_code == 0
    assert "No matching files found with pattern" in result.stdout
