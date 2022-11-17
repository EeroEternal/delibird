"""Test mock table."""


import pytest
import yaml

from delibird.cli import mock_data
from delibird.database import db, table_exist


@pytest.mark.parametrize(
    "mock_file",
    [("./tests/yamls/mock_table.yaml")],
)
def test_mock_table(mock_file):
    """Test generate mock data and write to table.

    Args:
        mock_file (str): workflow yaml config file
    """
    # get table name from mock yaml
    with(open(mock_file, "r", encoding="utf-8")) as mock:
        config = yaml.load(mock, Loader=yaml.FullLoader)

    if "mocks" not in config:
        print("mock file no mocks workflow")
        assert False

    # get mock table name
    tables = []
    for mock in config["mocks"]:
        if "direction" not in mock:
            print("mock file no direction")
            assert False
        if mock["direction"] == "table":
            # check table name
            if "table-name" not in mock:
                print("mock file no table-name")
                assert False

            # check dns
            if "dsn" not in mock:
                print("mock file no dsn")
                assert False

            #check row number
            if "row-number" not in mock:
                print("mock file no row-number")
                assert False

            tables.append((mock["table-name"], mock["dsn"], mock["row-number"]))
        else:
            print("mock file direction is not table")
            assert False

    # truncate mock table
    for table in tables:
        table_name , dsn, _ = table
        conn = db.connect(dsn)
        if not conn:
            print("connect database failed")
            assert False

        # check table exist
        if table_exist(conn, table_name):

            # truncate table
            truncate_sql = f"truncate table {table_name}"

            # db connect
            conn = db.connect(dsn)
            if not conn:
                print('connect database failed')
                assert False

            # execute and clean
            cursor = conn.cursor()
            cursor.execute(truncate_sql)
            conn.commit()
            cursor.close()
            conn.close()

    # execute mock table
    mock_data(mock_file)

    # need to check table and table count
    for table in tables:
        table_name, dsn, row_number = table
        conn = db.connect(dsn)
        if not conn:
            print("connect database failed")
            assert False

        if not table_exist(conn,table_name):
            print("table not exist")
            assert False

        cursor = conn.cursor()
        cursor.execute(f"select count(*) from {table_name}")
        count = cursor.fetchone()[0]
        cursor.close()

        if count != row_number:
            print("table count not match")
            assert False

        conn.close()
