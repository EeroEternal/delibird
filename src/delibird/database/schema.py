"""Row group utils."""

import pyarrow as pa

from delibird.database import db, table_exist
from delibird.mock import decimal_parse


schema_dict = {"postgresql": {
        "int8": "smallint",
        "int16": "smallint",
        "int32": "integer",
        "int64": "bigint",
        "uint8": "smallint",
        "uint16": "smallint",
        "uint32": "integer",
        "uint64": "bigint",
        "float": "double precision",
        "float32": "real",
        "float64": "double precision",
        "double": "double precision",
        "bool": "boolean",
        "string": "varchar(255)",
        "large_string": "text",
        "binary": "bytea",
        "large_binary": "bytea",
        "time32": "time",
        "time64": "time",
        "list": "text",
        "large_list": "text",
        "struct": "text",
        "duration": "text",
        "null": "text",
    }, "oracle": {
        "int8": "integer",
        "int16": "integer",
        "int32": "integer",
        "int64": "integer",
        "uint8": "integer",
        "uint16": "integer",
        "uint32": "integer",
        "uint64": "integer",
        "float": "number(38,8)",
        "float32": "number(38,8)",
        "float64": "number(38,8)",
        "double": "number(38,8)",
        "bool": "varchar2(10)",
        "string": "varchar2(255)",
        "large_string": "long",
        "binary": "blob",
        "large_binary": "blob",
        "time32": "timestamp",
        "time64": "timestamp",
        "list": "varchar2(2000)",
        "large_list": "varchar2(4000)",
        "struct": "varchar2(4000)",
        "duration": "varchar2(4000)",
        "null": "varchar2(4000)",
    }, "mysql": {
        "int8": "tinyint",
        "int16": "smallint",
        "int32": "mediumint",
        "int64": "int",
        "uint8": "tinyint",
        "uint16": "smallint",
        "uint32": "mediumint",
        "uint64": "int",
        "float": "float",
        "float32": "float",
        "float64": "float",
        "double": "decimal(25,8)",
        "bool": "varchar(10)",
        "string": "varchar(255)",
        "large_string": "text",
        "binary": "blob",
        "large_binary": "longblob",
        "time32": "timestamp",
        "time64": "timestamp",
        "list": "varchar(2000)",
        "large_list": "varchar(4000)",
        "struct": "varchar(4000)",
        "duration": "varchar(4000)",
        "null": "varchar(100)",
    }}

def create_arrow_schema(engine, dsn, table_name):
    """Create arrow schema based on table.

    Args:
        dsn (str): database connect string
        table_name (str): table name

    Returns:
        pyarrow.Schema: arrow schema
    """
    # connect database
    conn = db.connect(engine, dsn)
    if not conn:
        print("connect failed")
        return None

    # set dict cursor
    cursor = conn.cursor(dict_row_flag=True)
    if engine == "postgresql" or engine == "mysql":
        cursor.execute(f"select * from {table_name} limit 1")
    elif engine == "oracle":
        cursor.execute(f"select * from {table_name} where rownum <= 1")

    # type list
    type_list = []

    # get column name and type ,append to type list
    # 0:name, 1:type_code, OID
    for col in cursor.description:
        if engine == "postgresql":
            type_list.append(pa.field(col.name, arrow_type(engine, col)))
        elif engine == "oracle" or engine == "mysql":
            type_list.append(pa.field(col[0], arrow_type(engine, col)))

    # create schema
    return pa.schema(type_list)


def parquet_schema(conn, table_name) -> pa.Schema:
    """Cusor description to parquet schema.

    Args:
        cursor (db.conn): db-api cursor description.
                refer to https://peps.python.org/pep-0249/
        table_name (str): table name

    Returns:
        pyarrow.Schema: parquet schema

    """
    # set dict cursor
    cursor = conn.cursor(dict_row_flag=True)
    engine = conn.engine
    if engine == "postgresql" or engine == "mysql":
        cursor.execute(f"select * from {table_name} limit 1")
    elif engine == "oracle":
        cursor.execute(f"select * from {table_name} where rownum <= 1")

    # type list
    type_list = []

    # get column name and type ,append to type list
    # 0:name, 1:type_code, OID
    for col in cursor.description:
        type_list.append(pa.field(col.name, arrow_type(engine, col)))

    # create schema
    return pa.schema(type_list)


def arrow_type(engine, col):
    """Get arrow type based on sql type.

    https://stackoverflow.com/questions/37478323/how-to-programatically-get-table-structure-with-pyscopg2

    Args:
        oid (str): sql type oid
        cursor (db.cursor): database cursor

    Returns:
        pyarrow.DataType: pyarrow type
    """
    # database type map to arrow type
    type_map = {
        "tinyint": pa.int8(),
        "smallint": pa.int16(),
        "mediumint": pa.int32(),
        "int4": pa.int8(),
        "int8": pa.int8(),
        "int16": pa.int16(),
        "int32": pa.int32(),
        "int64": pa.int64(),
        "int": pa.int64(),
        "float": pa.float32(),
        "float8": pa.float32(),
        "float16": pa.float32(),
        "float32": pa.float32(),
        "float64": pa.float64(),
        "double": pa.float64(),
        "DB_TYPE_NUMBER": pa.float64(),
        "boolean": pa.bool_(),
        "blob": pa.large_binary(),
        "varchar": pa.string(),
        "varchar2": pa.string(),
        "varchar(255)": pa.string(),
        "varchar2(255)": pa.string(),
        "DB_TYPE_VARCHAR": pa.string(),
        "text": pa.large_string(),
        "date": pa.date32(),
        "DB_TYPE_DATE": pa.date32(),
        "time": pa.time32("s"),
        "timestamp": pa.timestamp(unit="s"),
        "DB_TYPE_TIMESTAMP": pa.timestamp(unit="s"),
    }

    mysql_type_mapper = {
        0: "float64",
        1: "tinyint",
        2: "int",
        3: "int",
        4: "float",
        5: "float64",
        6: "null",
        7: "timestamp",
        8: "longint",
        9: "int",
        10: "date",
        11: "time",
        12: "datetime",
        13: "year",
        14: "newdate",
        15: "varchar",
        16: "varchar",
        245: "varchar",
        246: "numeric",
        247: "varchar",
        248: "varchar",
        249: "blob",
        250: "blob",
        251: "longblob",
        252: "blob",
        253: "varchar",
        254: "text"
    }

    # trick to get arrow type, only to psycopy
    if engine == "postgresql":
        # pylint: disable=protected-access
        type_name = col._type.name
    elif engine == "oracle":
        type_name = col[1].name
    elif engine == "mysql":
        type_name = mysql_type_mapper[col[1]]

    result = None
    # numeric type , need to get precision and scale
    if type_name == "numeric":
        if engine == "postgresql":
            result = pa.decimal128(col.precision, col.scale)
        elif engine == "oracle":
            result = pa.decimal128(col[2], col[3])
        elif engine == "mysql":
            if col[4] < col[5]:
                result = pa.decimal128(col[5], col[4])
            else:
                result = pa.decimal128(col[4], col[5])
    elif type_name == "date":
        # check if date is in days or seconds
        result = pa.date32()
    elif type_name == "timestamp":
        # check if timestamp is in s、ms or us
        result = pa.timestamp(unit="s")
    else:
        result = type_map[type_name]

    return result


def table_by_arrow(conn, table_name, arrow_schema):
    """Create table by arrow schema.

    Args:
        conn (db.connection): database connection
        table_name (str): table name
        arrow_schema (str): table schema

    """
    # create cursor
    cursor = conn.cursor(dict_row_flag=True)

    #engine
    engine = conn.engine

    # change to sql schema
    table_schema = sql_schema(engine, arrow_schema)

    # if table exists, drop it
    if engine == "oracle":
        if table_exist(conn, table_name):
            cursor.execute(f"drop table {table_name}")
    else:
        cursor.execute(f"drop table if exists {table_name}")

    # create table
    cursor.execute(f"create table {table_name} ({table_schema})")

    # commit
    conn.commit()

    # close cursor
    cursor.close()


def create_table_by_schema(conn, table_name, arrow_schema):
    """Create table by arrow schema.

    Args:
        conn (db.connection): database connection
        table_name (str): table name
        arrow_schema (str): table schema

    """
    # create cursor
    cursor = conn.cursor()

    # change to sql schema
    table_schema = sql_schema(conn.engine, arrow_schema)

    # create table
    cursor.execute(f"create table {table_name} ({table_schema})")

    # commit
    conn.commit()

    # close cursor
    cursor.close()


def sql_schema(engine, schema):
    """Get 'create table' statement based on row group schema.

    create table tablename (id serial primary key, name varchar(255), age int)

    Args:
        schema (pyarrow.Schema): pyarrow schema

    """
    column_names = schema.names
    column_types = schema.types
    column_defs = []
    for name, type_ in zip(column_names, column_types):
        # get type name as string
        type_name = f"{type_}"
        column_defs.append(f"{name} {sql_type_map(engine, type_name)}")

    return ", ".join(column_defs)


def sql_type_map(engine, type_name):
    """Get sql type based on pyarrow type.

    Args:
        type_name (str): pyarrow type as string

    Returns:
        str

    """
    types_ = schema_dict[engine]

    if type_name.startswith("date"):
        # "date32[day]" :  pyarrow date32 is date32[day]
        # "date64[ms]" : pyarrow date64 is date64[ms]
        return "date"

    if type_name.startswith("timestamp"):
        #  timestamp[s, tz=Asia/Shanghai]
        data = type_name.split("[")[1].split("]")[0]

        # if need unit and timezone
        if type_name.find(",") > -1:
            unit, timezone = data.split(",")
            unit = unit.strip()
            timezone = timezone.split("=")[1].strip()
        else:
            unit = data

        return "timestamp"

    if type_name.startswith("decimal"):
        # decimal(10,2)
        precision, scale = decimal_parse(type_name)
        return f"decimal({precision},{scale})"

    return types_[type_name]
