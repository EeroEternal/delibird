"""Test command line."""

import pytest
from click.testing import CliRunner

from delibird.cli import cli


@pytest.mark.parametrize(
    "yaml_file",
    ["./tests/yaml/mock_dir.yaml"],
)
def test_yaml(yaml_file):
    """Test read parquet by yaml file.

    Args:
        yaml_file (str): workflow yaml config file
    """
    # cli runner
    runner = CliRunner()

    # execute read parquet command
    result = runner.invoke(cli, ["yaml", "-y", yaml_file])

    assert result.exit_code == 0
