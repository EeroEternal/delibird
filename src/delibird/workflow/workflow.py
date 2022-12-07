"""Workflow module."""


# pylint: disable=too-few-public-methods
class Workflow:
    """Workflow is a series of jobs with certain order"""

    def __init__(self):
        # plan is a list of jobs
        self.jobs = []

    def add_job(self, job):
        """Add job to workflow"""
        self.jobs.append(job)

    def __call__(self):
        """Call workflow."""
        for job in self.jobs:
            job()
