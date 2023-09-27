from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from api import ApiClient
import bot.states as states
import bot.keyboards as keyboards
import bot.commands as commands
from bot.handler.processes.common import AbstractProcess
from bot.handler.services import UnbindService


class UnbindProcess(AbstractProcess):

    def __init__(self, api: ApiClient, router: Router):
        super().__init__(api, router)
        self.service = UnbindService(api=api)

    def set(self):
        @self.router.message(Command(commands=[commands.List.unbind.name]))
        async def command_unbind_handler(message: Message, state: FSMContext) -> None:
            await self.service.command_unbind_handler(message=message, state=state)

        @self.router.message(
            states.Unbind.confirming,
            F.text.in_(keyboards.List.confirmation.value[0])
        )
        async def unbind_confirmed(message: Message, state: FSMContext) -> None:
            await self.service.unbind_confirmed(message=message, state=state)

        @self.router.message(
            states.Unbind.confirming,
            F.text.in_(keyboards.List.confirmation.value[1])
        )
        async def unbind_canceled(message: Message, state: FSMContext) -> None:
            await self.service.unbind_canceled(message=message, state=state)

        @self.router.message(
            states.Unbind.confirming
        )
        async def incorrect_input(message: Message) -> None:
            await self.service.incorrect_input(message=message)

        @self.router.message(
            states.Unbind.awaitingCode
        )
        async def check_unbind_code(message: Message, state: FSMContext) -> None:
            await self.service.check_unbind_code(message=message, state=state)
