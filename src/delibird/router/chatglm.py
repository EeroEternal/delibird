"""ChatGLM接口."""
from .base import Base
import time
import jwt
import json
from delibird.log import Log


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


class Chatglm(Base):
    """ChatGLM接口."""

    async def send(self, messages, model):
        """发送.

        Args:
            messages: 请求参数。格式为 [ {"role": "user", "content": "Python 如何实现异步编程"}]
            model: 对应的模型名称。格式为例如 qwen 就是 qwen-max、qwen-min、qwen-speed、qwen-turbo
        """
        logger = Log("delibird")

        self.model = model

        print(f"chatglm send messages: {messages}, model: {model}")

        # 拼接 header，增加 Authorization
        headers = {"Authorization": "Bearer " + generate_token(self.api_key, 3600)}

        # 返回的数据可能会有多个，所以使用 buffer 存储
        buffer = ""

        # 调用父类的 send 方法
        async for data in super().send(messages, model, headers=headers):
            # result 是最后输出的结果，可能是多个数据拼接的
            output = ""

            # decode data
            data = data.decode("utf-8")

            # 获取数据，和 buffer 拼接
            buffer += data

            # 获取数据到 "\n\n" 为止
            return_data = ""  # 可以返回的数据
            while "\n\n" in buffer:
                # 从字符串开头，获取到 "\n\n" 为止的数据
                head_str = buffer[: buffer.index("\n\n")]

                # 解析数据，返回内容. snippet_data 理解为一段可以返回的数据
                result, snippet_data = _decode_data(head_str)

                if not result:
                    break

                if snippet_data == "[DONE]":
                    break

                # 拼接返回的数据
                return_data += snippet_data

                # 剩下的数据, +2 是去掉 "\n\n"
                buffer = buffer[buffer.index("\n\n") + 2 :]

            print(f"return_data: {return_data}")

            yield return_data


def _decode_data(data):
    """解析数据."""

    # 检查开头是否是 data: 字符串
    if not data.startswith("data:"):
        return (False, "字符串开头不是 data: ")

    # 去掉开头的 data: 字符串
    data = data[5:]

    # 去掉末尾的 \n\n 字符串
    data = data.strip()

    # 检查是否是 '[DONE]'
    print(f"if done: {len(data)}")
    if data == "[DONE]":
        print("return done")
        return (True, data)

    # 将 json 字符串转换为字典
    try:
        data = json.loads(data)
    except json.JSONDecodeError as e:
        return (False, f"json 解析错误{e}")

    # 检查是否存在 choices 和 delta
    if "choices" in data and "delta" in data["choices"][0]:
        # {"id":"8313807536837492492","created":1706092316,"model":"glm-4","choices":[{"index":0,"delta":{"role":"assistant","content":"土"}}]}
        # data 格式类似上面的 json 结构，获取里面的 content
        return (True, data["choices"][0]["delta"]["content"])
    else:
        return (False, "数据格式错误")
