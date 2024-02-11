"""抽象类"""

from abc import ABC, abstractmethod


class Base(ABC):
    def __init__(self):
        self.url = ""
        self.messages = ""
        self.modal = None

    @abstractmethod
    def send(self):
        pass
