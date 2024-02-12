"""抽象类"""

import aiohttp
import websocket


class Base:
    def __init__(self):
        self.url = ""
        self.modal = None

    async def send(self, messages, chunk_size=512, protocol="http"):
        """发送.

        Args:
            messages: 请求参数。格式为 [ {"role": "user", "content": "Python 如何实现异步编程"}]
            chunk_size: 流式读取分块的大小。百度返回的是一个 json 结构
            protocol: 请求协议 http 或者 websocket
        """
        if not self.url:
            raise ValueError("url 不能为空")

        if protocol == "http":
            async for data in self._http_send(messages, chunk_size):
                yield data

        if protocol == "websocket":
            async for data in self._websocket_send(messages):
                yield data

    async def _http_send(self, messages, chunk_size=512):
        """发送.

        Args:
            messages: 请求参数。格式为 [ {"role": "user", "content": "Python 如何实现异步编程"}]
            chunk_size: 流式读取分块的大小。百度返回的是一个 json 结构
        """
        if not self.url:
            raise ValueError("url 不能为空")

        # send request
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.url, json={"messages": messages, "stream": True}
            ) as response:
                async for chunk in response.content.iter_chunked(chunk_size):
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

            yield data

    def read_config(self, config, router, modal):
        """读取配置文件.

        Args:
            config: Dict[str, Any], 读取的配置文件内容
            router: str, qwen, spark, ernie 或者其他
            modal: str, 模型名称
        return:
            (bool,str): (True, "success") or (False, "error message")
        """
        if not config:
            return (False, "config is None")

        if not config.get(router):
            return (False, "router is None")

        self.modal = modal

        # router config
        router_config = config.get(router)
        if not router_config:
            return (False, "router config is None")

        # get modal config
        modal_config = router_config.get(modal)
        if not modal_config:
            return (False, "modal config is None")

        return (True, "success")
