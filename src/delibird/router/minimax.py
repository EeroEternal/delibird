"""Minimax 大模型"""

from .base import Base
import json
from delibird.log import Log


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
        async for data in super().send(messages, model, headers=headers, body=body):
            if_finish, message = _decode_data(data)

            yield message

            if if_finish:
                break


def _decode_data(message):
    """解析 Minimax 返回的 messages

    Returns:
        True,message: 是否是最后一条消息，消息内容
        如果是 True，表示是最后一条消息
    """
    # {
    #     "created": 1689738159,
    #     "model": "abab5.5-chat",
    #     "reply": "Who am I?",
    #     "choices": [
    #         {
    #             "finish_reason": "stop",
    #             "messages": [
    #                 {"sender_type": "BOT",
    #                  "sender_name": "MM智能助理",
    #                  "text": "Who am I?"}
    #             ],
    #         }
    #     ],
    #     "usage": {"total_tokens": 191},
    #     "input_sensitive": false,
    #     "output_sensitive": false,
    #     "id": "01068eae26a39a3a39b7bb56cfbe4266",
    #     "base_resp": {"status_code": 0, "status_msg": ""},
    # },
    #
    #  从 choices 中取出 messages 的 text
    # 检查 message 开头是否以 data:
    if not message.startswith("data:"):
        return (True, message)

    # 去掉开头的 data: 字符串
    result = message[6:]

    # 转换为 json
    try:
        result = json.loads(result)

        # 获取 choices 中的 messages 中的 text
        result = result.get("choices")[0].get("messages")[0].get("text")

        # 如果 result 存在 "usage",说明流结束
        if "usage" in result:
            # 返回空，表示这个消息完成之后结束
            return (True, result)
        else:
            return (False, result)

    except json.JSONDecodeError as e:
        logger = Log("delibird")
        logger.echo(f"json 解析错误: {e}", "error")
        return (True, "json 解析错误")


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
