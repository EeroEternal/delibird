"""Test command line."""

from pathlib import Path

import pytest
import yaml
import pyarrow.parquet as pq

from delibird.cli import mock_data
from delibird.util import show


@pytest.mark.parametrize(
    "mock_file",
    [("./tests/yamls/mock_file.yaml")],
)
#pylint: disable=too-many-branches
def test_mock_file(mock_file):
    """Test generate mock data from mock file.

    Args:
        mock_file(str): workflow yaml config file
    """
    # get filepath and directory from mock yaml

    # read yaml
    with open(mock_file, "r", encoding="utf-8") as mock:
        config = yaml.load(mock, Loader=yaml.FullLoader)

    if "mocks" not in config:
        print("mock file no mocks workflow")
        assert False

    # get mock files path and directories
    files = []
    dirs = []
    file_row_numbers = []
    dir_row_numbers = []
    for mock in config["mocks"]:
        if "direction" not in mock:
            print("mock file no direction")
            assert False

        if mock["direction"] == "file":
            if "filepath" not in mock:
                print("mock file no filepath")
                assert False
            files.append(mock["filepath"])
            file_row_numbers.append(mock["row-number"])

        elif mock["direction"] == "directory":
            if "directory" not in mock:
                print("mock file no directory")
                assert False
            dirs.append(mock["directory"])
            dir_row_numbers.append(mock["row-number"])
        else:
            print("mock file direction is not file or directory")
            assert False

    # delete mock directory and files
    for file in files:
        path = Path(file)
        if path.exists and path.is_file():
            path.unlink()

    for directory in dirs:
        path = Path(directory)
        if path.exists and path.is_dir():
            for file in path.iterdir():
                file.unlink()
            path.rmdir()

    # execute read parquet command
    mock_data(mock_file)

    # check mock files and directories
    for file, row_count in zip(files, file_row_numbers):
        path = Path(file)
        parquet_file = pq.ParquetFile(file)
        rows = parquet_file.metadata.num_rows
        show(str(rows) + "," + str(row_count))
        assert path.exists() and path.is_file()
        assert rows == row_count

    for directory, row_count in zip(dirs, dir_row_numbers):
        path = Path(directory)
        assert path.exists and path.is_dir()
        file_count = 0
        rows = 0
        for file in path.iterdir():
            file_count += 1
            parquet_file = pq.ParquetFile(file)
            rows += parquet_file.metadata.num_rows
            assert file.exists() and file.is_file()
        show(str(rows) + "," + str(row_count))
        assert file_count > 0
        assert rows == row_count
