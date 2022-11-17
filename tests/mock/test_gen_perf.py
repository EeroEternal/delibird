"""Test generate performance."""

import timeit
from itertools import repeat
from multiprocessing import cpu_count
from multiprocessing.pool import Pool

import pytest

from delibird.mock.gen import gen_dict, gen_dict_one
from delibird.util.show import show

# from memory_profiler import profile


ALL_COUNT = 204800
CHUNK_SIZE = 2048

COLUMNS_DEF = {
    # stock code as a type
    "sec_code": "code",  # "600001"
    "date": "date",  # 2022-08-24
    "close": "float",  # 16.87
    "open": "float",  # 16.65
    "high": "float",  # 16.95
    "low": "float",  # 16.55
    "hold": "decimal(10,5)",  # 123.25515
    # datetime.datetime(2022,10,25).timestamp()
    "time": "timestample(unit=s,tz=Asia/Shanghai)",
    "volume": "int",  # 1530231
    "amount": "int",  # 2571196416
}

PARAM_LIST = [(COLUMNS_DEF, ALL_COUNT)]


@pytest.mark.parametrize("columns, count", PARAM_LIST)
def test_loop(columns, count):
    """Imap test.

    Args:
        columns (dict): columns's define. e.g {"sec_code":"string, "date":"date"}
        count (int): numbers of list
    """
    # create and configure the process pool
    start = timeit.default_timer()

    # loop is too long
    show(f"loop is too long ,ignore {count} set 1")
    result = gen_dict(columns, 1)

    end = timeit.default_timer()

    show(f"test loop success:{len(result)}, time:{end-start}")


# @profile
@pytest.mark.parametrize("columns, count", PARAM_LIST)
def test_map(columns, count):
    """Imap test.

    Args:
        columns (dict): columns's define. e.g {"sec_code":"string, "date":"date"}
        count (int): numbers of list
    """
    # create and configure the process pool
    start = timeit.default_timer()

    # cpu count
    cpu = cpu_count()

    if cpu > 1:
        cores = cpu - 1
    else:
        cores = cpu

    with Pool(processes=cores) as pool:
        result = pool.map(gen_dict_one, repeat(columns, count))

    end = timeit.default_timer()
    show(f"test map success:{len(result)}, time:{end-start}")


@pytest.mark.parametrize("columns, count", PARAM_LIST)
def test_map_chunk(columns, count):
    """Imap test.

    Args:
        columns (dict): columns's define. e.g {"sec_code":"string, "date":"date"}
        count (int): numbers of list
    """
    # create and configure the process pool
    start = timeit.default_timer()

    # cpu count
    cpu = cpu_count()

    if cpu > 1:
        cores = cpu - 1
    else:
        cores = cpu

    with Pool(processes=cores) as pool:
        result = pool.map(gen_dict_one, repeat(columns, count), chunksize=CHUNK_SIZE)

    end = timeit.default_timer()
    show(f"test map chunk success:{len(result)}, time:{end-start}")


@pytest.mark.parametrize("columns, count", PARAM_LIST)
def test_imap_unorder(columns, count):
    """Imap test.

    Args:
        columns (dict): columns's define. e.g {"sec_code":"string, "date":"date"}
        count (int): numbers of list
    """
    # create and configure the process pool
    start = timeit.default_timer()

    # cpu count
    cpu = cpu_count()

    if cpu > 1:
        cores = cpu - 1
    else:
        cores = cpu

    with Pool(processes=cores) as pool:
        result = list(pool.imap_unordered(gen_dict_one, repeat(columns, count)))

    end = timeit.default_timer()
    show(f"test imap unordered success:{len(result)}, time:{end-start}")


@pytest.mark.parametrize("columns, count", PARAM_LIST)
def test_imap(columns, count):
    """Imap test.

    Args:
        columns (dict): columns's define. e.g {"sec_code":"string, "date":"date"}
        count (int): numbers of list
    """
    # create and configure the process pool
    start = timeit.default_timer()

    # cpu count
    cpu = cpu_count()

    if cpu > 1:
        cores = cpu - 1
    else:
        cores = cpu

    with Pool(processes=cores) as pool:
        result = list(pool.imap(gen_dict_one, repeat(columns, count)))

    end = timeit.default_timer()
    show(f"test imap success:{len(result)}, time:{end-start}")


@pytest.mark.parametrize("columns, count", PARAM_LIST)
def test_map_async(columns, count):
    """Imap test.

    Args:
        columns (dict): columns's define. e.g {"sec_code":"string, "date":"date"}
        count (int): numbers of list
    """
    # create and configure the process pool
    start = timeit.default_timer()

    # cpu count
    cpu = cpu_count()

    if cpu > 1:
        cores = cpu - 1
    else:
        cores = cpu

    with Pool(processes=cores) as pool:
        result = pool.map_async(gen_dict_one, repeat(columns, count)).get()

    end = timeit.default_timer()

    show(f"test map async success:{len(result)}, time:{end-start}")


@pytest.mark.parametrize("columns, count", PARAM_LIST)
def test_map_async_chunk(columns, count):
    """Imap test.

    Args:
        columns (dict): columns's define. e.g {"sec_code":"string, "date":"date"}
        count (int): numbers of list
    """
    # create and configure the process pool
    start = timeit.default_timer()

    # cpu count
    cpu = cpu_count()

    if cpu > 1:
        cores = cpu - 1
    else:
        cores = cpu

    with Pool(processes=cores) as pool:
        result = pool.map_async(
            gen_dict_one, repeat(columns, count), chunksize=CHUNK_SIZE
        ).get()

    end = timeit.default_timer()

    show(f"test map async chunksize success:{len(result)}, time:{end-start}")
