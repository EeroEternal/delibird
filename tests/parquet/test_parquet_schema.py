"""Test schema function."""

import pyarrow as pa
import pytest

from delibird.database import db, parquet_schema, sql_schema


@pytest.mark.parametrize(
    "engine, schema",
    [
        (
            "postgresql",
            pa.schema(
                [
                    pa.field("id", pa.int32()),
                    pa.field("name", pa.string()),
                    pa.field("age", pa.int64()),
                ]
            )
        ),
        (
            "oracle",
            pa.schema(
                [
                    pa.field("id", pa.int32()),
                    pa.field("name", pa.string()),
                    pa.field("age", pa.int64()),
                ]
            )
        )
    ],
)
def test_schema(engine, schema):
    """test create sql schema

    Args:
        schema (pyarrow.Schema): arrow schema
    """
    sql_schema_inner = sql_schema(engine, schema)

    if engine == "postgresql":
        assert sql_schema_inner == "id integer, name varchar(255), age bigint"
    elif engine == "oracle":
        assert sql_schema_inner == "id integer, name varchar2(255), age number(38,8)"

@pytest.mark.parametrize(
    "dsn,table_name",
    [
        (
            "postgresql",
            "postgresql://test:test123@localhost:5432/delibird",
            "xichou"
        ),
        (
            "oracle",
            "system/oracle@222.71.193.222:43301/xe",
            "t_test"
        )
    ],
)
def test_desc_schema(engine, dsn, table_name):
    """Test desc to parquet schema."""
    conn = db.connect(engine, dsn)

    arrow_schema = parquet_schema(conn, table_name)

    print(f"arrow schema:\n{arrow_schema}")
