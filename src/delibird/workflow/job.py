"""Job base class."""
import warnings
from ..context import Registry


# pylint: disable=too-few-public-methods
@Registry.register
class Job:
    """Job definition.

    Job is a simple work. like read parquet file, write to database.
    To preserve the input and output types,
    """
    def __init__(self, func, name: str = None):
        """Initialize Job.

        Args:
            func: function to be run
            name: name of the workflow. default is None
        """
        self.name = name
        self.func = func

        # Get registry from current context
        registry = Registry.get()

        if not registry:
            raise RuntimeError("No registry found in context")

        # todo: Check if item has name?
        if any(isinstance(item, Job)
               for item in registry.get_instances(Job)
                if item.name == self.name
               ):
            warnings.warn(f"Job with name {self.name} already exists")


    def __call__(self, *args, **kwargs):
        """Call workflow."""
        # todo: add different runner
        return self.func(*args, **kwargs)


def job(func=None, name: str = None):
    """Decorator for workflow."""
    return Job(func, name)
