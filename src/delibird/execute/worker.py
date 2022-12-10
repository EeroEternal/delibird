"""Worker module."""
from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods
class Worker(ABC):
    """Worker is an execute unit that executes jobs"""

    def __init__(self):
        # plan list
        self._plans = []

    def add(self, plan):
        """Add task or plan to worker.

        Args:
            plan: task or plan. task also a plan
        """
        self._plans.append(plan)

    @abstractmethod
    def run(self):
        """Run plan list in the worker."""
