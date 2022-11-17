"""Test database class."""

from delibird.database.db import Database


def test_database():
    """Test database class."""
    my_database = Database()

    my_database.connect("postgresql", "test", "test123", "localhost", "5432", "delibird")
