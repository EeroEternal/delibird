"""Decimal type."""
import decimal
from random import randint


def random_decimal(precision, scale):
    """Generate random decimal with precision and scale.

    Args:
        precision (int): precision
        scale (int): scale
    Returns:
        decimal: random decimal
    """
    # random decimal with precision and scale
    with decimal.localcontext() as ctx:
        ctx.prec = precision

        # error
        if precision < scale:
            print("precision < scale")
            return None

        # avoid randint end with 0, Decimal will less one or more
        fraction = randint(10 ** (scale - 1), 10 ** (scale) - 1)
        # pass end with 0 and 5
        while fraction % 5 == 0:
            fraction = randint(10 ** (scale - 1), 10 ** (scale) - 1)

        # return random decimal with precision and scale
        integer = randint(10 ** (precision - scale - 1), 10 ** (precision - scale) - 1)

        decimal_str = f"{integer}.{fraction}"

        decimal_result = decimal.Decimal(decimal_str)

        return decimal_result
