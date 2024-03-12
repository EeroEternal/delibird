"""字节语雀大模型."""

import os
from .base import Base
from volcengine.maas import MaasService, MaasException, ChatRole


class Skylark(Base):
    def __init__(self):
        self.group_id = ""

    def read_config(self, config):
        result, message = super().read_config(config)

        if not result:
            return result, message

        # 读取 url 、region、access_key, secret_key
        url = config.get("url")
        region = config.get("region")
        access_token = config.get("access_token")
        secret_key = config.get("secret_key")

        if not all([url, region, access_token, secret_key]):
            return False, "url、region、access_key、secret_key 不能为空"

        self.url = url
        self.region = region
        self.access_token = access_token
        self.secret_key = secret_key

        return True, "success"

    async def send(self, messages, model):
        if not self.url:
            yield "url 不能为空"

        maas = MaasService(self.url, self.region)

        maas.set_ak(self.access_token)
        maas.set_sk(self.secret_key)

        # document: "https://www.volcengine.com/docs/82379/1099475"
        req = {
            "model": {
                "name": model,
            },
            "messages": messages,
        }

        try:
            resps = maas.stream_chat(req)
            for resp in resps:
                yield resp.choice.message.content

        except MaasException as e:
            print(e)
