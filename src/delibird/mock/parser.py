"""Parse data type from file."""

from ast import literal_eval

from magicbag import prefix_check

meta_types = ("int", "string", "float", "date", "datetime",
              "decimal", "timestamp")


def parse(type_name):
    """Get argument from literal.

    Args:
        type_name (str): input string. e.g "decimal(10,5)"
    Returns:
        tuple(str): argument. e.g "10,5"
    """
    # check literal start with category prefix
    # result is "decimal"
    result = prefix_check(type_name, meta_types)

    if result[0]:
        # parse argument by result
        return literal_eval(f"{result[1]}_parse")(type_name)

    return None


def int_parse(type_name):
    """Parse int type, get fix length.

    Args:
        type_name (str): int type, e.g "int(10)"
    Returns:
        int: fix length
    """
    if not type_name.startswith("int"):
        return None

    # get "10" from "int(10)" and return
    return int(type_name.split("(")[1].split(")")[0])


def decimal_parse(type_name):
    """Parse decimal str, get precision and scale.

    Args:
        type_name (str): decimal str, e.g "decimal(10,5)"
    Returns:
        int,int: precision, scale
    """
    if not type_name.startswith("decimal"):
        return None

    # get "10,5" from "decimal(10,5)"
    data = type_name.split("(")[1].split(")")[0]

    # get precision and scale
    precision_str, scale_str = data.split(",")

    return int(precision_str), int(scale_str)


def timestamp_parse(type_name):
    """Parse timestamp str, get unit and timezone.

    Args:
        type_name (str): timestamp str, e.g "timestamp(unit=s,tz=Asia/Shanghai)"
    Returns:
        str,str: unit, timezone
    """
    if not type_name.startswith("timestamp"):
        return None

    # get "unit='s',tz='Asia/Shanghai'" from "timestamp(unit='s',tz='Asia/Shanghai')"
    data = type_name.split("(")[1].split(")")[0]

    # get unit and timezone
    unit, timezone = data.split(",")

    # remove bracket in "'s'" "'Asia/Shanghai'"

    unit, timezone = unit.split("=")[1].strip(""), timezone.split("=")[1].strip("")

    return unit, timezone


def datetime_parse(type_name):
    """Parse datetime str, get unit and timezone.

    Args:
        type_name (str): datetime str, e.g "datetime(tz=Asia/Shanghai)"
    Returns:
        str: timezone
    """
    if not type_name.startswith("datetime"):
        return None

    # get "tz='Asia/Shanghai'" from "datetime(tz='Asia/Shanghai')"
    data = type_name.split("(")[1].split(")")[0]

    # remove bracket in "'Asia/Shanghai'"

    timezone = data.split("=")[1].strip("")

    return timezone