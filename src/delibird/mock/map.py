"""Type map for mock objects."""

import random
import string

from magicbag import (
    prefix_check,
    random_date,
    random_decimal,
    random_fixed_int,
    random_timestamp,
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

        # mapper is Class Mapper's instance
        mapper = Mapper(type_name)

        # get generate function by type name. result[1] is "decimal"
        func = getattr(mapper, f"map_{result[1]}")

        # call generate function
        return func()

    # not match any type, return None
    return None


class Mapper:
    """Map type to value."""

    def __init__(self, type_name):
        """Init.

        Args:
            type_name (str): type name. e.g "int(10)"
        """
        self.type_name = type_name

    def map_int(self):
        """Generate random int.

        if type_name is "int", return random int between 0 and 10000
        if type_name is "int(10)", return random fixed length int with 10 digits

        Returns:
            int: random int
        """
        fix_length = parse(self.type_name)

        if fix_length:
            return random_fixed_int(fix_length)

        # default int is between 0 and 10000
        return random.randint(0, 10000)

    def map_string(self):
        """Generate random string.

        Returns:
            str: random string
        """
        max_length = parse(self.type_name)

        if max_length is None:
            max_length = 255

        letters = string.ascii_lowercase

        use_length = random.randint(1, max_length)

        return "".join(random.choice(letters) for i in range(use_length))

    def map_float(self):
        """Generate random float with precision.

        Returns:
            float: random float
        """
        start, end = parse(self.type_name)

        # if not precision, return random float
        if start is None:
            start = 0
            end = 10000

        # return random float between start and end
        return start + (end - start) * random.random()

    @staticmethod
    def map_date():
        """Generate random date.

        Returns:
            datetime.date: random date
        """
        return random_date()

    def map_datetime(self):
        """Generate datetime with unit and timezone.

        Returns:
            datetime.datetime: random datetime
        """
        unit, timezone = parse(self.type_name)

        return random_timestamp(unit, timezone)

    def map_decimal(self):
        """Generate decimal with precision and scale.

        Returns:
            Decimal : decimal value
        """
        # python no scale define
        precision, scale = parse(self.type_name)

        # generate random decimal
        return random_decimal(precision, scale)

    def map_timestamp(self):
        """Generate timestamp with unit and timezone."""
        unit, timezone = parse(self.type_name)

        # check if timezone is str type
        if not isinstance(timezone, str):
            raise TypeError("timezone must be str type")

        return random_timestamp(unit, timezone)
