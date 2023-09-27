from aiogram import Dispatcher
from bot.client import Bot
from bot.router import Router


class BotDispatcher:

    def __init__(self, bot: Bot, api):
        self.instance = Dispatcher()
        self.__bot = bot
        self.__router = Router(api=api)
        self.instance.include_router(self.__router.instance)  # подключаем роутер

    async def feed_webhook(self, webhook) -> None:
        await self.instance.feed_webhook_update(self.__bot.instance, webhook)
        await self.__bot.close_session()
