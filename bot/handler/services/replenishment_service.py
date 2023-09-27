from bot.handler.services.common import AbstractService
import bot.states as states
import bot.handler.utils as utils
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class ReplenishmentService(AbstractService):

    async def choose_replenishment_type(self, message: Message, state: FSMContext):
        answer = self.messageBuilder.choose_replenishment_method()
        reply_markup = utils.replenishment_type_keyboard()
        await state.set_state(states.Replenishment.choosingMethod)
        await message.answer(answer, reply_markup=reply_markup)

    async def replenishment_cancel(self, message: Message, state: FSMContext):
        answer = self.messageBuilder.replenishment_canceled()
        await self.go_to_main_page(message=message, state=state, answer=answer)
        await message.delete()

    async def replenishment_chosen(self, message: Message, state: FSMContext):
        answer = f""
        reply_markup = None
        received_currency = ''.join(message.text.lower().split(' ')[::-1][0].split('-'))
        get_wallet_resp = await self.api.get_wallet(chat_id=message.chat.id, currency=received_currency)
        if self._check_response(response=get_wallet_resp):
            wallet = get_wallet_resp['wallet']
            currency = get_wallet_resp['currency']
            course = get_wallet_resp['course']
            answer += self.messageBuilder.replenish_message(wallet=wallet, currency=currency, course=course)
            reply_markup = await self._get_main_keyboard(chat_id=message.chat.id, state=state)
            await state.set_state(states.Common.onMainPage)
        else:
            answer += self.messageBuilder.error_message(code=self._get_error_code(response=get_wallet_resp))
            await state.clear()  # очищаем state, чтобы не появилось кнопок, потому как системная ошибка

        await message.answer(answer, parse_mode='MarkdownV2', reply_markup=reply_markup)
