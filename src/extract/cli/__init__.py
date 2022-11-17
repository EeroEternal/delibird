"""Command line interface for the project."""

import click

from delibird.cli.mock import mock_data
from delibird.cli.parquet import parquet as _parquet
from delibird.cli.workflow import workflow as workflow_func

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="0.0.1")
def cli():
    """delibird command line interface."""


# add parquet command
cli.add_command(_parquet)


# add yaml workflow option
@cli.command()
@click.argument(
    "yaml_file", type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
def workflow(yaml_file):
    """Execute yaml workflow."""
    return workflow_func(yaml_file)


@cli.command()
@click.argument(
    "workflow-file", type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
def mock(workflow_file):
    """Mock data to directory , file, or database."""
    return mock_data(workflow_file)


__all__ = ["cli"]
