import click
import psutil
import subprocess

from delibird.server import app
from delibird.log import Log, LogLevel
from delibird.pm import kill_process, http_process
from delibird.config import read_config


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--config", "-c", type=click.Path(exists=True), help="指定配置文件", required=True
)
def start(config):
    # init log
    logger = Log("delibird")

    # print and log
    logger.echo("Starting...")
    click.echo("Starting...")

    # check if the program is running
    if check_process("delibird"):
        logger.echo("The program is already running", "error")
        click.echo("The program is already running")
        return

    if not config:
        click.echo("没有配置文件")
        return

    # 从配置文件中读取 server 配置， host 和 port
    config_info = read_config(config)

    host = config_info.get("server", {}).get("host")
    port = config_info.get("server", {}).get("port")

    # check if host or port is null
    if not host or not port:
        logger.echo("host or port is null", "error")
        click.echo("host or port is null")
        return

    # Start the http server
    http_process(config, host, port)

    # Print and log
    logger.echo("Started")
    click.echo("Started")


@cli.command()
def stop():
    # get logger
    logger = Log("delibird")

    # print and log
    logger.echo("Stopping...")
    click.echo("Stopping...")

    # check if the program is running
    if not check_process("delibird"):
        click.echo("The program is not running")
        return

    # kill the process
    kill_process()

    # log and close
    logger.echo("Stopped")
    click.echo("Stopped")


def check_process(process_name):
    result = subprocess.run(
        ["pgrep", "-f", process_name], capture_output=True, text=True
    )

    # 如果pgrep命令的输出不是空的，则有匹配的进程正在运行
    return bool(result.stdout.strip())
