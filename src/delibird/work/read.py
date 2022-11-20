"""Read parquet file and write to database."""

from itertools import repeat
from multiprocessing import Pool
from pathlib import Path

import pyarrow.parquet as pq
import math
from alive_progress import alive_bar

from delibird.database import create_table_by_schema, db, insert_batch, table_exist


def read_parquet(filepath, dsn, table_name, engine="postgresql"):
    """Read parquet file and write to database.

    Args:
        filepath (str): filename with path
        dsn (str): data source name
        table_name (str): table name
    """

    #start load bra
    with alive_bar(2, dual_line=True, title='load parquet') as barload:

        # check file exist
        path = Path(filepath)
        if path.exists() is False:
            print(f"file not exist: {filepath}")
            return None

        if path.is_file() is False:
            print(f"not a file: {filepath}")
            return False

        if path.suffix != '.parquet':
            print(f"not a parquet file: {filepath}")
            return None

        # check table exist
        create_table_if_not_exist(filepath, engine, dsn, table_name)
        barload()

        # batch read parquet file by row group
        parquet_file = pq.ParquetFile(filepath)
        barload()


    for i in range(parquet_file.num_row_groups):
        #start read bar
        with alive_bar(1, dual_line=True,title='read parquet') as barread:
            # read row group
            row_group = parquet_file.read_row_group(i)
            
            #read readparquet
            barread()

        # write row group to database
        read_row_group(row_group, engine, dsn, table_name)
                

    return True


def read_row_group(row_group, engine, dsn, table_name, batch_size=1024 * 100):
    """Read parquet row group and write to database.

    Args:
        row_group (pyarrow.Table): parquet row group
        dsn (str): data source name
        table_name (str): table name
        batch_size (int): batch size
    """
    #start write bar
    with alive_bar(math.ceil(row_group.num_rows/batch_size), dual_line=True, title='write database') as barwrite:

        # connection
        conn = db.connect(engine, dsn)
        if not conn:
            return None

        # batch insert data to table
        for i in range(0, row_group.num_rows, batch_size):
            count = batch_size

            # avoid take out of bounds
            if i + batch_size > row_group.num_rows:
                count = row_group.num_rows - i

            # get batch
            batch = row_group.slice(i, count)

            # write batch to database
            insert_batch(batch, conn, table_name)
            
            #show write
            barwrite()

        # clean up
        conn.close()

    return True


def read_directory(directory, dsn, table_name, engine="postgresql"):
    """Read parquet file and write to database parrallel.

    Args:
        directory (str): directory name
        dsn (str): data source name
        table_name (str): table name
    """
    # check directory exist
    path = Path(directory)
    if path.exists() is False:
        print(f"directory not exist: {directory}")
        return None

    if path.is_dir() is False:
        print(f"not a directory: {directory}")
        return False

    # get file in directory
    files = [file for file in path.iterdir() if file.is_file() and file.suffix == '.parquet']
    if len(files) == 0:
        print("no parquet file in directory: {directory}")
        return None

    # check table exist
    create_table_if_not_exist(files[0], engine, dsn, table_name)

    # read parquet file
    with Pool() as pool:
        pool.starmap(read_parquet, zip(files, repeat(engine), repeat(dsn), repeat(table_name)))

    return True


def create_table_if_not_exist(filepath, engine, dsn, table_name):
    """Create table if it's not existed

    Args:
        table_name (str): table name
        filepath (str): parquet file path
    """
    # connection
    conn = db.connect(engine, dsn)
    if not conn:
        return False

    if not table_exist(conn, table_name):
        # get schema from parquet file
        parquet_file = pq.ParquetFile(filepath)
        if not parquet_file:
            print(f"open file failed: {filepath}")
            return False

        # read row group from paruqet file to get schema
        row_group = parquet_file.read_row_group(0)

        # get schema
        arrow_schema = row_group.schema

        # create table
        create_table_by_schema(conn, table_name, arrow_schema)

    # clean up
    conn.close()
