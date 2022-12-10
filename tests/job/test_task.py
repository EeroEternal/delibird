"""Job tests."""

from delibird.workflow import task
from delibird.context import init

# init instance
init()


# pylint: disable=invalid-name
@task(name="test")
def func(a, b):
    """Test function."""
    return a + b


def test_task():
    """Test task."""
    assert func(1, 2) == 3
