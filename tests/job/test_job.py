"""Job tests."""

from delibird.job import job


# pylint: disable=invalid-name
@job
def func(a, b):
    """Test function."""
    return a + b


def test_job():
    """Test job."""
    assert func(1, 2) == 3
