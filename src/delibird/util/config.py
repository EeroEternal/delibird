"""Read toml configuration from file."""
import tomllib


def read_config(filepath):
    """Read configuration from file."""

    # Read configuration from file
    with open(filepath, "rb") as file:
        config = tomllib.load(file)

    # Return configuration
    return config
