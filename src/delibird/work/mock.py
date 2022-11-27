"""Mock work."""
import uuid
from itertools import repeat
from multiprocessing import cpu_count
from multiprocessing.pool import Pool
from pathlib import Path
from alive_progress import alive_bar

import pyarrow as pa
import pyarrow.parquet as pq
import math

from delibird.database import db, insert_list, table_by_arrow, table_exist
from delibird.mock import gen_dict, gen_dict_list, gen_list_list, schema_from_dict
from delibird.util import show, simple_batch_size


def write_table(engine, dsn, table_name, schema, row_number):
    """Mock data and write to table.

    Args:
        dsn (str): database connect string
        table_name (str): table name
        schema (schema): parquet schema
        row_number (int): row number
    """
    #start bra
    with alive_bar(math.ceil(row_number/batch_size)) as bar:

        # connect database
        conn = db.connect(engine, dsn)
        if not conn:
            show("connect failed")
            return False

        # convert to arrow schema
        arrow_schema = schema_from_dict(schema)

        # check if table exists
        if not table_exist(conn, table_name):
            # create table
            table_by_arrow(conn, table_name, arrow_schema)

        # insert data
        batch_size = 1024 * 1024

        # batch copy data to database table by COPY protocol
        for i in range(0, row_number, batch_size):
            if i + batch_size > row_number:
                number = row_number - i
            else:
                number = batch_size

            # generate data
            dict_data = gen_list_list(engine, schema, number)

            # write to table
            insert_list(dict_data, conn, table_name)
            
            #show bar
            bar()

        # close connection
        conn.close()
        
 

    return True


def write_parquet(filepath, columns, row_number, batch_size=1024 * 1024):
    """Mock data, Write to parquet file.

    Args:
        filepath (str): file path
        columns (dict): columns
        row_number (int): row number
        batch_size (int, optional): batch size. Defaults to 1024*1024.
    """
    #start bra
    with alive_bar(1) as bar:

        # arrow schema
        arrow_schema = schema_from_dict(columns)

        # generate data as dict
        # dict_list = gen_dict_list(columns, row_number, batch_size)

        # check file exist
        path = Path(filepath)

        if not path.parent.exists():
            path.parent.mkdir(parents=True)

        path.touch(exist_ok=True)

        # write to parquet file
        # offset = 0
        # length = len(dict_list)
        with pq.ParquetWriter(filepath, schema=arrow_schema) as writer:
            # while True:
            for dict_list in gen_dict_list(columns, row_number, batch_size):
                # count batch size
                # if offset + batch_size > length:
                    # count = length - offset
                # else:
                    # count = batch_size

                # write batch
                batch = pa.RecordBatch.from_pylist(
                    # mapping=dict_list[offset:(offset+count)], schema=arrow_schema
                    mapping=dict_list, schema=arrow_schema
                )
                writer.write_batch(batch)

                # check if write finish
                # if offset + batch_size > length:
                    # break

                # refresh offset
                # offset += batch_size
        #show bar
        bar()

    show('write parquet finished')
    return True


def write_directory(directory, columns, row_number, batch_size=1024 * 1024):
    """Mock write to parquet file.

    Args:
        directory (str): directory name
        columns (dict): columns
        row_number (int): row number
        batch_size (int): write batch size
    """
    #start bra
    with alive_bar(1) as bar:

        # adjust a reasonable batch_size which would not cause an OutOfMemoryError
        sample_dict_list = gen_dict(columns, 1)
        safe_batch_size = simple_batch_size(sample_dict_list, min(row_number, batch_size))
        
        with Pool(processes=cpu_count()) as pool:
            # multiprocess starmap
            # init batch number list
            record_list = [safe_batch_size for _ in range(row_number // safe_batch_size)]
            if row_number % safe_batch_size:
                record_list.append(row_number % safe_batch_size)

            # map write
            pool.starmap(batch_write, zip(repeat(columns), repeat(directory), record_list))
            
        #When pool end show bar
        bar()

    show('write directory finished')
    return True


def batch_write(columns, directory, record_number):
    """Batch write to parquet file.

    Args:
        columns (dict): columns
        directory (str): directory name
        record_number (int): record number
    """
    # root directory
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)

    # arrow schema
    arrow_schema = schema_from_dict(columns)

    # generate data as dict
    dict_list = gen_dict(columns, record_number)

    # init file name and parquet writer
    file_name = uuid.uuid4().hex + ".parquet"
    with pq.ParquetWriter(root / file_name, schema=arrow_schema) as writer:

        # write to parquet file
        record_batch = pa.RecordBatch.from_pylist(mapping=dict_list, schema=arrow_schema)
        writer.write_batch(record_batch)
