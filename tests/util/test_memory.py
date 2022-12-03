"""Test calculate safe batch size."""
import pytest

from delibird.util import calculate_size
from delibird.mock import gen_dict_one


@pytest.mark.parametrize(
    "row_number, schema",
    [
        (10000, {
            "date": "date",  # 2022-08-24
            "close": "float",  # 16.87
            "open": "float",  # 16.65
            "low": "float",  # 16.55
            "hold": "decimal(10,5)",  # 123.25515
            "time": "timestamp(unit=s,tz=Asia/Shanghai)",  # not single quote
            "volume": "int",  # 1530231
            "amount": "int",  # 2571196416
        }),
        (100000, {
            "date": "date",  # 2022-08-24
            "close": "float",  # 16.87
            "open": "float",  # 16.65
            "low": "float",  # 16.55
            "hold": "decimal(10,5)",  # 123.25515
            "time": "timestamp(unit=s,tz=Asia/Shanghai)",  # not single quote
            "volume": "int",  # 1530231
            "amount": "int",  # 2571196416
        }),
        (800000, {
            "date": "date",  # 2022-08-24
            "close": "float",  # 16.87
            "open": "float",  # 16.65
            "low": "float",  # 16.55
            "hold": "decimal(10,5)",  # 123.25515
            "time": "timestamp(unit=s,tz=Asia/Shanghai)",  # not single quote
            "volume": "int",  # 1530231
            "amount": "int",  # 2571196416
        }),
        (1000000, {
            "date": "date",  # 2022-08-24
            "close": "float",  # 16.87
            "open": "float",  # 16.65
            "low": "float",  # 16.55
            "hold": "decimal(10,5)",  # 123.25515
            "time": "timestamp(unit=s,tz=Asia/Shanghai)",  # not single quote
            "volume": "int",  # 1530231
            "amount": "int",  # 2571196416
        }),
        (8000000, {
            "date": "date",  # 2022-08-24
            "close": "float",  # 16.87
            "open": "float",  # 16.65
            "low": "float",  # 16.55
            "hold": "decimal(10,5)",  # 123.25515
            "time": "timestamp(unit=s,tz=Asia/Shanghai)",  # not single quote
            "volume": "int",  # 1530231
            "amount": "int",  # 2571196416
        }),
        (12000000, {
            "date": "date",  # 2022-08-24
            "close": "float",  # 16.87
            "open": "float",  # 16.65
            "low": "float",  # 16.55
            "hold": "decimal(10,5)",  # 123.25515
            "time": "timestamp(unit=s,tz=Asia/Shanghai)",  # not single quote
            "volume": "int",  # 1530231
            "amount": "int",  # 2571196416
        }),
        (20000000, {
            "date": "date",  # 2022-08-24
            "close": "float",  # 16.87
            "open": "float",  # 16.65
            "low": "float",  # 16.55
            "hold": "decimal(10,5)",  # 123.25515
            "time": "timestamp(unit=s,tz=Asia/Shanghai)",  # not single quote
            "volume": "int",  # 1530231
            "amount": "int",  # 2571196416
        }),

    ],
)
def test_safe_size(row_number, schema):
    """Test calculate safe batch size.

    Args:
        row_number (int): row number
        schema (dict): schema
    """
    sample_list = gen_dict_one(schema)

    size = calculate_size(sample_list, row_number)

    print(f"safe size:{size}")

# .safe size:10000
# .safe size:100000
# .safe size:339417
# .safe size:339417
# .safe size:339417
# .safe size:339417
# .safe size:339417
