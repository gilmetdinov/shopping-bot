from bot.handler.factories.enum import OrderProcesses
from utils.factory import AbstractFactory


class OrderProcessFactory(AbstractFactory):

    def __init__(self):
        super().__init__()
        self.processes = OrderProcesses

    def get_order_process(self, order_type: str):
        enum_pos = self.get_attr(self.processes, order_type)
        if enum_pos is None:
            return None
        return enum_pos.value
