"""Test arrow parquet write meta."""

import pyarrow as pa
import pyarrow.parquet as pq


def test_arrow_meta():
    """Test arrow parquet write."""

    table = pa.table(
        {
            "n_legs": [2, 2, 4, 4, 5, 100],
            "animal": [
                "Flamingo",
                "Parrot",
                "Dog",
                "Horse",
                "Brittle stars",
                "Centipede",
            ],
        }
    )

    metadata_collector = []

    pq.write_to_dataset(
        table, "datasets/arrow/dataset_metadata", metadata_collector=metadata_collector
    )

    pq.write_metadata(table.schema, "datasets/arrow/dataset_metadata/_common_metadata")

    pq.write_metadata(
        table.schema,
        "datasets/arrow/dataset_metadata/_metadata",
        metadata_collector=metadata_collector,
    )
