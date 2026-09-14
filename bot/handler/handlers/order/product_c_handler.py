from bot.handler.handlers.order.common import BaseProductBHandler
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


class ProductCHandler(BaseProductBHandler):

    def __init__(self, api):
        super().__init__(api, _type='product_c')

    async def step_two(self, message, state):
        """Sending product_c message with requirements for product_c order"""
        await message.answer(self.messageBuilder.choose_product_c(), parse_mode=self.MD)
        await super().step_two(message, state)
        await state.update_data(page=1)

    async def set_handler(self, callback: CallbackQuery, state: FSMContext):
        await self._set_service_from_callback(callback, state, tg_username=True)
