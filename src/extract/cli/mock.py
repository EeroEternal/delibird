"""Mock data to directory , file, or database."""
import yaml

from delibird.util.show import show
from delibird.work import mock_write_directory, mock_write_parquet, mock_write_table


def mock_data(mock_file):
    """Mock data to directory , file, or database.

    Args:
        mock_file (str): mock data config file, yaml format
    """
    # read mock config file
    if not mock_file:
        show("yaml file is required")
        return

    with open(mock_file, "r", encoding="utf-8") as mock:
        config = yaml.load(mock, Loader=yaml.FullLoader)

    if "mocks" not in config:
        show("no mock or direction in config file")
        return

    mocks = config["mocks"]

    # get common keys from mocks
    for mock in mocks:
        # check keys in yaml
        if not all(key in mock for key in ("columns", "row-number", "direction")):
            show("directory, columns and  row-number is required")
            return

        direction = mock["direction"]
        row_number = mock["row-number"]
        columns = mock["columns"]

        # write to file
        if direction == "file":
            # check keys
            if "filepath" not in mock or not mock["filepath"]:
                show("filepath is required")
                continue

            # write file
            mock_write_parquet(mock["filepath"], columns, row_number)
        # write to directory
        if direction == "directory":
            # check keys
            if "directory" not in mock or not mock["directory"]:
                show("directory is required")
                continue

            # write directory
            mock_write_directory(mock["directory"], columns, row_number)

        # write to table
        if direction == "table":
            if not all(key in mock for key in ("dsn", "table-name")):
                show("dsn and table-name is required")
                continue

            engine = mock["engine"]
            if not engine:
                engine = "postgresql"
            mock_write_table(engine, mock["dsn"], mock["table-name"], columns, row_number)
