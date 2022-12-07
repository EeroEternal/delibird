"""Global registry for context objects."""

from .context import Context


# pylint: disable=too-few-public-methods
class Registry(Context):
    """Global registry for context objects."""

    # As class attribution, used as global variable?
    # _instance is a dict. key is type name ,value is a list
    # with all instances of this type.
    # like {type[T], [T, T, T]}, T is some type
    _instances: {}

    def __init__(self):
        """Initialize the registry."""
        self._registry = {}

    def add(self, context):
        """Add a context to the registry."""
        self._instances[type(context)].append(context)

    def get_instances(self, object_type):
        """Get all instances with the given type.

        Args:
            object_type: type of the object
        """
        # get all type and instance from _instances
        # Check type if subclass of given type
        # return all instances with given type
        return \
            [instance for type_, instance in self._instances.items()
             if issubclass(type_, object_type)]

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
