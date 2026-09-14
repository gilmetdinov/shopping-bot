from bot.handler.handlers.order.common import BaseProductBHandler
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


class ProductBHandler(BaseProductBHandler):

    def __init__(self, api):
        super().__init__(api, _type='product_b')

    async def set_handler(self, message: Message, state: FSMContext):
        await self._set_service_from_message(message, state, tg_username=True)
