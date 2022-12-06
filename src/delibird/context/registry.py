"""Global registry for context objects."""

from .context import Context


# pylint: disable=too-few-public-methods
class Registry(Context):
    """Global registry for context objects."""

    def __init__(self):
        """Initialize the registry."""
        self._registry = {}

    def add(self):
        """Add a context."""
        self._registry[context.name] = context


# global registry instance
GLOBAL_REGISTRY = Registry()


def init_registry():
    """Initialize the global registry."""
    global GLOBAL_REGISTRY

    # if existed, just return
    if GLOBAL_REGISTRY:
        return

    GLOBAL_REGISTRY = Registry()
