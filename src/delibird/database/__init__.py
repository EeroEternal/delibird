"""Database management."""

from .check import table_exist
from .db import Database as db
from .insert import insert_arrow_table, insert_batch, insert_list
from .schema import (
    create_arrow_schema,
    create_table_by_schema,
    parquet_schema,
    sql_schema,
    table_by_arrow,
)

__all__ = [
    "db",
    "parquet_schema",
    "sql_schema",
    "table_exist",
    "table_by_arrow",
    "create_arrow_schema",
    "create_table_by_schema",
    "insert_list",
    "insert_arrow_table",
    "insert_batch",
]
