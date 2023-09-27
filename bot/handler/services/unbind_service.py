from bot.handler.services.common import AbstractService
import bot.states as states
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
import bot.handler.utils as utils


class UnbindService(AbstractService):
    async def command_unbind_handler(self, message: Message, state: FSMContext) -> None:
        check_user = await self._handle_check_user(chat_id=message.chat.id)
        answer = f""
        reply_markup = None

        if check_user['status'] == self.CHECK_TRUE:
            answer += self.messageBuilder.unbind_confirmation()
            reply_markup = utils.confirmation_keyboard()
            await state.set_state(states.Unbind.confirming)
        elif check_user['status'] == self.CHECK_FALSE:
            answer += self.messageBuilder.incorrect_command()
        elif check_user['status'] == self.STATUS_ERROR:
            answer += self.messageBuilder.error_message(code=check_user['code'])

        await message.answer(answer, parse_mode='MarkdownV2', reply_markup=reply_markup)

    async def unbind_confirmed(self, message: Message, state: FSMContext) -> None:
        get_code_resp = await self.api.get_unbind_code(chat_id=message.chat.id)
        answer = f""
        if self._check_response(response=get_code_resp):
            unbind_code = get_code_resp['unbind_code']
            await state.update_data(unbind_code=unbind_code)
            answer += self.messageBuilder.unbind_instruction()
            await state.set_state(states.Unbind.awaitingCode)
        else:
            answer += self._handle_error(code=self._get_error_code(response=get_code_resp))
            await state.clear()  # очищаем state, чтобы не появилось кнопок, потому как системная ошибка
        await message.answer(answer, parse_mode='MarkdownV2', reply_markup=ReplyKeyboardRemove())

    async def unbind_canceled(self, message: Message, state: FSMContext):
        answer = self.messageBuilder.unbind_cancel()
        await self.go_to_main_page(message=message, state=state, answer=answer, parse_mode=self.MD)

    async def check_unbind_code(self, message: Message, state: FSMContext):
        received_code = message.text
        user_data = await state.get_data()
        answer = f""
        if received_code == str(user_data['unbind_code']):
            unbind_resp = await self.api.unbind(chat_id=message.chat.id)
            if self._check_response(response=unbind_resp):
                answer += self.messageBuilder.unbind_success()
                await state.clear()
            else:
                answer += self.messageBuilder.error_message(code=self._get_error_code(response=unbind_resp))
        else:
            answer += self.messageBuilder.error_message(code=self.errorCodes.InvalidUnbindCode.value)
        await message.answer(answer, parse_mode='MarkdownV2')
