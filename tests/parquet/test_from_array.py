"""Test arrow parquet write meta."""

import pyarrow as pa

from delibird.util.show import show


def test_from_array():
    """Test recordbatch from array."""

    codes = pa.array(["600001", "600002", "600003"], type=pa.string())

    times = pa.array(
        [1662957998.173656, 1662257998.173656, 1661957998.173656],
        type=pa.timestamp("us", tz="Asia/Shanghai"),
    )

    names = ["code", "time"]

    batch = pa.RecordBatch.from_arrays([codes, times], names=names)

    show(f"\r{batch.to_pandas()}")
