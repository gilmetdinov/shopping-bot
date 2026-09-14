from aiogram.exceptions import TelegramBadRequest
from bot.handler.handlers.common import AbstractHandler
import bot.handler.utils as utils
from bot.handler.dto import DtoFactory
from bot.helper import KeyboardHelper
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bot.states import FormFactory


class AbstractOrderHandler(AbstractHandler):

    def __init__(self, api, _type: str | None):
        super().__init__(api)
        self.type = _type
        self.formMessageFactory = utils.FormMessageFactory(self.messageBuilder)
        self.formKeyboardFactory = utils.FormKeyboardFactory()
        self.formStateFactory = FormFactory()
        # self.serviceListFactory = OrderListFactory()
        self.dtoFactory = DtoFactory()

    def _form_state(self):
        return self.formStateFactory.get_form_state(self.type)

    '''
    def _get_shortname(self, order: str) -> str:
        """Outdated, static service list is not used anymore"""
        try:
            service_list = self.serviceListFactory.get_order_list(self.type)
            service_list_reverse = KeyboardHelper.key_value_reverse(service_list)
            value = order.split('(')[0].rstrip()
            return service_list_reverse[value]
        except Exception:
            self.logger.log(self.logger.ERROR, f"Couldn't get shortname from {order}!")
            return 'error'
    '''

    '''
    @classmethod
    def _get_price(cls, order: str) -> float:
        """Gets price from reply markup: service_name: (price р.)"""
        return KeyboardHelper.get_price(order)
    '''

    @classmethod
    def _get_price(cls, order: str) -> float:
        """Gets price from reply markup button: "<label> (<price> р.)"."""
        return KeyboardHelper.get_price(order)

    async def _check_balance(self, chat_id, price):
        """Sends request to get user's balance
        :return: CHECK_TRUE, CHECK_FALSE, CHECK_ERROR"""
        balance = await utils.get_balance(api=self.api, chat_id=chat_id)
        if balance is None:
            return self.CHECK_ERROR
        elif float(balance) < price:
            return self.CHECK_FALSE
        return self.CHECK_TRUE

    def _get_form(self, dto, username: str = None):
        """Gets form (text message + inline markup) from factories by current order type"""
        form = self.formMessageFactory.get_form(self.type, {'dto': dto, 'username': username})
        inline_markup = self.formKeyboardFactory.get_form_keyboard(self.type, {'dto': dto})
        return form, inline_markup

    def _get_dto(self):
        """Gets dto from factory by current order type"""
        return self.dtoFactory.get_dto(self.type)

    async def _update_form(self, form: CallbackQuery | Message, dto):
        """Gets new form from updated dto and tries to update form if there are any changes"""
        try:
            message = form.message if type(form) is CallbackQuery else form
            new_form, inline_markup = self._get_form(dto=dto, username=message.chat.username)
            await message.edit_text(new_form, parse_mode='MarkdownV2', reply_markup=inline_markup)
        except TelegramBadRequest:
            pass

    async def _get_service_list(self, message: Message, state: FSMContext,
                                user_data: dict | None = None, force_update: bool = False,
                                _type: str | None = None) -> list | None:
        """Gets service list from state data or from api by type"""
        user_data = await state.get_data() if not force_update and user_data is None else user_data
        service_list: list or None = user_data['service_list'] \
            if not force_update and user_data and 'service_list' in user_data.keys() else None
        if service_list is None:
            _type = _type or self.type
            get_list_resp = await self.api.get_service_list(_type=_type, chat_id=message.chat.id)
            if not self._check_response(response=get_list_resp):
                answer = self._handle_response_error(response=get_list_resp)
                await message.answer(answer, parse_mode=self.MD)
                await state.clear()
                return
            service_list = [
                service | {'full_label': f"{service['label']} ({service['price']} р.)"}
                for service in get_list_resp['list']
            ]
            await state.update_data(service_list=service_list)
        return service_list

    async def step_two(self, message: Message, state: FSMContext):
        """Second step of any order (they differ greatly from type to type)"""
        pass
