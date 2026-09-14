from bot.handler.handlers.order.common import BaseOrderHandler
import bot.states as states
import bot.handler.utils as utils
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from bot.keyboards import List


class ProductHandler(BaseOrderHandler):

    def __init__(self, api):
        super().__init__(api, _type='product')
        self.productCategories = ['all', 'eps', 'eu']

    async def step_two(self, message: Message, state: FSMContext):
        """Product step two is displaying product categories"""
        user_data = await state.get_data()
        choose_order_msg: Message = user_data['choose_order_msg']

        answer = self.messageBuilder.choose_product_category()
        reply_markup = utils.product_category_keyboard()

        await state.set_state(states.Order.choosingProductCategory)
        choose_product_category_msg = await message.answer(answer, reply_markup=reply_markup, parse_mode='MarkdownV2')
        await state.update_data(choose_product_category_msg=choose_product_category_msg)

        await message.delete()
        try:
            await choose_order_msg.delete()
        except TelegramBadRequest:
            pass

    async def display_service_list(self, message, state):
        """Displaying service list after choosing product category (true step two as base step two is called here)"""
        user_data = await state.get_data()
        choose_product_category_msg: Message = user_data['choose_product_category_msg']

        index = List.productCategory.value.index(message.text) or None
        subtype = self.productCategories[index] if index and index < len(self.productCategories) else None

        product_alert = self.messageBuilder.product_alert()
        await message.answer(product_alert, parse_mode='MarkdownV2')
        await self._base_step_two(message=message, state=state, subtype=subtype)

        await state.update_data(page=1)
        await choose_product_category_msg.delete()
        await message.delete()

    async def set_handler(self, callback: CallbackQuery, state: FSMContext):
        await self._set_service_from_callback(callback, state)
