"""Tools for profile management."""


import pprint
import re
import glob
import traceback
from datetime import datetime
from pathlib import Path

import toml
import cerberus

from .utils import ChainedKeyMap
from .errors import ProfileError
from ._schema import SCHEMA


#: Default name used for newly created profiles.
DEFAULT_PROFILE_NAME = "profile.ptvpy.toml"

#: Pattern used to autodetect profile files.
PROFILE_PATTERN = Path("./*.ptvpy.toml")


def profile_template_path() -> Path:
    """Path to the file containing the profile template."""
    return Path(__file__).with_name("profile_template.toml")


def profile_template(parse=True):
    """Load the profile template.

    Parameters
    ----------
    parse : bool, optional
        If true parse the content of the file otherwise return the content as
        a string.

    Returns
    -------
    profile_template : ChainedKeyMap or str
        Depending on the value of `parse` either the parsed or raw content
        of the profile template.
    """
    with open(profile_template_path()) as stream:
        template = stream.read()
    if not parse:
        return template
    else:
        template = toml.loads(template)
        template = ProfileValidator(SCHEMA).normalized(template)
        return ChainedKeyMap(template)


def create_profile_file(path, image_files="", overwrite=False):
    """Create a file with the default profile at the desired location.

    Parameters
    ----------
    path : str or Path
        Specifies the folder and name of the new file.
    image_files : str, optional
        Set value of field ``image_files`` in the profile.
    overwrite : bool, optional
        If true raises a FileExistsError in case the file exists.
    """
    content = profile_template(parse=False)
    regex = r"data_files = \"(?P<path>.*)\""
    content = re.sub(regex, f'data_files = "{image_files}"', content)

    with open(path, "w" if overwrite else "x") as stream:
        stream.write(content)


def coerce_relative_path(path, working_dir="."):
    """Adjust relative paths in relation to a working directory.

    Parameters
    ----------
    path : str
        Path to ajdust if it is relative.
    working_dir : str
        When evaluating relative paths use this directory as the anchor /
        start. May be a relative directory itself. This has no effect on
        absolute paths.

    Returns
    -------
    path : str
        Potentially adjusted path.
    """
    if not Path(path).is_absolute():
        path = Path(working_dir) / path
    return str(path)


def pattern_matches(pattern, working_dir=".", no_files=None, no_dirs=None):
    """Check if a glob pattern matches.

    Parameters
    ----------
    pattern : str
        A glob like pattern. Recursive globs using "``**``" are supported.
    working_dir : str
        If `pattern` contains a relative path use this directory as the base.
        See :func:`coerce_relative_path`.
    no_files : bool, optional
        If true must match no files.
    no_dirs : bool, optional
        If true must match no directories.

    Returns
    -------
    out : bool
        Result of the evaluation.
    """
    pattern = coerce_relative_path(pattern, working_dir)
    matches = glob.glob(pattern, recursive=True)

    # Using any() allows the evaluation to return early
    if no_dirs and any(map(lambda x: Path(x).is_dir(), matches)):
        return False
    if no_files and any(map(lambda x: Path(x).is_file(), matches)):
        return False

    return len(matches) > 0


class ProfileValidator(cerberus.Validator):
    """Extended validator for profile validation and normalization.

    This class extends_ Cerberus's Validator class with new rules which are
    used in the profile schema:

    * Rule: *odd* may be ``True`` or ``False``

      - ``True``: evaluates if the number is odd.
      - ``False``: evaluates if the number is even.

    * Rule: *path* may contain one or a list of the following values:

      - "file": evaluates if a value points to a valid file.
      - "directory": evaluates if a value points to a valid directory.
      - "parent": evaluates if the value points to a file or directory
        within a valid directory (its parent).
      - "absolute": evaluates if a value is an absolute path.

    * Rule: *glob* may contain one of the following values:

      - "any": evaluates if the pattern matches at least once.
      - "no_files": evaluates if the pattern matches at least once and none of
        the matches are a file.
      - "no_dirs": evaluates if the pattern matches at least once and none of
        the matches are a directory.
      - "never": evaluates if the pattern matches never.

    Both of these are evaluated within the the working directory directory
    (see :attr:`~working_dir`).

    .. _extends: http://docs.python-cerberus.org/en/stable/customize.html
    """

    def _validate_odd(self, rule_values, field, field_value):
        """Custom rule to validate if an integer is odd.

        The rule's arguments are validated against this schema:

        {'type': 'boolean'}
        """
        is_odd = bool(field_value & 1)
        if rule_values is True and not is_odd:
            self._error(field, "must be an odd number")
        elif rule_values is False and is_odd:
            self._error(field, "must be an even number")

    def _validate_glob(self, rule_value, field, field_value):
        """Custom rule to validate strings as glob patterns.

        See class documentation for a full explanation of the rule.
        The rule's arguments are validated against this schema:

        {'type': 'string', 'allowed': ['any', 'no_files', 'no_dirs', 'never']}
        """
        if rule_value == "any":
            if not pattern_matches(field_value):
                self._error(field, "must match at least once")
        elif rule_value == "no_files":
            if not pattern_matches(field_value, no_files=True):
                self._error(field, "must match at least once and never a file")
        elif rule_value == "no_dirs":
            if not pattern_matches(field_value, no_dirs=True):
                self._error(field, "must match at least once and never a directory")
        elif rule_value == "never":
            if pattern_matches(field_value):
                self._error(field, "must never match")
        else:  # pragma: no cover
            # Should never reach this line
            raise ValueError("rule_value not supported")

    def _validate_path(self, rule_values, field, field_value):
        """Custom rule to validate strings as file system paths.

        See class documentation for a full explanation of the rule.
        The rule's arguments are validated against this schema:

        {'oneof': [{'type': 'string', 'allowed': ['file', 'directory',
        'parent', 'absolute']}, {'type': 'list', 'minlength': 1, 'schema': {
        'type': 'string', 'allowed': ['file', 'directory', 'parent',
        "absolute"]}}]}
        """
        path = Path(str(field_value))

        if isinstance(rule_values, str):
            rule_values = [rule_values]
        for rule_value in rule_values:
            if rule_value == "parent" and not path.parent.is_dir():
                self._error(
                    field, f"parent directory doesn't exist: " f"'{path.parent}'"
                )
            elif rule_value == "directory" and not path.is_dir():
                self._error(field, f"directory doesn't exist: '{path}'")
            elif rule_value == "file" and not path.is_file():
                self._error(field, f"file doesn't exist: '{path}'")
            elif rule_value == "absolute" and not path.is_absolute():
                self._error(field, f"path is not absolute: '{path}'")


def load_profile_file(path, validate=True):
    """Load a profile from the specified location.

    Parameters
    ----------
    path : str or Path
        Path to the file.
    validate : bool, optional
        If true the profile is validated after loading.

    Returns
    -------
    profile : ChainedKeyMap
        The profile found in the file.

    Raises
    ------
    ProfileError
        If the profile is not valid.
    """
    try:
        path = Path(path)
        with open(path) as stream:
            document = toml.loads(stream.read())
        if not document:
            raise ProfileError(f"'{path}' is empty")
        validator = ProfileValidator(SCHEMA)
        if validate:
            document = validator.validated(document)
        else:
            document = validator.normalized(document)
        if not document:
            raise ProfileError(
                f"'{path}' violates rule(s):\n{pprint.pformat(validator.errors)}"
            )
        return ChainedKeyMap(document)

    # Propagate ProfileErrors or reformat as such
    except toml.TomlDecodeError as error:
        raise ProfileError(f"'{path}' is not a valid TOML file:\n{error}")
    except ProfileError as error:
        raise error
    except Exception:  # pragma: no cover
        tb = traceback.format_exc()
        raise ProfileError(f"'{path}' raised an unexpected error:\n{tb}")


def find_profiles(pattern=PROFILE_PATTERN):
    """Detect profiles matching a pattern.

    Parameters
    ----------
    pattern : str or path_like, optional
        Path / glob pattern used to detect a candidates inside a directory.
        Defaults to :attr:`~PROFILE_PATTERN`.

    Returns
    -------
    valid_profiles : dict[Path, ChainedKeyMap]
        Files matching `pattern` that contain a valid profile.
    invalid_profiles : dict[Path, Error]
        Files matching `pattern` that don't contain a valid profile.
    """
    pattern = Path(pattern)
    candidates = list(pattern.parent.glob(pattern.name))
    results = {}
    for candidate in candidates:
        try:
            results[candidate] = load_profile_file(candidate)
        except ProfileError as error:
            results[candidate] = error
    valid_profiles = {
        path: result
        for path, result in results.items()
        if isinstance(result, ChainedKeyMap)
    }
    invalid_profiles = {
        path: result
        for path, result in results.items()
        if not isinstance(result, ChainedKeyMap)
    }
    return valid_profiles, invalid_profiles


def autodetect_profile(file=None, pattern=PROFILE_PATTERN, validate=True):
    """Try to find exactly one valid profile in the given directory.

    Parameters
    ----------
    file : str or path_like, optional
        Path to a profile file to open. If None, the `pattern` is used to find
        a valid profile.
    pattern : str or path_like, optional
        Path / glob pattern used to detect a valid profile inside a directory.
        Is ignored if `file` is given.
    validate : bool, optional
        If False and `file` is not None the content of the file is returned
        without validation. Autodetection ignores this argument.

    Returns
    -------
    path : str
        Path to the valid profile.
    profile : ChainedKeyMap
        The single candidate that was found matching the criteria given by
        `file` or `pattern`.

    Raises
    ------
    ProfileError
        Raised if not a single profile was found.
    """
    if file:
        # Directly load profile
        return Path(file), load_profile_file(file, validate)

    # Otherwise try to detect profile with a pattern
    valid_profiles, invalid_profiles = find_profiles(pattern)

    candidate_count = len(valid_profiles)
    if validate is False:
        candidate_count += len(invalid_profiles)

    if candidate_count == 1:
        if len(valid_profiles) == 1:
            return valid_profiles.popitem()
        # Candidate is an invalid profile, ignore error and load
        path, _ = invalid_profiles.popitem()
        return path, load_profile_file(path, validate=False)

    elif candidate_count == 0:
        if len(invalid_profiles) > 0:
            msg = (
                f"auto-detection was not successful, only found invalid "
                f"profile(s) with pattern: {pattern}"
            )
        else:
            msg = (
                f"auto-detection was not successful, no valid profile(s) "
                f"found with pattern: {pattern}"
            )
        raise ProfileError(msg)

    elif candidate_count > 1:
        raise ProfileError(
            f"auto-detection was ambiguous, found {candidate_count} "
            f"{'valid' if validate else ''} profiles"
        )
