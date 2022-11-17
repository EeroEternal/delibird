"""Database cursor"""


class Cursor:
    """Wrapper for a cursor to the database connection."""

    def __init__(self, connection):
        """Initialize the cursor of connection.

        Args:
            connection (Connection): database connection

        """
        engine = connection.engine
        self.engine = engine
        if engine == "postgresql":
            # pylint: disable = import-outside-toplevel
            from psycopg.rows import dict_row

            self._cursor = connection._conn.cursor(row_factory=dict_row)
        elif engine == "oracle":
            self._cursor = connection._conn.cursor()

    def __enter__(self):
        """Get the cursor."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the cursor."""
        self.close()

    def close(self):
        """Close the cursor."""
        self._cursor.close()

    # pylint: disable = dangerous-default-value
    def execute(self, sql, params=[], **kwargs):
        """Execute sql.

        Args:
            sql (str): sql statement
            params (list): param list

        """
        self._cursor.execute(sql, params, **kwargs)
        return self

    def executemany(self, sql, params):
        """Execute many sql

        Args:
            sql (str): sql statement
            params (list): param list

        """
        self._cursor.executemany(sql, params)

    def fetchall(self):
        """Fetch all"""
        return self._cursor.fetchall()
