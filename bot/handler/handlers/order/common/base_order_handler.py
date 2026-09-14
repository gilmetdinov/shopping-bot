from bot.handler.handlers.order.common import AbstractOrderHandler
import bot.states as states
from bot.handler.dto.common import BaseOrderDto
from bot.handler.utils import StepTwoKeyboardFactory, StepTwoMessageFactory, service_reply_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


# for Product, BaseProductB (ProductB, ProductC)
class BaseOrderHandler(AbstractOrderHandler):

    def __init__(self, api, _type=None):
        super().__init__(api, _type=_type)
        self.stepTwoMessageFactory = StepTwoMessageFactory(builder=self.messageBuilder)
        self.stepTwoKeyboardFactory = StepTwoKeyboardFactory()

    def display_service_list(self, message: Message, state: FSMContext):
        """More of an abstract method for real procedure of displaying service list"""
        pass

    def _step_two_state(self, service_type):
        """Getting step two which in fact is selecting service after selecting order type"""
        service_type = service_type if service_type else self.type
        return states.StepTwoFactory().get_step_two_state(service_type)

    async def _base_step_two(self, message: Message, state: FSMContext, subtype: str = None):
        """Getting and displaying service list of order type without order cache"""
        _type = f"{self.type}_{subtype}" if subtype else self.type
        service_list = await self._get_service_list(message=message, state=state, force_update=True, _type=_type)
        await state.update_data(service_list=service_list)
        answer = self.stepTwoMessageFactory.get_step_two_message(self.type, {'_type': self.type,
                                                                             'service_list': service_list,
                                                                             'page': 1})
        markup = self.stepTwoKeyboardFactory.get_step_two_keyboard(self.type, {'_type': self.type,
                                                                               'service_list': service_list,
                                                                               'page': 1})
        await state.set_state(self._step_two_state(self.type))
        await message.answer(answer, reply_markup=markup, parse_mode=self.MD)

    async def turn_page(self, callback: CallbackQuery, state: FSMContext, backward=False):
        """Making it base method as there may be more handlers in product_b type or new order types which
        need paginated service list"""
        user_data = await state.get_data()
        service_list: list = await self._get_service_list(message=callback.message, state=state, user_data=user_data)

        next_page = user_data['page'] - 1 if backward else user_data['page'] + 1
        if next_page < 1 or next_page > (len(service_list) // 10 + 1):
            await callback.answer(self.messageBuilder.unavailable())
            return

        answer = self.stepTwoMessageFactory.get_step_two_message(self.type, {'_type': self.type,
                                                                             'service_list': service_list,
                                                                             'page': next_page})
        inline_markup = self.stepTwoKeyboardFactory.get_step_two_keyboard(self.type, {'_type': self.type,
                                                                                      'service_list': service_list,
                                                                                      'page': next_page})
        await callback.message.edit_text(answer, parse_mode='MarkdownV2')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,
                                                 reply_markup=inline_markup)
        await state.update_data(page=next_page)

    async def _set_service_from_message(self, message: Message, state: FSMContext, tg_username=False):
        """Gets order form after choosing service from reply markup service list (via message)"""
        service_list: list = await self._get_service_list(message=message, state=state)
        message_text = message.text
        chosen_handler: dict or None = next(
            (service for service in service_list if service['full_label'] == message_text),
            None
        )
        if chosen_handler is None:
            answer = self.messageBuilder.incorrect_handler()
            reply_markup = service_reply_keyboard(_type=self.type, service_list=service_list)
            await message.answer(answer, reply_markup=reply_markup, parse_mode=self.MD)
            return

        dto_kwargs = {'service': chosen_handler['short'], 'price': float(chosen_handler['price']),
                      'service_label': chosen_handler['label']}
        if tg_username:
            dto_kwargs['telegram'] = f"@{message.chat.username}"
        dto = self.dtoFactory.get_dto(self.type, **dto_kwargs)
        answer, inline_markup = self._get_form(dto=dto, username=message.chat.username)
        order_form = await message.answer(answer, parse_mode='MarkdownV2', reply_markup=inline_markup)
        await message.delete()
        await state.update_data(order_dto=dto)
        await state.update_data(order_form=order_form)
        await state.set_state(self._form_state())

    async def _set_service_from_callback(self, callback: CallbackQuery, state: FSMContext, tg_username=False):
        """Gets order form after choosing service from paginated service list (via callback)"""
        service_list = await self._get_service_list(message=callback.message, state=state)
        service_short = callback.data
        chosen_handler: dict or None = next(
            (service for service in service_list if service['short'] == service_short),
            None
        )
        if chosen_handler is None:
            answer = self.messageBuilder.incorrect_handler(remove_entities=False)
            await callback.answer(answer, parse_mode=self.MD)
            return

        dto_kwargs = {'service': chosen_handler['short'], 'price': float(chosen_handler['price']),
                      'service_label': chosen_handler['label']}
        if tg_username:
            dto_kwargs['telegram'] = f"@{callback.message.chat.username}"
        dto = self.dtoFactory.get_dto(self.type, **dto_kwargs)
        answer, inline_markup = self._get_form(dto=dto, username=callback.message.chat.username)
        order_form = await callback.message.answer(answer, parse_mode='MarkdownV2', reply_markup=inline_markup)
        await callback.message.delete()
        await state.update_data(order_dto=dto)
        await state.update_data(order_form=order_form)
        await state.set_state(self._form_state())

    async def _post_set(self, form: CallbackQuery, state: FSMContext, dto: BaseOrderDto,
                        param_msg: Message | None = None):
        """Procedure done after updating order_dto in form states"""
        await self._update_form(form=form, dto=dto)
        await state.update_data(order_dto=dto)
        await state.set_state(self._form_state())
        if type(param_msg) is Message:
            await param_msg.delete()

    async def change_amount(self, callback: CallbackQuery, state: FSMContext):
        """For quantiable"""
        await state.update_data(order_form=callback)
        await state.set_state(states.Order.inputAmount)
        amount_msg = await callback.answer(self.messageBuilder.input_amount(), show_alert=True)
        await state.update_data(amount_msg=amount_msg)

    async def set_amount(self, message: Message, state: FSMContext):
        """For quantiable"""
        amount = message.text.strip()
        if amount.isdigit():
            user_data = await state.get_data()
            dto = user_data['order_dto']
            form: CallbackQuery = user_data['order_form']
            amount_msg: Message = user_data['amount_msg']
            dto.set_amount(int(amount))
            await self._post_set(state=state, dto=dto, form=form, param_msg=amount_msg)
        else:
            await message.answer(self.messageBuilder.incorrect_input())

        await message.delete()
