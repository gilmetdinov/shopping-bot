from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import bot.states as states
from bot.keyboards import Callbacks
from bot.handler.processes.common import AbstractProcess
from bot.handler.handlers.order import ProductCHandler


class ProductCProcess(AbstractProcess):

    def __init__(self, api, router):
        super().__init__(api, router)
        self.service = ProductCHandler(api=self.api)

    def set(self):
        @self.router.callback_query(
            states.Order.choosingProductC
        )
        async def set_product_c_type(callback: CallbackQuery, state: FSMContext) -> None:
            await self.service.set_handler(callback=callback, state=state)
