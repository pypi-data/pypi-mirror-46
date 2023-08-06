"""Test module `ptvpy._profile`"""


import os

import pytest
import toml
from cerberus import SchemaError

from ptvpy import _profile


def test_template():
    # Test path to default profile
    assert _profile.profile_template_path().is_file()

    with open(_profile.profile_template_path()) as stream:
        template_str = stream.read()
    assert template_str == _profile.profile_template(parse=False)
    # Regression test: ensure ASCII compatibility
    template_str.encode("ascii")

    # Should be valid TOML file
    template_dict = toml.loads(template_str)

    def compare(d1, d2):
        if isinstance(d1, (list, tuple)):
            # Turn lists into dictionaries
            d1 = dict(enumerate(d1))
            d2 = dict(enumerate(d2))
        if isinstance(d1, dict):
            # Keys in d1 should be subset of d2
            assert not d1.keys() - d2.keys()
            for key in d1.keys():
                compare(d1[key], d2[key])
        else:
            assert d1 == d2

    compare(template_dict, _profile.profile_template()._dict)


def test_create_profile(tmpdir):
    # Create path to file in temporary directory
    file = tmpdir.join("profile.toml")
    # Create profile file
    _profile.create_profile_file(file.strpath)
    assert file.isfile()
    # Recreate when overwrite is False
    with pytest.raises(FileExistsError):
        _profile.create_profile_file(file.strpath)
    # Recreate when overwrite is True
    _profile.create_profile_file(
        file.strpath, image_files="path/to/dataset/*.tiff", overwrite=True
    )
    # Compare content with original file
    with open(_profile.profile_template_path()) as stream:
        assert file.read() == stream.read()


def test_load_profile(tmpdir):
    os.chdir(tmpdir)
    file = "profile.toml"
    # Create default profile in temporary directory
    _profile.create_profile_file(file, "./*.tiff")
    # Opening should fail because (implicit) validation fails for
    # the glob in the field 'data_files'
    with pytest.raises(_profile.ProfileError, match="must match at least once"):
        _profile.load_profile_file(file)
    # If we create a dummy file to satisfy the pattern...
    with open(tmpdir.join("fake.tiff"), "x"):
        pass
    # Opening should work without validation
    _profile.load_profile_file(file, validate=False)
    # Opening with validation should be successful
    profile = _profile.load_profile_file(file, validate=True)

    # Check the loaded content
    assert isinstance(profile, _profile.ChainedKeyMap)
    # Path to image files should have been replaced
    profile_str = repr(profile)
    assert "./*.tiff" in profile_str
    # But restoring the old one should yield exactly the same as template
    profile_str = profile_str.replace("./*.tiff", "path/to/dataset/*.tiff")
    assert profile_str == repr(_profile.profile_template())


class Test_ProfileValidator:
    @pytest.mark.parametrize("number", [-100, -2, 0, 10, 888])
    def test_odd_rule(self, number):
        schema = {"field": {"odd": True, "type": "integer"}}
        validator = _profile.ProfileValidator(schema)
        assert validator.validate({"field": number + 1})
        assert not validator.validate({"field": number})
        assert "must be an odd number" in str(validator.errors)

        schema = {"field": {"odd": False, "type": "integer"}}
        validator = _profile.ProfileValidator(schema)
        assert validator.validate({"field": number})
        assert not validator.validate({"field": number + 1})
        assert "must be an even number" in str(validator.errors)

        with pytest.raises(SchemaError, match="must be of boolean type"):
            _profile.ProfileValidator({"field": {"odd": "true"}})
        with pytest.raises(SchemaError, match="must be of boolean type"):
            _profile.ProfileValidator({"field": {"odd": 1}})

    def test_path_rule(self, tmpdir):
        os.mkdir(tmpdir / "image_folder")
        with open(tmpdir / "image.tiff", "x"):
            pass
        tmpdir = str(tmpdir) + "/"

        schema = {"field": {"path": "file", "type": "string"}}
        validator = _profile.ProfileValidator(schema)
        assert validator.validate({"field": tmpdir + "image.tiff"})
        assert not validator.validate({"field": tmpdir + "image_folder"})
        assert "file doesn't exist" in str(validator.errors)
        assert not validator.validate({"field": tmpdir + "not_existing"})
        assert "file doesn't exist" in str(validator.errors)

        schema = {"field": {"path": "directory", "type": "string"}}
        validator = _profile.ProfileValidator(schema)
        assert validator.validate({"field": tmpdir + "image_folder"})
        assert not validator.validate({"field": tmpdir + "image.tiff"})
        assert "directory doesn't exist" in str(validator.errors)
        assert not validator.validate({"field": tmpdir + "not_existing"})
        assert "directory doesn't exist" in str(validator.errors)

        schema = {"field": {"path": "parent", "type": "string"}}
        validator = _profile.ProfileValidator(schema)
        assert validator.validate({"field": tmpdir + "image_folder"})
        assert validator.validate({"field": tmpdir + "image.tiff"})
        assert validator.validate({"field": tmpdir + "not_existing"})
        assert not validator.validate({"field": tmpdir + "not_existing/*"})
        assert "parent directory doesn't exist" in str(validator.errors)

        schema = {"field": {"path": "absolute", "type": "string"}}
        validator = _profile.ProfileValidator(schema)
        assert validator.validate({"field": tmpdir + "image_folder"})
        assert validator.validate({"field": tmpdir + "image.tiff"})
        assert not validator.validate({"field": "."})
        assert "path is not absolute" in str(validator.errors)

        schema = {"field": {"path": "absolute", "type": "string"}}
        validator = _profile.ProfileValidator(schema)
        assert validator.validate({"field": tmpdir + "image_folder"})
        assert validator.validate({"field": tmpdir + "image.tiff"})
        assert not validator.validate({"field": "."})
        assert "path is not absolute" in str(validator.errors)

        schema = {"field": {"path": ["file", "directory"], "type": "string"}}
        validator = _profile.ProfileValidator(schema)
        assert not validator.validate({"field": tmpdir + "image_folder"})
        assert "file doesn't exist" in str(validator.errors)
        assert not validator.validate({"field": tmpdir + "image.tiff"})
        assert "directory doesn't exist" in str(validator.errors)

        with pytest.raises(SchemaError, match="unallowed value folder"):
            _profile.ProfileValidator({"field": {"path": "folder"}})
        with pytest.raises(SchemaError, match="min length is 1"):
            _profile.ProfileValidator({"field": {"path": []}})

    def test_glob_rule(self, tmpdir):
        os.mkdir(tmpdir / "image_folder")
        with open(tmpdir / "image.tiff", "x"):
            pass
        tmpdir = str(tmpdir) + "/"

        schema = {"field": {"glob": "any", "type": "string"}}
        error_msg = "must match at least once"
        validator = _profile.ProfileValidator(schema)
        assert validator.validate({"field": tmpdir + "image*"})
        assert validator.validate({"field": tmpdir + "image_folder"})
        assert validator.validate({"field": tmpdir + "image.tiff"})
        assert not validator.validate({"field": tmpdir + "image_folder/*"})
        assert error_msg in str(validator.errors)
        assert not validator.validate({"field": tmpdir + "not_existing"})
        assert error_msg in str(validator.errors)

        schema = {"field": {"glob": "no_files", "type": "string"}}
        error_msg = "must match at least once and never a file"
        validator = _profile.ProfileValidator(schema)
        assert validator.validate({"field": tmpdir + "image_*"})
        assert not validator.validate({"field": tmpdir + "image*"})
        assert error_msg in str(validator.errors)

        schema = {"field": {"glob": "no_dirs", "type": "string"}}
        error_msg = "must match at least once and never a directory"
        validator = _profile.ProfileValidator(schema)
        assert validator.validate({"field": tmpdir + "image.*"})
        assert not validator.validate({"field": tmpdir + "image*"})
        assert error_msg in str(validator.errors)

        schema = {"field": {"glob": "never", "type": "string"}}
        error_msg = "must never match"
        validator = _profile.ProfileValidator(schema)
        assert validator.validate({"field": tmpdir + "*/*"})
        assert validator.validate({"field": tmpdir + "not_existing"})
        assert not validator.validate({"field": tmpdir + "image.*"})
        assert error_msg in str(validator.errors)
        assert not validator.validate({"field": tmpdir + "image_*"})
        assert error_msg in str(validator.errors)
        assert not validator.validate({"field": tmpdir + "image*"})
        assert error_msg in str(validator.errors)

        with pytest.raises(SchemaError, match="unallowed value all"):
            _profile.ProfileValidator({"field": {"glob": "all"}})
        with pytest.raises(SchemaError, match="must be of string type"):
            _profile.ProfileValidator({"field": {"glob": False}})
