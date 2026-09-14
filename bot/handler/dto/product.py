from bot.handler.dto.common import BaseOrderDto


class ProductDto(BaseOrderDto):

    def __init__(self, service: str, service_label: str, price: float):
        super().__init__(_type='product', service=service, service_label=service_label, price=price)
