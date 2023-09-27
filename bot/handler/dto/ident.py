from bot.handler.dto import ImageDto
from bot.handler.dto.common import AbstractOrderDto


class IdentDto(AbstractOrderDto):

    def __init__(self, order_cache: dict):
        super().__init__(_type='ident')
        self.order_cache_id = order_cache['id']
        self.service = order_cache['service']
        self.service_price = order_cache['service_price']
        self.wallet = order_cache['wallet'] or None
        # todo MD: не реализован заказ с кастомными данными,
        #  поэтому костыль, на случай если получили data_type 2 из кэша
        self.docs_type = 1 if order_cache['data_type'] == 2 else order_cache['data_type']
        self.docs_price = order_cache['data_price']
        self.premium = order_cache['premium'] or 0
        self.premium_price = order_cache['premium_price']
        self.price = self.service_price + self.docs_price + self.premium * self.premium_price
        self.docs_images = {'img_one': ImageDto(),
                            'img_two': ImageDto(),
                            'img_three': ImageDto()}
        self.docs_string = None
        if self.docs_type == 0:
            for key in self.docs_images.keys():
                self.docs_images[key] = ImageDto(*order_cache['data'][key].values())
        elif self.docs_type == 3:
            self.docs_string = order_cache['data']

    def load_images(self, data: dict):
        for key in data.keys():
            self.docs_images[key].set_image(url=data[key]['url'],
                                            path=data[key]['path'],
                                            name=data[key]['name'])

    def delete_images(self):
        self.docs_images = {'img_one': ImageDto(),
                            'img_two': ImageDto(),
                            'img_three': ImageDto()}
        return True

    def set_service(self, service, price: int | float):
        self.service = service
        self.price -= self.service_price
        self.service_price = int(price) if float(price).is_integer() else price
        self.price += self.service_price

    def set_wallet(self, wallet_number):
        self.wallet = wallet_number

    def set_docs_type(self, docs_type, price: int | float = 0):
        self.docs_type = docs_type
        self.price -= self.docs_price
        self.docs_price = int(price) if float(price).is_integer() else price
        self.price += self.docs_price

    def set_docs_string(self, data: str):
        self.docs_string = data.strip() or None

    def switch_premium(self, price: int | float = 0):
        self.price -= self.premium_price * self.premium
        self.premium = int(not bool(self.premium))
        if price:
            self.premium_price = int(price) if float(price).is_integer() else price
        self.price += self.premium_price * self.premium

    def __validate_docs_images(self):
        flag = False
        for image in self.docs_images.values():
            if image.validate():
                flag = True
        return flag

    def validate_docs(self):
        if self.docs_type == 0 and not self.__validate_docs_images():
            return False
        elif self.docs_type == 3 and not self.docs_string:
            return False
        return True

    def validate(self):
        if self.service and self.wallet and self.validate_docs() and self.price:
            return True
        return False

    def order_data(self):
        return {
            'type': self.type,
            'order_cache_id': self.order_cache_id,
            'service': self.service,
            'wallet': self.wallet,
            'docs_type': self.docs_type,
            'docs_string': self.docs_string,
            'docs_images': {
                'img_one': self.docs_images['img_one'].get_data(),
                'img_two': self.docs_images['img_two'].get_data(),
                'img_three': self.docs_images['img_three'].get_data()
            },
            'premium': self.premium,
            'service_price': self.service_price,
            'docs_price': self.docs_price,
            'premium_price': self.premium_price if self.premium else 0
        }

    def docs_data(self):
        data = {}
        if self.docs_type == 0:
            for key in self.docs_images.keys():
                if self.docs_images[key].url:
                    data[key] = self.docs_images[key].url
        elif self.docs_type == 3:
            data['string'] = self.docs_string
        return data
