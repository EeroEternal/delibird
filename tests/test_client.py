from delibird.client import Chat
import asyncio


async def stream_fetch():
    """Test client."""

    messages = [
        {"role": "system", "content": "你现在是一个优秀的程序员，以程序员的身份和我聊天吧"},
        {"role": "user", "content": "Python 如何实现异步编程"},
    ]

    host = "localhost"
    port = 8000
    router = "qwen"
    url = f"http://{host}:{port}/{router}/chat/completion"

    chat = Chat("qwen-max")

    async for result in chat.stream_fetch(messages, url):
        print(result)


def test_client():
    asyncio.run(stream_fetch())
