import logging
import os

from api import ApiClient
import message as _message
from utils.enums import ErrorCodes
import bot.handler.utils as utils
import bot.states as states
from bot.helper import KeyboardHelper
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class AbstractHandler:
    STATUS_SUCCESS = 'success'
    STATUS_ERROR = 'error'

    CHECK_ERROR = -1
    CHECK_FALSE = 0
    CHECK_TRUE = 1

    MD = 'MarkdownV2'

    def __init__(self, api: ApiClient):
        self.api = api
        self.messageBuilder = _message.Builder()
        self.errorCodes = ErrorCodes
        self.keyboardHelper = KeyboardHelper()
        self.logger = logging

    @classmethod
    def _get_dir(cls, chat_id):
        """Gets directory for temporary savings"""
        _dir = f"tmp/{chat_id}"
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        return _dir

    def _check_response(self, response):
        if response['status'] == self.STATUS_ERROR:
            return False
        elif response['status'] == self.STATUS_SUCCESS:
            return True
        else:
            return False

    def _handle_error(self, code=ErrorCodes.Unexpected.value):
        return self.messageBuilder.error_message(code=code)

    def _handle_inline_error(self, code=ErrorCodes.Unexpected.value):
        return self.messageBuilder.error_message(code=code, remove_entities=False)

    def _get_error_code(self, response: dict):
        return response['code'] if 'code' in response.keys() else self.errorCodes.Unexpected.value

    def _handle_response_error(self, response):
        return self._handle_error(code=self._get_error_code(response=response))

    async def _throw_error(self, message: Message, state: FSMContext = None, clear_state=False,
                           code=ErrorCodes.Unexpected.value):
        answer = self.messageBuilder.error_message(code=code)
        await message.answer(answer, parse_mode='MarkdownV2', reply_markup=None)
        if state and clear_state:
            await state.clear()

    async def _handle_check_user(self, chat_id):
        check_user_resp = await self.api.check_user(chat_id)
        if not self._check_response(response=check_user_resp):
            return {'status': self.CHECK_ERROR, 'code': check_user_resp['code']}
        elif self._check_response(response=check_user_resp) and check_user_resp['is_bound']:
            return {'status': self.CHECK_TRUE}
        elif self._check_response(response=check_user_resp) and not check_user_resp['is_bound']:
            return {'status': self.CHECK_FALSE}
        else:
            return {'status': self.CHECK_ERROR, 'code': ErrorCodes.Unexpected.value}

    async def _get_main_keyboard(self, chat_id, state):
        return utils.main_keyboard(
            await utils.update_balance(api=self.api, chat_id=chat_id, state=state)
        )

    async def incorrect_input(self, message: Message):
        answer = self.messageBuilder.incorrect_input()
        await message.answer(answer)

    async def go_to_main_page(self, message: Message, state: FSMContext,
                              answer="Возврат на главную страницу...", parse_mode=None):
        reply_markup = await self._get_main_keyboard(chat_id=message.chat.id, state=state)
        await state.set_state(states.Common.onMainPage)
        await message.answer(answer, reply_markup=reply_markup, parse_mode=parse_mode)
