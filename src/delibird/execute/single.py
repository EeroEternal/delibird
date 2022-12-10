"""Single execution mode."""
from ..workflow import Plan, Task
from .worker import Worker


# pylint: disable=too-few-public-methods
class Single(Worker):
    """Multiprocess worker is a worker that executes jobs in multiprocess"""

    def run(self, executor, *args, **kwargs):
        """Run multiprocess worker.

        Args:
            executor: job or workflow to be executed
            args: args of the job or workflow
            kwargs: kwargs of the job or workflow
        """
        # if instance is 'job' type, run this job
        if isinstance(executor, Task):
            executor(args, kwargs)

        # if workflow, run workflow
        if isinstance(executor, Plan):
            # execute plan
            for job in executor.jobs:
                job(args, kwargs)
