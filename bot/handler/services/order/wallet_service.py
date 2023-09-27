from bot.handler.services.order.common import BaseOrderService
import bot.states as states
import bot.handler.utils as utils
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from bot.keyboards import List


class WalletService(BaseOrderService):

    def __init__(self, api):
        super().__init__(api, _type='wallet')
        self.walletCategories = ['all', 'eps', 'eu']

    async def step_two(self, message: Message, state: FSMContext):
        """Wallet step two is displaying wallet categories"""
        user_data = await state.get_data()
        choose_order_msg: Message = user_data['choose_order_msg']

        answer = self.messageBuilder.choose_wallet_category()
        reply_markup = utils.wallet_category_keyboard()

        await state.set_state(states.Order.choosingWalletCategory)
        choose_wallet_category_msg = await message.answer(answer, reply_markup=reply_markup, parse_mode='MarkdownV2')
        await state.update_data(choose_wallet_category_msg=choose_wallet_category_msg)

        await message.delete()
        try:
            await choose_order_msg.delete()
        except TelegramBadRequest:
            pass

    async def display_service_list(self, message, state):
        """Displaying service list after choosing wallet category (true step two as base step two is called here)"""
        user_data = await state.get_data()
        choose_wallet_category_msg: Message = user_data['choose_wallet_category_msg']

        index = List.walletCategory.value.index(message.text) or None
        subtype = self.walletCategories[index] if index and index < len(self.walletCategories) else None

        wallet_alert = self.messageBuilder.wallet_alert()
        await message.answer(wallet_alert, parse_mode='MarkdownV2')
        await self._base_step_two(message=message, state=state, subtype=subtype)

        await state.update_data(page=1)
        await choose_wallet_category_msg.delete()
        await message.delete()

    async def set_service(self, callback: CallbackQuery, state: FSMContext):
        await self._set_service_from_callback(callback, state)
