"""Schema for parquet file."""

import pyarrow as pa

from .parser import decimal_parse, timestamp_parse


def schema_from_dict(schema_dict):
    """Create Schema from dict.

    Args:
        schema_dict (dict): schema define by dict
    """
    # type list
    type_list = []

    # get column name and type ,append to type list
    # 0:name, 1:type_code, OID
    for col in schema_dict.keys():
        type_list.append(pa.field(col, type_map(schema_dict[col])))

    # create schema
    return pa.schema(type_list)


def type_map(type_str):
    """Type map from python to pyarrow type."""
    # database type map to arrow type
    # code is special string for security code
    maps = {
        "code": pa.string(),
        "str": pa.string(),
        "int": pa.int64(),
        "float": pa.float64(),
        "boolean": pa.bool_(),
        "date": pa.date32(),
        "time": pa.time32("s"),
        "string": pa.string(),
    }

    # decimal like : decimal(10,5)
    if type_str.startswith("decimal"):
        precision, scale = decimal_parse(type_str)
        return pa.decimal128(precision, scale)

    # timestampe like: timestample(unit='s',tz='Asia/Shanghai')
    if type_str.startswith("timestamp"):
        unit, timezone = timestamp_parse(type_str)
        return pa.timestamp(unit, tz=timezone)

    return maps[type_str]
