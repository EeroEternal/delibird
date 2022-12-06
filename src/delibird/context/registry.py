"""Global registry for context objects."""

from .context import Context


# pylint: disable=too-few-public-methods
class Registry(Context):
    """Global registry for context objects."""

    def __init__(self):
        """Initialize the registry."""
        self._registry = {}

    def add(self, context, name="default"):
        """Add a context."""
        self._registry[name] = context

    @classmethod
    def register(cls, class_):
        """Decorator for a class.

        Add registration to the registry object on init instance
        """
        class_init = class_.__init__

        def __wrap_init__(wrap_self, *args, **kwargs):
            """Initialize the context."""

            # get the context instance
            registry = cls.get()

            # invoke wrapped class init
            class_init(wrap_self, *args, **kwargs)

            # add wrapped class instance to registry
            registry.add(wrap_self)

        # add new init to wrapper class
        class_.__init__ = __wrap_init__
        return class_


# global registry instance
GLOBAL_REGISTRY = Registry()


def init_registry():
    """Initialize the global registry."""
    global GLOBAL_REGISTRY

    # if existed, just return
    if GLOBAL_REGISTRY:
        return

    GLOBAL_REGISTRY = Registry()
