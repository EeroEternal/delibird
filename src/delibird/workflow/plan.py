"""Plan module."""

from .task import Task


# pylint: disable=too-few-public-methods
class Plan:
    """Plan is a series of tasks with certain order"""

    def __init__(self):
        # plan is a list of jobs
        self.jobs = []

    def add_job(self, task: Task):
        """Add job to workflow"""
        self.jobs.append(task)

    def __call__(self):
        """Call workflow."""
        for job in self.jobs:
            job()
