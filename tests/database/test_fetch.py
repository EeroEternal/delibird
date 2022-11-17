"""Fetch data from database."""

import click
import pyarrow as pa
import pytest

from delibird.database import db


@pytest.mark.parametrize(
    "engine, dsn, table_name",
    [
        (
            "postgresql",
            "postgresql://test:test123@localhost:5432/delibird",
            "xichou"
        ),
        (
            "oracle",
            "system/oracle@222.71.193.222:43301/xe",
            "t_test"
        )
    ],
)
def test_fetch_many(engine, dsn, table_name):
    """Test fetch many data from database, and construct recordBatch object.

    Args:
        dsn (str): database
    """
    # connect database
    conn = db.connect(engine, dsn)
    if not conn:
        click.echo("connect database failed")
        return "connect database failed"

    # get cursor
    cursor = conn.cursor()

    row_number = 2

    # fetch many data
    cursor.execute(f"select * from {table_name}")
    rows = cursor.fetchmany(row_number)

    # get schema
    # schema = parquet_schema(conn, table_name)

    # construct recordBatch object
    batch = pa.RecordBatch.from_pylist(rows)
    print(f"batch\n: {batch.to_pandas()}")

    assert len(rows) == row_number

    # close cursor
    cursor.close()

    return "success"
