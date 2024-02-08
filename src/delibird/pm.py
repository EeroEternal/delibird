""""Process Manager"""

import os
import subprocess
from multiprocessing import Process, cpu_count
from delibird.config import read_config


def kill_process():
    # Kill process named 'delibird' if it exists
    os.system("pkill -f delibird")


def http_process(config_file, host, port):
    # 不占满所有的 cpu
    cpu_cores = cpu_count() - 1

    # Start http server use gunicorn
    command = [
        "gunicorn",
        "--env",
        f"CONFIG_FILE={config_file}",
        "-w",
        str(cpu_cores),
        "-k",
        "uvicorn.workers.UvicornWorker",
        "-b",
        f"{host}:{port}",
        "delibird.server:app",
        "--timeout",
        "60",
    ]

    # Start the process
    process = subprocess.Popen(
        command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
