"""Test read parquet."""

from pathlib import Path

import pytest

from delibird.work import read_directory, read_parquet


@pytest.mark.parametrize(
    "path, directory, engine, dsn, table_name",
    [
        # (
        #     "./datasets/write/000471.parquet",
        #     None,
        #     "postgresql://test:test123@localhost:5432/delibird",
        #     "fuguo000471",
        # ),
        (
            None,
            "./datasets/write/pinganbank",
            "postgresql",
            "postgresql://test:test123@localhost:5432/delibird",
            "pinganbank",
        ),
        (
            None,
            "./datasets/mock_data/mock_stocks_ora.parquet",
            "oracle",
            "system/oracle@222.71.193.222:43301/xe",
            "mock_stocks_ora",
        )
    ],
)
def test_read(path, directory, engine, dsn, table_name):
    """Test from_parquet function.

    Args:
        path (str): filename with path
        directory (str): directory
        dsn (str): data source name,like 'postgresql://user:password@localhost:port/dbname'
        table_name (str): table name, default is None
    """
    # test from parquet function

    if path:
        filepath = Path(path)
        if filepath.exists & filepath.is_file():
            result = read_parquet(path, engine, dsn, table_name)
            assert result == "success"
    elif directory:
        dir_ = Path(directory)

        if dir_.is_dir():
            result = read_directory(directory, engine, dsn, table_name)
            assert result == "success"
        else:
            print("directory not exist")
