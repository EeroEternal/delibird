"""Parse data type from file."""
import pytz


def decimal_parse(data):
    """Parse decimal str, get precision and scale.

    Args:
        data (str): decimal str, e.g "decimal(10,5)"
    Returns:
        int,int: precision, scale
    """
    if not data.startswith("decimal"):
        return None

    # get "10,5" from "decimal(10,5)"
    data = data.split("(")[1].split(")")[0]

    # get precision and scale
    precision_str, scale_str = data.split(",")

    return int(precision_str), int(scale_str)


def timestamp_parse(data):
    """Parse timestampl str, get unit and timezone.

    Args:
        data (str): timestamp str, e.g "timestamp(unit=s,tz=Asia/Shanghai)"
    Returns:
        str,str: unit, timezone
    """
    if not data.startswith("timestamp"):
        return None

    # get "unit='s',tz='Asia/Shanghai'" from "timestamp(unit='s',tz='Asia/Shanghai')"
    data = data.split("(")[1].split(")")[0]

    # get unit and timezone
    unit, timezone = data.split(",")

    # remove bracket in "'s'" "'Asia/Shanghai'"

    unit, timezone_str = unit.split("=")[1].strip(""), timezone.split("=")[1].strip("")

    timezone = pytz.timezone(timezone_str)

    return unit, timezone
