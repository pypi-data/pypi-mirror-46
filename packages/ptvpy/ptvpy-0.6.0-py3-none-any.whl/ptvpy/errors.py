"""Application specific errors."""


class PtvPyError(Exception):
    """A general application specific error."""

    pass


class ProfileError(PtvPyError):
    """An error related to a profile validation or parsing."""

    pass
