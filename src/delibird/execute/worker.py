"""Worker module."""
from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods
class Worker(ABC):
    """Worker is an execute unit that executes jobs"""

    def __init__(self):
        pass

    @abstractmethod
    def run(self, execute_job):
        """Run worker.

        Args:
            execute_job: job or workflow to be executed
        """
        # check if job or workflow

        # if instance is 'job' type, run this job
