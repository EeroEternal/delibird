"""Multiprocess worker module."""
from multiprocessing import Pool, cpu_count

from .worker import Worker


# pylint: disable=too-few-public-methods
class Multiprocess(Worker):
    """Multiprocess worker is a worker that executes tasks in multiprocess"""

    def __init__(self, processes=None):
        """Initialize multiprocess worker.

        Args:
            processes: number of processes to be used
        """
        super().__init__()

        if processes is None:
            self.processes = cpu_count() - 1

    def run(self):
        """Run multiprocess worker."""
        # check if workflow or workflow

        # todo: add multiprocess pool
        # if workflow, run workflow
        # with Pool(self.processes) as pool:
        #     pool.starmap(executor, parameters)
        #     for job in executor.tasks:
        #             job(parameters)
