"""Job base class."""
import warnings
from contextvars import copy_context

from uuid import uuid4

from ..context import Instance


# pylint: disable=too-few-public-methods
class Task:
    """Job definition.

    Job is a simple work. like read parquet file, write to database.
    To preserve the input and output types,
    """

    def __init__(self, func, name=None, worker=None, context=None):
        """Initialize Job.

        Args:
            func: function to be run
            name: name of the workflow. default is None
            worker: worker to run the job. default is None
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
        self.worker = worker

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
        # get items with Task type
        for item_list in instance.get_instances(Task):
            for item in item_list:
                if item.name == self.name:
                    warnings.warn(f"Job with name {self.name} already exists")

        # register job instance to instance manager
        instance.add(self)

    def set_worker(self, worker):
        """Set worker for job."""
        self.worker = worker

    def __call__(self, *args, **kwargs):
        """Call workflow."""
        # if worker is set, send job to worker
        if self.worker:
            self.worker.run(self.func, *args, **kwargs)

        # if worker is not set, run in current process
        if self.func:
            return self.func(*args, **kwargs)

        # no function to run
        raise RuntimeError("No function to run")


def task(func=None, name=None, worker=None):
    """Decorator for job.

    Args:
        func: function to be run
        name: name of the workflow. default is None
        worker: worker to run the job. default is None
    """
    if func:
        return Task(func, name, worker=worker)

    return lambda function: Task(function, name, worker)
