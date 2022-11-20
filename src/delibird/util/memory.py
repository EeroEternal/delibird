"""Analysis host memory"""

import psutil
import sys
import math

from multiprocessing import cpu_count


def avaliable_memory():
    """Avaliable memory"""
    pc_mem = psutil.virtual_memory()
    return pc_mem.available


def analysis_data_memory(example_dict_list, virtual_size):
    """Analysis memory cost of list of dict"""
    example_dict = example_dict_list[0]
    virtual_dict_list = [example_dict for i in range(virtual_size)]
    list_mem = sys.getsizeof(virtual_dict_list)
    dict_mem = deep_getsizeof_dict(example_dict)
    return list_mem + (dict_mem * virtual_size), dict_mem


def deep_getsizeof_dict(example_dict):
    """Analysis memory cost of dict"""
    dict_mem = sys.getsizeof(example_dict)
    member_mem = 0
    for k in example_dict.keys():
        member_mem += sys.getsizeof(k)
        member_mem += sys.getsizeof(example_dict[k])
    return dict_mem + member_mem


def simple_batch_size(example_dict_list, virtual_batch_size):
    """Analysis a safe pool size simply"""
    mem_adjust_factor = 1.2
    heap_pointer_mem = 8
    mem_saver_factor = 0.9

    avaliable_mem = avaliable_memory()

    # simply calsulate a safe batch size which would't cause OutOfMemoryErro
    safe_batch_mem = math.ceil(avaliable_mem * mem_saver_factor / cpu_count())

    # analysis size of sample list and single data in the sample list
    example_mem, single_data_mem = analysis_data_memory(example_dict_list, virtual_batch_size)

    # memory not overflow, just return old size
    if ((example_mem * mem_adjust_factor) < safe_batch_mem):
        return virtual_batch_size

    # calculate a new size
    # 8: heap_pointer_mem
    # old_mem - offset_size * single_data_mem - offset_size * 8 = safe_new_mem
    # old_mem - offset_size * (single_data_mem + 8) = safe_new_mem
    # old_mem - safe_new_mem = offset_size * (single_data_mem + 8)
    # offset_size = (old_mem - safe_new_mem) / (single_data_mem + 8)
    offset_batch_size = math.ceil((example_mem - safe_batch_mem / mem_adjust_factor) / (single_data_mem + heap_pointer_mem))
    safe_batch_size = virtual_batch_size - offset_batch_size
    return safe_batch_size 
