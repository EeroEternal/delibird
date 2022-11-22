"""Test database schema inspect."""

import pytest

from delibird.database import db


@pytest.mark.parametrize(
    "engine, dsn",
    [
        (
            "postgresql",
            "postgresql://test:test123@localhost:5432/delibird"
        ),
        (
            "oracle",
            "system/oracle@222.71.193.222:43301/xe"
        ),
        (
            "mysql",
            "jdbc:mysql://localhost:3306/test?user=root&password=feng17zhu"
        )
    ]
)
def test_schema(engine, dsn):
    """Test database schema.

    Args:
        dsn (str): database connect string
    """
    conn = db.connect(engine, dsn)

    # with psycopg.connect(dsn) as conn:
    #     result = conn.execute("select * from pinganbank limit 1")
    #     assert result == "success"

    with open("test.txt", "w", encoding="utf-8") as myfile:
        myfile.write("test")
