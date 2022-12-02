"""Analysis host memory"""

import math
import sys
from multiprocessing import cpu_count

import psutil


def available_memory():
    """Check available memory.

    Returns:
        int: available memory
    """
    pc_mem = psutil.virtual_memory()

    if pc_mem:
        return pc_mem.available

    return 0


def calculate_memory(list_data, length):
    """Analysis memory cost of list of dict.

    Args:
        list_data (list): list of dict
        length (int): length of list
    Returns:
        int: memory cost of list of dict
    """
    sample = list_data[0]

    dict_list = [sample for i in range(length)]

    list_mem = sys.getsizeof(dict_list)
    dict_mem = deep_size(sample)

    return list_mem + (dict_mem * length), dict_mem


def deep_size(sample):
    """Deep calculate size of dict.

    Args:
        sample (dict): sample dict
    Return:
        int: size of dict
    """
    # get sample size
    sample_size = sys.getsizeof(sample)

    # calculate all  size
    all_size = 0

    for k in sample:
        all_size += sys.getsizeof(k)
        all_size += sys.getsizeof(sample[k])

    return sample_size + all_size


def calculate_size(list_data, batch_size):
    """Analysis a safe pool size simply.

    Args:
        list_data (list): list of dict
        batch_size (int): batch size

    Returns:
        int: safe pool size
    """
    mem_adjust_factor = 1.2
    heap_pointer_mem = 8
    mem_saver_factor = 0.9

    available_mem = available_memory()

    # simply calculate a safe batch size which wouldn't cause OutOfMemoryErro
    safe_batch_mem = math.ceil(available_mem * mem_saver_factor / cpu_count())

    # analysis size of sample list and single data in the sample list
    example_mem, single_data_mem = calculate_memory(list_data, batch_size)

    # memory not overflow, just return old size
    if (example_mem * mem_adjust_factor) < safe_batch_mem:
        return batch_size

    # calculate a new size
    # 8: heap_pointer_mem
    # old_mem - offset_size * single_data_mem - offset_size * 8 = safe_new_mem
    # old_mem - offset_size * (single_data_mem + 8) = safe_new_mem
    # old_mem - safe_new_mem = offset_size * (single_data_mem + 8)
    # offset_size = (old_mem - safe_new_mem) / (single_data_mem + 8)
    offset_batch_size = math.ceil(
        (example_mem - safe_batch_mem / mem_adjust_factor) / (single_data_mem + heap_pointer_mem))
    safe_batch_size = batch_size - offset_batch_size
    return safe_batch_size
