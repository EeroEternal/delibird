from .base import Base
from delibird.util import common_decode


class Baichuan(Base):
    def __init__(self):
        self.name = "baichuan"

    async def send(self, messages, model):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key,
        }

        # 调用父类的 send 方法
        async for data in super().send(
            messages, model, headers=headers, filter_func=common_decode
        ):
            yield data
