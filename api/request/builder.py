import aiohttp
import logging
from utils.sign import SignGenerator


class RequestBuilder:

    def __init__(self, client: aiohttp.ClientSession, request: str, request_type: str, params, data):
        self.client = client
        self.request = request
        self.type = request_type
        self.params = params
        self.data = data
        self.signGenerator = SignGenerator()

    async def get_request(self):
        query = ''
        if self.params is not None:
            query += '/?'
            for key in self.params:
                query += f"{key}={self.params}&"
            query -= '&'

        async with self.client.get(self.request + query) as resp:
            if resp.status != 200:
                logging.log(level=logging.WARN, msg=f"Unsuccessful status on GET request: {resp.status}!")
                return {'status': 'error', 'code': -1}
            return await resp.json()

    async def post_request(self):
        self.data = self.signGenerator.add_sign(json_data=self.data)
        logging.log(level=logging.INFO, msg=str(self.data))  # todo MD: undeployed
        async with self.client.post(self.request, data=self.data) as resp:
            if resp.status != 200:
                logging.log(level=logging.WARN, msg=f"Unsuccessful status on POST request: {resp.status}!")
                return {'status': 'error', 'code': -1}
            return await resp.json()

    async def post_file_request(self):
        async with self.client.post(self.request, data=self.data) as resp:
            if resp.status != 200:
                logging.log(level=logging.WARN, msg=f"Unsuccessful status on POST FILE request: {resp.status}!")
                return {'status': 'error', 'code': -1}
            return await resp.json()

    async def process_request(self):
        if self.type.upper() == 'POST':
            return await self.post_request()
        elif self.type.upper() == 'FILE':
            return await self.post_file_request()
        elif self.type.upper() == 'GET':
            return await self.get_request()
        else:
            return {'status': 'error', 'message': 'Unexpected request type!'}
