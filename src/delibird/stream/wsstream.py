from .base import StreamBase
from delibird.log import Log
import websocket
import json


class WsStream(StreamBase):
    def __init__(self, url):
        self.url = url
        self.websocket = None  # websocket hanlder

    async def send(self, data, protocol, modal, app_id=None):
        """发送消息.

        Args:
            data: 发送的内容
            protocol: 协议。基于 websocket 上的应用层解析协议
            modal: 模型名称
            app_id: 应用 id，可选
        """
        if protocol == "spark":
            async for result in self._spark_send(data, modal, app_id):
                yield result

    def close(self):
        """关闭 websocket 连接."""
        if self.websocket is not None:
            self.websocket.close()

    async def _spark_send(self, messages, modal, app_id):
        """星火大模型发送处理."""
        logger = Log("delibird")
        websocket.enableTrace(False)

        self.websocket = websocket.create_connection(self.url)

        # json 解析
        data = json.dumps(gen_params(appid=app_id, messages=messages, version=modal))

        async for result in self._send(data):
            if result == "#None#":
                logger.echo("没有接收到数据，关闭 websocket 连接")
                break

            result = json.loads(result)
            code = result["header"]["code"]

            if code != 0:
                logger.echo(f"请求错误: {code}, {result}")
                break
            else:
                choices = result["payload"]["choices"]
                status = choices["status"]
                content = choices["text"][0]["content"]

                if status == 2:
                    yield "#finished#"

                # 返回内容
                yield content

    async def _send(self, data):
        """发送消息.

        Args:
            data: 发送的内容
            protocol: 协议。基于 websocket 上的应用层解析协议
        """
        if self.websocket is None:
            raise ValueError("websocket is not connected")

        self.websocket.send(data)

        while True:
            result = self.websocket.recv()
            if result is None:
                yield "#None#"  # finished signal
            yield result


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
