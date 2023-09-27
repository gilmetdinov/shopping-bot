import aiohttp
from api import request as _request


class RequestSender:

    def __init__(self, base_url):
        self.__base_url = base_url

    async def send_request(self, request, request_type, params=None, data=None):
        async with aiohttp.ClientSession(base_url=self.__base_url) as client:
            return await _request.Builder(client=client,
                                          request=request,
                                          request_type=request_type,
                                          params=params,
                                          data=data).process_request()
