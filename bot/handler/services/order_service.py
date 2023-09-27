from bot.handler.services.common import AbstractService
import bot.states as states
import bot.handler.utils as utils
from bot.handler.services.order.common import BaseOrderService
from bot.keyboards import List
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bot.handler.factories import OrderServiceFactory


class OrderService(AbstractService):

    def __init__(self, api):
        super().__init__(api)
        self.serviceFactory = OrderServiceFactory()

    async def __get_service(self, state: FSMContext):
        """Gets service by order_dto.type or current_order_type in state storage"""
        user_data = await state.get_data()
        dto = user_data['order_dto'] or None
        order_type = dto.type if dto and dto.type else (user_data['current_order_type'] or None)
        return self.serviceFactory.get_order_service(order_type) if order_type else None

    async def __call_service_method(self, method_name: str, **kwargs):
        """Calls a method from certain order type service with given kwargs (message/callback, state, etc)"""
        service_name = '-'
        try:
            state = kwargs['state']
            service_name = await self.__get_service(state)
            if not service_name:
                message = kwargs['message'] if 'message' in kwargs.keys() else kwargs['callback'].message
                await self._throw_error(message=message, state=state, clear_state=True)
                return

            service: BaseOrderService = service_name(api=self.api)
            await getattr(service, method_name)(**kwargs)
            del service  # удаляем, тк этот объект больше использоваться не будет
        except AttributeError:
            self.logger.log(self.logger.ERROR, f"Couldn't call {method_name} in {service_name or '-'}!")

    async def step_one(self, message: Message, state: FSMContext):
        """Step of choosing type of order (ident/wallet/bundle/debit)"""
        await state.update_data(order_dto=None)
        await state.update_data(current_order_type=None)
        answer = self.messageBuilder.choose_order_type()
        reply_markup = utils.order_type_keyboard()

        await state.set_state(states.Order.choosingType)
        choose_order_msg = await message.answer(answer, reply_markup=reply_markup)
        await state.update_data(choose_order_msg=choose_order_msg)

    # перекидываем с выбора типа заказа на второй шаг заказа (первый шаг внутри типа заказа)
    async def step_two(self, message: Message, state: FSMContext):
        """Stepping into order type with its ordering procedure"""
        order_type_short = self.keyboardHelper.key_value_reverse(List.orderType.value)[message.text]
        service_name = self.serviceFactory.get_order_service(order_type_short)
        if service_name:
            await state.update_data(current_order_type=order_type_short)
            await service_name(api=self.api).step_two(message=message, state=state)
        else:
            await self._throw_error(message=message, state=state, clear_state=True)

    # перелистывание страницы в выборе кошелька/дебета (мб где-то еще будет, поэтому выношу как можно выше и обобщаю)
    async def turn_page(self, callback: CallbackQuery, state: FSMContext, backward=False):
        """Turning page of paginated service list to both sides"""
        method_name = self.turn_page.__name__
        await self.__call_service_method(method_name, callback=callback, state=state, backward=backward)

    async def send_order(self, callback: CallbackQuery, state: FSMContext):
        """Sending order from order_dto to the server"""
        user_data = await state.get_data()
        dto = user_data['order_dto']
        answer = f""
        reply_markup = None
        order_resp = await self.api.make_order(chat_id=callback.message.chat.id, _type=dto.type, dto=dto)

        if self._check_response(response=order_resp):
            answer += self.messageBuilder.order_success(response=order_resp)
            reply_markup = await self._get_main_keyboard(chat_id=callback.message.chat.id, state=state)
            await state.set_state(states.Common.onMainPage)
        else:
            code = self._get_error_code(response=order_resp)
            answer += self._handle_error(code=code)
            if code > 0:
                reply_markup = await self._get_main_keyboard(chat_id=callback.message.chat.id, state=state)
                await state.set_state(states.Common.onMainPage)
            else:
                await state.clear()  # очищаем state, потому как системная ошибка

        await callback.message.answer(answer, reply_markup=reply_markup, parse_mode='MarkdownV2')
        await callback.message.delete()

    async def change_amount(self, callback: CallbackQuery, state: FSMContext):
        """Stepping into changing amount of quantiable order types (wallet, bundle, debit)"""
        method_name = self.change_amount.__name__
        await self.__call_service_method(method_name, callback=callback, state=state)

    async def set_amount(self, message: Message, state: FSMContext):
        """Setting amount of quantiable order types (wallet, bundle, debit)"""
        method_name = self.set_amount.__name__
        await self.__call_service_method(method_name, message=message, state=state)

    async def input_address(self, callback: CallbackQuery, state: FSMContext):
        """Stepping into inputting address of delivery order types (bundle, debit)"""
        method_name = self.input_address.__name__
        await self.__call_service_method(method_name, callback=callback, state=state)

    async def set_address(self, message: Message, state: FSMContext):
        """Setting address of delivery order types (bundle, debit)"""
        method_name = self.set_address.__name__
        await self.__call_service_method(method_name, message=message, state=state)

    async def input_full_name(self, callback: CallbackQuery, state: FSMContext):
        """Stepping into inputting full name of delivery order types (bundle, debit)"""
        method_name = self.input_full_name.__name__
        await self.__call_service_method(method_name, callback=callback, state=state)

    async def set_full_name(self, message: Message, state: FSMContext):
        """Setting full name of delivery order types (bundle, debit)"""
        method_name = self.set_full_name.__name__
        await self.__call_service_method(method_name, message=message, state=state)

    async def input_phone_number(self, callback: CallbackQuery, state: FSMContext):
        """Stepping into inputting phone number of delivery order types (bundle, debit)"""
        method_name = self.input_phone_number.__name__
        await self.__call_service_method(method_name, callback=callback, state=state)

    async def set_phone_number(self, message: Message, state: FSMContext):
        """Setting phone number of delivery order types (bundle, debit)"""
        method_name = self.set_phone_number.__name__
        await self.__call_service_method(method_name, message=message, state=state)

    async def input_telegram(self, callback: CallbackQuery, state: FSMContext):
        """Stepping into inputting telegram username of delivery order types (bundle, debit)"""
        method_name = self.input_telegram.__name__
        await self.__call_service_method(method_name, callback=callback, state=state)

    async def set_telegram(self, message: Message, state: FSMContext):
        """Setting telegram username of delivery order types (bundle, debit)"""
        method_name = self.set_telegram.__name__
        await self.__call_service_method(method_name, message=message, state=state)

    async def choose_delivery_type(self, callback: CallbackQuery, state: FSMContext):
        """Stepping into choosing delivery method of delivery order types (bundle, debit)"""
        method_name = self.choose_delivery_type.__name__
        await self.__call_service_method(method_name, callback=callback, state=state)

    async def set_delivery_type(self, message: Message, state: FSMContext):
        """Setting delivery method of delivery order types (bundle, debit)"""
        method_name = self.set_delivery_type.__name__
        await self.__call_service_method(method_name, message=message, state=state)

