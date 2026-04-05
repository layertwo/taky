from importlib.metadata import PackageNotFoundError, version

from . import cot  # noqa: F401

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"
