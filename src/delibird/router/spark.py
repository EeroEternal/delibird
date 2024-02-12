from contextlib import closing
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
from delibird.log import Log
from time import sleep
import asyncio
from .base import Base
from delibird.log import Log


class Spark(Base):
    def __init__(self):
        super().__init__()
        # spark 版本
        self.version = ""

    def read_config(self, config, modal):
        """读取配置文件.

        Args:
            config: 配置文件
            modal: 模型名称。格式为 v35、v30、v20、v15
        """
        # 执行父类的 read_config 方法
        result = super().read_config(config, "spark", modal)

        spark_config = config.get("spark")
        if not spark_config or modal not in spark_config:
            return (False, "spark 配置项不存在")

        modal_config = spark_config.get(modal)
        required_keys = ["version", "app_id", "api_key", "api_secret", "url"]

        # 检查并设置必要配置项
        for key in required_keys:
            value = modal_config.get(key)
            if not value:
                return (False, f"{key} 在 {modal} 配置项下不能为空")

        self.version = modal_config.get("version")

        self.app_id = modal_config.get("app_id")
        self.api_key = modal_config.get("api_key")
        self.api_secret = modal_config.get("api_secret")
        self.url = modal_config.get("url")

        return (True, "success")

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
        messages,
        **kwargs,
    ):
        # 生成 url
        url = self._create_url()

        # 准备数据
        data = self._prepare_data(messages)

        # 执行父类的 send 方法，发送数据
        async for result in super().send(data, protocol="websocket"):
            # 处理返回的数据
            async for filter_data in self._process_data(result):
                if filter_data:
                    yield filter_data
                else:
                    break

    async def _process_data(self, data):
        logger = Log("delibird")
        json_result = json.loads(data)

        # 检查是否存在 header 字段
        if "header" not in json_result:
            logger.echo("缺少 header 字段", "error")
            # 返回空，super 会关闭 websocket
            yield ""

        # 检查是否存在 code 字段
        if "code" not in json_result["header"]:
            logger.echo("缺少 code 字段", "error")
            yield ""

        code = json_result["header"]["code"]

        if code != 0:
            logger.echo(f"code error: {code}", "error")
            yield ""

        choices = json_result["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]

        if status == 2:
            yield ""

        # 返回内容
        yield content

    def _prepare_data(self, messages):
        """把 messages 转化为 spark 需要的 json 格式"""
        # 转换 messages 为 json 格式
        return json.dumps(
            gen_params(appid=self.app_id, messages=messages, version=self.version)
        )


def send(config, request):
    """
    发送消息
    """
    # 创建 Spark 实例
    spark = Spark()

    # 从 request 中获取 modal 和 messages
    modal = request.get("modal")
    messages = request.get("chat")

    # 读取配置文件
    result, message = spark.read_config(config, modal)
    if not result:
        return message

    # 流式请求
    return StreamingResponse(
        spark.send(messages),
        media_type="text/event-stream",
    )


def gen_params(appid, messages, version, max_tokens=2048, top_k=4, chat_id=None):
    """
    通过appid和用户的提问来生成请参数

    appid: str, 用户的appid
    question: str, 用户的提问
    version: str, 星火的版本：
        general 指向V1.5版本;
        generalv2 指向V2版本;
        generalv3 指向V3版本;
        generalv3.5 指向V3.5版本;
    max_tokens: int, 最大生成长度
        V1.5 取值范围为[1,4096]
        V2.0、V3.0和V3.5 取值范围为[1,8192]，默认为2048。
    top_k: int, 从k个候选中随机选择⼀个（⾮等概率） 取值为[1，6],默认为4

    messages:
        包含 role 和 content 的列表，role 为system、 user 、assistant，content 为消息内容
    """

    # 拼接请求参数
    data = {
        "header": {"app_id": appid},
        "parameter": {
            "chat": {"domain": version, "max_tokens": max_tokens, "top_k": top_k}
        },
        "payload": {"message": {"text": messages}},
    }

    # 如果 chat_id 不为空，则添加到请求参数中
    if chat_id:
        data["parameter"]["chat"]["chat_id"] = chat_id

    return data
