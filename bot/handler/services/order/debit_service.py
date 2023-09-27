from bot.handler.services.order.common import BaseBundleService
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


class DebitService(BaseBundleService):

    def __init__(self, api):
        super().__init__(api, _type='debit')

    async def step_two(self, message, state):
        """Sending bundle message with requirements for bundle order"""
        await message.answer(self.messageBuilder.choose_bundle(), parse_mode=self.MD)
        await super().step_two(message, state)
        await state.update_data(page=1)

    async def set_service(self, callback: CallbackQuery, state: FSMContext):
        await self._set_service_from_callback(callback, state, tg_username=True)
