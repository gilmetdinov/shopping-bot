from bot.handler.handlers.common import AbstractHandler
import bot.states as states
import bot.handler.utils as utils
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class ReplenishmentHandler(AbstractHandler):

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
        get_payment_address_resp = await self.api.get_payment_address(chat_id=message.chat.id, currency=received_currency)
        if self._check_response(response=get_payment_address_resp):
            payment_address = get_payment_address_resp['payment_address']
            currency = get_payment_address_resp['currency']
            course = get_payment_address_resp['course']
            answer += self.messageBuilder.replenish_message(payment_address=payment_address, currency=currency, course=course)
            reply_markup = await self._get_main_keyboard(chat_id=message.chat.id, state=state)
            await state.set_state(states.Common.onMainPage)
        else:
            answer += self.messageBuilder.error_message(code=self._get_error_code(response=get_payment_address_resp))
            await state.clear()  # очищаем state, чтобы не появилось кнопок, потому как системная ошибка

        await message.answer(answer, parse_mode='MarkdownV2', reply_markup=reply_markup)
