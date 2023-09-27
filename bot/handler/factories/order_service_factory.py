from bot.handler.factories.enum import OrderServices
from utils.factory import AbstractFactory


class OrderServiceFactory(AbstractFactory):

    def __init__(self):
        super().__init__()
        self.services = OrderServices

    def get_order_service(self, order_type: str):
        enum_pos = self.get_attr(self.services, order_type)
        if enum_pos is None:
            return None
        return enum_pos.value
