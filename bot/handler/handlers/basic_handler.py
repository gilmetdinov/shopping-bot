from bot.handler.handlers.common import AbstractHandler
import bot.states as states
import bot.handler.utils as utils
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class BasicHandler(AbstractHandler):

    async def command_start_handler(self, message: Message, state: FSMContext) -> None:
        check_user = await self._handle_check_user(chat_id=message.chat.id)
        answer = f""
        reply_markup = None
        if check_user['status'] == self.CHECK_TRUE:
            answer += self.messageBuilder.start_bound()
            reply_markup = await self._get_main_keyboard(chat_id=message.chat.id, state=state)
            await state.set_state(states.Common.onMainPage)
        elif check_user['status'] == self.CHECK_FALSE:
            answer += self.messageBuilder.start_unbound()
        elif check_user['status'] == self.CHECK_ERROR:
            answer += self._handle_error(code=check_user['code'])

        await message.answer(answer, reply_markup=reply_markup, parse_mode='MarkdownV2')

    async def command_help_handler(self, message: Message, state: FSMContext) -> None:
        check_user = await self._handle_check_user(chat_id=message.chat.id)
        answer = f""
        reply_markup = None
        if check_user['status'] == self.CHECK_TRUE:
            answer += self.messageBuilder.help_bound()
            reply_markup = utils.main_keyboard(
                await utils.update_balance(api=self.api, chat_id=message.chat.id, state=state)
            )
            await state.set_state(states.Common.onMainPage)
        elif check_user['status'] == self.CHECK_FALSE:
            answer += self.messageBuilder.help_unbound()
        elif check_user['status'] == self.CHECK_ERROR:
            answer += self.messageBuilder.error_message(code=check_user['code'])

        await message.answer(answer, reply_markup=reply_markup, parse_mode='MarkdownV2')
