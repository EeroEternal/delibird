"""ChatGLM接口."""
from .base import Base
import time
import jwt


def generate_token(apikey: str, exp_seconds: int):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise Exception("invalid apikey", e)

    payload = {
        "api_key": id,
        "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
        "timestamp": int(round(time.time() * 1000)),
    }

    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )


class ChatGLM(Base):
    """ChatGLM接口."""

    async def send(self, messages, model):
        """发送.

        Args:
            messages: 请求参数。格式为 [ {"role": "user", "content": "Python 如何实现异步编程"}]
            model: 对应的模型名称。格式为例如 qwen 就是 qwen-max、qwen-min、qwen-speed、qwen-turbo
        """
        self.model = model

        # 拼接 header，增加 Authorization
        headers = {"Authorization": "Bearer " + generate_token(self.api_key, 3600)}

        # 调用父类的 send 方法
        async for data in super().send(messages, model, headers=headers):
            # 判断是否已经到结尾
            if data == "[DONE]":
                yield data

            # 去掉开头的 data: 字符串
            data = data[5:]

            # 去掉末尾的换行符
            data = data.rstrip()
