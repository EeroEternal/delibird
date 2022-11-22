"""Test write parquet."""

from pathlib import Path

import pyarrow.parquet as pq
import pytest

from delibird.database import db
from delibird.work import write_parquet


@pytest.mark.parametrize(
    "filepath, engine, dsn, table_name",
    [
        (
            "./datasets/write/mock_stocks.parquet",
            "postgresql",
            "postgresql://test:test123@localhost:5432/delibird",
            "mock_stocks",
        ),
        (
            "./datasets/write/mock_stocks_ora.parquet",
            "oracle",
            "system/oracle@222.71.193.222:43301/xe",
            "mock_stocks_eng",
        ),
        (
            "./datasets/mock_data/mock_read_my.parquet",
            "mysql",
            "jdbc:mysql://localhost:3306/test?user=root&password=feng17zhu",
            "mock_stocks_my"
        )
    ],
)
def test_write_parquet(filepath, engine, dsn, table_name):
    """Test from_parquet function.

    Args:
        filepath (str): filename with path
        dsn (str): data source name,like 'postgresql://user:password@localhost:port/dbname'
        table_name (str): table name, default is None
    """
    # delete exist parquet file
    path = Path(filepath)
    if path.exists():
        if path.is_file():
            path.unlink()
        else:
            print("filepath is not file")
            assert False

    # test from parquet function
    write_parquet(filepath, dsn, table_name, engine)

    # check file exist
    assert path.exists()

    # check parquet row number

    # get row number from table
    conn = db.connect(dsn)
    if not conn:
        print("connect database failed")
        assert False

    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_number = cursor.fetchone()[0]

    # get row number from parquet file
    parquet_file = pq.ParquetFile(filepath).read()
    print(f'table row number: {row_number}, parquet row number: {parquet_file.num_rows}')
    assert parquet_file.num_rows == row_number
