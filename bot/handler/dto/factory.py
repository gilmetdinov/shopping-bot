from enum import Enum
from .ident import IdentDto
from .wallet import WalletDto
from .bundle import BundleDto
from .debit import DebitDto
from utils.factory import AbstractFactory


class DtoEnum(Enum):
    ident = IdentDto
    wallet = WalletDto
    bundle = BundleDto
    debit = DebitDto


class DtoFactory(AbstractFactory):

    def __init__(self):
        super().__init__()
        self.dtoEnum = DtoEnum

    def get_dto(self, order_type: str, **kwargs):
        enum_info = self.get_attr(self.dtoEnum, order_type)
        return enum_info.value(**kwargs) if enum_info else None
