"""Generate data."""

from itertools import repeat
from multiprocessing import cpu_count
from multiprocessing.pool import Pool

from .map import map_value


def gen_dict_one(schema):
    """Generate one dict from column's.

    Args:
        schema (dict): column's schema. e.g {"sec_code":"string", "date":"date"}

    Returns:
        dict: generate dict

    """
    # new dict for map result
    dict_value = {}

    # item is schema's key, schema is a dict type
    for item in schema:
        dict_value[item] = map_value(schema[item])

    return dict_value


def gen_dict_seq(schema, count, chunk_size=1024):
    """Generate iterator use generator.

    Args:
        schema (dict): column's schema
        count (int): number of list
        chunk_size (int, optional): chunk size. Defaults to 1024.

    Returns:
        dict iterator

    """
    for i in range(0, count, chunk_size):
        # last chunk size may be less than chunk_size
        actual_chunk_size = min(chunk_size, count - i)

        # generate data
        dict_data = gen_dict(schema, actual_chunk_size)

        yield dict_data


def gen_dict_list(schema, count, batch_size, chunk_size=None):
    """Generate dict type list.

    Args:
        schema (dict): column's schema. e.g {"sec_code":"string, "date":"date"}
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
                gen_dict_one, repeat(schema, sub_count), chunksize=chunk_size
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


def gen_dict(schema, count):
    """Generate dict.

    Args:
        schema (dict): column's schema. e.g {"sec_code":"string, "date":"date"}
        count (int): numbers of list

    Returns:
        list: dict list. e.g [{"sec_code":"600001", "count": 20},{"sec_code":"600001", "count": 25}]

    """
    dict_list = []
    for _ in range(0, count):
        dict_list.append(gen_dict_one(schema))

    return dict_list
