"""Schema for parquet file."""

import pyarrow as pa

from .parser import parse, meta_types

from magicbag import prefix_check

# database type map to arrow type
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
        arrow_type = type_map(schema_dict[col])
        if arrow_type:
            type_list.append(pa.field(col, arrow_type))

    # create schema
    return pa.schema(type_list)


def type_map(type_name):
    """Type map from python to pyarrow type."""
    # get type name by prefix
    result = prefix_check(type_name, meta_types)

    # result[0] is True or False, result[1] is type name
    if result[0] and result[1]:
        if result[1] == "decimal":
            # get precision and scale
            precision, scale = parse(type_name)

            # return decimal type
            return pa.decimal128(precision, scale)

        if result[1] == "timestamp":
            # get precision
            unit, timezone = parse(type_name)

            # return timestamp with unit and timezone
            return pa.timestamp(unit, tz=timezone)

        # other type return from maps
        return maps[result[1]]

    return None
