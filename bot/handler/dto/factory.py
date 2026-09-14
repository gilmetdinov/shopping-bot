from enum import Enum
from .service import ServiceDto
from .product import ProductDto
from .product_b import ProductBDto
from .product_c import ProductCDto
from utils.factory import AbstractFactory


class DtoEnum(Enum):
    service = ServiceDto
    product = ProductDto
    product_b = ProductBDto
    product_c = ProductCDto


class DtoFactory(AbstractFactory):

    def __init__(self):
        super().__init__()
        self.dtoEnum = DtoEnum

    def get_dto(self, order_type: str, **kwargs):
        enum_info = self.get_attr(self.dtoEnum, order_type)
        return enum_info.value(**kwargs) if enum_info else None
