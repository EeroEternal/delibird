"""Qwen 接口."""
from logging import Logger
import platform
from fastapi.responses import StreamingResponse
from http import HTTPStatus
import dashscope
from delibird.log import Log


class Qwen:
    """Qwen 接口."""

    def __init__(self):
        """初始化.

        Args:
            protocol: 协议。http https websocket
            model: 模型名称
            api_key: api key
            url: 请求地址
        """
        self.api_key = ""
        self.config = None
        self.request = None
        self.messages = ""
        self.model = ""

    def read_config(self, config, request):
        """读取配置文件.

        Args:
            config: 配置文件
            request: 请求参数.格式为 {"chat": messages, "model": "v15"}
        """

        logger = Log("delibird")
        # 检查配置文件和模型是否存在
        if not config:
            logger.echo("配置文件不存在", "error")
            return False

        model = request.get("model")
        if not model:
            logger.echo("model 不存在", "error")
            return False

        # 读取配置文件
        qwen_config = config.get("qwen")
        if not qwen_config or model not in qwen_config:
            logger.echo("qwen 配置项不存在", "error")
            return False

        model_config = qwen_config.get(model)
        # check api_key
        if not model_config.get("api_key"):
            logger.echo("api_key 不能为空", "error")
            return False

        self.api_key = model_config.get("api_key")
        self.model = model

        # 检查是否存在 chat 字段
        if "chat" not in request:
            logger.echo("请求参数中不存在 chat 字段", "error")
            return False

        self.messages = request["chat"]

        return True

    async def send(self, chunk_size=24):
        """发送.

        Args:
            data: 发送的数据，json 格式
            chunk_size: 流式读取分块的大小
        """
        responses = dashscope.Generation.call(
            self.model,
            messages=self.messages,
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
    """发送处理."""
    logger = Log("delibird")

    # 创建 Qwen 实例
    qwen = Qwen()

    # 读取配置文件
    if not qwen.read_config(config, request):
        logger.echo("读取配置文件失败", "error")
        return "读取配置文件失败"

    # 流式返回
    return StreamingResponse(qwen.send(), media_type="text/event-stream")
