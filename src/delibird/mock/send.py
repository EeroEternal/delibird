import asyncio

mock_data = (
    (
        "Python is a high-level, interpreted programming language that is widely used"
        " in various fields such as web development, data analysis, artificial"
        " intelligence, scientific computing, and more. It was first released in 1991"
        " by Guido van Rossum and is now maintained by the Python Software Foundation."
    ),
    (
        "Some of the key features of Python include its simplicity, readability, and"
        " flexibility. It has a clear and concise syntax that makes it easy to learn"
        " and use, even for beginners. Python also has a large standard library that"
        " provides a wide range of modules and functions for tasks such as string"
        " manipulation, file I/O, and network communication."
    ),
    (
        "Python is an interpreted language, which means that it does not need to be"
        " compiled before it can be run. Instead, Python code is executed line-by-line"
        " by an interpreter, making it easy to write and test code quickly."
    ),
    (
        "Python is also an object-oriented language, which means that it supports the"
        " concept of objects and classes. This allows for better organization of code"
        " and easier reuse of code across different projects."
    ),
    (
        "Overall, Python is a powerful and versatile language that is well-suited for a"
        " wide range of programming tasks."
    ),
)


async def send_mock(prompt, app_id, api_key, api_secret, gpt_url):
    # check if prompt start with "总结以下内容"
    if prompt.startswith("总结以下内容"):
        yield "总结内容"
        return

    for data in mock_data:
        yield data + "\n\n"

        # sleep 0.5s
        await asyncio.sleep(0.5)
