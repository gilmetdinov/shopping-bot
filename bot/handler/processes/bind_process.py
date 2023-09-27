from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from api import ApiClient
from bot.handler.processes.common import AbstractProcess
from bot.handler.services import BindService
from bot.commands import List


class BindProcess(AbstractProcess):

    def __init__(self, api: ApiClient, router: Router):
        super().__init__(api, router)
        self.service = BindService(api=self.api)

    def set(self):
        @self.router.message(Command(commands=[List.bind.name]))
        async def command_bind_handler(message: Message, state: FSMContext) -> None:
            await self.service.command_bind_handler(message=message, state=state)
