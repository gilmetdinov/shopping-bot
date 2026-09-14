from aiogram import Router
from api import ApiClient
from bot.handler import Handler


class BotRouter:

    def __init__(self, api: ApiClient):
        self.api = api
        self.instance = Router()
        self.handler = Handler(api=self.api, router=self.instance)
        self.set_commands()

    def set_commands(self):

        self.handler.set_basic_processes()

        self.handler.set_bind_process()

        self.handler.set_unbind_process()

        self.handler.set_replenishment_process()

        self.handler.set_settings()

        self.handler.set_order_process()

        self.handler.set_order_list_process()

        # Глобальный fallback — ПОСЛЕДНИМ, ловит всё нераспознанное.
        self.handler.set_fallback_process()

        # self.handler.set_test()
