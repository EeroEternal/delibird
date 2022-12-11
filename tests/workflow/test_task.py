"""Task tests."""

from delibird.workflow import task, Plan
from delibird.context import init
from delibird.execute import Single, Concurrent

# init instance
init()
worker = Single()


# pylint: disable=invalid-name
@task(name="test", worker=worker)
def plus(a, b):
    """Test function."""
    return a + b


# pylint: disable=invalid-name
# test same name in instance, will warn
# UserWarning: Job with name test already exists
@task(name="test_again")
def plus_again(a, b):
    """Test function."""
    return a + b


def test_task():
    """Test task."""
    assert plus(1, 2) == 3
    assert plus_again(2, 3) == 5

    # multiprocess worker
    multi_worker = Concurrent(processes=2)

    plan = Plan(worker=multi_worker)
    plan.add_task(plus, 1, 2)
    plan.add_task(plus, 4, 5)
    result = plan()
    assert result == [3, 9]
