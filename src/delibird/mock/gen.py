"""Generate data."""


from itertools import repeat
from multiprocessing import cpu_count
from multiprocessing.pool import Pool

from .map import map_value


def gen_dict_one(columns):
    """Generate one dict from column's.

    Args:
        columns (dict): column's define

    Returns:
        dict: generate dict

    """
    dict_value = {}
    for col in columns:
        dict_value[col] = map_value(columns[col])

    return dict_value


def gen_dict_seq(columns, count, chunk_size=1024):
    """Generate iterator use generator.

    Args:
        columns (dict): column's define
        count (int): number of list
        chunk_size (int, optional): chunk size. Defaults to 1024.

    Returns:
        dict iterator

    """
    for i in range(0, count, chunk_size):
        # last chunk size may be less than chunk_size
        actual_chunk_size = min(chunk_size, count - i)

        # generate data
        dict_data = gen_dict(columns, actual_chunk_size)

        yield dict_data


def gen_dict_list(columns, count, batch_size, chunk_size=None):
    """Generate dict type list.

    Args:
        columns (dict): column's define. e.g {"sec_code":"string, "date":"date"}
        count (int): numbers of list
        chunk_size (int, optional): chunk size. Default None

    Returns:
        list: dict list. e.g [{"sec_code":"600001", "count": 20},{"sec_code":"600001", "count": 25}]

    """
    offset = 0
    cpu = cpu_count()

    if cpu > 1:
        cores = cpu - 1
    else:
        cores = cpu

    while True:
        # count batch size
        if offset + batch_size > count:
            sub_count = count - offset
        else:
            sub_count = batch_size

        with Pool(processes=cores) as pool:
            result = pool.map_async(
                gen_dict_one, repeat(columns, sub_count), chunksize=chunk_size
            ).get()

        # check if write finish
        if offset + batch_size > count:
            break

        # refresh offset
        offset += batch_size

        yield result


def gen_list_list(engine, columns, count):
    """Generate list's list.

    Args:
        engine (str): database engine
        columns (list): column's define. e.g ["string", "date"]
        count (int): numbers of list
    Returns:
        list: list list. e.g [["600001", "2020-01-01"], ["600001", "2020-01-01"]]
    """
    list_data = []
    for _ in range(0, count):
        if engine in ["postgresql", "mysql"]:
            list_value = []
            for col in columns:
                list_value.append(map_value(columns[col]))
        elif engine == "oracle":
            list_value = {}
            for col in columns:
                list_value[col] = map_value(columns[col])

        list_data.append(list_value)

    return list_data


def gen_dict(columns, count):
    """Generate dict.

    Args:
        columns (dict): column's define. e.g {"sec_code":"string, "date":"date"}
        count (int): numbers of list

    Returns:
        list: dict list. e.g [{"sec_code":"600001", "count": 20},{"sec_code":"600001", "count": 25}]

    """
    dict_list = []
    for _ in range(0, count):
        dict_list.append(gen_dict_one(columns))

    return dict_list
