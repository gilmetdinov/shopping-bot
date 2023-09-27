from abc import ABC, abstractmethod
from aiogram import Router
from api import ApiClient
import message as _message
from bot.helper import StateHelper


class AbstractProcess(ABC):

    service = None

    def __init__(self, api: ApiClient, router: Router):
        self.api = api
        self.router = router
        self.messageBuilder = _message.Builder()
        self.stateHelper = StateHelper()

    @abstractmethod
    def set(self):
        """Setting State + Message/Callback or Command routes for service methods"""
        pass
