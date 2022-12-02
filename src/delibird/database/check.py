"""Check database or table if existed."""


def check_database(conn, database_name):
    """Check database if exist,if not create it.

    Args:
        conn (db.connection): database connection handler
        database_name (_type_): _description_
    """
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("select datname from pg_database;")

    databases = [item[0] for item in cur.fetchall()]

    if database_name not in databases:
        cur.execute(f"create database {database_name}")

    # postgresql doesn't need use database
    # cur.execute(f"use {database_name}")

    conn.commit()


def table_exist(conn, table_name):
    """Check table if existed.

    Args:
        conn (db.connection): database connection handler
        table_name (str): table name

    Returns:
        bool: True if table exist, False if not
    """
    engine = conn.engine
    if engine == "postgresql":
        sql = f"select * from pg_tables WHERE tablename ='{table_name}'"
    elif engine == "oracle":
        sql = f"select * from user_tables WHERE table_name = '{table_name.upper()}'"
    elif engine == "mysql":
        sql = f"SELECT table_name FROM information_schema.tables WHERE table_schema = (SELECT DATABASE()) and table_name = '{table_name}'"
    with conn.cursor() as cur:
        # check table if exist
        cur.execute(sql)
        result = cur.fetchone()

        if result is None:
            return False

        return True
