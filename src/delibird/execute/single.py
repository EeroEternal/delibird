"""Single process execution mode."""
from .worker import Worker


# pylint: disable=too-few-public-methods
class Single(Worker):
    """Multiprocess worker is a worker that executes jobs in multiprocess"""

    def run(self):
        """Run multiprocess worker."""
        # execute plan
        result = []
        for plan in self._plans:
            for task in plan.tasks:
                # execute task
                func = task[0]
                args = task[1]
                kwargs = task[2]
                result.append(func(*args, **kwargs))

        # clean worker
        self.clean()

        # return result
        return result
