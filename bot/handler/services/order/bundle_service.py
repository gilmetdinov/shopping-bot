from bot.handler.services.order.common import BaseBundleService
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


class BundleService(BaseBundleService):

    def __init__(self, api):
        super().__init__(api, _type='bundle')

    async def set_service(self, message: Message, state: FSMContext):
        await self._set_service_from_message(message, state, tg_username=True)
