"""Job base class."""
import warnings
from contextvars import copy_context

from uuid import uuid4

from ..context import Instance
from ..util import get_parameters


# pylint: disable=too-few-public-methods
class Task:
    """Job definition.

    Job is a simple work. like read parquet file, write to database.
    To preserve the input and output types,
    """

    def __init__(self, func, name: str = None, context=None):
        """Initialize Job.

        Args:
            func: function to be run
            name: name of the workflow. default is None
            context: context of the Job. default is None
        """
        # job name must be unique
        if not name:
            # generate random name
            self.name = uuid4().hex
        else:
            self.name = name

        # function to be run
        self.func = func

        # job worker to run func
        self.worker = None

        # set job context
        if context is None:
            # copy current context
            self._context = copy_context()
        else:
            # set given context
            self._context = context

        # get global instance manager
        instance = Instance.get()

        if not instance:
            raise RuntimeError("No global instance manager found in context")

        # check if it has same name job in instance manager
        if any(isinstance(item, Task)
               for item in instance.get_instances(task)
               if item.name == self.name
               ):
            warnings.warn(f"Job with name {self.name} already exists")

        # register job instance to instance manager
        instance.register(self)

    def set_worker(self, worker):
        """Set worker for job."""
        self.worker = worker

    def __call__(self, *args, **kwargs):
        """Call workflow."""
        # if worker is set, send job to worker
        if self.worker:
            parameters = get_parameters(self.func)
            self.worker.run(self, parameters)

        # if worker is not set, run in current process
        if self.func:
            return self.func(*args, **kwargs)

        # no function to run
        raise RuntimeError("No function to run")


def task(func=None, name=None):
    """Decorator for job."""
    if func:
        return Task(func, name)

    return lambda function: Task(function, name)
