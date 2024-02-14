"""抽象类"""

import aiohttp
import websocket


class Base:
    def __init__(self):
        self.url = ""
        self.api_key = ""
        self.model = ""
        self.support_models = []

    async def send(
        self,
        messages,
        model,
        chunk_size=512,
        protocol="http",
        headers=None,
        params=None,
        body=None,
    ):
        """发送.

        Args:
            messages: 请求参数。格式为 [ {"role": "user", "content": "Python 如何实现异步编程"}]
            model: 对应的模型名称。格式为例如 qwen 就是 qwen-max、qwen-min、qwen-speed、qwen-turbo
            chunk_size: 流式读取分块的大小。百度返回的是一个 json 结构
            protocol: 请求协议 http 或者 websocket

            header: 如何存在，就按照这个 header 发送请求
            params: 如何存在，就按照这个 params 发送请求
            body: 如何存在，就按照这个 body 发送请求
        """
        if not self.url:
            raise ValueError("url 不能为空")

        # 设置 model 名称，作为子类拼接 url 使用
        self.model = model

        # 检查 model 对应的 models 是否存在，就是检查对应模型是否支持
        if model not in self.support_models:
            yield "不支持该模型"

        if protocol == "http":
            async for data in self._http_send(messages, headers, body, chunk_size):
                yield data

        if protocol == "websocket":
            async for data in self._websocket_send(messages):
                yield data

    async def _http_send(self, messages, headers=None, body=None, chunk_size=512):
        """发送.

        Args:
            messages: 请求参数。格式为 [ {"role": "user", "content": "Python 如何实现异步编程"}]
            model: 对应的模型名称。格式为例如 qwen 就是 qwen-max、qwen-min、qwen-speed、qwen-turbo
            chunk_size: 流式读取分块的大小。百度返回的是一个 json 结构
        """
        if not self.url:
            raise ValueError("url 不能为空")

        if not headers:
            headers = {}

        if not body:
            body = {"messages": messages, "stream": True}

        # send request
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=headers, json=body) as response:
                async for chunk in response.content.iter_chunked(chunk_size):
                    if not chunk:
                        break

                    data = chunk.decode("utf-8")
                    yield data

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
