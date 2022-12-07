"""Job base class."""
import warnings
from ..context import Registry
from ..util import get_parameters
from ..execute import Worker


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
        self.worker = None

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

    def set_worker(self, worker: Worker):
        """Set worker for job."""
        self.worker = worker

    def __call__(self, *args, **kwargs):
        """Call workflow."""
        # if worker is set, send job to worker
        if self.worker:
            parameters = get_parameters(self.func)

        # if worker is not set, run in current process
        return self.func(*args, **kwargs)


def job(func=None, name: str = None):
    """Decorator for workflow."""
    return Job(func, name)
