from .base_order_handler import BaseOrderHandler
import bot.states as states
import bot.handler.utils as utils
from bot.handler.dto import DeliveryDto
from bot.keyboards import List
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


class BaseProductBHandler(BaseOrderHandler):

    async def step_two(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        choose_order_msg: Message = user_data['choose_order_msg']
        await self._base_step_two(message=message, state=state)
        await message.delete()
        await choose_order_msg.delete()

    async def input_address(self, callback: CallbackQuery, state: FSMContext):
        answer = self.messageBuilder.input_address()
        await callback.answer(answer, show_alert=True)
        await state.set_state(states.Order.inputAddress)

    async def set_address(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        dto: DeliveryDto = user_data['order_dto']
        form: CallbackQuery = user_data['order_form']

        address = message.text.strip()
        dto.set_address(address)
        await self._post_set(form=form, state=state, dto=dto)
        await message.delete()

    async def input_full_name(self, callback: CallbackQuery, state: FSMContext):
        answer = self.messageBuilder.input_full_name()
        await callback.answer(answer, show_alert=True)
        await state.set_state(states.Order.inputFullName)

    async def set_full_name(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        dto: DeliveryDto = user_data['order_dto']
        form: CallbackQuery = user_data['order_form']

        full_name = message.text.strip()
        dto.set_full_name(full_name)
        await self._post_set(form=form, state=state, dto=dto)
        await message.delete()

    async def input_phone_number(self, callback: CallbackQuery, state: FSMContext):
        answer = self.messageBuilder.input_phone_number()
        await callback.answer(answer, show_alert=True)
        await state.set_state(states.Order.inputPhoneNumber)

    async def set_phone_number(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        dto: DeliveryDto = user_data['order_dto']
        form: CallbackQuery = user_data['order_form']

        phone_number = message.text.strip()
        dto.set_phone_number(phone_number)
        await self._post_set(form=form, state=state, dto=dto)
        await message.delete()

    async def input_telegram(self, callback: CallbackQuery, state: FSMContext):
        answer = self.messageBuilder.input_telegram()
        await callback.answer(answer, show_alert=True)
        await state.set_state(states.Order.inputTelegram)

    async def set_telegram(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        dto: DeliveryDto = user_data['order_dto']
        form: CallbackQuery = user_data['order_form']

        telegram = message.text.strip()
        dto.set_telegram(telegram)
        await self._post_set(form=form, state=state, dto=dto)
        await message.delete()

    async def choose_delivery_type(self, callback: CallbackQuery, state: FSMContext):
        answer = self.messageBuilder.choose_delivery_type()
        reply_markup = utils.delivery_type_keyboard()
        delivery_type_msg = await callback.message.answer(answer, reply_markup=reply_markup)
        await state.set_state(states.Order.choosingDeliveryType)
        await state.update_data(delivery_type_msg=delivery_type_msg)

    async def set_delivery_type(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        dto: DeliveryDto = user_data['order_dto']
        form: CallbackQuery = user_data['order_form']
        delivery_type_msg: Message = user_data['delivery_type_msg']

        delivery_type = self.keyboardHelper.key_value_reverse(List.deliveryType.value)[message.text]
        dto.set_delivery_type(delivery_type)
        await self._post_set(form=form, state=state, dto=dto, param_msg=delivery_type_msg)
        await message.delete()
