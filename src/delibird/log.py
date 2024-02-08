import logging
import sys
import os
import platform
import tempfile
import pwd
from enum import Enum


# 创建一个枚举类对应 log 级别
class LogLevel:
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


def get_log_path(log_name):
    system = platform.system()

    if system == "Linux":
        # 获取当前用户的HOME目录，如果HOME环境变量未设置，则使用当前用户的HOME目录
        home_dir = os.getenv("HOME", pwd.getpwuid(os.getuid()).pw_dir)
        return os.path.join(home_dir, ".local", "share", log_name, "logs")

    elif system == "Darwin":  # macOS
        return os.path.join(
            os.path.expanduser("~"), "Library", "Logs", f"{log_name}.log"
        )
    elif system == "Windows":
        appdata = os.getenv("APPDATA")
        if appdata:
            return os.path.join(appdata, log_name, log_name, "Logs", f"{log_name}.log")
        else:
            # 如果APPDATA环境变量未设置，则采用临时目录
            return os.path.join(tempfile.gettempdir(), f"{log_name}.log")
    else:
        raise Exception(f"Unsupported operating system: {system}")


class Log:
    """日志类."""

    def __init__(self, name, level=LogLevel.DEBUG):
        """初始化日志类."""

        # 设置日志格式
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # 创建一个StreamHandler，用于输出到控制台（stdout）
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # 创建文件处理器并设置日志文件路径
        log_file_path = get_log_path("llmproxy")
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)

        # 创建一个logger 并设置日志级别
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 添加文件和控制台处理器到 logger
        self.logger.addHandler(file_handler)

    def echo(self, message: object, level="info"):
        """记录日志.

        Args:
            msg (object): 日志消息
            *args (object): 日志参数
        """
        if hasattr(logging, level):
            getattr(self.logger, level)(message)
        else:
            self.logger.warning(f"Invalid log level: {level}")
