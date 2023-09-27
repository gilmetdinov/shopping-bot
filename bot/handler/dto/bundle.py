from bot.handler.dto.common import DeliveryDto


class BundleDto(DeliveryDto):

    def __init__(self, service: str, price: float, telegram: str = None):
        super().__init__(_type='bundle', service=service, price=price, telegram=telegram)
