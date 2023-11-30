from bot.handler.dto.common import DeliveryDto


class BundleDto(DeliveryDto):

    def __init__(self, service: str, service_label: str, price: float, telegram: str = None):
        super().__init__(_type='bundle', service=service, price=price, telegram=telegram, service_label=service_label)
