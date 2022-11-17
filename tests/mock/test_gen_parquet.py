"""Generate parquet directory datasets."""


from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from delibird.mock import gen_dict, schema_from_dict


@pytest.mark.parametrize(
    "row_number, columns, directory",
    [
        (
            2048,
            {
                # stock code as a type
                "sec_code": "code",  # "600001"
                "date": "date",  # 2022-08-24
                "close": "float",  # 16.87
                "open": "float",  # 16.65
                "high": "float",  # 16.95
                "low": "float",  # 16.55
                "hold": "decimal(10,5)",  # 123.25515
                # datetime.datetime(2022,10,25).timestamp()
                "time": "timestample(unit='s',tz='Asia/Shanghai')",
                "volume": "int",  # 1530231
                "amount": "int",  # 2571196416
            },
            "./datasets/gen/stocks",
        ),
    ],
)
def test_gen_parquet(row_number, columns, directory):
    """Generate sample parquet directory datasets.

    Args:
        row_number (int): number of rows
        columns (dict): columns and types
        dir (str): directory path for parquet files
    """
    dir_ = Path(directory)

    # check directory exist
    if not dir_.is_dir():
        print("directory not exist, create it")
        dir_.mkdir(parents=True)

    # arrow schema
    arrow_schema = schema_from_dict(columns)

    dict_list = gen_dict(columns, row_number)
    print(f"generate dict length:{len(dict_list)}\n")

    # python dict to py table
    table = pa.Table.from_pylist(dict_list)

    # write to parquet file in directory
    pq.write_to_dataset(
        table,
        dir_,
        schema=arrow_schema,
        use_legacy_dataset=False,
        existing_data_behavior="overwrite_or_ignore",
    )

    assert True
