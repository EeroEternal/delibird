"""DB API wrapper."""
from .connection import Connection
from .mysql import dsn_to_args


class Database:
    """Database class."""

    def __init__(self, engine="postgresql"):
        """Initialize the database.

        Args:
            engine (str): 'postgresql','mysql','sqlite'.default is 'postgresql'
        """
        self.engine = engine
        self.apilevel = "1.0"
        self.threadsafety = 2
        self.paramstyle = "pyformat"

    def dpapi_compliance(self, api_level, thread_safety, param_style):
        """DB API compliance.
        according to  https://peps.python.org/pep-0249/

        Args:
            api_level (str): DB API level
            thread_safety (int): thread safety
            param_style (str): paramstyle
        """
        self.apilevel = api_level
        self.threadsafety = thread_safety
        self.paramstyle = param_style

    @classmethod
    def connect(cls, engine, *args,  **kwargs):
        """Connect to database.

        Args:
            engine (str): engine
        """
        if engine == 'mysql':
            if len(kwargs) == 0 and len(args) == 1:
                dsn_to_args(args[0], kwargs)
            return Connection(engine, **kwargs)
        # pylint: disable = too-many-function-args
        return Connection(engine, *args, **kwargs)
