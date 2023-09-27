from aiogram import Router, F
from api import ApiClient
from aiogram.filters import Command
import bot.commands as commands
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.handler.processes.common import AbstractProcess
from bot.handler.services import BasicService
import bot.keyboards as keyboards
from bot.helper import StateHelper


class BasicProcess(AbstractProcess):

    def __init__(self, api: ApiClient, router: Router):
        super().__init__(api=api, router=router)
        self.service = BasicService(api=api)

    def set(self):
        @self.router.message(Command(commands=[commands.List.start.name]))
        async def command_start_handler(message: Message, state: FSMContext) -> None:
            await self.service.command_start_handler(message=message, state=state)

        @self.router.message(Command(commands=[commands.List.help.name]))
        async def command_help_handler(message: Message, state: FSMContext) -> None:
            await self.service.command_help_handler(message=message, state=state)

        for _state in StateHelper().to_main_page_states():
            @self.router.message(
                _state,
                F.text.contains(keyboards.List.toMain.value[0])
            )
            async def go_to_main_page(message: Message, state: FSMContext) -> None:
                await self.service.go_to_main_page(message=message, state=state)
