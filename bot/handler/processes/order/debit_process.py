from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
import bot.states as states
from bot.keyboards import Callbacks
from bot.handler.processes.common import AbstractProcess
from bot.handler.services.order import DebitService


class DebitProcess(AbstractProcess):

    def __init__(self, api, router):
        super().__init__(api, router)
        self.service = DebitService(api=self.api)

    def set(self):
        @self.router.callback_query(
            states.Order.choosingDebit
        )
        async def set_debit_type(callback: CallbackQuery, state: FSMContext) -> None:
            await self.service.set_service(callback=callback, state=state)
