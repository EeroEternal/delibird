"""Test command line."""

import click
import pytest
from click.testing import CliRunner

from delibird.cli import cli
from delibird.database import db


@pytest.mark.parametrize(
    "path, mode, engine, dsn, table_name,",
    [
        (
            "./datasets/write/000471.parquet",
            "file",
            "postgresql",
            "postgresql://test:test123@localhost:5432/delibird",
            "fuguo000471",
        ),
        (
            "./datasets/write/allfunds",
            "dir",
            "postgresql",
            "postgresql://test:test123@localhost:5432/delibird",
            "allfunds",
        ),
        (
            "./datasets/write/mock_stocks_ora.parquet",
            "file",
            "oracle",
            "system/oracle@222.71.193.222:43301/xe",
            "mock_stocks_eng",
        ),
        (
            "./datasets/write/mock_stocks_ora",
            "dir",
            "oracle",
            "system/oracle@222.71.193.222:43301/xe",
            "mock_stocks_eng",
        ),
    ],
)
def test_write(path, mode, engine, dsn, table_name):
    """Test read parquet.

    Args:
        path (str): filename with path
        mode (str): "file" or "dir"
        dsn (str): data source name,like 'dbname=delibird user=test password=test123'
        table_name: table name
        partition_cols (list[str]): partition column names
    """
    # cli runner
    runner = CliRunner()

    # connect database
    conn = db.connect(engine, dsn)
    if not conn:
        click.echo("connect database failed")
        return

    # read filename
    if mode == "file":
        # execute read parquet command
        result = runner.invoke(
            cli, ["parquet", "write", path, engine, dsn, table_name]
        )

    # read from directory
    elif mode == "dir":
        result = runner.invoke(
            cli,
            [
                "parquet",
                "write",
                path,
                engine,
                dsn,
                table_name,
            ],
        )
        assert result.exit_code == 0

    print(f"result output:{result.output}")
    # clean up
    conn.close()


def test_version():
    """Test version."""
    runner = CliRunner()
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert result.output == "0.0.1\n"
