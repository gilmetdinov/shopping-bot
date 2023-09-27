import json
from api import request
from config.routes.api import ApiRoutes


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.routes = ApiRoutes
        self.__sender = request.Sender(self.base_url)

    async def ping(self):
        return await self.__sender.send_request(self.routes.ping.value,
                                                request_type='get')

    async def test(self, data):
        return await self.__sender.send_request(self.routes.test.value,
                                                request_type='post',
                                                data=json.dumps(data))

    async def bind(self, key, chat_id, username=''):
        return await self.__sender.send_request(self.routes.bind.value,
                                                request_type='post',
                                                data=json.dumps({'key': key, 'chat_id': chat_id, 'username': username}))

    async def check_user(self, chat_id):
        return await self.__sender.send_request(self.routes.check_user.value,
                                                request_type='post',
                                                data=json.dumps({'chat_id': chat_id}))

    async def get_unbind_code(self, chat_id):
        return await self.__sender.send_request(self.routes.get_unbind_code.value,
                                                request_type='post',
                                                data=json.dumps({'chat_id': chat_id}))

    async def unbind(self, chat_id):
        return await self.__sender.send_request(self.routes.unbind.value,
                                                request_type='post',
                                                data=json.dumps({'chat_id': chat_id}))

    async def get_wallet(self, chat_id, currency):
        return await self.__sender.send_request(self.routes.get_wallet.value,
                                                request_type='post',
                                                data=json.dumps({'chat_id': chat_id, 'currency': currency}))

    async def get_balance(self, chat_id):
        return await self.__sender.send_request(self.routes.get_balance.value,
                                                request_type='post',
                                                data=json.dumps({'chat_id': chat_id}))

    async def get_notif_settings(self, chat_id):
        return await self.__sender.send_request(self.routes.get_notif_settings.value,
                                                request_type='post',
                                                data=json.dumps({'chat_id': chat_id}))

    async def switch_notif(self, chat_id, _type):
        return await self.__sender.send_request(self.routes.switch_notif.value,
                                                request_type='post',
                                                data=json.dumps({'chat_id': chat_id,
                                                                 'type': _type}))

    async def get_service_list(self, _type, chat_id):
        return await self.__sender.send_request(self.routes.get_service_list.value,
                                                request_type='post',
                                                data=json.dumps({'type': _type,
                                                                 'chat_id': chat_id}))

    async def get_verif_order_cache(self, chat_id):
        return await self.__sender.send_request(self.routes.get_verif_order_cache.value,
                                                request_type='post',
                                                data=json.dumps({'chat_id': chat_id}))

    async def update_verif_order_cache(self, chat_id, order_data):
        return await self.__sender.send_request(self.routes.update_verif_order_cache.value,
                                                request_type='post',
                                                data=json.dumps({'chat_id': chat_id,
                                                                 'order_data': order_data}))

    async def delete_images(self, order_cache_id, chat_id):
        return await self.__sender.send_request(self.routes.delete_images.value,
                                                request_type='post',
                                                data=json.dumps({'chat_id': chat_id,
                                                                 'order_cache_id': order_cache_id}))

    async def upload_image(self, chat_id, order_cache_id, img_path):
        with open(img_path, 'rb') as img:
            return await self.__sender.send_request(self.routes.upload_image.value,
                                                    request_type='file',
                                                    data={'chat_id': chat_id,
                                                          'order_cache_id': order_cache_id,
                                                          'img': img})

    async def make_order(self, chat_id, _type, dto):
        order_data = dto.order_data()
        return await self.__sender.send_request(self.routes.make_order.value,
                                                request_type='post',
                                                data=json.dumps({'chat_id': chat_id,
                                                                 'order_data': order_data}))

    async def get_order_list(self, chat_id, _type, page):
        return await self.__sender.send_request(self.routes.get_order_list.value,
                                                request_type='post',
                                                data=json.dumps({'chat_id': chat_id,
                                                                 'type': _type,
                                                                 'page': page}))

    async def get_order_info(self, chat_id, _type, order_id):
        return await self.__sender.send_request(self.routes.get_order_info.value,
                                                request_type='post',
                                                data=json.dumps({'chat_id': chat_id,
                                                                 'type': _type,
                                                                 'order_id': order_id}))

    async def get_order_add_info(self, chat_id, _type, order_id):
        return await self.__sender.send_request(self.routes.get_order_add_info.value,
                                                request_type='post',
                                                data=json.dumps({'chat_id': chat_id,
                                                                 'type': _type,
                                                                 'order_id': order_id}))

    async def search_order(self, chat_id, params):
        return await self.__sender.send_request(self.routes.search_order.value,
                                                request_type='post',
                                                data=json.dumps({'chat_id': chat_id,
                                                                 'params': params}))
