"""Analysis host memory"""

import psutil
import sys
import math


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
    return list_mem + (dict_mem * virtual_size)


def deep_getsizeof_dict(example_dict):
    """Analysis memory cost of dict"""
    dict_mem = sys.getsizeof(example_dict)
    member_mem = 0
    for k in example_dict.keys():
        member_mem += sys.getsizeof(k)
        member_mem += sys.getsizeof(example_dict[k])
    return dict_mem + member_mem


def simple_safe_size(example_dict_list, virtual_size):
    """Analysis a safe pool size simply"""
    avaliable_mem = avaliable_memory()
    example_mem = analysis_data_memory(example_dict_list, virtual_size) * 1.2
    safe_size = math.ceil(avaliable_mem * 0.85 / example_mem)
    return safe_size 
