"""Router 入口类."""
import tomllib
from delibird.util import Log
from fastapi.responses import StreamingResponse
from delibird.driver import *

import sys


class Gateway:
    def __init__(self):
        self.__routers = []
        self._configs = {}

    def read_config(self, config_file):
        """读取配置文件.

        Args:
            config_file: str, 配置文件路径
        """
        logger = Log("delibird")

        # 读取 config 文件
        file = open(config_file, "rb")
        # check file
        if not file:
            logger.echo("配置文件没找到", "error")
            return
        config = tomllib.load(file)

        # 读取 server 项
        server = config.get("server")
        if not server:
            logger.echo("server is None", "error")
            return

        # 读取 routers
        routers = server.get("routers")
        if not routers:
            logger.echo("routers is None", "error")
            return

        # 读取 drivers
        configs = config.get("config")
        if not configs:
            logger.echo("configs is None", "error")
            return

        # set routers
        self.__routers = routers

        # set drives
        self._configs = configs

    def send(self, router, messages, model):
        """对不同的 router 发送请求."""
        # 根据 router 获取 driver 名称.
        # self._routers 是一个数组
        driver_names = [
            item.get("driver") for item in self.__routers if item.get("name") == router
        ]

        # 如果 driver_names 长度不为 1，说明配置文件中有重复的 router
        if len(driver_names) != 1:
            return "配置文件中有重复的 router 或者没有对应的 driver"

        # 获取 driver 名称
        driver_name = driver_names[0]

        # 根据 driver 获取对应的类
        driver_name = driver_name.capitalize()
        if driver_name == "Base":
            driver_object = Base()
        else:
            driver_object = Base(class_type=driver_name)  # type: ignore

        if not driver_object:
            return "实例化失败"

        # 获取 router 对应的配置
        router_config = self._configs.get(router)
        if not router_config:
            return f"{router_config} 对应的配置不存在"

        result, message = driver_object.read_config(router_config)
        if not result:
            return message

        return StreamingResponse(
            driver_object.send(messages, model), media_type="text/event-stream"
        )
