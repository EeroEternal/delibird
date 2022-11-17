"""Test read parquet to database table"""

import pytest

from delibird.database import db
from delibird.work import read_directory


@pytest.mark.parametrize(
    "directory, engine, dsn, table_name",
    [
        (
            "./datasets/write/mock_stocks",
            "postgresql",
            "postgresql://test:test123@localhost:5432/delibird",
            "mock_stocks",
        ),
        (
            "./datasets/write/mock_stocks_ora",
            "oracle",
            "system/oracle@222.71.193.222:43301/xe",
            "mock_stocks_eng",
        )
    ],
)
def test_read_dir(directory, engine, dsn, table_name):
    """Test from_parquet function.

    Args:
        directory (str): directory of parquet files
        dsn (str): data source name,like 'postgresql://user:password@localhost:port/dbname'
        table_name (str): table name, default is None
    """
    # truncate table
    conn = db.connect(dsn)
    if not conn:
        print("connect database failed")
        assert False

    cursor = conn.cursor()
    cursor.execute(f"TRUNCATE TABLE {table_name}")
    conn.commit()

    # test from parquet function
    read_directory(directory, engine, dsn, table_name)

    # check table exist
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_number = cursor.fetchone()[0]
    print(f"table row number: {row_number}")

    # check parquet row number
    assert row_number > 0
