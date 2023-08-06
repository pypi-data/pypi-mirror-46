"""A command line tool for particle tracking velocimetry.

You may invoke the command line interface with ``python -m ptvpy`` or directly
import functionality from this package.
"""


from ._version import get_versions

_version_info = get_versions()
__version__ = _version_info["version"]
del get_versions
