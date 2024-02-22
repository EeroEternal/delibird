from delibird.client import Chat
import asyncio
import random

test_map = [
    {
        "name": "chatglm",
        "model": "glm-3-turbo",
    },
    {
        "name": "chatglm",
        "model": "glm-4",
    },
    {
        "name": "ernie",
        "model": "ernie-bot-turbo",
    },
    {"name": "minimax", "model": "abab5.5-chat"},
    {"name": "baichuan", "model": "Baichuan2-Turbo"},
    {"name": "moonshot", "model": "moonshot-v1-8k"},
    {"name": "qwen", "model": "qwen-turbo"},
    {"name": "spark", "model": "generalv3"},
    {"name": "skylark", "model": "skylark-pro-public"},
]


questions = ["Python 如何构建一个类", "Rust 语言的特点", "Python 异步是如何实现的", "Python 如何处理字符串"]


async def stream_fetch():
    """Test client."""

    # 生成一个0到4随机数
    index = random.randint(0, len(questions) - 1)

    messages = [
        {"role": "user", "content": questions[index]},
    ]

    # test index
    index = 8
    host = "localhost"
    port = 8000
    router = test_map[index]["name"]
    url = f"http://{host}:{port}/{router}/chat/completion"

    chat = Chat(test_map[index]["model"])

    async for result in chat.stream_fetch(messages, url):
        # 不要自动加换行
        print(result, end="")


def test_client():
    asyncio.run(stream_fetch())
