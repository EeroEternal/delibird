"""Generate stock or fund code."""

from random import choice, randrange


def china_code(exchange):
    """Generate china stock code.

    Args:
        exchange (str): exchange. "sh":shanghai, "sz":shenzhen

    Returns:
        str : stock code
    """
    low_code = randrange(999)

    if exchange == "sh":
        # 600 or 603
        high_code = choice(["600", "603"])
    elif exchange == "sz":
        high_code = "000"

    # low code with fix length 3, eg: 001, 023
    return f"{high_code}{low_code:0>3}"
