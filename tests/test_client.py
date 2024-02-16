from delibird.client import Chat
import asyncio


async def stream_fetch():
    """Test client."""

    messages = [
        {"role": "user", "content": "Python 如何实现异步编程"},
    ]

    host = "localhost"
    port = 8000
    router = "spark"
    url = f"http://{host}:{port}/{router}/chat/completion"

    chat = Chat("ernie-speed")

    async for result in chat.stream_fetch(messages, url):
        print(result)


def test_client():
    asyncio.run(stream_fetch())
