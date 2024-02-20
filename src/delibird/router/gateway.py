"""Router 入口类."""
import tomllib
from delibird.util import Log
from fastapi.responses import StreamingResponse
from delibird.driver import *

import sys


class Gateway:
    def __init__(self):
        self.__routers = []
        self._drivers = {}

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
        driver = config.get("driver")
        if not driver:
            logger.echo("driver is None", "error")
            return

        # set routers
        self.__routers = routers

        # set drives
        self._drivers = driver

        # check drivers
        result, message = self._check_drivers()
        if not result:
            logger.echo(message, "error")

    def send(self, router, messages, model):
        """对不同的 router 发送请求."""

        # 根据 router 获取 driver 名称.
        # self._routers 是一个数组
        driver_names = [
            router.get("driver")
            for router in self.__routers
            if router.get("name") == router
        ]

        # 如果 driver_names 长度不为 1，说明配置文件中有重复的 router
        if len(driver_names) != 1:
            return "配置文件中有重复的 router"

        # 获取 driver 名称
        driver_name = driver_names[0]

        # 根据 driver 获取对应的类
        driver_name = driver_name.capitalize()
        driver_object = Base(class_type=driver_name)  # type: ignore
        if not driver_object:
            return "实例化失败"

        # 获取 router 对应的配置
        router_config = self._drivers.get(router)
        if not router_config:
            return f"{router_config} 对应的配置不存在"

        result, message = driver_object.read_config(router_config)
        if not result:
            return message

        return StreamingResponse(
            driver_object.send(messages, model), media_type="text/event-stream"
        )

    def _router_config(self, router_name):
        """根据 router_name 获取对应的配置."""
        driver_config = self._drivers.get(router_name)
        return driver_config if driver_config else None

    def _check_drivers(self):
        """检查读取的规则是否正确.

        routers 对应的 drivers 是否存在.
        """

        for router in self.__routers:
            if router.get("driver") not in self._drivers:
                return (False, f"{router['name']} 对应的 driver 不存在")
        return (True, "success")
