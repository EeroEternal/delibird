"""Minimax 大模型"""

from .base import Base
import json
from delibird.util import Log, decode_data


class Minimax(Base):
    def __init__(self):
        self.group_id = ""

    # 重写 read_config
    def read_config(self, config):
        """读取配置文件.

        Args:
            config_file: str, 配置文件路径
        """
        result, message = super().read_config(config)
        if not result:
            return result, message

        # 读取 group_id
        group_id = config.get("group_id")

        if not group_id:
            return False, "group_id 不能为空"

        self.group_id = group_id

        return True, "success"

    async def send(self, messages, model):
        """发送.

        Args:
            messages: 请求参数。格式为 [ {"role": "user", "content": "Python 如何实现异步编程"}]
            model: 对应的模型名称。格式为例如 qwen 就是 qwen-max、qwen-min、qwen-speed、qwen-turbo
            protocol: 请求协议 http 或者 websocket
        """
        if not self.url:
            raise ValueError("url 不能为空")

        # 拼接 header，增加 Authorization
        headers = {
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json",
        }

        # 给 url 增加 group_id
        self.url = self.url + "?GroupId=" + self.group_id

        # 拼接 body
        body = {
            "model": model,
            "messages": _build_messages(messages),
            "stream": True,
            "bot_setting": [
                {
                    "bot_name": "智能助理",
                    "content": "你是一个智能助理，帮助用户解决问题",
                }
            ],
            "reply_constraints": {"sender_type": "BOT", "sender_name": "智能助理"},
        }

        # 调用父类的 send 方法
        async for data in super().send(
            messages, model, headers=headers, body=body, filter_func=_decode_data
        ):
            yield data


def _decode_data(data):
    """解析 Minimax 返回的 messages."""

    # 解析 data
    result, data = decode_data(data, start="data: ")

    if not result:
        return (False, data)

    if not data:
        return (False, "")

    return_data = ""

    # 检查 data 是否存在 choices
    try:
        return_data = data["choices"][0]["messages"][0].get("text")

        # 检查 data 是否存在 usage，如果存在，说明流结束
        if "usage" in data:
            # 在 usage 获取 text，在后面增加 [DONE]
            return_data = return_data + "[DONE]"

        return (True, return_data)
    except KeyError as e:
        return (False, "数据格式错误")


def _build_messages(messages):
    """把标准messages转换成Minimax的messages"""

    minimax_messages = []

    for message in messages:
        # get role
        role = message.get("role")

        if not role:
            raise ValueError("role 不能为空")

        if role == "user":
            minimax_messages.append(
                {
                    "sender_type": "USER",
                    "sender_name": "anonymous",
                    "text": message.get("content"),
                }
            )

    return minimax_messages
