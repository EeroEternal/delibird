"""Multiprocess worker module."""
from ..workflow import Plan, Task
from .worker import Worker


# pylint: disable=too-few-public-methods
class Multiprocess(Worker):
    """Multiprocess worker is a worker that executes jobs in multiprocess"""

    def run(self, executor, parameters=None):
        """Run multiprocess worker.

        Args:
            executor: job or workflow to be executed
            parameters: parameters of the job or workflow
        """
        # check if job or workflow

        # if instance is 'job' type, run this job
        if isinstance(executor, Task):
            executor()

        # if workflow, run workflow
        if isinstance(executor, Plan):
            for job in executor.jobs:
                job(parameters)
