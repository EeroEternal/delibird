"""Fast api server."""

# pylint: disable=no-name-in-module, unused-argument, no-member, unused-variable
import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from delibird.util import read_config
from delibird.util import Log
from delibird.router import Gateway


app = FastAPI()

gateway = Gateway()

# Allow requests from any domain
origins = ["*"]

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    """Startup."""
    global router
    config_file = os.getenv("CONFIG_FILE", "config.toml")
    gateway.read_config(config_file)


@app.on_event("shutdown")
def shutdown():
    """Shutdown."""


@app.get("/ping")
async def ping():
    return "pong"


@app.post("/{maas}/chat/completion")
async def chat_completion(maas: str, request: dict):
    """Chat completion.

    Args:
        maas (str): llm 服务.例如 spark、openai、qwen等，代表各种模型路由
        request (object): 类似 {"chat": messages, "model": "v15"}
    """

    # get messages and model from request
    messages = request.get("chat")
    model = request.get("model")

    # check if messages and model are not None
    if not messages or not model:
        return "messages or model is None"

    # 发送请求
    global gateway
    return gateway.send(maas, messages, model)
