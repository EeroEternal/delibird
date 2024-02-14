"""百度文心."""
from delibird.log import Log
import aiohttp
import json
from .base import Base
from fastapi.responses import StreamingResponse

url_map = {
    "v4": "completions_pro",
    "8k": "ernie_bot_8k",
    "bot": "completions",
    "speed": "ernie_speed",
}


class Ernie(Base):
    def __init__(self):
        super().__init__()
        self.access_token = ""

    def read_config(self, config):
        """读取配置文件.

        Args:
            config: 配置文件
        return:
            (bool, str): (True, "success") or (False, "error message")
        """
        result, message = super().read_config(config)

        if not result:
            return (result, message)

        # get access token
        access_token = config.get("access_token")
        if not access_token:
            return (False, "access_token 不存在")
        self.access_token = access_token

        # read url
        url = config.get("url")
        if not url:
            return (False, "url不能为空")

        self.url = url
        return (True, "success")

    def _create_url(self, model):
        logger = Log("delibird")

        # 根据 model 从 url_map 中获取对应的 url_suffix
        url_suffix = url_map.get(model)
        if not url_suffix:
            logger.echo(f"model: {model} 不存在", "error")
            return ""

        # 根据 url_prefix 最后是否有 "/" 来决定是否添加 "/"
        if self.url[-1] == "/":
            self.url = self.url + url_suffix
        else:
            self.url = self.url + "/" + url_suffix

        # 为 url 添加 access_token，这个是父类实例的 url
        self.url = self.url + "?access_token=" + self.access_token

    async def send(self, messages, model, chunk_size=512):
        """发送.

        Args:
            messages: 发送的消息。格式为 [ {"role": "user", "content": "Python 如何实现异步编程"}]
            chunk_size: 流式读取分块的大小。百度返回的是一个 json 结构
        """
        # 创建 url
        self._create_url(model)

        # 消费父类的 send 方法
        async for data in super().send(messages, chunk_size):
            # 去掉开头的 data: 字符串
            data = data[5:]
            # 去掉结尾的 /n/n 字符串
            data = data[:-2]

            # 将 json 字符串转换为字典
            try:
                data = json.loads(data)

                # 获取 data 中 result 字段返回
                result = data.get("result")

                # 返回 result 字段
                yield result

            except json.JSONDecodeError as e:
                logger = Log("delibird")
                logger.echo(f"json 解析错误: {e}", "error")
                yield ""
