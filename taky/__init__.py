from importlib.metadata import PackageNotFoundError, version

from . import cot

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"
