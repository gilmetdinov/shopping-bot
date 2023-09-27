from bot.handler.dto.common import BaseOrderDto


class WalletDto(BaseOrderDto):

    def __init__(self, service: str, price: float):
        super().__init__(_type='wallet', service=service, price=price)
