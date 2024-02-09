"""Fast api server."""

# pylint: disable=no-name-in-module, unused-argument, no-member, unused-variable
import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from delibird.router import spark_send, qwen_send, ernie_send
from delibird.config import read_config
from delibird.log import Log


app = FastAPI()

config = None

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
    global config
    config_file = os.getenv("CONFIG_FILE", "config.toml")
    config = read_config(config_file)


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
    global config

    if maas == "spark":
        return spark_send(config, request)

    if maas == "qwen":
        return qwen_send(config, request)

    if maas == "ernie":
        return ernie_send(config, request)
