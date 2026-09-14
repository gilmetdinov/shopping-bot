from enum import Enum
from .order import Order
from utils.factory import AbstractFactory


class StepTwoStates(Enum):
    product = Order.choosingProduct
    product_b = Order.choosingProductB
    product_c = Order.choosingProductC


class StepTwoFactory(AbstractFactory):
    def __init__(self):
        super().__init__()
        self.states = StepTwoStates

    def get_step_two_state(self, order_type: str):
        return self.get_attr(self.states, order_type).value if self.get_attr(self.states, order_type) else None


class FormStates(Enum):
    service = Order.serviceForm
    product = Order.productForm
    product_b = Order.product_bForm
    product_c = Order.product_cForm


class FormFactory(AbstractFactory):
    def __init__(self):
        super().__init__()
        self.states = FormStates

    def get_form_state(self, order_type: str):
        return self.get_attr(self.states, order_type).value if self.get_attr(self.states, order_type) else None
