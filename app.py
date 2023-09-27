import logging
import asyncio
from aiohttp import web
from bot.dispatcher import Dispatcher
from bot.client import Bot
from web import WebApp
import api


class App:

    def __init__(self, token, webhook_url, base_api_url, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.apiCli = api.ApiClient(base_url=base_api_url)
        self.bot = Bot(token=token, webhook_url=webhook_url)
        self.dp = Dispatcher(bot=self.bot, api=self.apiCli)
        self.webApp = WebApp(bot=self.bot, dp=self.dp, api=self.apiCli)
        self.logInfo = logging.INFO
        self.logWarn = logging.WARNING
        self.loop = asyncio.new_event_loop()

    @classmethod
    def __get_logger(cls, filename, level, name):
        logging.basicConfig(filename=filename,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=level)
        logging.info(f"Setting up {name} logger")
        return logging.getLogger(name)

    async def on_startup(self) -> None:
        if await self.bot.set_webhook():
            logging.log(self.logInfo, "Webhook url set successfully")
        else:
            logging.log(self.logWarn, "Couldn't set up webhook url!")

        if await self.bot.set_commands():
            logging.log(self.logInfo, "Commands set successfully")
        else:
            logging.log(self.logWarn, "Couldn't set up commands!")

        await self.bot.close_session()

    async def on_shutdown(self) -> None:
        await self.bot.close_session()

        if await self.bot.delete_webhook():
            logging.log(self.logInfo, "Successfully deleted webhook url")
        else:
            logging.log(self.logWarn, "Couldn't delete webhook url!")

        if await self.bot.delete_commands():
            logging.log(self.logInfo, "Successfully deleted commands")
        else:
            logging.log(self.logWarn, "Couldn't delete commands!")

        await self.bot.close_session()

    def run(self):
        logging.basicConfig(filename='logs/info.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=self.logInfo)

        self.loop.run_until_complete(self.on_startup())

        web.run_app(self.webApp.instance, loop=self.loop, host=self.host, port=self.port)

        if self.loop.is_closed():
            self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.on_shutdown())
        self.loop.close()
