"""Test command line."""

import pytest

from test_cli_file import test_mock


@pytest.mark.parametrize(
    "mock_files",
    [(
        (
        "./tests/yamls/mock_file_enormous.yaml",
        "./tests/yamls/mock_dir_enormous.yaml",
        "./tests/yamls/mock_file_large.yaml",
        "./tests/yamls/mock_file_edge.yaml"
        )
    )],
)
def test_cli_files(mock_files):
    """Test generate mock data from mock files.

    Args:
        mock_files (str list): workflow yaml config file list
    """
    for mock_file in mock_files:
        test_mock(mock_file)
