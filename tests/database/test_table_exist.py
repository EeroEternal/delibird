"""Test database check."""

import click
import pytest

from delibird.database import db, table_exist


@pytest.mark.parametrize(
    "engine, dsn, table_name",
    [
        ("postgresql", "postgresql://test:test123@localhost:5432/delibird", "green"),
        ("postgresql", "postgresql://test:test123@localhost:5432/delibird", "notexist"),
        ("oracle", "system/oracle@222.71.193.222:43301/xe", "mock_stocks_ora"),
        ("oracle", "system/oracle@222.71.193.222:43301/xe", "mock_stocks_o"),
        ("mysql", "jdbc:mysql://localhost:3306/test?user=root&password=feng17zhu", "mock_stocks_in")
    ],
)
def test_table_exist(engine, dsn, table_name):
    """Test table_exist function."""
    conn = db.connect(engine, dsn)
    if not conn:
        click.echo("connect database failed")

    result = table_exist(conn, table_name)

    if table_name == "green":
        assert result is True

    if table_name == "notexist":
        assert result is False

    conn.close()
