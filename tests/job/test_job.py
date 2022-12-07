"""Job tests."""

from delibird.workflow import job


# pylint: disable=invalid-name
@job
def func(a, b):
    """Test function."""
    return a + b


def test_job():
    """Test workflow."""
    assert func(1, 2) == 3
