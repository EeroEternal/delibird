"""抽象类"""

import aiohttp
import websocket
from delibird.util import common_decode


class Meta(type):
    def __call__(cls, *args, **kwargs):
        class_type = kwargs.pop("class_type", None)
        if class_type is not None:
            subclasses = {
                subclass.__name__: subclass for subclass in cls.__subclasses__()
            }
            try:
                return subclasses[class_type](*args, **kwargs)
            except KeyError:
                raise ValueError(f"Invalid class type: {class_type}")
        else:
            return super().__call__(*args, **kwargs)


class Base(metaclass=Meta):
    def __init__(self):
        self.url = ""
        self.api_key = ""
        self.model = ""
        self.support_models = []

    async def send(
        self,
        messages,
        model,
        protocol="http",
        headers=None,
        params=None,
        body=None,
        filter_func=None,
        split_tag="\n\n",
        done_tag="[DONE]",
    ):
        """发送.

        Args:
            messages: 请求参数。格式为 [ {"role": "user", "content": "Python 如何实现异步编程"}]
            model: 对应的模型名称。格式为例如 qwen 就是 qwen-max、qwen-min、qwen-speed、qwen-turbo
            protocol: 请求协议 http 或者 websocket

            header: 如何存在，就按照这个 header 发送请求
            params: 如何存在，就按照这个 params 发送请求
            body: 如何存在，就按照这个 body 发送请求
            filter_func: 过滤数据的函数. 默认是 common_decode，通用解析方式
            split_tag: 分割数据的标志
            done_tag: 完成的标志
        """
        if not self.url:
            raise ValueError("url 不能为空")

        # 设置 model 名称，作为子类拼接 url 使用
        self.model = model

        # 检查 model 对应的 models 是否存在，就是检查对应模型是否支持
        if model not in self.support_models:
            raise ValueError(f"不支持该模型: {model}")

        if protocol == "http":
            async for data in self._http_send(
                messages, headers, body, filter_func, split_tag, done_tag
            ):
                yield data

        if protocol == "websocket":
            async for data in self._websocket_send(messages):
                yield data

    async def _http_send(
        self,
        messages,
        headers=None,
        body=None,
        filter_func=None,
        split_tag="\n\n",
        end_tag="[DONE]",
    ):
        """发送.

        Args:
            messages: 请求参数。格式为 [ {"role": "user", "content": "Python 如何实现异步编程"}]
            model: 对应的模型名称。格式为例如 qwen 就是 qwen-max、qwen-min、qwen-speed、qwen-turbo
            headers: 请求头
            body: 请求体
            filter_func: 过滤数据的函数. 默认是 common_decode，通用解析方式
            split_tag: 分割数据的标志
            end_tag: 完成的标志
        """
        if not self.url:
            raise ValueError("url 不能为空")

        if not headers:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key,
            }

        if not body:
            body = (
                {"messages": messages, "stream": True}
                if not self.model
                else {"messages": messages, "model": self.model, "stream": True}
            )

        session = aiohttp.ClientSession()
        response = await session.post(self.url, headers=headers, json=body)
        buffer = ""  # 有些服务返回的时候是一次多个或者碎片，需要自己处理

        # 迭代返回的数据
        async for chunk in response.content.iter_any():
            # 解码
            try:
                chunk = chunk.decode("utf-8")
            except UnicodeDecodeError:
                print(f"解码错误: {chunk}")
                continue

            # 获取数据，和 buffer 拼接
            buffer += chunk

            # 这一批次处理的结果输出
            output = ""

            # 解析数据，返回内容
            while split_tag in buffer:
                # 从字符串开头，获取到第一个分割标志的位置
                try:
                    first_index = buffer.index(split_tag)
                except ValueError:
                    # 没有找到分割标志，跳出
                    break

                # 获取到分割标志之前的数据
                head_str = buffer[:first_index]

                # 如果有处理函数，就调用处理函数。返回处理后的数据
                # 如果没有处理函数，就使用 common_decode 处理
                # result 是处理是否成功，snippet_data 是处理后的数据
                filter_func = filter_func or common_decode

                result, snippet_data = filter_func(head_str)

                # 数据处理没有成功，跳出
                if not result:
                    break

                # 如果数据是结束标记，跳出
                if snippet_data == end_tag:
                    break

                # 如果数据末尾包含结束标记
                # 去掉结尾标记，获取数据，跳出
                if snippet_data.endswith(end_tag):
                    snippet_data = snippet_data[: -len(end_tag)]

                    # 循环检查一遍末尾是否有结束标记,有就去掉
                    # 为了避免有些服务返回结束标记，然后在最后一条也有 finish_reason
                    while snippet_data.endswith(end_tag):
                        snippet_data = snippet_data[: -len(end_tag)]

                    output += snippet_data
                    break

                # 拼接返回的数据
                output += snippet_data

                # 剩下的数据,跳过分割标志，再放到 buffer里面
                buffer = buffer[buffer.index(split_tag) + len(split_tag) :]

            # 返回这一批次处理的结果
            yield output

        # 关闭 session
        await session.close()

    async def _websocket_send(self, messages):
        """发送.

        Args:
            messages: 请求参数。格式为 [ {"role": "user", "content": "Python 如何实现异步编程"}]
        """
        if not self.url:
            raise ValueError("url 不能为空")

        ws_handler = websocket.create_connection(self.url)

        if not ws_handler:
            raise ValueError("websocket 连接失败")

        ws_handler.send(messages)

        while True:
            data = ws_handler.recv()

            # 如果 data 为空，说明已经接收完毕
            if not data:
                # 关闭 websocket 连接
                ws_handler.close()
                break

            # 返回 bytes 类型数据
            if isinstance(data, str):
                yield data.encode("utf-8")
            else:
                yield data

    def read_config(self, config):
        """读取配置.

        Args:
            config: Dict[str, Any], 对应的配置
        return:
            (bool,str): (True, "success") or (False, "error message")
        """
        if not config:
            return (False, "config is None")

        # 读取 api_key
        if not config.get("api_key"):
            return (False, "api_key 不存在")
        self.api_key = config.get("api_key")

        # 读取 url
        if config.get("url"):
            self.url = config.get("url")

        # 读取 support models
        self.support_models = config.get("support_models")
        if not self.support_models:
            return (False, "support_models 不存在")

        return (True, "success")
