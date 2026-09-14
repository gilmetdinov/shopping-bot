import json
from aiohttp import web
from aiohttp.web_request import Request
from config.routes import WebRoutes
from bot.client import Bot
from bot.dispatcher import Dispatcher as Dp
from api import ApiClient
import utils


class WebApp:

    def __init__(self, bot: Bot, dp: Dp, api: ApiClient):
        self.bot = bot
        self.dp = dp
        self.api = api
        self.routes = web.RouteTableDef()
        self.set_routes()  # устанавливаем руты
        self.instance = web.Application()
        self.instance.add_routes(self.routes)  # подключаем руты

    def set_routes(self):
        @self.routes.get(WebRoutes.ping.value)
        async def ping(request: Request):
            resp = {'status': 'success'}
            if 'status' in resp:
                return web.Response(text=json.dumps({'status': resp['status']}))
            else:
                return web.Response(text=json.dumps({'status': 'error', 'message': 'No status received from server!'}))

        @self.routes.post(WebRoutes.test.value)
        async def test(request: Request):
            post_data = await request.json(loads=json.loads)
            # resp = await self.api.test(data=post_data)
            return web.Response(text=json.dumps(post_data))

        @self.routes.post(WebRoutes.hook.value)
        async def hook_handler(request: Request):
            post_data = await request.json(loads=json.loads)
            await self.dp.feed_webhook(post_data)
            return web.Response(text="Success")

        @self.routes.post(WebRoutes.sendMessage.value)
        async def send_message(request: Request):
            try:
                post_data = await request.json(loads=json.loads)
            except Exception:
                response = json.dumps({'status': 'error', 'message': f"{await request.text()}"})
                return web.Response(text=response)
            chat_id = post_data['chat_id']
            message = post_data['message']
            if await self.bot.send_message(chat_id=chat_id, message=message):
                response = json.dumps({'status': 'success'})
            else:
                response = json.dumps({'status': 'error', 'message': "Couldn't send the message"})
            return web.Response(text=response)

        @self.routes.post(WebRoutes.sendMessageMass.value)
        async def send_message_mass(request: Request):
            try:
                post_data = await request.json(loads=json.loads)
            except Exception:
                response = json.dumps({'status': 'error', 'message': f"{await request.text()}"})
                return web.Response(text=response)
            chat_ids = post_data['chat_ids']
            message = post_data['message']
            bot_resp = await self.bot.send_message_mass(chat_ids=chat_ids, message=message)
            response = json.dumps(utils.response.check_mass_send_response(response=bot_resp))
            return web.Response(text=response)

        @self.routes.post(WebRoutes.sendNotification.value)
        async def send_notification(request: Request):
            try:
                post_data = await request.json(loads=json.loads)
            except Exception:
                response = json.dumps({'status': 'error', 'message': f"{await request.text()}"})
                return web.Response(text=response)
            chat_id = post_data['chat_id']
            notif_type = post_data['type']
            contents = post_data['contents']
            if await self.bot.send_notification(chat_id=chat_id, notif_type=notif_type, contents=contents):
                response = json.dumps({'status': 'success'})
            else:
                response = json.dumps({'status': 'error', 'message': "Couldn't send the notification"})
            return web.Response(text=response)

        @self.routes.post(WebRoutes.sendNotificationMass.value)
        async def send_notification_mass(request: Request):
            try:
                post_data = await request.json(loads=json.loads)
            except Exception:
                response = json.dumps({'status': 'error', 'message': f"{await request.text()}"})
                return web.Response(text=response)
            chat_ids = post_data['chat_ids']
            notif_type = post_data['type']
            contents = post_data['contents']
            # print(post_data)  # debug
            bot_resp = await self.bot.send_notification_mass(chat_ids=chat_ids, notif_type=notif_type, contents=contents)
            if bot_resp:
                response = json.dumps(utils.response.check_mass_send_response(response=bot_resp))
            else:
                response = json.dumps({'status': 'error', 'message': "Undefined notification type"})
            return web.Response(text=response)
