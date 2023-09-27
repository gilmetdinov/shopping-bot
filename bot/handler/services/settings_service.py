from bot.handler.services.common import AbstractService
import bot.handler.utils as utils
import bot.states as states
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class SettingsService(AbstractService):

    async def __get_settings_keyboard(self, chat_id, state):
        return utils.settings_keyboard(
            *await utils.update_settings(api=self.api, chat_id=chat_id, state=state)
        )

    async def settings_menu(self, message: Message, state: FSMContext):
        answer = self.messageBuilder.settings_message()
        reply_markup = await self.__get_settings_keyboard(chat_id=message.chat.id, state=state)
        await state.set_state(states.Settings.menu)
        await message.answer(answer, parse_mode='MarkdownV2', reply_markup=reply_markup)

    async def switch_notif(self, message: Message, state: FSMContext, _type: str):
        answer = f""
        reply_markup = None

        switch_notif_resp = await self.api.switch_notif(chat_id=message.chat.id, _type=_type)
        if self._check_response(response=switch_notif_resp):
            answer += self.messageBuilder.notif_set_message(_type=_type,
                                                            setting=switch_notif_resp['new_setting'])
            reply_markup = await self.__get_settings_keyboard(chat_id=message.chat.id, state=state)
        else:
            answer += self.messageBuilder.error_message(code=self._get_error_code(response=switch_notif_resp))
            await state.clear()  # очищаем state, чтобы не появилось кнопок, потому как системная ошибка

        await message.delete()
        await message.answer(answer, parse_mode='MarkdownV2', reply_markup=reply_markup)
