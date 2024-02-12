"""Qwen 接口."""
from logging import Logger
import platform
from fastapi.responses import StreamingResponse
from http import HTTPStatus
import dashscope
from .base import Base
from delibird.log import Log


class Qwen(Base):
    """Qwen 接口."""

    def __init__(self):
        """初始化."""
        super().__init__()
        self.api_key = ""

    def read_config(self, config, modal):
        """读取配置文件.

        Args:
            config: 配置文件
            modal: 模型名称。格式为 max、min、speed、turbo
        """
        # modal 是 max，需要加上 qwen 前缀
        result, message = super().read_config(config, "qwen", modal)

        if not result:
            return (result, message)

        # 读取配置文件
        qwen_config = config.get("qwen")
        if not qwen_config or modal not in qwen_config:
            return (False, "qwen 配置项不存在")

        modal_config = qwen_config.get(modal)
        # check api_key
        if not modal_config.get("api_key"):
            return (False, "api_key 不存在")

        self.api_key = modal_config.get("api_key")

        # modal 加上 qwen 前缀
        self.modal = "qwen-" + modal

        return (True, "success")

    async def send(self, messages, chunk_size=512):
        """发送.

        Args:
            messages: 发送的消息
            chunk_size: 分块大小
        """
        responses = dashscope.Generation.call(
            self.modal,
            messages=messages,
            result_format="message",  # set the result to be "message" format.
            stream=True,
            incremental_output=True,  # get streaming output incrementally
            api_key=self.api_key,
        )

        for response in responses:
            if response.status_code == HTTPStatus.OK:
                yield response.output.choices[0]["message"]["content"]
            else:
                print(
                    "Request id: %s, Status code: %s, error code: %s, error message: %s"
                    % (
                        response.request_id,
                        response.status_code,
                        response.code,
                        response.message,
                    )
                )


def send(config, request):
    """发送处理.

    Args:
        config: 配置文件
        request: 请求参数.格式为 {"chat":messages, "modal":modal}
    """

    # 创建 Qwen 实例
    qwen = Qwen()
    logger = Log("delibird")

    # 从 request 中获取 modal 和 messages
    modal = request.get("modal")
    messages = request.get("chat")

    # 读取配置文件
    result, message = qwen.read_config(config, modal)
    if not result:
        logger.echo(message, "error")
        return message

    # 流式返回
    return StreamingResponse(qwen.send(messages), media_type="text/event-stream")
