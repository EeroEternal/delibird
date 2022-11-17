"""Test write parquet to directory"""

from pathlib import Path

import pytest

from delibird.work import write_directory


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
def test_write_dir(directory, engine, dsn, table_name):
    """Test from_parquet function.

    Args:
        directory(str): filename with path
        dsn (str): data source name,like 'postgresql://user:password@localhost:port/dbname'
        table_name (str): table name, default is None
    """
    # delete exist directories
    path = Path(directory)
    if path.exists():
        print('path exist')
        if path.is_dir():
            for file in path.iterdir():
                print(f'remove file: {file}')
                file.unlink()
            path.rmdir()
        else:
            print("directory is not dir")
            assert False

    # test from parquet function
    write_directory(directory, engine, dsn, table_name, batch_size=10240)

    # check file exist
    assert path.exists() and path.is_dir()

    # check if parquet file exist in directory
    count = 0
    for file in path.iterdir():
        if file.is_file():
            count += 1

    assert count > 0
