"""Job base class."""

from typing import (
    TypeVar,
    Generic,
    Callable,
    ParamSpec,
    cast
)
from functools import partial

# Generic type var for capturing the inner return type of async funcs
T = TypeVar("T")
# The return type of the user's function
R = TypeVar("R")
# The parameters of the job
P = ParamSpec("P")


# pylint: disable=too-few-public-methods
class Job(Generic[P, R]):
    """Job definition.

    Job is a simple work. like read parquet file, write to database.
    To preserve the input and output types,
    we use the generic type variables P and R for "Parameters"
    """

    def __init__(self, func: Callable[P, R], name: str = None):
        """Initialize Job."""
        self.name = name
        self.func = func

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        """Call job."""
        return self.func(*args, **kwargs)


def job(func: Callable[P, R], name: str = None):
    """Job decorator.

    Args:
        func (Callable): function
        name (str): job name

    Returns:
        Callable[ [Callable[[ParamSpec("P")], R]], Job[ParamSpec("P"), R]] | Job[ P, R]
    """
    if func:
        return cast(Job[P, R], Job(func, name))

    return cast(Callable[[Callable[P, R]], Job[P, R]], partial(job, name=name))
