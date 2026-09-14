from bot.handler.factories.enum import OrderHandlers
from utils.factory import AbstractFactory


class OrderHandlerFactory(AbstractFactory):

    def __init__(self):
        super().__init__()
        self.handlers = OrderHandlers

    def get_order_handler(self, order_type: str):
        enum_pos = self.get_attr(self.handlers, order_type)
        if enum_pos is None:
            return None
        return enum_pos.value
