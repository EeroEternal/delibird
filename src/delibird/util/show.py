"""Print wrapper for print, click.echo, logging."""
import logging

import click


def show(message, level="print"):
    """Print wrapper for print, click.echo, logging.

    Args:
        message (any): message to print
        level (str, optional): print,echo,log. Default "print".\
            echo:click.echo,log:logging
    """
    if level == "print":
        print(message)

    elif level == "echo":
        click.echo(message)

    elif level == "log":
        logging.info(message)
