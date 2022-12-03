"""Test command line."""

import pytest
from click.testing import CliRunner

from delibird.cli import cli


@pytest.mark.parametrize(
    "mock_file",
    ["./tests/yaml/mock_file.yaml"],
)
def test_mock(mock_file):
    """Test generate mock data from mock file.

    Args:
        mock_file(str): workflow yaml config file
    """
    # cli runner
    runner = CliRunner()

    # execute read parquet command
    result = runner.invoke(cli, ["mock", mock_file])

    assert result.exit_code == 0
