import requests
import json
import aiohttp
import asyncio
import tomllib
import websocket
import ssl
from contextlib import closing
from websocket import create_connection


async def fetch_streaming_response(router, model):
    messages = [
        {"role": "system", "content": "你现在是一个优秀的程序员，以程序员的身份和我聊天吧"},
        {"role": "user", "content": "Python 如何实现异步编程"},
    ]

    host = "localhost"
    port = 8000

    url = f"http://{host}:{port}/{router}/chat/completion"

    # 用 messages 构建一个请求参数, 读取 spark v35 模型，对应 toml 配置文件中的 spark 配置项
    json_data = {"chat": messages, "model": model}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            data=json.dumps(json_data),
            headers={"Content-Type": "application/json"},
        ) as response:
            if response.status == 200:
                async for chunk in response.content.iter_chunked(1024):
                    print(f"{chunk.decode('utf-8')}")
            else:
                print(f"Error: {response.status}")


def test_client():
    """Test client."""

    # test client request
    # asyncio.run(fetch_streaming_response("qwen", "qwen-max"))

    asyncio.run(fetch_streaming_response("spark", "v35"))
