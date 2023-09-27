from bot.handler.dto.common import DeliveryDto


class DebitDto(DeliveryDto):

    def __init__(self, service: str, price: float, telegram: str = None):
        super().__init__(_type='debit', service=service, price=price, telegram=telegram)
