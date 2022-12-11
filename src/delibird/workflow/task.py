"""Task base class."""

from .plan import Plan


# pylint: disable=too-few-public-methods
class Task(Plan):
    """Task definition.

    Task is a simple work. like read parquet file, write to database.
    To preserve the input and output types,
    Task is also a plan, which has only one task.
    """

    def __init__(self, func, name=None, worker=None, context=None):
        """Initialize task.

        Args:
            func: function to be run
            name: name of the task. default is None
            worker: worker to run the task. default is None
            context: context of the Task. default is None
        """
        # rewrite __init__,so need invoke super().__init__
        super().__init__(name, worker, context)

        # set task function
        self._func = func

    def __call__(self, *args, **kwargs):
        """Run task.

        Args:
            args: args of the task
            kwargs: kwargs of the task
        """
        # run task
        self.add_task(self, *args, **kwargs)

        # call super to run task
        return super().__call__()

    @property
    def func(self):
        """Get task function."""
        return self._func


def task(func=None, name=None, worker=None):
    """Decorator for task.

    Args:
        func: function to be run
        name: name of the task. default is None
        worker: worker to run the task. default is None
    """
    if func:
        return Task(func, name, worker=worker)

    return lambda function: Task(function, name, worker)
