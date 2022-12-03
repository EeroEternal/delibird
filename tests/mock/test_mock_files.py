"""Test command line."""

import pytest
from test_mock_file import test_mock_file


@pytest.mark.parametrize(
    "mock_files",
    ["./tests/yaml/mock_dir.yaml"]
)
def test_mock_files(mock_files):
    """Test generate mock data from mock file list.

    Args:
        mock_files (str list): workflow yaml config file list
    """
    for mock_file in mock_files:
        test_mock_file(mock_file)
