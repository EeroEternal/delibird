"""Analysis host memory"""

import math
import sys
from multiprocessing import cpu_count

import psutil


def calculate_size(list_data, batch_size):
    """Analysis a safe pool size simply.

    Args:
        list_data (dict): dict item. e.g {"sec_code":"000001", "date":"2020-01-01"}
        batch_size (int): batch size

    Returns:
        int: safe pool size
    """
    # get available memory
    # [Memory](https://psutil.readthedocs.io/en/latest/)
    # available: the memory that can be given instantly to processes
    # without the system going into swap
    available = psutil.virtual_memory().available

    # check if None
    if not available:
        return batch_size

    # safe memory must less than available memory. "0.8" is a magic number
    safe_memory = math.ceil(available * 0.8 / cpu_count())

    # calculate size of list_data with batch_size
    # batch_size is in "getsizeof"
    possible_memory = sys.getsizeof(list_data) * batch_size

    # if possible_memory is less than safe_memory, return batch_size
    if possible_memory < safe_memory:
        return batch_size

    # calculate a safe batch size. "0.6" is a magic number
    safe_batch_size = math.ceil(safe_memory / sys.getsizeof(list_data)) * 0.6

    return int(safe_batch_size)
