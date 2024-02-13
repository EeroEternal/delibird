"""Request and stream response."""
import aiohttp
import asyncio
import json
from delibird.log import Log


class Chat:
    """请求和流式响应.

    Args:
        router: 服务名称,例如: qwen
        model: 模型名称，例如: max
    """

    def __init__(self, model):
        self.model = model

    async def stream_fetch(self, messages, url):
        """请求和流式响应."""

        # 用 messages 构建一个请求参数, 读取 spark v35 模型，对应 toml 配置文件中的 spark 配置项
        json_data = {"chat": messages, "model": self.model}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=json_data,
                headers={"Content-Type": "application/json"},
            ) as response:
                if response.status == 200:
                    async for chunk in response.content.iter_chunked(1024):
                        yield chunk.decode("utf-8")
                    else:
                        logger = Log("delibird")
                        logger.echo(f"Error: {response.status}", "error")
