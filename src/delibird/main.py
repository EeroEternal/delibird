import click
import psutil

from llmproxy.server import app
from log import Log, LogLevel
from llmproxy.pm import kill_process, http_process
from llmproxy.config import read_config


@click.group()
def cli():
    pass


@cli.command()
@click.option("--config", "-c", type=click.Path(exists=True), help="指定配置文件路径")
def start(config):
    # init log
    logger = Log("llmproxy")

    # print and log
    logger.echo("Starting...")
    click.echo("Starting...")

    # check if the program is running
    if check_process("llmproxy"):
        logger.echo("The program is already running", "error")
        click.echo("The program is already running")
        return

    # 从配置文件中读取 server 配置， host 和 port
    config_info = read_config(config)

    host = config_info.get("server", {}).get("host", "localhost")
    port = config_info.get("server", {}).get("port", 8000)

    # Start the http server
    http_process(config, host, port)

    # Print and log
    logger.echo("Started")
    click.echo("Started")


@cli.command()
def stop():
    # get logger
    logger = Log("llmproxy")

    # print and log
    logger.echo("Stopping...")
    click.echo("Stopping...")

    # kill the process
    kill_process()

    # log and close
    logger.echo("Stopped")
    click.echo("Stopped")


def check_process(process_name):
    for proc in psutil.process_iter():
        print(f"proc name: {proc.name()}")
        if process_name in proc.name():
            return True
    return False


if __name__ == "__main__":
    cli()
