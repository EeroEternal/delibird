"""Parse data type from file."""

from magicbag import prefix_check

meta_types = ("int", "string", "float", "date", "datetime", "decimal", "timestamp")


def parse(type_name):
    """Get argument from literal.

    Args:
        type_name (str): input string. e.g "decimal(10,5)"
    Returns:
        tuple(str): argument. e.g "10,5"
    """
    # check literal start with category prefix
    # result is "decimal", not "decimal(10,5)"
    result = prefix_check(type_name, meta_types)

    if result[0]:
        # call parser function by type name

        # parser is Class Parser's instance
        parser = Parser(type_name)

        # get parser function by type name
        func = getattr(parser, f"parse_{result[1]}")

        # call parser function
        return func()

    return None


class Parser:
    """Parse data type from file."""

    def __init__(self, type_name):
        """Init parser.

        Args:
            type_name (str): data type name define
        """
        self.type_name = type_name

    def parse_int(self):
        """Parse int type, get fix length.

        int(10) means fix length 10, return 10
        int return None

        Returns:
            int: fix length
        """
        if not self.type_name.startswith("int"):
            return None

        if len(self.type_name) == 3:
            return None

        # get "10" from "int(10)" and return
        try:
            return int(self.type_name.split("(")[1].split(")")[0])
        except ValueError:
            return None

    def parse_float(self):
        """Parse float str, get precision.

        float(100,1000) return 100, 1000
        float return None, None

        Returns:
            int,int: start, end
        """
        if not self.type_name.startswith("float"):
            return None

        # check if it has range
        if len(self.type_name) == 5:
            return None, None

        # get "-10, 100" from "float(-10, 100)"
        try:
            content = self.type_name.split("(")[1].split(")")[0]

            # get start and end
            start, end = content.split(",")

            # return as integer
            return int(start), int(end)
        except ValueError:
            return None, None

    def parse_string(self):
        """Parse string str, get float precision.

        string(100) return max length 100
        string return None

        Returns:
            int: string max length
        """
        if not self.type_name.startswith("string"):
            return None

        if len(self.type_name) == 6:
            return None

        # get "10" from "float10"
        try:
            return int(self.type_name[5:].strip())
        except ValueError:
            return None

    def parse_decimal(self):
        """Parse decimal str, get precision and scale.

        decimal(10,5) return 10, 5
        decimal return None, None

        Returns:
            int,int: precision, scale
        """
        if not self.type_name.startswith("decimal"):
            return None

        try:
            # get "10,5" from "decimal(10,5)"
            data = self.type_name.split("(")[1].split(")")[0]

            # get precision and scale
            precision_str, scale_str = data.split(",")

            return int(precision_str), int(scale_str)
        except ValueError:
            return None, None

    def parse_timestamp(self):
        """Parse timestamp str, get unit and timezone.

        Returns:
            str,str: unit, timezone
        """
        if not self.type_name.startswith("timestamp"):
            return None

        # if no argument, return default value
        if len(self.type_name) == 9:
            return "s", "UTC"

        try:
            # get "unit='s',tz='Asia/Shanghai'" from "timestamp(unit=s,tz=Asia/Shanghai)"
            data = self.type_name.split("(")[1].split(")")[0]

            # get unit and timezone
            unit, timezone = data.split(",")

            # get unit and timezone value .remember remove double quote
            unit, timezone = unit.split("=")[1].strip(""), timezone.split("=")[1].strip("")

            return unit, timezone
        except ValueError:
            return None, None

    def parse_datetime(self):
        """Parse datetime str, get unit and timezone.

        Returns:
            str: timezone
        """
        if not self.type_name.startswith("datetime"):
            return None

        # if no argument, return default value
        if len(self.type_name) == 8:
            return "UTC"

        # get "tz='Asia/Shanghai'" from "datetime(tz=Asia/Shanghai)"
        data = self.type_name.split("(")[1].split(")")[0]

        # remove bracket in "'Asia/Shanghai'"
        timezone = data.split("=")[1].strip("")

        return timezone
