"""Date type generate."""
from datetime import timedelta
from random import randrange


def date_gen(start_day, end_day):
    """Generate random day between start and end day.

    Args:
        start_day (datatime.date): start day
        end_day (datetime.date): end day
    Returns:
        datetime.date: random day
    """
    delta = (end_day - start_day).days

    # random day between start and end day
    return start_day + timedelta(days=randrange(delta))
