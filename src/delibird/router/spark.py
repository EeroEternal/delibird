from contextlib import closing
import _thread as thread
import asyncio
import base64
import datetime
from datetime import datetime
import hashlib
import hmac
import json
from socket import timeout
from time import mktime
from urllib.parse import urlencode, urlparse
import ssl
from websocket import create_connection
import websocket
from wsgiref.handlers import format_date_time
from fastapi.responses import StreamingResponse
from llmproxy.log import Log
from time import sleep
import asyncio
from llmproxy.stream import WsStream


class Spark:
    def __init__(self, config, request):
        self.app_id = None
        self.api_key = None
        self.api_secret = None
        self.url = ""
        self.model = None
        self.messages = None
        self.config = config
        self.request = request

    def read_config(self):
        """读取配置文件.

        Args:
            config: 配置文件
            request: 请求参数.格式为 {"chat": messages, "model": "v15"}
        """
        logger = Log("llmproxy")
        if not self.config:
            logger.echo("配置文件不存在", "error")
            return False

        model = self.request.get("model")
        if not model:
            logger.echo("model 不存在", "error")
            return False

        spark_config = self.config.get("spark")
        if not spark_config or model not in spark_config:
            logger.echo("spark 配置项不存在", "error")
            return False

        model_config = spark_config.get(model)
        required_keys = ["version", "app_id", "api_key", "api_secret", "url"]

        # 检查并设置必要配置项
        for key in required_keys:
            value = model_config.get(key)
            if not value:
                logger.echo(f"{key} 在 {model} 配置项下不能为空", "error")
                return False

        self.model = model_config.get("version")
        self.app_id = model_config.get("app_id")
        self.api_key = model_config.get("api_key")
        self.api_secret = model_config.get("api_secret")
        self.url = model_config.get("url")

        # 检查是否存在 chat 字段
        if "chat" not in self.request:
            logger.echo("请求参数中不存在 chat 字段", "error")
            return False

        self.messages = self.request["chat"]

        return True

    def _create_url(self):
        """生成 websocket url."""

        # check api_secret and api_key
        if not self.api_secret or not self.api_key:
            raise ValueError("api_secret 或 api_key 不存在")

        host = urlparse(self.url).netloc
        path = urlparse(self.url).path

        # 生成RFC1123格式的时间戳
        now = datetime.now()  # type: ignore
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(
            self.api_secret.encode("utf-8"),
            signature_origin.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding="utf-8")

        authorization_origin = (
            f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date'
            f' request-line", signature="{signature_sha_base64}"'
        )

        authorization = base64.b64encode(authorization_origin.encode("utf-8")).decode(
            encoding="utf-8"
        )

        # 将请求的鉴权参数组合为字典
        v = {"authorization": authorization, "date": date, "host": host}
        # 拼接鉴权参数，生成url
        url = self.url + "?" + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url

    async def send(
        self,
        n=1,
        frequency_penalty=0,
        logit_bias=None,
        logprobs=False,
        presence_penalty=0,
        stop=None,
        stream=False,
        temperature=1,
        top_p=1,
        **kwargs,
    ):
        # 从 kwargs 获取 max_tokens 参数
        max_tokens = kwargs.get("max_tokens", 2048)

        url = self._create_url()

        # 实例化 WsStream
        ws = WsStream(url)

        async for message in ws.send(self.messages, "spark", self.model, self.app_id):
            # 检查是否需要关闭连接
            if message == "#finished#" or message == "#None#":
                ws.close()
                break

            yield message


def send(config, request):
    """
    发送消息
    """
    # 创建 Spark 实例
    spark = Spark(config, request)

    # 读取配置文件
    if not spark.read_config():
        return {"error": "配置文件错误"}

    # 流式请求
    return StreamingResponse(
        spark.send(),
        media_type="text/event-stream",
    )
