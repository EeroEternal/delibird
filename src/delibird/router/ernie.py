"""百度文心."""
from delibird.log import Log
import aiohttp
import json
from .base import Base
from fastapi.responses import StreamingResponse


class Ernie(Base):
    def __init__(self):
        super().__init__()
        self.access_token = ""

    def read_config(self, config, modal):
        """读取配置文件.

        Args:
            config: 配置文件
            modal: 模型名称。格式为 v4、8k、bot、speed、turbo
        return:
            (bool, str): (True, "success") or (False, "error message")
        """
        result, message = super().read_config(config, "ernie", modal)

        if not result:
            return (result, message)

        if not config.get("ernie"):
            return (False, "ernie 配置项不存在")

        # get access token
        access_token = config.get("ernie").get("access_token")
        if not access_token:
            return (False, "access_token 不存在")
        self.access_token = access_token

        # read url prefix
        url_prefix = config.get("ernie").get("url_prefix")
        if not url_prefix:
            return (False, "url_prefix 不能为空")

        modal_config = config.get("ernie").get(modal)
        if not modal_config:
            return (False, "modal section 配置项不存在")

        # get url_suffix
        url_suffix = modal_config.get("url_suffix")
        if not url_suffix:
            return (False, "url_suffox 不能为空")

        # 根据 url_prefix 最后是否有 "/" 来决定是否添加 "/"
        if url_prefix[-1] == "/":
            url = url_prefix + url_suffix
        else:
            url = url_prefix + "/" + url_suffix

        # 为 url 添加 access_token，这个是父类实例的 url
        self.url = url + "?access_token=" + self.access_token
        return (True, "success")

    async def send(self, messages, chunk_size=512):
        """发送.

        Args:
            messages: 发送的消息。格式为 [ {"role": "user", "content": "Python 如何实现异步编程"}]
            chunk_size: 流式读取分块的大小。百度返回的是一个 json 结构
        """
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


def send(config, request):
    """发送请求.

    Args:
        config: 配置文件
        request: 请求参数.格式为 {"chat": messages, "modal": "turbo"}
    """
    ernie = Ernie()
    logger = Log("delibird")

    # 从 requeust 中获取 modal 和 messages
    modal = request.get("modal")
    messages = request.get("chat")

    if not modal or not messages:
        logger.echo("modal 或 messages 不存在", "error")
        return "modal 或 messages 不存在"

    # 读取配置文件
    result, message = ernie.read_config(config, modal)
    if not result:
        logger.echo(message, "error")
        return "读取配置文件失败"

    # 发送请求
    return StreamingResponse(ernie.send(messages), media_type="text/event-stream")
