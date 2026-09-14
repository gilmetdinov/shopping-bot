from enum import Enum
from .keyboards import service_form_keyboard, product_form_keyboard, delivery_form_keyboard
from utils.factory import AbstractMessageFactory, AbstractKeyboardFactory


class FormKeyboards(Enum):
    service = (service_form_keyboard, ['dto'])
    product = (product_form_keyboard, [])
    product_b = (delivery_form_keyboard, ['dto'])
    product_c = (delivery_form_keyboard, ['dto'])


class FormKeyboardFactory(AbstractKeyboardFactory):
    def __init__(self):
        super().__init__(FormKeyboards)

    def get_form_keyboard(self, order_type: str, kwargs: dict = None):
        return self.get_keyboard(order_type, kwargs)


class FormMessages(Enum):
    service = ('get_service_form', ['dto'])
    product = ('get_product_form', ['dto'])
    product_b = ('get_delivery_form', ['dto', 'username'])
    product_c = ('get_delivery_form', ['dto', 'username'])


class FormMessageFactory(AbstractMessageFactory):
    def __init__(self, builder):
        super().__init__(builder, FormMessages)

    def get_form(self, order_type: str, kwargs: dict = None):
        return self.get_message(order_type, kwargs)
