import aiohttp
import os
import json
import asyncio


async def stream_fetch(url, messages):
    json_data = {"messages": messages, "stream": True}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data) as response:
            async for chunk in response.content.iter_chunked(2048):
                data = chunk.decode("utf-8")

                # 去掉开头的 data: 字符串
                data = data.strip()
                data = data.lstrip("data: ")
                data = data.rstrip("\n")

                # decode to json
                try:
                    json_data = json.loads(data)
                except json.JSONDecodeError as e:
                    print(f"json error: {e}")
                    result = ""

                result = json_data.get("result")


def test_ernie():
    access_token = (
        "24.f7c4b90df8bf9e0d48ce91a1b21c1010.2592000.1710053471.282335-50396495"
    )

    url = (
        "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions"
    )

    url = url + "?access_token=" + access_token

    messages = [
        {"role": "user", "content": "Python 如何构建一个类"},
    ]

    asyncio.run(stream_fetch(url, messages))
