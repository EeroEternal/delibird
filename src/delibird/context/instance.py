"""Workflow instance management."""

from contextvars import ContextVar


class Instance:
    """Workflow instance management.

    used to check if the instance is already in the workflow
    or get all instances with the given type
    """

    # As class attribution, used as global variable
    # _instance is a dict. key is type name ,value is a list
    # with all instances of this type.
    # like {type[T], [T, T, T]}, T is some type
    __instances__ = {}

    # used to tag different context
    __var__: ContextVar = ContextVar("Instance")

    def __init__(self):
        """Initialize the registry."""
        # Set current instance to contextVar
        print("init instance")
        self._token = self.__var__.set(self)

    def add(self, instance_):
        """Add an instance object to the  Instance."""
        # init _instances
        if type(instance_) not in self.__instances__:
            self.__instances__[type(instance_)] = []

        self.__instances__[type(instance_)].append(instance_)

    @classmethod
    def get_instances(cls, object_type):
        """Get all instances with the given type.

        support subclass of given type

        Args:
            object_type: type of the object
        """
        # get all type and instance from _instances
        # Check type if subclass of given type
        # return all instances with given type
        return \
            [instance for type_, instance in cls.__instances__.items()
             if issubclass(type_, object_type)]

    @classmethod
    def get(cls):
        """Get the context instance."""
        return cls.__var__.get()
