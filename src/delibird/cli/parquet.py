"""Read parquet file."""

from pathlib import Path

import click

from delibird.work import read_directory, read_parquet, write_directory, write_parquet


@click.group()
def parquet():
    """Write or read Parquet file or directory."""


@parquet.command()
@click.argument("path", type=click.Path(exists=True, file_okay=True, dir_okay=True))
@click.option("-e", "--engine", default="postgresql", type=str)
@click.argument("dsn")
@click.argument("table_name")
def read(path, engine, dsn, table_name):
    """Read parquet file, write to database.

    dsn sample:postgresql://user:password@host:port/dbname.
    """
    if Path(path).is_dir():
        read_directory(path, dsn, table_name, engine)

    if Path(path).is_file():
        read_parquet(path, dsn, table_name, engine)


@parquet.command()
@click.argument("path", type=click.Path(file_okay=True, dir_okay=True))
@click.option("-e", "--engine", default="postgresql", type=str)
@click.argument("dsn")
@click.argument("table_name")
@click.option("-s", "--batch_size", default=1024 * 1024, type=int)
def write(path, engine, dsn, table_name, batch_size):
    """Read from database and write to parquet file.

    dsn sample:postgresql://user:password@host:port/dbname.
    """
    path_obj = Path(path)
    if path_obj.exists() is False:
        # check dir or file
        if path_obj.suffix == ".parquet":
            write_parquet(path, engine, dsn, table_name, batch_size)
        else:
            write_directory(path, engine, dsn, table_name, batch_size)
    else:
        # file or directory exist
        if path_obj.is_dir():
            write_directory(path, engine, dsn, table_name, batch_size)
        if path_obj.is_file():
            write_parquet(path, engine, dsn, table_name, batch_size)
