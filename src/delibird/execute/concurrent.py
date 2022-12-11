"""Multiprocess worker module."""
from multiprocessing import Pool, cpu_count

from .worker import Worker


# pylint: disable=too-few-public-methods
class Concurrent(Worker):
    """Multiprocess worker is a worker that executes tasks in multiprocess"""

    def __init__(self, processes=None):
        """Initialize multiprocess worker.

        Args:
            processes: number of processes to be used
        """
        super().__init__()

        self.processes = processes
        if processes is None:
            self.processes = cpu_count() - 1

        # pylint: disable=consider-using-with
        self._pool = Pool(processes=self.processes)

    def run(self):
        """Run multiprocess worker."""

        # map run plan
        result = []
        for plan in self._plans:
            result.append(self._pool.starmap(run_func, plan.tasks))

        # terminal pool
        self._pool.close()


def run_func(func, args, kwargs):
    """Run func with args and kwargs."""
    return func(*args, **kwargs)
