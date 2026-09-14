from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import bot.states as states
from bot.handler.processes.common import AbstractProcess
from bot.handler.handlers.order import ProductHandler
from bot.keyboards import List, Callbacks


class ProductProcess(AbstractProcess):
    type = 'product'

    def __init__(self, api, router):
        super().__init__(api, router)
        self.service = ProductHandler(api=self.api)

    def set(self):
        @self.router.message(
            states.Order.choosingProductCategory,
            F.text.in_(List.productCategory.value)
        )
        async def choose_product(message: Message, state: FSMContext) -> None:
            await self.service.display_service_list(message=message, state=state)

        @self.router.callback_query(
            states.Order.choosingProduct,
            F.data == Callbacks.GoBack.value
        )
        async def go_back_from_product(callback: CallbackQuery, state: FSMContext) -> None:
            await self.service.step_two(message=callback.message, state=state)

        @self.router.callback_query(
            states.Order.choosingProduct
        )
        async def product_chosen(callback: CallbackQuery, state: FSMContext) -> None:
            await self.service.set_handler(callback=callback, state=state)
