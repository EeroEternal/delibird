"""Generate data by arrow datatype."""

from random import randint, uniform

import pyarrow as pa

from delibird.mock.code import china_code
from delibird.mock.datatype import decimal_parse, timestamp_parse
from delibird.mock.decimal import random_decimal
from delibird.mock.gen import map_date
from delibird.mock.schema import type_map
from delibird.mock.time import now_timestamp


def gen_arrays_seq(columns, count, chunk_size=1024):
    """Generate arrays.

    Args:
        columns (dict): column's define
        count (int): number of list
        chunk_size (int, optional): chunk size. Defaults to 1024.
    """
    for i in range(0, count, chunk_size):
        # last chunk size may be less than chunk_size
        actual_chunk_size = min(chunk_size, count - i)

        # generate data
        arrays = gen_arrays(columns, actual_chunk_size)

        yield arrays


def gen_arrays(columns, count):
    """Generate data from columns's define dict.

    Args:
        columns (dict): columns's define. e.g {"sec_code":"string, "date":"date"}
        count (int): numbers of list

    Returns:
        list: dict list. e.g [{"sec_code":"600001", "count": 20},{"sec_code":"600001", "count": 25}]
    """
    arrays = []
    for col in columns:
        arrays.append(gen_array(columns[col], count))

    return arrays


def gen_array(column_type, count):
    """Generate array by column's define.

    Args:
        column_name (str): column's define. e.g "string", "date", "decimal(10,2)"
        count (int): numbers of list

    Returns:
        list: array
    """
    array = []
    for _ in range(count):
        array.append(gen_data(column_type))

    arrow_array = pa.array(array, type=type_map(column_type))

    return arrow_array


def gen_data(column_type):
    """Generate data by arrow datatype.

    Args:
        column_type (str): column's define. e.g "string", "date", "decimal(10,2)"

    Returns:
        list: array
    """
    # other map to type
    maps = {
        "code": china_code("sh"),
        "date": map_date(),
        "float": uniform(0, 100),
        "int": randint(0, 100),
        "string": "hello",
    }

    if column_type.startswith("decimal"):
        precision, scale = decimal_parse(column_type)
        return random_decimal(precision, scale)

    if column_type.startswith("timestamp"):
        unit, timezone = timestamp_parse(column_type)
        return now_timestamp(unit, timezone)

    return maps[column_type]
