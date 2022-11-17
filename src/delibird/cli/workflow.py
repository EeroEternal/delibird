"""Read parquet file and write to database,config file is yaml format."""


import click
import yaml

from delibird.work import read_directory, read_parquet, write_directory, write_parquet


# pylint:disable=too-many-branches
def workflow(yaml_file):
    """Read parquet file and write to database, config file is yaml format.

    Args:
        yaml_file (str): yaml file with path
        conn (db.connection): database connection
    """
    # read yaml config file
    with open(yaml_file, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if "workflows" not in config:
        click.echo("no workflow in config file")

    # read workflows
    workflows = config["workflows"]

    for flow in workflows:
        # get direction
        if "direction" in flow and flow["direction"]:
            direction = flow["direction"]

            if direction == "table":
                if "read-type" in flow and flow["read-type"]:
                    read_type = flow["read-type"]
                else:
                    click.echo("read-type is required")
                    continue

                if read_type == "file":
                    # read file , write to table
                    if "filepath" in flow:
                        # pylint:disable=line-too-long
                        click.echo(
                            f'begin read file {flow["filepath"]}, write to table'
                            f' {flow["table-name"]}'
                        )
                        read_parquet(flow["filepath"], flow["dsn"], flow["table-name"], engine=flow["engine"])
                        click.echo("finish")
                    else:
                        click.echo("no filepath in workflow")
                elif read_type == "directory":
                    # read parquets from directory, write to table
                    if "filepath" in flow:
                        # pylint:disable=line-too-long
                        click.echo(
                            f'begin read file {flow["filepath"]}, write to'
                            f' {flow["table-name"]}'
                        )
                        read_directory(
                            flow["directory"], flow["dsn"], flow["table-name"], engine=flow["engine"]
                        )
                        click.echo("finish")
                    else:
                        click.echo("no directory in workflow")

            elif direction == "file":
                # read from table ,write to file
                if "filepath" in flow:
                    if "batch-size" in flow:
                        # pylint: disable=line-too-long
                        click.echo(
                            f'begin read table {flow["table-name"]}, write to file'
                            f' {flow["filepath"]} batch {flow["batch_size"]}'
                        )
                        write_parquet(
                            flow["filepath"],
                            flow["dsn"],
                            flow["table-name"],
                            engine=flow["engine"],
                            batch_size=flow["batch_size"],
                        )
                        click.echo("finish")
                    else:
                        click.echo(
                            f'begin read table {flow["table-name"]}, write to file'
                            f' {flow["filepath"]}'
                        )
                        # pylint: disable=line-too-long
                        write_parquet(flow["filepath"], flow["dsn"], flow["table-name"], engine=flow["engine"])
                        click.echo("finish")
                else:
                    click.echo("no filepath in workflow")
            elif direction == "directory":
                # read from table, write to directory
                if "directory" in flow:
                    # pylint: disable=line-too-long
                    click.echo(
                        f'begin read table {flow["table-name"]}, write to directory'
                        f' {flow["directory"]}'
                    )
                    write_directory(flow["directory"], flow["dsn"], flow["table-name"], engine=flow["engine"])
                    click.echo("finish")
                else:
                    click.echo("no directory in workflow")
