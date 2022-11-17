"""Generate data."""

import decimal
from datetime import date, datetime
from itertools import repeat
from multiprocessing import cpu_count
from multiprocessing.pool import Pool
from random import randint, uniform

from delibird.mock.code import china_code
from delibird.mock.datatype import decimal_parse, timestamp_parse
from delibird.mock.date import date_gen


def gen_dict_one(columns):
    """Generate one dict from column's.

    Args:
        columns (dict): columns'define

    Returns:
        dict: generate dict

    """
    dict_value = {}
    for col in columns:
        dict_value[col] = map_value(columns[col])

    return dict_value


def gen_dict_seq(columns, count, chunk_size=1024):
    """Generate itertor use generator.

    Args:
        columns (dict): columns's define
        count (int): number of list
        chunk_size (int, optional): chunk size. Defaults to 1024.

    Returns:
        dict itertor

    """
    for i in range(0, count, chunk_size):
        # last chunk size may be less than chunk_size
        actual_chunk_size = min(chunk_size, count - i)

        # generate data
        dict_data = gen_dict(columns, actual_chunk_size)

        yield dict_data


def gen_dict_list(columns, count, chunk_size=None):
    """Generate dict's list.

    Args:
        columns (dict): columns's define. e.g {"sec_code":"string, "date":"date"}
        count (int): numbers of list
        chunk_size (int, optional): chunk size. Default None

    Returns:
        list: dict list. e.g [{"sec_code":"600001", "count": 20},{"sec_code":"600001", "count": 25}]

    """
    cpu = cpu_count()

    if cpu > 1:
        cores = cpu - 1
    else:
        cores = cpu

    with Pool(processes=cores) as pool:
        result = pool.map_async(
            gen_dict_one, repeat(columns, count), chunksize=chunk_size
        ).get()

    return result


def gen_list_list(engine, columns, count):
    """Generate list's list.

    Args:
        columns (list): columns's define. e.g ["string", "date"]
        count (int): numbers of list
    Returns:
        list: list list. e.g [["600001", "2020-01-01"], ["600001", "2020-01-01"]]
    """
    list_data = []
    for _ in range(0, count):
        if engine == "postgresql":
            list_value = []
            for col in columns:
                list_value.append(map_value(columns[col]))
        elif engine == "oracle":
            list_value = dict()
            for col in columns:
                list_value[col] = map_value(columns[col])

        list_data.append(list_value)

    return list_data


def gen_dict(columns, count):
    """Generate dict.

    Args:
        columns (dict): columns's define. e.g {"sec_code":"string, "date":"date"}
        count (int): numbers of list

    Returns:
        list: dict list. e.g [{"sec_code":"600001", "count": 20},{"sec_code":"600001", "count": 25}]

    """
    dict_list = []
    for _ in range(0, count):
        dict_list.append(gen_dict_one(columns))

    return dict_list


def map_value(col):
    """Map type to dict value.

    Args:
        col (str): column type. e.g 'float','init'

    """
    if col.startswith("decimal"):
        return map_decimal(col)

    if col.startswith("timestamp"):
        return map_timestamp(col)

    # other map to type
    maps = {
        "code": china_code("sh"),
        "date": map_date(),
        "float": uniform(0, 100),
        "int": randint(0, 100),
        "string": "hello",
    }

    return maps[col]


def map_date():
    """Generate random date."""
    end_day = date.today()
    start_day = end_day.replace(year=end_day.year - 1)
    return date_gen(start_day, end_day)


def map_decimal(col):
    """Generate decimal with precision and scale.

    Args:
        col (str): decimal type define. e.g "decimal(10,5)"

    Returns:
        Decimal : decimal value

    """
    # python no scale define
    precision, scale = decimal_parse(col)

    # random decimal with precision and scale
    with decimal.localcontext() as ctx:
        ctx.prec = precision

        # error
        if precision < scale:
            print("precision < scale")
            return None

        # avoid randint end with 0, Decimal will less one or more
        fraction = randint(10 ** (scale - 1), 10 ** (scale) - 1)
        # pass end with 0 and 5
        while fraction % 5 == 0:
            fraction = randint(10 ** (scale - 1), 10 ** (scale) - 1)

        # return random decimal with precision and scale
        integer = randint(10 ** (precision - scale - 1), 10 ** (precision - scale) - 1)

        decimal_str = f"{integer}.{fraction}"

        decimal_result = decimal.Decimal(decimal_str)

        return decimal_result


def map_timestamp(col):
    """Generate timestamp with unit and timezone.

    Args:
        col (str): timestamp type. e.g "timestamp(s,Asia/Shanghai)"

    """
    unit, timezone = timestamp_parse(col)

    default = datetime.now(tz=timezone).timestamp()

    if unit == "ms":
        default = default * 1000

    if unit == "us":
        default = default * 1000 * 1000

    return datetime.fromtimestamp(default)
