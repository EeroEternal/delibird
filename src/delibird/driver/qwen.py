"""Qwen 接口."""
from fastapi.responses import StreamingResponse
from http import HTTPStatus
import dashscope
from .base import Base


class Qwen(Base):
    """Qwen 接口."""

    def __init__(self):
        """初始化."""
        super().__init__()

    async def send(self, messages, model):
        """发送.

        Args:
            messages: 发送的消息
        """
        self.model = model

        responses = dashscope.Generation.call(
            self.model,
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
