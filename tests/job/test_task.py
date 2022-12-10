"""Job tests."""

from delibird.workflow import task
from delibird.context import init
from delibird.execute import Single

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
    print(f'plus:{type(plus)}')
    assert plus(1, 2) == 3
    assert plus_again(2, 3) == 5
