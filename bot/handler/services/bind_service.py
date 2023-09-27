from bot.handler.services.common import AbstractService
import bot.states as states
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class BindService(AbstractService):

    async def command_bind_handler(self, message: Message, state: FSMContext) -> None:
        exploded_message = message.text.strip().split()
        answer = f""
        reply_markup = None
        if len(exploded_message) == 2:
            key = exploded_message[1]
            resp = await self.api.bind(key=key, chat_id=message.chat.id, username=message.chat.username)
            if self._check_response(response=resp):
                answer += self.messageBuilder.bind_success()
                reply_markup = await self._get_main_keyboard(chat_id=message.chat.id, state=state)
                await state.set_state(states.Common.onMainPage)
            else:
                answer += self._handle_response_error(response=resp)
        else:
            answer += self.messageBuilder.incorrect_command()
        await message.answer(answer, reply_markup=reply_markup, parse_mode='MarkdownV2')
