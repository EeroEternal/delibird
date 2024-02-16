"""Router 入口类."""
import tomllib
from delibird.log import Log
from fastapi.responses import StreamingResponse
from .base import Base
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
        logger = Log("delibird")

        # 根据 router 从 self.__routers 中获取对应的 driver
        driver_name = self._driver_name(router)
        if not driver_name:
            return f"{router} 对应的 driver 不存在"

        # 根据 driver 获取对应的类
        router_object = Base(class_type=driver_name)  # type: ignore

        if not router_object:
            return "实例化失败"

        # 获取 driver 对应的配置
        driver_config = self._driver_config(driver_name)

        if not driver_config:
            return f"{driver_name} 对应的配置不存在"

        result, message = router_object.read_config(driver_config)
        if not result:
            logger.echo(message, "error")
            return message

        return StreamingResponse(
            router_object.send(messages, model), media_type="text/event-stream"
        )

    def _driver_name(self, router):
        """根据 router 获取对应的 driver."""
        for item in self.__routers:
            if item.get("name") == router:
                return item.get("driver")

        return None

    def _driver_config(self, driver_name):
        """根据 driver_name 获取对应的配置."""
        driver_config = self._drivers.get(driver_name)
        return driver_config if driver_config else None

    def _check_drivers(self):
        """检查读取的规则是否正确.

        routers 对应的 drives 是否存在.
        """

        for router in self.__routers:
            if router.get("driver") not in self._drivers:
                return (False, f"{router['name']} 对应的 driver 不存在")
        return (True, "success")
