import abc


class StreamBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def send(self):
        """ "发送消息.

        返回一个 fastapi 的 StreamingResponse 消息
        """
        pass

    @abc.abstractmethod
    def close(self):
        """关闭连接."""
        pass
