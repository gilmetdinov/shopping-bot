from utils.enums import DeliveryType
from bot.handler.dto.common import BaseOrderDto


class DeliveryDto(BaseOrderDto):
    address = None
    full_name = None
    phone_number = None
    delivery_type = DeliveryType.PickUpPoint.value

    def __init__(self, service: str, price: float, telegram: str = None, _type: str = None):
        super().__init__(_type=_type, service=service, price=price)
        self.telegram = telegram
        self.total_price = self.price * self.amount

    def set_address(self, address: str):
        self.address = address

    def set_full_name(self, full_name: str):
        self.full_name = full_name

    def set_phone_number(self, phone_number: str):
        self.phone_number = phone_number

    def set_telegram(self, telegram: str):
        self.telegram = telegram

    def set_delivery_type(self, delivery_type):
        self.delivery_type = delivery_type

    def validate(self):
        return 1 <= self.amount <= 20 and self.service and self.telegram and self.address and self.full_name and \
            self.phone_number

    def order_data(self):
        return {
            'type': self.type,
            'service': self.service,
            'amount': self.amount,
            'address': self.address,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'telegram': self.telegram,
            'delivery_type': self.delivery_type
        }
