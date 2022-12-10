"""Environment management for different executor."""

from .instance import Instance


def init():
    """Initialize the environment."""
    Instance()


__all__ = ["init"]
