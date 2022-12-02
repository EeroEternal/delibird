"""Type map for mock objects."""

from ast import literal_eval
from random import randint, random

from magicbag import (
    prefix_check, random_date,
    random_decimal, random_timestamp, random_int
)

from delibird.mock.parser import parse

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


def map_int(type_name):
    """Generate random int.

    if type_name is "int", return random int between 0 and 10000
    if type_name is "int(10)", return random fixed length int with 10 digits

    Returns:
        int: random int
    """
    fix_length = parse(type_name)

    if fix_length:
        return random_int(fix_length)

    # default int is between 0 and 10000
    return randint(0, 10000)


def map_string(_type_name):
    """Generate random string.

    Returns:
        str: random string
    """
    # todo: generate random string
    return


def map_float(type_name):
    """Generate random float with precision.

    Args:
        type_name (str): float type. e.g "float(10)"

    Returns:
        float: random float

    """
    start, end = parse(type_name)

    # if not precision, return random float
    if start is None:
        start = 0
        end = 10000

    # return random float between start and end
    return start + (end - start) * random()


def map_date(_type_name):
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
    unit, timezone = parse(type_name)

    return random_timestamp(unit, timezone)


def map_decimal(type_name):
    """Generate decimal with precision and scale.

    Args:
        type_name (str): decimal type define. e.g "decimal(10,5)"

    Returns:
        Decimal : decimal value

    """
    # python no scale define
    precision, scale = parse(type_name)

    # generate random decimal
    return random_decimal(precision, scale)


def map_timestamp(type_name):
    """Generate timestamp with unit and timezone.

    Args:
        type_name (str): timestamp type. e.g "timestamp(s,Asia/Shanghai)"

    """
    unit, timezone = parse(type_name)

    return random_timestamp(unit, timezone)
