import aiohttp
import os
import json
import asyncio


async def stream_fetch(url, messages):
    json_data = {"messages": messages, "stream": True}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data) as response:
            async for chunk in response.content.iter_chunked(1024):
                data = chunk.decode("utf-8")

                # 去掉开头的 data: 字符串
                data = data[5:]

                # 去掉结尾的 \n 字符串
                data = data[:-2]

                # decode to json
                json_data = json.loads(data)
                result = json_data.get("result")
                print(f"result: {result}")


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
