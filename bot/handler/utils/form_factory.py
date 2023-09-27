from enum import Enum
from .keyboards import ident_form_keyboard, wallet_form_keyboard, delivery_form_keyboard
from utils.factory import AbstractMessageFactory, AbstractKeyboardFactory


class FormKeyboards(Enum):
    ident = (ident_form_keyboard, ['dto'])
    wallet = (wallet_form_keyboard, [])
    bundle = (delivery_form_keyboard, ['dto'])
    debit = (delivery_form_keyboard, ['dto'])


class FormKeyboardFactory(AbstractKeyboardFactory):
    def __init__(self):
        super().__init__(FormKeyboards)

    def get_form_keyboard(self, order_type: str, kwargs: dict = None):
        return self.get_keyboard(order_type, kwargs)


class FormMessages(Enum):
    ident = ('get_ident_form', ['dto'])
    wallet = ('get_wallet_form', ['dto'])
    bundle = ('get_delivery_form', ['dto', 'username'])
    debit = ('get_delivery_form', ['dto', 'username'])


class FormMessageFactory(AbstractMessageFactory):
    def __init__(self, builder):
        super().__init__(builder, FormMessages)

    def get_form(self, order_type: str, kwargs: dict = None):
        return self.get_message(order_type, kwargs)
