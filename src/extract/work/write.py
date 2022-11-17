"""Write to parquet file or directory from database."""
import uuid
from itertools import repeat
from multiprocessing import Pool
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from delibird.database import create_arrow_schema, db, table_exist
from delibird.util import show


def write_directory(directory, dsn, table_name, engine="postgresql", batch_size=1024 * 1024):
    """Write parquet directory from database.

    Args:
        directory (str): directory name for parquet files
        dsn (dsn): database connect string
        table_name (str): table name
        batch_size (int): write batch size
    """
    # connect database
    conn = db.connect(engine, dsn)
    if not conn:
        print("connect failed")
        return False

    # get table count
    cursor = conn.cursor()
    cursor.execute(f"select count(*) from {table_name}")
    row = cursor.fetchone()
    count = row[0]
    conn.close()

    # get columns schema from database table
    schema = create_arrow_schema(engine, dsn, table_name)

    if not schema:
        print("create schema failed")
        return False

    # split count according to batch size
    record_index = list(range(count // batch_size))
    record_range = list(zip(record_index, repeat(batch_size)))

    if count % batch_size:
        record_range.append((len(record_index), count % batch_size))

    # check directory exist.
    # keep directory exist and no files in it
    path = Path(directory)
    if not path.exists():
        path.mkdir(parents=True)
    else:
        if not path.is_dir():
            path.unlink()
        else:
            # remove directory and files
            for file_obj in path.iterdir():
                file_obj.unlink()

    # add work to multiprocessing pool
    with Pool() as pool:
        pool.starmap(
            range_write_parquet,
            zip(
                repeat(directory),
                repeat(engine),
                repeat(dsn),
                repeat(schema),
                repeat(table_name),
                record_range,
            ),
        )

    return True


def range_write_parquet(directory, engine, dsn, schema, table_name, record_range):
    """Write parquet file from database.

    Args:
        directory (str): directory name for parquet files
        dsn (str): database connection string
        schema (pyarrow.schema): pyarrow schema
        table_name (str): database table name
        record_range (tuple): record range
    """
    # connect database
    conn = db.connect(engine, dsn)
    if not conn:
        print("connect failed")
        return False

    # get record according to record range
    cursor = conn.cursor(dict_row_flag=True)
    index, count = record_range
    if engine == "postgresql":
        cursor.execute(f"select * from {table_name} limit {count} offset {index * count}")
    elif engine == "oracle":
        cursor.execute(f"select * from {table_name} where rownum <= {count} "\
            "and rownum > {index * count}")
        cursor.rowfactory = \
            lambda *args: dict(zip([d[0] for d in cursor.description], args))
    records = cursor.fetchall()

    # random create filename
    filename = uuid.uuid4().hex + ".parquet"

    # get batch from table
    batch = pa.RecordBatch.from_pylist(mapping=records, schema=schema)

    # write to parquet file
    with pq.ParquetWriter(Path(directory) / filename, schema) as writer:
        writer.write_batch(batch)

    return True


def write_parquet(filepath, dsn, table_name, engine="postgresql", batch_size=1024 * 1024):
    """Write data to parquet from database.

    Args:
        filepath (str): filename with path
        dsn (str): database connection string
        table_name (str): database table name
        batch_size (int, optional): write batch size. Defaults to 1024*1024.
    """
    # connect database
    conn = db.connect(engine, dsn)
    if not conn:
        print("connect failed")
        return False

    # check if table exist
    if not table_exist(conn, table_name):
        return False

    # create schema
    schema = create_arrow_schema(engine, dsn, table_name)
    show(schema)
    # batch get and write to parquet file
    cursor = conn.cursor(dict_row_flag=True)
    offset = 0

    # check file exist
    path = Path(filepath)

    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    path.touch(exist_ok=True)

    # write to parquet file
    with pq.ParquetWriter(filepath, schema) as writer:
        while True:
            if engine == "postgresql":
                cursor.execute(
                    f"select * from {table_name} limit {batch_size} offset {offset}"
                )
            elif engine == "oracle":
                cursor.execute(
                    f"select * from {table_name} where rownum <= {batch_size} and rownum > {offset}"
                )
                cursor.rowfactory = \
                    lambda *args: dict(zip([d[0] for d in cursor.description], args))
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break

            # rows to py table
            batch = pa.RecordBatch.from_pylist(mapping=rows, schema=schema)
            writer.write_batch(batch)

            # refresh offset
            offset += batch_size

    # clean up
    cursor.close()
    conn.close()

    return True
