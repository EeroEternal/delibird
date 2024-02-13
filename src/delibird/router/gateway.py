"""Router 入口类."""
import tomllib
from delibird.log import Log
from fastapi.responses import StreamingResponse
from .qwen import Qwen
from .openai import OpenAI
from .spark import Spark
from .minimax import Minimax
from .ernie import Ernie


class Gateway:
    def __init__(self):
        self.__routes = []
        self._drives = []

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

        # 读取 routers
        routes = config.get("routes")
        if not routes:
            logger.echo("routes is None", "error")
            return

        # 读取 drives
        drives = config.get("drives")
        if not drives:
            logger.echo("drives is None", "error")
            return

        # set routes
        self.__routes = routes

        # set drives
        self._drives = drives

        # check drivers
        result, message = self._check_drivers()
        if not result:
            logger.echo(message, "error")

    def send(self, router, messages, model):
        """对不同的 router 发送请求."""

        # 根据 router 从 self.__routes 中获取对应的 driver
        driver = self._get_driver(router)
        if not driver:
            return f"{router} 对应的 driver 不存在"

        # 根据 driver 获取对应的类
        router_class = getattr(self, driver)
        if not router_class:
            return f"{driver} 对应的类不存在"

        # 调用实例化类的 read_config 和 send 方法
        router_object = router_class()
        result, message = router_object.read_config(driver)
        if not result:
            return message

        return StreamingResponse(
            router_object.send(messages), media_type="text/event-stream"
        )

    def _get_driver(self, router):
        """根据 router 获取对应的 driver."""
        for route in self.__routes:
            if route.get("name") == router:
                return route.get("driver")
            else:
                return None

    def _check_drivers(self):
        """检查读取的规则是否正确.

        routers 对应的 drives 是否存在.
        """

        for route in self.__routes:
            if route.get("driver") not in self._drives:
                return (False, f"{route['name']} 对应的 driver 不存在")
        return (True, "success")
