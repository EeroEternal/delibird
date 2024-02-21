<div align="center">
  <picture>
    <img alt="Delibird" src="images/describe.png" width=10%>
  </picture>
</div>

---
Delibird 是一个多合一大模型接口网关。主要针对国内的大模型，包括文心、百川、千问、星火、智谱等提供统一的接口调用。基于 Python 开发，容易集成。原生提供 Streaming 接口、多进程异步调度模式，性能较好、调用接口完全兼容 openai APi，方便集成。

## 特点

- 完全 python 代码，容易修改和集成到项目中
- 接口简单。兼容 openai 接口，一套接口调用全部模型
- 支持 http、https 和 websocket 接口
- 支持几乎全部国内大模型，包括文心、百川、千问、星火、智谱等
- 支持 Streaming 接口，支持多轮对话
- 采用 Python asyncio 原生异步和多进程模型，性能较好

## 支持模型列表

- [通义千问](https://dashscope.console.aliyun.com/model)
- [文心](https://cloud.baidu.com/product/wenxinworkshop)
- [星火](https://xinghuo.xfyun.cn/sparkapi)
- [Minimax](https://api.minimax.chat/)
- [ChatGLM](https://open.bigmodel.cn/dev/api)
- [百川](https://www.baichuan-ai.com/home)

## 未来计划
- [ ] 开发管理页面
- [ ] function calling 支持

## 使用教程

### 环境配置

建议基于 python 3.12 以上版本，可以获得更好的性能。具体依赖库可以参考 requirements.txt 文件。

~~~shell
pip install -r requirements.txt
~~~

### 安装

通过 Pypi 安装

~~~shell
pip install delibird
~~~

### 运行

启动服务之前需要配置一个配置文件，文件内设置好对应的模型端口和 api_key。配置文件格式如下：

```toml
[server]
host = "localhost"
port = 8000

# name 是 router 的名称，对应的配置在 "config.name" 下面。driver 是对应的驱动名称。
# base 是默认的驱动,兼容 openai
routers = [
    { name = "spark", driver = "spark" },
    { name = "qwen", driver = "qwen" },
    { name = "ernie", driver = "ernie" },
    { name = "minimax", driver = "minimax" },
    { name = "chatglm", driver = "chatglm" },
    { name = "baichuan", driver = "base" },
    { name = "moonshot", driver = "base" }]

[config]
[config.spark]
# general 指向V1.5版本; generalv2 指向V2版本; generalv3 指向V3版本; generalv3.5 指向V3.5版本;
app_id = "XXX"
api_key = "XXX"
api_secret = "XXX"
url = "wss://spark-api.xf-yun.com"
models = ["general", "generalv2", "generalv3", "generalv3.5"]

[config.qwen]
api_key = "XXX"
models = ["qwen-turbo", "qwen-plus", "qwen-max"]


[config.ernie]
appid = 50396495
api_key = "XXX"
secret_key = "XXX"
url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat"
access_token = "XXX"
models = [ "ernie", "ernie-v4", "ernie-8k", "ernie-bot", "ernie-speed", "ernie-bot-turbo"]

[config.minimax]
api_key = "XXX"
url = "https://api.minimax.chat/v1/text"
models = ["chatcompletion", "chatcompletion_pro"]

[config.openai]
api_key = "xxx"
models = ["gpt-3.5-turbo", "gpt-4"]
```

替换掉上面的 "XXX" 为对应的 api_key 或者其他配置信息。"qwen.max" 后面的 max 代表模型名称，前面的 "qwen" 代表模型服务路由

- 配置文件可以参考 [config.toml](./examples/config.toml) 文件

然后运行服务

```shell
delibird start -c config.toml
```
key.toml 就是配置文件，可以带路径。例如，/home/aaa/delibird/config.toml

停止服务

```shell
delibird stop
```

### 调用接口
通过 http 调用接口，下面是用 python 的一个例子

```python
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

    chat = Chat("v30")

    async for result in chat.stream_fetch(messages, url):
        print(result)


def test_client():
    asyncio.run(stream_fetch())
```

指定url、模型名称和版本号，然后调用接口即可。

## 监控页面



## 版权
基于 [Apache-2.0](LICENSE) 版权，可以自由使用和修改。
