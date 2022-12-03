"""Test mock data to table."""

import pytest

from delibird.cli import mock_data


@pytest.mark.parametrize("mock_file", ["./tests/yaml/mock_table.yaml"])
def test_mock_table(mock_file):
    """Test mock data to table."""
    mock_data(mock_file)
