from aiogram import Router
from api import ApiClient
from bot.handler.processes import *
from bot.handler.processes.common import AbstractProcess


class Handler:

    def __init__(self, api: ApiClient, router: Router):
        self.api = api
        self.router = router

    def set_basic_processes(self):
        """/start, /help"""
        BasicProcess(api=self.api, router=self.router).set()

    def set_bind_process(self):
        """/bind"""
        BindProcess(api=self.api, router=self.router).set()

    def set_unbind_process(self):
        """/unbind, unbind confirm/cancel, unbind code, incorrect input"""
        UnbindProcess(api=self.api, router=self.router).set()

    def set_replenishment_process(self):
        """Choosing method, getting wallet"""
        ReplenishmentProcess(api=self.api, router=self.router).set()

    def set_settings(self):
        """Settings menu, switching notification settings"""
        SettingsProcess(api=self.api, router=self.router).set()

    def set_order_process(self):
        """Choosing order type, choosing service, creating order, not enough funds warning"""
        OrderProcess(api=self.api, router=self.router).set()
        for subprocess_name in OrderProcess.get_subprocesses():
            subprocess: AbstractProcess = subprocess_name(api=self.api, router=self.router)
            subprocess.set()

    def set_order_list_process(self):
        """Choosing order type, displaying order list, viewing order info, /search_order"""
        ListProcess(api=self.api, router=self.router).set()

    def set_test(self):
        pass
