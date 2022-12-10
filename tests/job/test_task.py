"""Job tests."""

from delibird.workflow import task
from delibird.context import init

# init instance
init()


# pylint: disable=invalid-name
@task(name="test")
def plus(a, b):
    """Test function."""
    return a + b


# pylint: disable=invalid-name
# test same name in instance, will warn
# UserWarning: Job with name test already exists
@task(name="test")
def plus_again(a, b):
    """Test function."""
    return a + b


def test_task():
    """Test task."""
    assert plus(1, 2) == 3
    assert plus_again(2, 3) == 5
