<div align="center">
  <picture>
    <img alt="Delibird" src="images/describe.png" width=20%>
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
- [文心大模型](https://cloud.baidu.com/product/wenxinworkshop)
- [星火大模型](https://xinghuo.xfyun.cn/sparkapi)

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

[spark]
name = "spark"

[spark.v35]
version = "generalv3.5"
app_id = "XXX"
api_key = "XXX"
api_secret = "XXX"
url = "wss://spark-api.xf-yun.com/v3.5/chat"


[spark.v30]
version = "generalv3"
app_id = "XXX"
api_key = "XXX"
api_secret = "XXX"
url = "wss://spark-api.xf-yun.com/v3.1/chat"

[qwen]
name = "qwen"

[qwen.max] # qwen-turbo, qwen-plus, qwen-max
#http or websocket
api_key = "XXX"

[qwen.plus]
api_key = "XXX"

[ernie]
appid = 123456678
api_key = "XXX"
secret_key = "XXX"
url_prefix = "XXX"
access_token = "XXX"
# curl 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=[API Key]&client_secret=[Secret Key]'
# 获取 access_token

[ernie.v4]
url_suffix = "completions_pro"

[ernie.8k]
url_suffix = "ernie_bot_8k"
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

## 监控页面



## 版权
基于 [Apache-2.0](LICENSE) 版权，可以自由使用和修改。
