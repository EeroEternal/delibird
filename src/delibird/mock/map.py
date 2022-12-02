"""Type map for mock objects."""
from ast import literal_eval

from magicbag import prefix_check, random_date, random_decimal, random_timestamp

from delibird.mock.parser import decimal_parse, timestamp_parse

from .parser import meta_types


def map_value(type_name):
    """Map type to dict value.

    Args:
        type_name (str): type name. e.g 'float','init'
    Return:
        different types
    """
    # like type_name = "decimal(10,2)". result is "decimal"
    # meta_types is a tuple include all types
    result = prefix_check(type_name, meta_types)

    if result[0]:
        # call generate function by type name
        # use literal_eval safe convert str to int, float, etc.
        return literal_eval(f"map_{result[1]}")(type_name)

    # not match any type, return None
    return None


def map_date():
    """Generate random date.

    calendar date (year, month, day). e.g 2020-01-01

    Returns:
        datetime.date: random date
    """
    return random_date()


def map_datetime(type_name):
    """Generate datetime with unit and timezone.

    Args:
        type_name (str): datetime type. e.g "datetime(s,Asia/Shanghai)"

    """
    unit, timezone = timestamp_parse(type_name)

    return random_timestamp(unit, timezone)


def map_decimal(type_name):
    """Generate decimal with precision and scale.

    Args:
        type_name (str): decimal type define. e.g "decimal(10,5)"

    Returns:
        Decimal : decimal value

    """
    # python no scale define
    precision, scale = decimal_parse(type_name)

    # generate random decimal
    return random_decimal(precision, scale)


def map_timestamp(type_name):
    """Generate timestamp with unit and timezone.

    Args:
        type_name (str): timestamp type. e.g "timestamp(s,Asia/Shanghai)"

    """
    unit, timezone = timestamp_parse(type_name)

    return random_timestamp(unit, timezone)
