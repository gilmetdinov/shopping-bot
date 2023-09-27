from enum import Enum
from .keyboards import service_reply_keyboard, service_pagination_keyboard
from utils.factory import AbstractMessageFactory, AbstractKeyboardFactory


class StepTwoKeyboards(Enum):
    ident = (service_reply_keyboard, ['_type', 'service_list'])
    wallet = (service_pagination_keyboard, ['service_list', 'page'])
    bundle = (service_reply_keyboard, ['_type', 'service_list'])
    debit = (service_pagination_keyboard, ['service_list', 'page'])


class StepTwoKeyboardFactory(AbstractKeyboardFactory):
    def __init__(self):
        super().__init__(StepTwoKeyboards)

    def get_step_two_keyboard(self, order_type: str, kwargs: dict = None):
        return self.get_keyboard(order_type, kwargs)


class StepTwoMessages(Enum):
    ident = ('choose_service', ['is_alert'])
    wallet = ('service_pagination_list', ['_type', 'service_list', 'page'])
    bundle = ('choose_bundle', [])
    debit = ('service_pagination_list', ['_type', 'service_list', 'page'])


class StepTwoMessageFactory(AbstractMessageFactory):
    def __init__(self, builder, messages=StepTwoMessages):
        super().__init__(builder=builder, messages=messages)

    def get_step_two_message(self, order_type: str, kwargs: dict = None):
        return self.get_message(order_type, kwargs)
