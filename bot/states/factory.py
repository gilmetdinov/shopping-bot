from enum import Enum
from .order import Order
from utils.factory import AbstractFactory


class StepTwoStates(Enum):
    wallet = Order.choosingWallet
    bundle = Order.choosingBundle
    debit = Order.choosingDebit


class StepTwoFactory(AbstractFactory):
    def __init__(self):
        super().__init__()
        self.states = StepTwoStates

    def get_step_two_state(self, order_type: str):
        return self.get_attr(self.states, order_type).value if self.get_attr(self.states, order_type) else None


class FormStates(Enum):
    ident = Order.identForm
    wallet = Order.walletForm
    bundle = Order.bundleForm
    debit = Order.debitForm


class FormFactory(AbstractFactory):
    def __init__(self):
        super().__init__()
        self.states = FormStates

    def get_form_state(self, order_type: str):
        return self.get_attr(self.states, order_type).value if self.get_attr(self.states, order_type) else None
