from enum import Enum
from .keyboards import service_reply_keyboard, service_pagination_keyboard
from utils.factory import AbstractMessageFactory, AbstractKeyboardFactory


class StepTwoKeyboards(Enum):
    service = (service_reply_keyboard, ['_type', 'service_list'])
    product = (service_pagination_keyboard, ['service_list', 'page'])
    product_b = (service_reply_keyboard, ['_type', 'service_list'])
    product_c = (service_pagination_keyboard, ['service_list', 'page'])


class StepTwoKeyboardFactory(AbstractKeyboardFactory):
    def __init__(self):
        super().__init__(StepTwoKeyboards)

    def get_step_two_keyboard(self, order_type: str, kwargs: dict = None):
        return self.get_keyboard(order_type, kwargs)


class StepTwoMessages(Enum):
    service = ('choose_handler', ['is_alert'])
    product = ('service_pagination_list', ['_type', 'service_list', 'page'])
    product_b = ('choose_product_b', [])
    product_c = ('service_pagination_list', ['_type', 'service_list', 'page'])


class StepTwoMessageFactory(AbstractMessageFactory):
    def __init__(self, builder, messages=StepTwoMessages):
        super().__init__(builder=builder, messages=messages)

    def get_step_two_message(self, order_type: str, kwargs: dict = None):
        return self.get_message(order_type, kwargs)
