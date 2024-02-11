"""百度文心."""
from delibird.log import Log
import aiohttp
import json
from .base import Base
from fastapi.responses import StreamingResponse


class Ernie(Base):
    def __init__(self):
        self.access_token = ""

    def read_config(self, config, request):
        """读取配置文件.

        Args:
            config: 配置文件
            request: 请求参数.格式为 {"chat": messages, "modal": "v15"}
        return:
            bool
        """
        logger = Log("delibird")

        if not config:
            logger.echo("配置文件不存在", "error")
            return False

        if not config.get("ernie"):
            logger.echo("ernie 配置项不存在", "error")
            return False

        # get access token
        access_token = config.get("ernie").get("access_token")
        if not access_token:
            logger.echo("access_token 不能为空", "error")
            return False
        self.access_token = access_token

        # read url prefix
        url_prefix = config.get("ernie").get("url_prefix")
        if not url_prefix:
            logger.echo("url_prefix 不能为空", "error")
            return False

        # get modal name
        modal = request.get("modal")
        if not modal:
            logger.echo("modal 不存在", "error")
            return False

        self.modal = modal

        print(f"modal: {modal}")

        # get modal config
        modal_config = config.get("ernie").get(modal)
        if not modal_config:
            logger.echo("模型配置文件不存在", "error")
            return False

        # get url_suffix
        url_suffix = modal_config.get("url_suffix")
        if not url_suffix:
            logger.echo("url_suffox 不能为空", "error")
            return False

        # 根据 url_prefix 最后是否有 "/" 来决定是否添加 "/"
        if url_prefix[-1] == "/":
            self.url = url_prefix + url_suffix
        else:
            self.url = url_prefix + "/" + url_suffix

        if "chat" not in request:
            logger.echo("请求参数中不存在 chat 字段", "error")
            return False

        self.messages = request.get("chat")
        return True

    async def send(self, chunk_size=512):
        """发送.

        Args:
            chunk_size: 流式读取分块的大小。百度返回的是一个 json 结构
        """

        # add access token to url
        url = self.url + "?access_token=" + self.access_token

        # send request
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, json={"messages": self.messages, "stream": True}
            ) as response:
                async for chunk in response.content.iter_chunked(chunk_size):
                    data = chunk.decode("utf-8")

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

    # 读取配置文件
    if not ernie.read_config(config, request):
        logger.echo("读取配置文件失败", "error")
        return "读取配置文件失败"

    # 发送请求
    return StreamingResponse(ernie.send(), media_type="text/event-stream")
