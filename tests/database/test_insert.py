"""Test insert function."""
import click
import pyarrow.parquet as pq
import pytest

from delibird.database import db, insert_batch, table_by_arrow, table_exist


@pytest.mark.parametrize(
    "parquet_file, engine, dsn ,table_name, sample_size",
    [
        (
            "./datasets/stocks/000001.parquet",
            "postgresql",
            "postgresql://test:test123@localhost:5432/delibird",
            "pinganbank",
            1024,
        ),
        (
            "./datasets/mock_data/mock_stocks_ora.parquet",
            "oracle",
            "system/oracle@222.71.193.222:43301/xe",
            "mock_stocks_ora",
            1024,
        ),
        (
            "./datasets/mock_data/mock_my.parquet",
            "mysql",
            "jdbc:mysql://localhost:3306/test?user=root&password=feng17zhu",
            "mock_stocks_in",
            2048
        )
    ],
)
def test_insert_table(parquet_file, engine, dsn, table_name, sample_size):
    """test insert row group to table

    Args:
        parquet_file (filepath): filename with path
        dsn (str): database connect string
        table_name (str): table name
        sample_size (int): size of sample records
    """

    # connect database
    conn = db.connect(engine, dsn)
    if not conn:
        click.echo("connect database failed")
        return

    # parquet file object
    file = pq.ParquetFile(parquet_file)

    # get sample row group data
    row_group_sample = file.read_row_group(0)

    # get cursor
    cursor = conn.cursor()

    # check table exists
    if not table_exist(conn, table_name):
        # create table by arrow schema
        table_by_arrow(conn, table_name, row_group_sample.schema)
    else:
        # truncate table for test easy
        cursor.execute(f"truncate table {table_name}")

    # get table row number
    sql_statement = f"select count(*) from {table_name}"

    # execute sql
    cursor.execute(sql_statement)

    # get table row number
    row_number_before = cursor.fetchone()[0]

    # avoid out of bounds
    if row_group_sample.num_rows < sample_size:
        sample_size = row_group_sample.num_rows

    # take sample records
    row_group_limit = row_group_sample.take(list(range(0, sample_size)))

    # insert row group sample to table
    insert_batch(row_group_limit, conn, table_name)

    # get table row number again
    cursor.execute(sql_statement)
    row_number_after = cursor.fetchone()[0]

    # close connection
    conn.close()

    # assert row number is increasing
    assert row_number_after == row_number_before + sample_size
