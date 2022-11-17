"""Test command line."""

import click
import pytest
from click.testing import CliRunner

from delibird.cli import cli
from delibird.database import db
from delibird.database.check import table_exist


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
            "./datasets/write/allfunds",
            "postgresql://test:test123@localhost:5432/delibird",
            "allfunds",
        ),
    ],
)
def test_read(path, directory, engine, dsn, table_name):
    """Test read parquet.

    Args:
        filepath (str): filename with path
        directory (str): directory
        dsn (str): data source name,like 'dbname=delibird user=test password=test123'
        table_name: table name
    """
    # cli runner
    runner = CliRunner()

    # connect database
    conn = db.connect(engine, dsn)
    if not conn:
        click.echo("connect database failed")
        return

    # sql for count table rows
    sql_statement = f"select count(*) from {table_name}"

    # get cursor
    cursor = conn.cursor()

    # get table row number before read
    row_number_before = 0
    if table_exist(conn, table_name):

        # get table row number
        cursor.execute(sql_statement)
        row_number_before = cursor.fetchone()[0]

    # read filename
    if path:
        # execute read parquet command
        result = runner.invoke(
            cli, ["parquet", "read", path, engine, dsn, table_name]
        )

    # read from directory
    if directory:
        result = runner.invoke(
            cli, ["parquet", "read", directory, engine, dsn, table_name]
        )
        assert result.exit_code == 0

    # get table row number again
    row_number_after = 0
    if table_exist(conn, table_name):
        cursor.execute(sql_statement)
        row_number_after = cursor.fetchone()[0]

    # assert insert some rows
    assert row_number_after - row_number_before > 0
    assert row_number_after != 0

    print(f"cli output:{result.output}")
    # clean up
    cursor.close()
    conn.close()


def test_version():
    """Test version."""
    runner = CliRunner()
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert result.output == "0.0.1\n"
