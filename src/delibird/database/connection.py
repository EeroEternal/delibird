"""Database connection."""


class Connection:
    """Wrapper for a connection to the database."""

    def __init__(self, engine, *args, **kwargs):
        """Initialize the connection.

        Args:
            engine (str): database engine

        """
        self.engine = engine
        self.autocommit = False
        if engine == "postgresql":
            # pylint: disable = import-outside-toplevel
            import psycopg

            self._conn = psycopg.connect(*args, **kwargs)
        elif engine == "oracle":
            # pylint: disable = import-outside-toplevel
            import oracledb

            oracledb.init_oracle_client()
            self._conn = oracledb.connect(*args, **kwargs)
        elif engine == 'mysql':
            # pylint: disable = import-outside-toplevel
            import pymysql

            self._conn = pymysql.connect(*args, **kwargs)

    @classmethod
    def connection(cls, *args, **kwargs):
        """Connect to the database."""
        raise NotImplementedError

    def __enter__(self):
        """Enter the connection."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the connection."""
        self.close()

    def close(self):
        """Close the connection."""
        self._conn.close()

    def cursor(self, dict_row_flag=False):
        """Get the cursor of the connection."""
        if self.autocommit is True:
            if engine == "mysql":
                self._conn.autocommit(True)
            else:
                self._conn.autocommit = True
        engine = self.engine
        if engine == "postgresql":
            if dict_row_flag is True:
                # pylint: disable = import-outside-toplevel
                from psycopg.rows import dict_row

                _cursor = self._conn.cursor(row_factory=dict_row)
            else:
                _cursor = self._conn.cursor()
        elif engine == "oracle":
            _cursor = self._conn.cursor()
            if dict_row_flag is True:
                _cursor.rowfactory = \
                    lambda *args: dict(zip([d[0] for d in _cursor.description], args))
        elif engine == "mysql":
            if dict_row_flag is True:
                # pylint: disable = import-outside-toplevel
                from pymysql.cursors import DictCursor

                _cursor = self._conn.cursor(DictCursor)
            else:
                _cursor = self._conn.cursor()
        return _cursor

    def commit(self):
        """commit"""
        self._conn.commit()
