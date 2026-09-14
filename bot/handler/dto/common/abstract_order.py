from abc import ABC, abstractmethod


class AbstractOrderDto(ABC):

    def __init__(self, _type: str or None = None):
        self.type = _type

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def order_data(self):
        pass
