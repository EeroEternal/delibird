"""Global registry for context objects."""

from .context import Context


# pylint: disable=too-few-public-methods
class Registry:
    """Global registry for context objects."""

    def __init__(self):
        """Initialize the registry."""
        self._registry = {}

    def register(self, context: Context):
        """Register a context."""
        self._registry[context.name] = context
