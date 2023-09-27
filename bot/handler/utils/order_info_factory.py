from enum import Enum
from utils.factory import AbstractMessageFactory


class OrderInfoMessages(Enum):
    ident = ('ident_info', ['order_info'])
    wallet = ('wallet_info', ['order_info'])
    bundle = ('bundle_info', ['order_info'])


class OrderInfoFactory(AbstractMessageFactory):

    def __init__(self, builder, messages=OrderInfoMessages):
        super().__init__(builder=builder, messages=messages)

    def get_order_info_message(self, _type: str, order_info: dict):
        return self.get_message(_type, {'order_info': order_info})
