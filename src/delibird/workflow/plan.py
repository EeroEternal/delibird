"""Plan module."""

import warnings
from uuid import uuid4

from contextvars import copy_context

from ..context import Instance


# pylint: disable=too-few-public-methods
class Plan:
    """Plan is a series of tasks with certain order"""

    def __init__(self, name=None, worker=None, context=None):
        """Initialize plan.

        Args:
            name: name of the plan. default is None
            worker: worker to run the plan. default is None
            context: context of the plan. default is None
        """
        # plan is a list of tasks, task is defined in a function
        # plan type is a tuple of (task, args, kwargs)
        self._tasks = []

        if not name:
            # generate random name
            self._name = uuid4().hex
        else:
            self._name = name

        # task worker to run func
        self._worker = worker
        if self._worker:
            self._worker.add(self)

        # set task context
        if context is None:
            # copy current context
            self._context = copy_context()
        else:
            # set given context
            self._context = context

        # get global instance manager
        instance = Instance.get()

        if not instance:
            raise RuntimeError("No global instance manager found in context")

        # check if it has same name Plan in instance manager
        # get items with Plan type
        for item_list in instance.get_instances(Plan):
            for item in item_list:
                if item.name == self._name:
                    warnings.warn(f"plan or task with name {self._name} already exists")

        # register task instance to instance manager
        instance.add(self)

    @property
    def name(self):
        """Get plan name."""
        return self._name

    def add_task(self, func, *args, **kwargs):
        """Add task to plan.

        Args:
            func: task to be added
            args: args of task
            kwargs: kwargs of task
        """
        self._tasks.append((func, args, kwargs))

    @property
    def tasks(self):
        """Get tasks.

        Returns:
            list: tasks
        """
        return self._tasks

    def set_worker(self, worker):
        """Set worker for plan."""
        self._worker = worker

    def __call__(self):
        """Call plan."""
        # check tasks
        if len(self._tasks) == 0:
            raise RuntimeError("No tasks in plan")

        # check worker
        result = []
        if not self._worker:
            # run in single process
            for task in self._tasks:
                func = task[0]
                arg = task[1]
                kwarg = task[2]
                result.append(func(*arg, **kwarg))
        else:
            # run in worker
            print('run in worker')
            result = self._worker.run()
            print(f'result: {result}')

        # return result. if only one ,return one
        if len(result) == 1:
            return result[0]
        return result
