"""Insert data to database."""


def insert_arrow_table(table, conn, table_name):
    """Insert arrow table to table.

    Args:
        table (pyarrow.Table): parquet row group data
        conn (db.connection): database connection
        table_name (str): tablename
    """
    # batch size for insert to table per time
    batch_size = 25

    # split dataframe to batchs and insert to table
    batches = table.to_batches(max_chunksize=batch_size)

    for batch in batches:
        insert_batch(batch, conn, table_name)


def gen_columns(engine, data):
    """Gen columns."""
    if engine == "postgresql" or engine == "mysql":
        return ",".join(["%s"] * len(data))
    elif engine == "oracle":
        return ",".join([":" + key for key in data.keys()])


def insert_list(list_data, conn, table_name):
    """Insert list data to table.

    Args:
        list_data (list): list data
        conn (db.connection): database connection
        table_name (str): tablename
    """
    # create cursor
    cursor = conn.cursor()

    # set column data as "%s", "%s", "%s"...
    columns = gen_columns(conn.engine, list_data[0])

    # insert sql
    sql_statement = f"INSERT INTO {table_name} VALUES ({columns})"

    # insert batch data to table
    cursor.executemany(sql_statement, list_data)

    # commit
    conn.commit()

    # close cursor
    cursor.close()


def gen_batch_columns(engine, batch):
    """Gen columns from batch.

    Args:
        engine (str); engine
        batch (pyarrow.table.Table): parquet table

    """
    if engine == "postgresql" or engine == "mysql":
        return ",".join(["%s"] * batch.num_columns)
    elif engine == "oracle":
        column_datas = []
        col_index = 1
        # pylint:disable=unused-variable
        for col in batch.itercolumns():
            column_datas.append(f":VAL_{col_index}")
            col_index += 1
        return ",".join(column_datas)


def insert_batch(batch, conn, table_name):
    """Insert batch data to table.

    Args:
        batch (pyarrow.RecordBatch): batch data
        conn (db.connection): database connection
        table_name (str): tablename
    """
    # create cursor
    cursor = conn.cursor()

    engine = conn.engine
    # set column data as "%s", "%s", "%s"...
    column_data = gen_batch_columns(engine, batch)

    # insert sql
    sql_statement = f"INSERT INTO {table_name} VALUES ({column_data})"

    # insert batch data to table
    all_values = table_values(engine, batch)

    cursor.executemany(sql_statement, all_values)

    # commit
    conn.commit()

    # close cursor
    cursor.close()


def table_values(engine, batch):
    """Change batch data to list of values.

    Args:
        batch (pyarrow.RecordBatch): batch data

    Returns:
        list: list of values,e.g.[(1,2,3),(4,5,6)]
    """
    values = []
    # row tuple
    for i in range(0, batch.num_rows):
        if engine == "postgresql" or engine == "mysql":
            row = ()

            # add data to row tuple
            for j in range(0, batch.num_columns):
                row += (batch.column(j)[i].as_py(),)
        elif engine == "oracle":
            row = dict()

            # put data to row dict
            for j in range(0, batch.num_columns):
                row[f"VAL_{j + 1}"] = batch.column(j)[i].as_py()

        # append row to list
        values.append(row)

    return values
