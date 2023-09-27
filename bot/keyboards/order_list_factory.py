from enum import Enum
from bot.keyboards.enum import KeyboardEnum as List
from utils.factory import AbstractFactory


class OrderTypeList(Enum):
    ident = List.identType.value
    wallet = List.walletType.value
    bundle = List.bundleType.value
    debit = List.debitType.value
    identList = List.identType.value
    walletList = List.walletType.value
    bundleList = dict(list(List.bundleType.value.items()) + list(List.debitType.value.items()))


class OrderListFactory(AbstractFactory):

    def __init__(self):
        super().__init__()
        self.list = OrderTypeList

    def get_order_list(self, order_type: str):
        service_list = self.get_attr(self.list, order_type)
        if service_list is None:
            return None
        return service_list.value
