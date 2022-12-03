"""Datetime type."""

from datetime import datetime

import pytz


def now_timestamp(unit, timezone):
    """Generate random timestamp with unit and timezone.

    Args:
        unit (str): unit of timestamp. e.g "s", "ms", "us", "ns"
        timezone (str): timezone of timestamp. e.g "Asia/Shanghai"
    """
    # get current timestamp
    zone = pytz.timezone(timezone)
    default = datetime.now(tz=zone).timestamp()

    # unit to timestamp
    if unit == "ms":
        default = default * 1000
    elif unit == "us":
        default = default * 1000000
    elif unit == "ns":
        default = default * 1000000000

    # random timestamp
    return datetime.fromtimestamp(default, tz=zone)
