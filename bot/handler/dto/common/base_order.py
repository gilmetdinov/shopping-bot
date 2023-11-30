from bot.handler.dto.common import AbstractOrderDto


class BaseOrderDto(AbstractOrderDto):

    def __init__(self, service: str, service_label: str, price: float, _type: str = None):
        super().__init__(_type=_type)
        self.service = service
        self.service_label = service_label
        self.price = price
        self.amount = 1
        self.total_price = self.price * self.amount

    def set_amount(self, amount: int):
        self.amount = amount
        self.total_price = self.price * self.amount

    def validate(self):
        return 1 <= self.amount <= 50 and self.service

    def order_data(self):
        return {
            'type': self.type,
            'service': self.service,
            'amount': self.amount
        }
