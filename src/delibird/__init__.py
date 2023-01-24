"""delibird init file."""

from delibird import util

__all__ = ["util"]

from . import _version
__version__ = _version.get_versions()['version']
