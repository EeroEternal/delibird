"""More flexible multiprocess pool."""
import os
import queue


# pylint: disable=too-few-public-methods
class Pool:
    """Multiprocess pool."""

    def __init__(self, process_number=None):
        """Initialize multiprocess pool.

        Args:
            process_number: number of processes in the pool. default is None
        """
        self._pool = []

        # task queue for processes to get
        self._taskqueue = queue.SimpleQueue()

        # The _change_notifier queue exist to wake up self._handle_workers()
        # when the cache (self._cache) is empty or when there is a change in
        # the _state variable of the thread that runs _handle_workers.
        self._change_notifier = queue.SimpleQueue()

        # process number
        self._process_number = process_number or os.cpu_count() or 1
