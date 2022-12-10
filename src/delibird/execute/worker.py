"""Worker module."""
from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods
class Worker(ABC):
    """Worker is an execute unit that executes jobs"""

    def __init__(self):
        pass

    @abstractmethod
    def run(self, executor, parameters=None):
        """Run worker.

        Args:
            executor: job or workflow to be executed
            parameters: parameters of the job or workflow. default is None
        """
        # check if job or workflow

        # if instance is 'job' type, run this job
