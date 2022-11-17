"""Test read parquet."""

import os
import timeit
from itertools import repeat
from multiprocessing import cpu_count
from multiprocessing.pool import Pool

import pyarrow.compute as pc
import pyarrow.parquet as pq
import pytest


@pytest.mark.parametrize(
    "filepath", [("datasets/mock_data/dir/39119f8ce8c9441b96867c3e4e56bb76.parquet")]
)
def test_read_one(filepath):
    """Test read one parquet."""
    # -------------
    start = timeit.default_timer()
    # read paruqet
    table = pq.read_table(filepath)
    end = timeit.default_timer()
    print(f"\rread table, time:{end-start}")

    # -------------
    start = timeit.default_timer()
    # read paruqet
    parquet_file = pq.ParquetFile(filepath)
    table = parquet_file.read()
    end = timeit.default_timer()
    print(f"\rparquet file, time:{end-start}")

    # -------------
    start = timeit.default_timer()
    expr = pc.field("sec_code") == "600677"
    table.filter(expr)
    end = timeit.default_timer()
    print(f"\rfilter file, time:{end-start}")


@pytest.mark.parametrize("directory", [("datasets/mock_data/dir")])
def test_dir_query(directory):
    """Test query directory."""
    start = timeit.default_timer()

    # loop directory and read parquet
    for filename in os.listdir(directory):
        if filename.endswith(".parquet"):
            # join file path
            filepath = os.path.join(directory, filename)

            # read parquet file
            parquet_file = pq.ParquetFile(filepath)
            table = parquet_file.read()
            # filter
            expr = pc.field("sec_code") == "600601"
            filter_table = table.filter(expr)

            print(f"filter {filename}:{filter_table.num_rows}")

    end = timeit.default_timer()
    print(f"\rall time:{end-start}")


@pytest.mark.parametrize("directory", [("datasets/mock_data/dir")])
def test_query_par(directory):
    """Test query directory parallel."""
    start = timeit.default_timer()

    # multiprocess starmap
    with Pool(processes=cpu_count()) as pool:
        pool.starmap(query_parquet, zip(repeat(directory), os.listdir(directory)))

    end = timeit.default_timer()
    print(f"\rall time:{end-start}")


def query_parquet(directory, filename):
    """Query parquet.

    Args:
        directory (dir): directory
        filename (str): file
    """
    # loop directory and read parquet
    # join file path
    filepath = os.path.join(directory, filename)

    # read parquet file
    parquet_file = pq.ParquetFile(filepath)
    table = parquet_file.read()

    # filter
    expr = pc.field("sec_code") == "600601"
    filter_table = table.filter(expr)

    print(f"filter {filename}:{filter_table.num_rows}")
